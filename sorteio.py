"""Sorteio da escala: aleatório, mas favorecendo quem serviu menos recentemente."""
import math
import random
from datetime import date, timedelta

JANELA_DIAS = 60           # "recentemente" = últimos 60 dias (e missas já marcadas)
FUNCAO_PADRAO = "Cerimoniário"
FUNCOES_PADRAO = ["Padre", "Missal", "Leitor", "Gerenciar Coroinha"]


def _contagens(conn, missa_id, hoje):
    limite = (date.fromisoformat(hoje) - timedelta(days=JANELA_DIAS)).isoformat()
    recentes = {
        r["cerimoniario_id"]: r["n"]
        for r in conn.execute(
            """SELECT e.cerimoniario_id, COUNT(*) AS n
                 FROM escala e JOIN missas m ON m.id = e.missa_id
                WHERE m.id != ? AND m.data >= ?
                GROUP BY e.cerimoniario_id""",
            (missa_id, limite),
        )
    }
    totais = {
        r["cerimoniario_id"]: r["n"]
        for r in conn.execute(
            """SELECT e.cerimoniario_id, COUNT(*) AS n
                 FROM escala e JOIN missas m ON m.id = e.missa_id
                WHERE m.id != ?
                GROUP BY e.cerimoniario_id""",
            (missa_id,),
        )
    }
    return recentes, totais


def contagens_para_painel(conn, hoje):
    """Quantas vezes cada cerimoniário serviu (recente e total), para exibir no painel."""
    return _contagens(conn, -1, hoje)


# Regras fixas (só aparecem aqui no código).
# Pares que nunca saem na mesma escala sorteada:
REGRAS_FIXAS = []

# Pares que só saem juntos se não houver mais ninguém disponível para completar a escala:
REGRAS_SO_SE_NAO_HOUVER_OUTRA_OPCAO = [
    ("Thabata", "Nicolas"),
]

# Pares que SEMPRE saem juntos: se um é sorteado, o outro entra na mesma escala.
# (Se um dos dois não estiver marcado como disponível, o outro pode sair sozinho.)
REGRAS_SEMPRE_JUNTOS = [
    ("Thabata", "Nicollas Augusto"),
]

# Bônus de chance: (quem ganha o bônus, com quem, fator).
# Quando "com quem" é sorteado para a missa, "quem ganha" tem essa chance multiplicada
# (ex.: 1.2 = 20% a mais). Hoje vazio, porque REGRAS_SEMPRE_JUNTOS já garante a dupla.
BONUS_COM = []


def _ids_por_nome(conn):
    return {r["nome"]: r["id"] for r in conn.execute("SELECT id, nome FROM cerimoniarios")}


def mapa_conflitos(conn, regras=None):
    """id -> conjunto de ids que o sorteio não coloca juntos (por padrão, REGRAS_FIXAS)."""
    ids = _ids_por_nome(conn)
    mapa = {}
    for a, b in (REGRAS_FIXAS if regras is None else regras):
        if a in ids and b in ids:
            mapa.setdefault(ids[a], set()).add(ids[b])
            mapa.setdefault(ids[b], set()).add(ids[a])
    return mapa


def mapa_juntos(conn):
    """id -> id do parceiro que sempre sai junto (REGRAS_SEMPRE_JUNTOS)."""
    ids = _ids_por_nome(conn)
    mapa = {}
    for a, b in REGRAS_SEMPRE_JUNTOS:
        if a in ids and b in ids:
            mapa[ids[a]] = ids[b]
            mapa[ids[b]] = ids[a]
    return mapa


def _montar(unidades, n, proibido, presentes):
    """Primeira combinação de exatamente n pessoas, na ordem do sorteio, formada por
    "unidades" (1 pessoa, ou 2 que saem juntas) sem nenhum par proibido — inclusive em
    relação a quem já está presente. None se não houver nenhuma."""
    def livre(membros, atuais):
        conj = set(membros)
        return all(not (proibido.get(m, set()) & (atuais | (conj - {m}))) for m in membros)

    def rec(i, escolhidos, atuais):
        if len(escolhidos) == n:
            return escolhidos
        if i >= len(unidades):
            return None
        if len(escolhidos) + sum(len(u) for u in unidades[i:]) < n:
            return None
        u = unidades[i]
        if len(escolhidos) + len(u) <= n and livre(u, atuais):
            r = rec(i + 1, escolhidos + list(u), atuais | set(u))
            if r is not None:
                return r
        return rec(i + 1, escolhidos, atuais)
    return rec(0, [], set(presentes))


