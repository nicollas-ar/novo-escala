"""Santo do dia, buscado na API do CatolicoApp (a mesma usada pelo plugin WP Santo do Dia).

A consulta é por dia e mês: https://catolicoapp.com/wp-json/wp/v2/santos?dia=D&mes=M
O site que responde é quem decide qual é o santo de cada data. Nada é gravado no banco de dados:
o resultado fica só em memória (cache de 12 horas) e a foto é carregada direto do servidor deles.

Se a API falhar, as novas tentativas ficam pausadas por 15 minutos (como no plugin), para o site
não ficar esperando uma API fora do ar.
"""
import json
import threading
import time
from html import unescape
from html.parser import HTMLParser
from urllib.error import URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

API_URL = "https://catolicoapp.com/wp-json/wp/v2/santos"
PAGINA_FONTE = "https://catolicoapp.com/santo-do-dia"
USER_AGENT = "EscalaCerimoniariosLimao/1.0 (aplicativo paroquial; Flask; urllib)"

TTL_OK = 12 * 3600
PAUSA_FALHA = 15 * 60
LIMITE_RESPOSTA = 1024 * 1024          # 1 MB, como no plugin
LIMITE_TEXTO = 1600                    # caracteres do texto da vida exibidos na página

_cache = {}                            # (dia, mes) -> (expira_em, resultado)
_pausa_ate = 0.0
_trava = threading.Lock()


# ----------------------------------------------------------------- utilitários
class _HtmlParaTexto(HTMLParser):
    """Converte HTML em parágrafos de texto puro (ignora script/style)."""
    BLOCOS = {"p", "br", "div", "li", "ul", "ol", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote", "tr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.partes = []
        self._ignorar = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._ignorar += 1
        elif tag in self.BLOCOS:
            self.partes.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self._ignorar = max(0, self._ignorar - 1)
        elif tag in self.BLOCOS:
            self.partes.append("\n")

    def handle_data(self, data):
        if not self._ignorar:
            self.partes.append(data)


def _html_para_paragrafos(html):
    p = _HtmlParaTexto()
    p.feed(html or "")
    p.close()
    texto = "".join(p.partes).replace("\xa0", " ")
    paragrafos = [" ".join(l.split()) for l in texto.split("\n")]
    return [x for x in paragrafos if x]


def _cortar(paragrafos, limite=LIMITE_TEXTO):
    """Mantém parágrafos inteiros até o limite; corta no fim de uma frase se o primeiro já passar."""
    saida, total = [], 0
    for p in paragrafos:
        if total + len(p) <= limite:
            saida.append(p)
            total += len(p)
            continue
        if not saida:
            corte = p[:limite]
            fim = max(corte.rfind(". "), corte.rfind("! "), corte.rfind("? "))
            saida.append(corte[:fim + 1] if fim > limite // 3 else corte.rstrip() + "…")
        break
    return saida


def _url_ok(url):
    """Só aceita endereços http(s) com host, para nunca exibir javascript: ou similares."""
    if not isinstance(url, str):
        return None
    url = url.strip()
    p = urlparse(url)
    return url if p.scheme in ("http", "https") and p.netloc else None


def _campo_texto(valor):
    """Campos do WordPress vêm como {"rendered": "..."}; aceita também texto simples."""
    if isinstance(valor, dict):
        valor = valor.get("rendered")
    return valor if isinstance(valor, str) else ""


# ------------------------------------------------------------------ API
def _buscar_json(dia, mes, timeout=8):
    url = API_URL + "?" + urlencode({"dia": dia, "mes": mes})
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urlopen(req, timeout=timeout) as resp:
        corpo = resp.read(LIMITE_RESPOSTA + 1)
    if len(corpo) > LIMITE_RESPOSTA:
        raise ValueError("resposta grande demais")
    return json.loads(corpo.decode("utf-8"))


def _interpretar(dados):
    """Valida a resposta (lista; usa o primeiro item) e devolve o santo, ou None se for inválida."""
    if not isinstance(dados, list) or not dados or not isinstance(dados[0], dict):
        return None
    item = dados[0]
    nome = " ".join(_html_para_paragrafos(_campo_texto(item.get("title"))))
    link = _url_ok(item.get("link"))
    if not nome or not link:
        return None
    imagem = _url_ok(item.get("imagem_destacada"))
    # a API é um WordPress: se expuser o conteúdo (ou o resumo), mostramos o texto da vida
    html_texto = _campo_texto(item.get("content")) or _campo_texto(item.get("excerpt"))
    return {
        "nome": nome,
        "imagem": imagem,
        "url": link,
        "paragrafos": _cortar(_html_para_paragrafos(html_texto)),
    }


def obter(dia, mes):
    """Santo da data (dict com nome, imagem, url, paragrafos) ou None se a API não respondeu."""
    global _pausa_ate
    agora = time.time()
    chave = (int(dia), int(mes))
    with _trava:
        item = _cache.get(chave)
        if item and item[0] > agora:
            return item[1]
        if agora < _pausa_ate:           # API falhou há pouco: não fica esperando de novo
            return None
    try:
        resultado = _interpretar(_buscar_json(*chave))
        falhou = resultado is None
    except (URLError, TimeoutError, OSError, ValueError, KeyError, IndexError):
        resultado, falhou = None, True
    with _trava:
        if falhou:
            _pausa_ate = time.time() + PAUSA_FALHA
        else:
            _pausa_ate = 0.0
            _cache[chave] = (time.time() + TTL_OK, resultado)
            if len(_cache) > 400:
                _cache.clear()
    return resultado
