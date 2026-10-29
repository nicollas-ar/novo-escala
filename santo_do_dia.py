"""Santo do dia: escolhe o santo pela data e busca foto e texto na Wikipédia (pt).

Nada é gravado no banco: o texto e a foto vêm da Wikipédia a cada dia e ficam só em memória
(cache de 24 horas). A foto é carregada direto dos servidores da Wikimedia.

O calendário abaixo foi montado a partir do Calendário Romano Geral (com algumas memórias do Brasil).
Cada linha é:  MM-DD|Nome exibido|Título do artigo na Wikipédia
Se o título não existir ou for uma página de desambiguação, o sistema procura pelo nome.
Para corrigir ou acrescentar um santo, basta editar as linhas. Nos dias sem linha, aparece um santo
da lista POOL, identificado como "Para conhecer hoje" (sem afirmar que é a festa daquele dia).
"""
import json
import threading
import time
from datetime import date
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

CALENDARIO_TXT = """
01-01|Santa Maria, Mãe de Deus|Maria, mãe de Jesus
01-02|São Basílio Magno|Basílio de Cesareia
01-03|Santa Genoveva|Genoveva de Paris
01-06|Epifania do Senhor|Epifania
01-07|São Raimundo de Peñafort|Raimundo de Peñafort
01-13|Santo Hilário de Poitiers|Hilário de Poitiers
01-17|Santo Antão do Deserto|Antão do Egito
01-20|São Sebastião|São Sebastião
01-21|Santa Inês|Inês de Roma
01-22|São Vicente de Saragoça|Vicente de Saragoça
01-24|São Francisco de Sales|Francisco de Sales
01-25|Conversão de São Paulo|Conversão de Paulo
01-26|São Timóteo e São Tito|Timóteo (bispo de Éfeso)
01-27|Santa Ângela Mérici|Ângela Mérici
01-28|São Tomás de Aquino|Tomás de Aquino
01-31|São João Bosco|João Bosco
02-02|Apresentação do Senhor|Apresentação de Jesus no Templo
02-03|São Brás|Brás de Sebaste
02-04|São João de Brito|João de Brito
02-05|Santa Águeda|Águeda de Catânia
02-06|São Paulo Miki e companheiros|Paulo Miki
02-08|Santa Josefina Bakhita|Josefina Bakhita
02-10|Santa Escolástica|Escolástica
02-11|Nossa Senhora de Lourdes|Nossa Senhora de Lourdes
02-14|São Cirilo e São Metódio|Cirilo e Metódio
02-17|Sete Santos Fundadores da Ordem dos Servitas|Ordem dos Servos de Maria
02-21|São Pedro Damião|Pedro Damião
02-22|Cátedra de São Pedro|Cátedra de São Pedro
02-23|São Policarpo|Policarpo de Esmirna
03-03|Santa Katharine Drexel|Katharine Drexel
03-04|São Casimiro|Casimiro Jagelão
03-07|Santas Perpétua e Felicidade|Perpétua e Felicidade
03-08|São João de Deus|João de Deus
03-09|Santa Francisca Romana|Francisca Romana
03-12|São Luís Orione|Luís Orione
03-15|Santa Luísa de Marillac|Luísa de Marillac
03-17|São Patrício|Patrício da Irlanda
03-18|São Cirilo de Jerusalém|Cirilo de Jerusalém
03-19|São José, esposo de Maria|José de Nazaré
03-23|São Turíbio de Mogrovejo|Turíbio de Mogrovejo
03-24|São Óscar Romero|Óscar Romero
03-25|Anunciação do Senhor|Anunciação
04-02|São Francisco de Paula|Francisco de Paula
04-04|Santo Isidoro de Sevilha|Isidoro de Sevilha
04-05|São Vicente Ferrer|Vicente Ferrer
04-07|São João Batista de La Salle|João Batista de La Salle
04-11|Santo Estanislau|Estanislau de Cracóvia
04-13|São Martinho I|Martinho I
04-15|São Damião de Molokai|Damião de Molokai
04-16|Santa Bernadette Soubirous|Bernadette Soubirous
04-19|Santo Expedito|Expedito
04-21|Santo Anselmo|Anselmo de Cantuária
04-23|São Jorge|São Jorge
04-24|São Fidélis de Sigmaringa|Fidélis de Sigmaringa
04-25|São Marcos Evangelista|Marcos, o Evangelista
04-28|São Luís Grignion de Montfort|Luís Maria Grignion de Montfort
04-29|Santa Catarina de Sena|Catarina de Sena
04-30|São Pio V|Pio V
05-01|São José Operário|São José Operário
05-02|Santo Atanásio|Atanásio de Alexandria
05-03|São Filipe e São Tiago Menor|Filipe (apóstolo)
05-04|São Floriano|Floriano de Lorch
05-10|São João de Ávila|João de Ávila
05-12|São Pancrácio|Pancrácio de Roma
05-13|Nossa Senhora de Fátima|Nossa Senhora de Fátima
05-14|São Matias|Matias (apóstolo)
05-15|Santo Isidro Lavrador|Isidro, o Lavrador
05-17|São Pascoal Bailão|Pascoal Bailão
05-18|São João I|João I (papa)
05-20|São Bernardino de Sena|Bernardino de Sena
05-21|São Cristóvão de Magalhães|Cristóvão de Magalhães
05-22|Santa Rita de Cássia|Rita de Cássia
05-24|Nossa Senhora Auxiliadora|Nossa Senhora Auxiliadora
05-25|São Beda, o Venerável|Beda
05-26|São Filipe Néri|Filipe Néri
05-27|Santo Agostinho de Cantuária|Agostinho de Cantuária
05-30|Santa Joana d'Arc|Joana d'Arc
05-31|Visitação de Nossa Senhora|Visitação de Maria
06-01|São Justino|Justino de Roma
06-02|Santos Marcelino e Pedro|Marcelino e Pedro
06-03|São Carlos Lwanga e companheiros|Carlos Lwanga
06-05|São Bonifácio|Bonifácio de Mogúncia
06-06|São Norberto|Norberto de Xanten
06-09|São José de Anchieta|José de Anchieta
06-11|São Barnabé|Barnabé
06-13|Santo Antônio de Pádua|Antônio de Pádua
06-19|São Romualdo|Romualdo de Ravena
06-21|São Luís Gonzaga|São Luís Gonzaga
06-22|São Tomás More|Tomás More
06-24|Natividade de São João Batista|João Batista
06-26|São Josemaria Escrivá|Josemaría Escrivá
06-27|São Cirilo de Alexandria|Cirilo de Alexandria
06-28|Santo Irineu de Lyon|Irineu de Lyon
06-29|São Pedro e São Paulo|Pedro (apóstolo)
06-30|Primeiros Mártires da Igreja de Roma|Primeiros Mártires da Igreja de Roma
07-03|São Tomé, apóstolo|Tomé (apóstolo)
07-04|Santa Isabel de Portugal|Santa Isabel de Portugal
07-05|Santo Antônio Maria Zaccaria|Antônio Maria Zaccaria
07-06|Santa Maria Goretti|Maria Goretti
07-09|Santa Paulina|Madre Paulina
07-11|São Bento|Bento de Núrsia
07-13|Santo Henrique|Henrique II do Sacro Império Romano-Germânico
07-14|São Camilo de Lélis|Camilo de Lélis
07-15|São Boaventura|Boaventura de Bagnoregio
07-16|Nossa Senhora do Carmo|Nossa Senhora do Carmo
07-20|Santo Apolinário|Apolinário de Ravena
07-21|São Lourenço de Brindisi|Lourenço de Brindisi
07-22|Santa Maria Madalena|Maria Madalena
07-23|Santa Brígida da Suécia|Brígida da Suécia
07-24|São Charbel Makhlouf|Charbel Makhlouf
07-25|São Tiago Maior|Tiago, filho de Zebedeu
07-26|Santos Joaquim e Ana|Joaquim e Ana
07-29|Santa Marta|Marta de Betânia
07-30|São Pedro Crisólogo|Pedro Crisólogo
07-31|Santo Inácio de Loyola|Inácio de Loyola
08-01|Santo Afonso Maria de Ligório|Afonso Maria de Ligório
08-02|Santo Eusébio de Vercelli|Eusébio de Vercelli
08-04|São João Maria Vianney|João Maria Vianney
08-05|Dedicação da Basílica de Santa Maria Maior|Basílica de Santa Maria Maior
08-06|Transfiguração do Senhor|Transfiguração de Jesus
08-07|São Caetano|Caetano de Thiene
08-08|São Domingos de Gusmão|Domingos de Gusmão
08-09|Santa Teresa Benedita da Cruz (Edith Stein)|Edith Stein
08-10|São Lourenço|Lourenço de Roma
08-11|Santa Clara de Assis|Clara de Assis
08-12|Santa Joana Francisca de Chantal|Joana Francisca de Chantal
08-13|Santa Dulce dos Pobres|Irmã Dulce
08-14|São Maximiliano Maria Kolbe|Maximiliano Kolbe
08-15|Assunção de Nossa Senhora|Assunção de Maria
08-16|São Roque|Roque de Montpellier
08-18|Santa Helena|Santa Helena
08-19|São João Eudes|João Eudes
08-20|São Bernardo de Claraval|Bernardo de Claraval
08-21|São Pio X|Pio X
08-22|Nossa Senhora Rainha|Realeza de Maria
08-23|Santa Rosa de Lima|Rosa de Lima
08-24|São Bartolomeu|Bartolomeu (apóstolo)
08-25|São Luís IX, rei da França|Luís IX de França
08-27|Santa Mônica|Mônica de Hipona
08-28|Santo Agostinho|Agostinho de Hipona
08-29|Martírio de São João Batista|João Batista
09-03|São Gregório Magno|Gregório I
09-05|Santa Teresa de Calcutá|Teresa de Calcutá
09-08|Natividade de Nossa Senhora|Natividade de Maria
09-09|São Pedro Claver|Pedro Claver
09-12|Santíssimo Nome de Maria|Santíssimo Nome de Maria
09-13|São João Crisóstomo|João Crisóstomo
09-14|Exaltação da Santa Cruz|Exaltação da Santa Cruz
09-15|Nossa Senhora das Dores|Nossa Senhora das Dores
09-16|Santos Cornélio e Cipriano|Cipriano de Cartago
09-17|São Roberto Belarmino|Roberto Belarmino
09-19|São Januário|Januário de Benevento
09-20|São André Kim Taegon e companheiros|André Kim Taegon
09-21|São Mateus, apóstolo e evangelista|Mateus, o Evangelista
09-23|São Pio de Pietrelcina|Padre Pio
09-26|São Cosme e São Damião|Cosme e Damião
09-27|São Vicente de Paulo|Vicente de Paulo
09-28|São Venceslau|Venceslau I da Boêmia
09-29|São Miguel, São Gabriel e São Rafael|Miguel (arcanjo)
09-30|São Jerônimo|Jerônimo de Estridão
10-01|Santa Teresinha do Menino Jesus|Teresa de Lisieux
10-02|Santos Anjos da Guarda|Anjo da guarda
10-04|São Francisco de Assis|Francisco de Assis
10-06|São Bruno|Bruno de Colônia
10-07|Nossa Senhora do Rosário|Nossa Senhora do Rosário
10-09|São Dionísio|Dionísio de Paris
10-11|São João XXIII|João XXIII
10-12|Nossa Senhora Aparecida|Nossa Senhora da Conceição Aparecida
10-14|São Calisto I|Calisto I
10-15|Santa Teresa de Ávila|Teresa de Ávila
10-16|Santa Edwiges|Edwiges da Silésia
10-17|Santo Inácio de Antioquia|Inácio de Antioquia
10-18|São Lucas Evangelista|Lucas, o Evangelista
10-19|São Paulo da Cruz|Paulo da Cruz
10-22|São João Paulo II|João Paulo II
10-23|São João de Capistrano|João de Capistrano
10-24|Santo Antônio Maria Claret|Antônio Maria Claret
10-28|São Simão e São Judas Tadeu|Judas Tadeu
11-01|Todos os Santos|Dia de Todos os Santos
11-02|Comemoração dos Fiéis Defuntos|Dia de Finados
11-03|São Martinho de Porres|Martinho de Porres
11-04|São Carlos Borromeu|Carlos Borromeu
11-09|Dedicação da Basílica de Latrão|Arquibasílica de São João de Latrão
11-10|São Leão Magno|Leão I
11-11|São Martinho de Tours|Martinho de Tours
11-12|São Josafá|Josafá Kuntsevych
11-13|Santa Francisca Xavier Cabrini|Francisca Xavier Cabrini
11-15|Santo Alberto Magno|Alberto Magno
11-16|Santa Gertrudes|Gertrudes de Helfta
11-17|Santa Isabel da Hungria|Isabel da Hungria
11-18|Dedicação das Basílicas de São Pedro e São Paulo|Basílica de São Pedro
11-21|Apresentação de Nossa Senhora|Apresentação de Maria
11-22|Santa Cecília|Cecília de Roma
11-23|São Clemente I|Clemente I
11-24|Santo André Dung-Lac e companheiros|André Dũng-Lạc
11-25|Santa Catarina de Alexandria|Catarina de Alexandria
11-30|Santo André, apóstolo|André (apóstolo)
12-03|São Francisco Xavier|Francisco Xavier
12-04|Santa Bárbara|Bárbara de Nicomédia
12-06|São Nicolau|Nicolau de Mira
12-07|Santo Ambrósio|Ambrósio de Milão
12-08|Imaculada Conceição de Nossa Senhora|Imaculada Conceição
12-09|São Juan Diego|Juan Diego
12-11|São Dâmaso I|Dâmaso I
12-12|Nossa Senhora de Guadalupe|Nossa Senhora de Guadalupe
12-13|Santa Luzia|Luzia de Siracusa
12-14|São João da Cruz|João da Cruz
12-21|São Pedro Canísio|Pedro Canísio
12-23|São João de Kety|João de Kęty
12-25|Natal do Senhor|Natal
12-26|Santo Estêvão|Estêvão
12-27|São João Evangelista|João, o Apóstolo
12-28|Santos Inocentes|Santos Inocentes
12-29|São Tomás Becket|Tomás Becket
12-31|São Silvestre I|Silvestre I
"""