def _sortear_ponderado(candidatos, n, peso, duros, moles, juntos, presentes, rng):
    """Sorteio ponderado sem reposição (Efraimidis–Spirakis, em escala logarítmica).
    Ordem de prioridade das regras, da mais forte para a mais fraca:
      1. conflitos "duros" (nunca juntos)      2. pares "sempre juntos"
      3. conflitos "moles" (só se não houver outra opção)
    Se não houver combinação possível, as regras mais fracas são liberadas primeiro:
    a escala nunca sai incompleta."""
    chaves = {}
    for cid in candidatos:
        u = 1.0 - rng.random()          # (0, 1]
        chaves[cid] = math.log(u) / peso(cid)

    # cada dupla "sempre junta" entra no sorteio como uma unidade só, com chance
    # equivalente à média da chance dos dois (assim ela não perde nem ganha vantagem)
    chaves_dupla = {}
    for cid in candidatos:
        par = juntos.get(cid)
        if par is not None and par in chaves and frozenset((cid, par)) not in chaves_dupla:
            u = 1.0 - rng.random()
            chaves_dupla[frozenset((cid, par))] = math.log(u) / ((peso(cid) + peso(par)) / 2)

    def montar_unidades(com_pares):
        unidades, usados = [], set()
        for cid in candidatos:
            if cid in usados:
                continue
            par = juntos.get(cid) if com_pares else None
            if par is not None and par in chaves and par not in usados:
                usados.update((cid, par))
                unidades.append((chaves_dupla[frozenset((cid, par))], (cid, par)))
            else:
                usados.add(cid)
                unidades.append((chaves[cid], (cid,)))
        unidades.sort(key=lambda x: x[0], reverse=True)
        return [u for _, u in unidades]

    todos = {cid: duros.get(cid, set()) | moles.get(cid, set()) for cid in candidatos}
    pares, soltos = montar_unidades(True), montar_unidades(False)
    for unidades, proibido in ((pares, todos), (pares, duros),
                               (soltos, todos), (soltos, duros),
                               (pares, {}), (soltos, {})):
        r = _montar(unidades, n, proibido, presentes)
        if r is not None:
            return r
    return [m for u in soltos for m in u][:n]


def sortear_pessoas(conn, missa_id, candidatos, n, hoje, rng=random, fixos=()):
    """Escolhe n pessoas entre os candidatos (ids). Quem serviu menos recentemente
    tem mais chance, mas ninguém tem chance zero (sorteio ponderado)."""
    candidatos = list(dict.fromkeys(candidatos))
    n = max(0, min(n, len(candidatos)))
    if n == 0:
        return []
    recentes, totais = _contagens(conn, missa_id, hoje)

    def peso(cid):
        r = recentes.get(cid, 0)
        t = totais.get(cid, 0)
        return 1.0 / ((1 + r) ** 3) / (1 + t / 20.0)

    duros = mapa_conflitos(conn)
    moles = mapa_conflitos(conn, REGRAS_SO_SE_NAO_HOUVER_OUTRA_OPCAO)
    juntos = mapa_juntos(conn)

    # vaga extra numa escala que já existe: se alguém já escalado tem parceiro que
    # "sempre sai junto", o parceiro entra primeiro (a menos que quebre um conflito duro)
    forcados, presentes = [], set(fixos)
    for f in list(fixos):
        par = juntos.get(f)
        if (par in candidatos and par not in presentes and len(forcados) < n
                and not (duros.get(par, set()) & presentes)):
            forcados.append(par)
            presentes.add(par)
    if forcados:
        candidatos = [c for c in candidatos if c not in forcados]
        n -= len(forcados)
        if n == 0:
            return forcados

    escolhidos = forcados + _sortear_ponderado(candidatos, min(n, len(candidatos)), peso,
                                              duros, moles, juntos, presentes, rng)

    # bônus de chance (BONUS_COM): se "com quem" saiu, refaz o resto da escala
    # mantendo "com quem" fixo e dando o fator a "quem ganha"
    ids = _ids_por_nome(conn)
    for quem, com_quem, fator in BONUS_COM:
        if quem not in ids or com_quem not in ids:
            continue
        q, c = ids[quem], ids[com_quem]
        if c in escolhidos and q in candidatos:
            def peso_bonus(cid, q=q):
                return peso(cid) * (fator if cid == q else 1.0)
            resto = [x for x in candidatos if x != c]
            novos = _sortear_ponderado(resto, n - 1, peso_bonus, duros, moles, juntos,
                                       set(fixos) | {c}, rng)
            escolhidos = [c] + novos
    return escolhidos


def atribuir_funcoes(conn, missa_id, pessoas, funcoes, rng=random):
    """Distribui as funções entre as pessoas sorteadas, preferindo quem menos
    exerceu aquela função antes. Sobras ficam como 'Cerimoniário'.
    Retorna lista de (cerimoniario_id, funcao) já na ordem de exibição."""
    historico = {}
    for r in conn.execute(
        """SELECT e.cerimoniario_id, e.funcao, COUNT(*) AS n
             FROM escala e WHERE e.missa_id != ? GROUP BY e.cerimoniario_id, e.funcao""",
        (missa_id,),
    ):
        historico[(r["cerimoniario_id"], r["funcao"].lower())] = r["n"]

    restantes = list(pessoas)
    rng.shuffle(restantes)
    resultado = []
    for funcao in funcoes[: len(pessoas)]:
        melhor = min(
            restantes,
            key=lambda cid: (historico.get((cid, funcao.lower()), 0), rng.random()),
        )
        restantes.remove(melhor)
        resultado.append((melhor, funcao))
    for cid in restantes:
        resultado.append((cid, FUNCAO_PADRAO))
    return resultado
