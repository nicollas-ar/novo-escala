"""Referências da liturgia, com cache por data e sem acesso ao banco."""
import json
from http.client import HTTPException
from threading import Lock
from time import monotonic
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API = "https://liturgia.up.railway.app/v2/"
FONTE_OFICIAL = "https://liturgiadiaria.edicoescnbb.com.br/"
SECOES = (
    ("primeiraLeitura", "Primeira leitura"),
    ("salmo", "Salmo responsorial"),
    ("segundaLeitura", "Segunda leitura"),
    ("evangelho", "Evangelho"),
)
LIMITE_RESPOSTA = 512 * 1024
REPETIR_APOS = 300

_trava = Lock()
_dia_cache = None
_dados_cache = None
_tentar_depois = 0


def _buscar(dia):
    parametros = urlencode({"dia": f"{dia.day:02d}", "mes": f"{dia.month:02d}", "ano": dia.year})
    requisicao = Request(API + "?" + parametros, headers={"Accept": "application/json"})
    with urlopen(requisicao, timeout=4) as resposta:
        corpo = resposta.read(LIMITE_RESPOSTA + 1)
    if len(corpo) > LIMITE_RESPOSTA:
        raise ValueError("Resposta grande demais.")

    dados = json.loads(corpo)
    if not isinstance(dados, dict) or dados.get("data") != dia.strftime("%d/%m/%Y"):
        raise ValueError("A API retornou uma data diferente.")
    celebracao, cor, leituras = dados.get("liturgia"), dados.get("cor"), dados.get("leituras")
    if not isinstance(celebracao, str) or not celebracao.strip() or not isinstance(leituras, dict):
        raise ValueError("A API não retornou a celebração e suas leituras.")

    secoes = []
    for chave, nome in SECOES:
        itens = leituras.get(chave) or []
        if not isinstance(itens, list):
            raise ValueError("Formato de leitura inesperado.")
        referencias = []
        for item in itens:
            referencia = item.get("referencia") if isinstance(item, dict) else None
            if isinstance(referencia, str) and referencia.strip():
                referencias.append(referencia.strip())
        if not referencias and chave != "segundaLeitura":
            raise ValueError("A API não retornou todas as referências obrigatórias.")
        if referencias:
            secoes.append({"nome": nome, "referencias": referencias})

    return {"celebracao": celebracao.strip(), "cor": cor.strip() if isinstance(cor, str) else "",
            "secoes": secoes}


def obter(dia):
    global _dia_cache, _dados_cache, _tentar_depois
    with _trava:
        if dia == _dia_cache and (_dados_cache is not None or monotonic() < _tentar_depois):
            return _dados_cache

        try:
            dados = _buscar(dia)
        except (HTTPException, OSError, ValueError):
            dados = None

        _dia_cache = dia
        _dados_cache = dados
        _tentar_depois = monotonic() + REPETIR_APOS
        return dados