# Nos dias sem festa no calendário acima, mostramos um destes santos ("Para conhecer hoje").
POOL_TXT = """
São Benedito|Benedito, o Mouro
São Cristóvão|Cristóvão (santo)
São Geraldo Majela|Geraldo Majela
Santa Zita|Zita de Lucca
São Tarcísio|Tarcísio
São Domingos Sávio|Domingos Sávio
Frei Galvão|Antônio de Sant'Anna Galvão
Beata Nhá Chica|Nhá Chica
São Pantaleão|Pantaleão
Santa Teresa dos Andes|Teresa de los Andes
Santa Rosa de Viterbo|Rosa de Viterbo
Santa Gemma Galgani|Gemma Galgani
Santa Faustina Kowalska|Faustina Kowalska
Santa Kateri Tekakwitha|Kateri Tekakwitha
Santa Isabel Ana Seton|Elizabeth Ann Seton
São João Neumann|João Nepomuceno Neumann
Santa Rafaela Maria|Rafaela Maria
São Ladislau|Ladislau I da Hungria
São Lourenço Ruiz|Lourenço Ruiz
São José Cafasso|José Cafasso
São José Bento Cottolengo|José Bento Cottolengo
São Leopoldo Mandić|Leopoldo Mandić
São Miguel Garicoits|Miguel Garicoits
Santa Maria Mazzarello|Maria Domingas Mazzarello
São Francisco Régis|Francisco Régis
São José Moscati|Giuseppe Moscati
São João Calábria|João Calábria
Santa Catarina Labouré|Catarina Labouré
Santos Luís e Zélia Martin|Louis e Zélie Martin
Santo Ivo|Ivo de Kermartin
São Lázaro|Lázaro de Betânia
São Onofre|Onofre
São Vito|Vito
Santa Mônica|Mônica de Hipona
São Francisco e Santa Jacinta Marto|Francisco e Jacinta Marto
Beata Chiara Luce Badano|Chiara Luce Badano
Beato Carlo Acutis|Carlo Acutis
São Nuno de Santa Maria|Nuno Álvares Pereira
São João de Deus|João de Deus
Santa Josefina Bakhita|Josefina Bakhita
"""


def _ler(txt, partes):
    linhas = []
    for linha in txt.strip().splitlines():
        p = [x.strip() for x in linha.split("|")]
        if len(p) == partes and all(p):
            linhas.append(p)
    return linhas


CALENDARIO = {}
for _mmdd, _nome, _titulo in _ler(CALENDARIO_TXT, 3):
    CALENDARIO[_mmdd] = (_nome, _titulo)
POOL = [(n, t) for n, t in _ler(POOL_TXT, 2)]


def escolher(dia: date):
    """Retorna (nome exibido, título na Wikipédia, é_festa_do_dia)."""
    chave = f"{dia.month:02d}-{dia.day:02d}"
    if chave in CALENDARIO:
        nome, titulo = CALENDARIO[chave]
        return nome, titulo, True
    nome, titulo = POOL[dia.timetuple().tm_yday % len(POOL)]
    return nome, titulo, False


# ------------------------------------------------------------------ Wikipédia
API = "https://pt.wikipedia.org/w/api.php"
USER_AGENT = "EscalaCerimoniariosLimao/1.0 (aplicativo paroquial; Flask; urllib)"
TTL_OK = 24 * 3600
TTL_FALHA = 5 * 60
LIMITE_TEXTO = 1600

_cache = {}            # titulo -> (expira_em, resultado ou None)
_trava = threading.Lock()


def _chamar(params, timeout=6):
    url = API + "?" + urlencode({**params, "format": "json", "formatversion": "2"})
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _cortar(texto, limite=LIMITE_TEXTO):
    """Divide em parágrafos e corta no fim de uma frase, sem passar do limite."""
    paragrafos = [p.strip() for p in texto.replace("\r", "").split("\n") if p.strip()]
    saida, total = [], 0
    for p in paragrafos:
        if total + len(p) <= limite:
            saida.append(p)
            total += len(p)
            continue
        if not saida:  # primeiro parágrafo já é maior que o limite
            corte = p[:limite]
            fim = max(corte.rfind(". "), corte.rfind("! "), corte.rfind("? "))
            saida.append(corte[:fim + 1] if fim > limite // 3 else corte.rstrip() + "…")
        break
    return saida


def _pagina(titulo):
    dados = _chamar({
        "action": "query", "redirects": "1", "titles": titulo,
        "prop": "extracts|pageimages|pageprops|info",
        "exintro": "1", "explaintext": "1", "exlimit": "1",
        "piprop": "thumbnail", "pithumbsize": "500",
        "ppprop": "disambiguation", "inprop": "url",
    })
    paginas = (dados.get("query") or {}).get("pages") or []
    pg = paginas[0] if paginas else None
    if not pg or pg.get("missing") or pg.get("invalid"):
        return None
    if "disambiguation" in (pg.get("pageprops") or {}):
        return None
    extrato = (pg.get("extract") or "").strip()
    if len(extrato) < 80:
        return None
    return {
        "titulo": pg.get("title", titulo),
        "paragrafos": _cortar(extrato),
        "imagem": (pg.get("thumbnail") or {}).get("source"),
        "url": pg.get("fullurl") or "https://pt.wikipedia.org/wiki/" + pg.get("title", titulo).replace(" ", "_"),
    }


def _achar_titulo(termo):
    dados = _chamar({"action": "query", "list": "search", "srsearch": termo,
                     "srlimit": "1", "srnamespace": "0"})
    achados = (dados.get("query") or {}).get("search") or []
    return achados[0]["title"] if achados else None


def obter(titulo, nome):
    """Texto e foto da Wikipédia para o santo; None se não der (sem internet, página inexistente...)."""
    agora = time.time()
    with _trava:
        item = _cache.get(titulo)
        if item and item[0] > agora:
            return item[1]
    resultado = None
    try:
        resultado = _pagina(titulo)
        if resultado is None:
            achado = _achar_titulo(nome)
            if achado:
                resultado = _pagina(achado)
    except (URLError, TimeoutError, OSError, ValueError, KeyError, IndexError):
        resultado = None
    with _trava:
        _cache[titulo] = (agora + (TTL_OK if resultado else TTL_FALHA), resultado)
        if len(_cache) > 500:  # evita crescer sem limite
            _cache.clear()
    return resultado
