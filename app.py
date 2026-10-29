"""Escala cerimoniarios do Limão — Paróquia Santo Antônio do Limão."""
import json
import os
import re
import secrets
import time
from datetime import date, datetime, timedelta, timezone
from functools import wraps
from zoneinfo import ZoneInfo

from flask import (Flask, Response, abort, flash, g, redirect, render_template, request,
                   send_from_directory, session, url_for)
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.security import check_password_hash

import database as dbm
import quiz_perguntas
import santo_do_dia
from sorteio import (FUNCAO_PADRAO, FUNCOES_PADRAO, atribuir_funcoes,
                     contagens_para_painel, sortear_pessoas)

try:
    FUSO = ZoneInfo("America/Sao_Paulo")
except Exception:  # Windows sem o pacote tzdata: o Brasil não usa horário de verão
    FUSO = timezone(timedelta(hours=-3))

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=8)
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = bool(os.environ.get("PRODUCAO"))

dbm.init_db()


def _chave_secreta():
    if os.environ.get("SECRET_KEY"):
        return os.environ["SECRET_KEY"]
    arq = dbm.DATA_DIR / "secret_key"
    if not arq.exists():
        arq.write_text(secrets.token_hex(32))
    return arq.read_text().strip()


app.secret_key = _chave_secreta()

# ---------------------------------------------------------------- utilidades

DIAS = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira",
        "sexta-feira", "sábado", "domingo"]
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]


def hoje_iso():
    return datetime.now(FUSO).date().isoformat()


def agora_hora():
    """Hora atual (HH:MM) no fuso de São Paulo."""
    return datetime.now(FUSO).strftime("%H:%M")


# Uma missa "já passou" quando chega o horário dela (às 19h de uma missa das 19h, ela sai da lista).
FUTURA = "(data > ? OR (data = ? AND hora > ?))"
PASSADA = "(data < ? OR (data = ? AND hora <= ?))"


def get_db():
    if "db" not in g:
        g.db = dbm.conectar()
    return g.db


@app.teardown_appcontext
def fechar_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.template_filter("dia_semana")
def dia_semana(iso):
    return DIAS[date.fromisoformat(iso).weekday()]


@app.template_filter("data_extensa")
def data_extensa(iso):
    d = date.fromisoformat(iso)
    return f"{d.day} de {MESES[d.month - 1]}"


@app.template_filter("dia_num")
def dia_num(iso):
    return f"{date.fromisoformat(iso).day:02d}"


@app.template_filter("mes_curto")
def mes_curto(iso):
    return MESES[date.fromisoformat(iso).month - 1][:3]


@app.template_filter("hora_fmt")
def hora_fmt(hora):
    h, m = hora.split(":")
    return f"{int(h)}h" if m == "00" else f"{int(h)}h{m}"


@app.template_filter("data_curta")
def data_curta(iso):
    d = date.fromisoformat(iso)
    return d.strftime("%d/%m/%Y")


def csrf_token():
    if "csrf" not in session:
        session["csrf"] = secrets.token_urlsafe(32)
    return session["csrf"]


app.jinja_env.globals["csrf_token"] = csrf_token


@app.context_processor
def contexto():
    return {"admin": bool(session.get("admin"))}


@app.before_request
def proteger_posts():
    if request.method == "POST":
        esperado = session.get("csrf", "")
        enviado = request.form.get("csrf_token", "")
        try:
            ok = bool(esperado) and secrets.compare_digest(esperado, enviado)
        except TypeError:
            ok = False
        if not ok:
            abort(400)


@app.after_request
def cabecalhos(resp):
    resp.headers.setdefault("X-Content-Type-Options", "nosniff")
    resp.headers.setdefault("X-Frame-Options", "DENY")
    return resp


def login_obrigatorio(f):
    @wraps(f)
    def interno(*a, **kw):
        if not session.get("admin"):
            flash("Entre como coordenador para acessar essa área.", "erro")
            return redirect(url_for("entrar"))
        return f(*a, **kw)
    return interno


def carregar_escalas(db, ids_missas):
    if not ids_missas:
        return {}
    marcas = ",".join("?" * len(ids_missas))
    linhas = db.execute(
        f"""SELECT e.id, e.missa_id, e.cerimoniario_id, e.funcao, c.nome, c.foto
              FROM escala e JOIN cerimoniarios c ON c.id = e.cerimoniario_id
             WHERE e.missa_id IN ({marcas})
             ORDER BY e.missa_id, e.ordem, e.id""",
        ids_missas,
    ).fetchall()
    por_missa = {i: [] for i in ids_missas}
    for l in linhas:
        por_missa[l["missa_id"]].append(l)
    return por_missa


# ------------------------------------------------------------------ público

@app.route("/")
def index():
    db = get_db()
    hoje = hoje_iso()
    missas = db.execute(
        f"SELECT * FROM missas WHERE {FUTURA} AND publicada = 1 ORDER BY data, hora, id",
        (hoje, hoje, agora_hora()),
    ).fetchall()
    escalas = carregar_escalas(db, [m["id"] for m in missas])
    return render_template("index.html", missas=missas, escalas=escalas, hoje=hoje)


@app.route("/saude")
def saude():
    # usado pelo monitor que mantém o site acordado; não consulta o banco de propósito
    return f"ok\nbanco: {dbm.MODO_BANCO}", 200, {"Content-Type": "text/plain; charset=utf-8", "Cache-Control": "no-store"}


@app.route("/funcoes")
def funcoes():
    return render_template("funcoes.html")


@app.route("/santo")
def santo():
    hoje = date.fromisoformat(hoje_iso())
    try:
        dia = date.fromisoformat(request.args.get("dia", ""))
        if not (2000 <= dia.year <= 2100):
            raise ValueError
    except ValueError:
        dia = hoje
    info = santo_do_dia.obter(dia.day, dia.month)
    return render_template(
        "santo.html", info=info, dia=dia.isoformat(),
        ontem=(dia - timedelta(days=1)).isoformat(), amanha=(dia + timedelta(days=1)).isoformat(),
        e_hoje=(dia == hoje), fonte=santo_do_dia.PAGINA_FONTE,
    )


@app.route("/quiz")
def quiz():
    return render_template("quiz.html", perguntas=quiz_perguntas.carregar())


@app.route("/fotos/<path:nome>")
def foto(nome):
    resp = send_from_directory(dbm.FOTOS_DIR, nome)
    resp.headers["Cache-Control"] = "public, max-age=86400"
    return resp


# -------------------------------------------------------------------- login

TENTATIVAS = {}      # ip -> (falhas, bloqueado_ate)
MAX_FALHAS = 5
BLOQUEIO_SEG = 300


@app.route("/entrar", methods=["GET", "POST"])
def entrar():
    if session.get("admin"):
        return redirect(url_for("painel"))
    if request.method == "POST":
        ip = request.remote_addr or "?"
        falhas, ate = TENTATIVAS.get(ip, (0, 0))
        if ate > time.time():
            flash("Muitas tentativas. Aguarde alguns minutos e tente de novo.", "erro")
            return render_template("login.html"), 429
        usuario = request.form.get("usuario", "").strip()
        senha = request.form.get("senha", "")
        row = get_db().execute(
            "SELECT * FROM admins WHERE usuario = ?", (usuario,)
        ).fetchone()
        if row and check_password_hash(row["senha_hash"], senha):
            session.clear()
            session["admin"] = row["usuario"]
            session.permanent = True
            TENTATIVAS.pop(ip, None)
            return redirect(url_for("painel"))
        falhas += 1
        TENTATIVAS[ip] = (falhas, time.time() + BLOQUEIO_SEG if falhas >= MAX_FALHAS else 0)
        flash("Usuário ou senha incorretos.", "erro")
        return render_template("login.html"), 401
    return render_template("login.html")


@app.route("/sair", methods=["POST"])
def sair():
    session.clear()
    return redirect(url_for("index"))


# -------------------------------------------------------------------- painel

@app.route("/admin")
@login_obrigatorio
def painel():
    db = get_db()
    hoje = hoje_iso()
    agora = agora_hora()
    proximas = db.execute(
        f"SELECT * FROM missas WHERE {FUTURA} ORDER BY data, hora, id", (hoje, hoje, agora)
    ).fetchall()
    anteriores = db.execute(
        f"SELECT * FROM missas WHERE {PASSADA} ORDER BY data DESC, hora DESC LIMIT 10",
        (hoje, hoje, agora),
    ).fetchall()
    escalas = carregar_escalas(db, [m["id"] for m in proximas + anteriores])
    return render_template("painel.html", proximas=proximas, anteriores=anteriores,
                           escalas=escalas, hoje=hoje)


def _ativos(db):
    return db.execute(
        "SELECT * FROM cerimoniarios WHERE ativo = 1 ORDER BY nome COLLATE NOCASE"
    ).fetchall()


def ler_funcoes(form):
    funcoes = []
    for i in range(1, 7):
        v = " ".join(form.get(f"funcao_{i}", "").split())[:30]
        if v and v.lower() not in [f.lower() for f in funcoes]:
            funcoes.append(v)
    return funcoes


def ler_missa(db, form, exigir_futuro=False):
    erros = []
    nome = " ".join(form.get("nome", "").split())[:80]
    if not nome:
        erros.append("Informe o nome da celebração.")
    data = form.get("data", "")
    try:
        d = date.fromisoformat(data)
        if exigir_futuro and data < hoje_iso():
            erros.append("A data da missa já passou. Escolha hoje ou uma data futura.")
    except ValueError:
        erros.append("Informe uma data válida.")
    hora = form.get("hora", "")
    if not re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", hora):
        erros.append("Informe um horário válido.")
    elif exigir_futuro and data == hoje_iso() and hora <= agora_hora():
        erros.append("O horário dessa missa já passou. Escolha um horário futuro.")
    recado = form.get("recado", "").replace("\r", "").strip()[:300]
    try:
        qtd = int(form.get("quantidade", ""))
        if not 1 <= qtd <= 30:
            raise ValueError
    except ValueError:
        qtd = 0
        erros.append("A quantidade de cerimoniários deve ser entre 1 e 30.")
    ativos = {c["id"] for c in _ativos(db)}
    disponiveis = [int(x) for x in form.getlist("disponiveis") if x.isdigit() and int(x) in ativos]
    if not disponiveis:
        erros.append("Marque ao menos um cerimoniário disponível.")
    elif qtd and len(disponiveis) < qtd:
        erros.append(f"Você pediu {qtd} cerimoniários, mas marcou só {len(disponiveis)} disponíveis.")
    return {"nome": nome, "data": data, "hora": hora, "quantidade": qtd,
            "disponiveis": disponiveis, "funcoes": ler_funcoes(form), "recado": recado}, erros


def valores_form(dados=None):
    dados = dados or {}
    funcoes = list(dados.get("funcoes", FUNCOES_PADRAO))
    funcoes += [""] * (6 - len(funcoes))
    return {
        "nome": dados.get("nome", ""),
        "data": dados.get("data", ""),
        "hora": dados.get("hora", ""),
        "recado": dados.get("recado", ""),
        "quantidade": dados.get("quantidade") or 6,
        "disponiveis": set(dados.get("disponiveis", [])),
        "funcoes": funcoes[:6],
    }


def gravar_sorteio(db, missa_id, dados):
    pessoas = sortear_pessoas(db, missa_id, dados["disponiveis"], dados["quantidade"], hoje_iso())
    atribuicoes = atribuir_funcoes(db, missa_id, pessoas, dados["funcoes"])
    db.execute("DELETE FROM escala WHERE missa_id = ?", (missa_id,))
    db.executemany(
        "INSERT INTO escala (missa_id, cerimoniario_id, funcao, ordem) VALUES (?, ?, ?, ?)",
        [(missa_id, cid, fn, i) for i, (cid, fn) in enumerate(atribuicoes)],
    )
    if len(pessoas) < dados["quantidade"]:
        flash(f"Não foi possível completar a escala: saíram {len(pessoas)} de "
              f"{dados['quantidade']} cerimoniários. Marque mais pessoas disponíveis e sorteie de novo.", "aviso")
    if len(dados["funcoes"]) > len(pessoas):
        flash("Há mais funções do que cerimoniários: as últimas funções ficaram sem ninguém.", "aviso")


def gravar_missa(db, missa_id, dados):
    db.execute(
        "UPDATE missas SET nome=?, data=?, hora=?, quantidade=?, funcoes=?, recado=? WHERE id=?",
        (dados["nome"], dados["data"], dados["hora"], dados["quantidade"],
         json.dumps(dados["funcoes"], ensure_ascii=False), dados["recado"], missa_id),
    )
    db.execute("DELETE FROM missa_disponiveis WHERE missa_id = ?", (missa_id,))
    db.executemany(
        "INSERT INTO missa_disponiveis (missa_id, cerimoniario_id) VALUES (?, ?)",
        [(missa_id, c) for c in dados["disponiveis"]],
    )


@app.route("/admin/missas/nova", methods=["GET", "POST"])
@login_obrigatorio
def nova_missa():
    db = get_db()
    if request.method == "POST":
        dados, erros = ler_missa(db, request.form, exigir_futuro=True)
        if erros:
            for e in erros:
                flash(e, "erro")
            return render_template("missa_nova.html", v=valores_form(
                {**dados, "funcoes": [request.form.get(f"funcao_{i}", "") for i in range(1, 7)]}),
                cerimoniarios=_ativos(db), hoje=hoje_iso()), 400
        cur = db.execute(
            "INSERT INTO missas (nome, data, hora, quantidade, funcoes, recado, publicada) VALUES (?, ?, ?, ?, ?, ?, 0)",
            (dados["nome"], dados["data"], dados["hora"], dados["quantidade"],
             json.dumps(dados["funcoes"], ensure_ascii=False), dados["recado"]),
        )
        mid = cur.lastrowid
        gravar_missa(db, mid, dados)
        gravar_sorteio(db, mid, dados)
        db.commit()
        flash("Escala sorteada! Ela ainda é um rascunho e não aparece no site. Ajuste as funções, se quiser, "
              "e clique em “Publicar”. Depois de publicada, não dá mais para alterar.", "ok")
        return redirect(url_for("painel"))
    return render_template("missa_nova.html", v=valores_form(), cerimoniarios=_ativos(db),
                           hoje=hoje_iso())


@app.route("/admin/missas/<int:mid>/funcoes", methods=["GET", "POST"])
@login_obrigatorio
def editar_funcoes(mid):
    """Antes de publicar, o coordenador pode ajustar só as funções de cada vaga."""
    db = get_db()
    missa = db.execute("SELECT * FROM missas WHERE id = ?", (mid,)).fetchone()
    if not missa:
        abort(404)
    if missa["publicada"]:
        flash("Esta escala já foi publicada e não pode mais ser alterada. Se precisar, exclua a missa e cadastre de novo.", "aviso")
        return redirect(url_for("painel"))
    escala = carregar_escalas(db, [mid])[mid]
    if request.method == "POST":
        validas = {str(e["id"]) for e in escala}
        for sid, fn in zip(request.form.getlist("slot_id"), request.form.getlist("funcao_vaga")):
            if sid not in validas:
                continue
            fn = " ".join(fn.split())[:30] or FUNCAO_PADRAO
            db.execute("UPDATE escala SET funcao = ? WHERE id = ? AND missa_id = ?", (fn, int(sid), mid))
        if request.form.get("acao") == "publicar":
            db.execute("UPDATE missas SET publicada = 1 WHERE id = ?", (mid,))
            flash("Funções salvas e escala publicada no site.", "ok")
        else:
            flash("Funções salvas. A escala continua como rascunho.", "ok")
        db.commit()
        return redirect(url_for("painel"))
    sugestoes = []
    for f in json.loads(missa["funcoes"] or "[]") + [FUNCAO_PADRAO]:
        if f and f not in sugestoes:
            sugestoes.append(f)
    return render_template("funcoes_editar.html", missa=missa, escala=escala, sugestoes=sugestoes)


@app.route("/admin/missas/<int:mid>/publicar", methods=["POST"])
@login_obrigatorio
def publicar_missa(mid):
    db = get_db()
    db.execute("UPDATE missas SET publicada = 1 WHERE id = ?", (mid,))
    db.commit()
    flash("Escala publicada no site.", "ok")
    return redirect(url_for("painel"))


@app.route("/admin/missas/<int:mid>/excluir", methods=["POST"])
@login_obrigatorio
def excluir_missa(mid):
    db = get_db()
    db.execute("DELETE FROM missas WHERE id = ?", (mid,))
    db.commit()
    flash("Missa excluída.", "ok")
    return redirect(url_for("painel"))


# ------------------------------------------------------------ backup e restauração

@app.route("/admin/backup")
@login_obrigatorio
def backup():
    """Baixa um arquivo com tudo (cerimoniários, missas, disponíveis e escalas), sem depender de ids."""
    db = get_db()
    cer = db.execute("SELECT id, nome, ativo FROM cerimoniarios ORDER BY id").fetchall()
    nome_de = {c["id"]: c["nome"] for c in cer}
    missas = db.execute("SELECT * FROM missas ORDER BY data, hora, id").fetchall()
    disp = {m["id"]: [] for m in missas}
    esc = {m["id"]: [] for m in missas}
    for r in db.execute("SELECT missa_id, cerimoniario_id FROM missa_disponiveis"):
        if r["missa_id"] in disp and r["cerimoniario_id"] in nome_de:
            disp[r["missa_id"]].append(nome_de[r["cerimoniario_id"]])
    for r in db.execute("SELECT missa_id, cerimoniario_id, funcao, ordem FROM escala ORDER BY missa_id, ordem, id"):
        if r["missa_id"] in esc and r["cerimoniario_id"] in nome_de:
            esc[r["missa_id"]].append({"nome": nome_de[r["cerimoniario_id"]], "funcao": r["funcao"]})
    dados = {
        "versao": 1,
        "gerado_em": datetime.now(FUSO).isoformat(timespec="seconds"),
        "cerimoniarios": [{"nome": c["nome"], "ativo": int(c["ativo"])} for c in cer],
        "missas": [{
            "nome": m["nome"], "data": m["data"], "hora": m["hora"], "quantidade": m["quantidade"],
            "funcoes": json.loads(m["funcoes"] or "[]"), "recado": m["recado"],
            "publicada": int(m["publicada"]), "disponiveis": disp[m["id"]], "escala": esc[m["id"]],
        } for m in missas],
    }
    corpo = json.dumps(dados, ensure_ascii=False, indent=1)
    return Response(corpo, mimetype="application/json", headers={
        "Content-Disposition": f'attachment; filename="backup-escala-{hoje_iso()}.json"',
        "Cache-Control": "no-store",
    })


@app.route("/admin/restaurar", methods=["POST"])
@login_obrigatorio
def restaurar():
    """Substitui TODAS as missas pelas do arquivo de backup (cerimoniários são casados pelo nome)."""
    arq = request.files.get("arquivo")
    if not arq or not arq.filename:
        flash("Escolha o arquivo de backup.", "erro")
        return redirect(url_for("painel"))
    try:
        dados = json.loads(arq.read().decode("utf-8"))
        if dados.get("versao") != 1 or not isinstance(dados.get("missas"), list) \
                or not isinstance(dados.get("cerimoniarios"), list):
            raise ValueError("formato")
    except Exception:
        flash("Arquivo de backup inválido.", "erro")
        return redirect(url_for("painel"))

    db = get_db()
    try:
        ids = {r["nome"]: r["id"] for r in db.execute("SELECT id, nome FROM cerimoniarios")}

        def id_de(nome):
            nome = str(nome).strip()[:80]
            if nome not in ids:
                db.execute("INSERT INTO cerimoniarios (nome, foto, ativo) VALUES (?, NULL, 1)", (nome,))
                ids[nome] = db.execute("SELECT id FROM cerimoniarios WHERE nome = ?", (nome,)).fetchone()["id"]
            return ids[nome]

        for c in dados["cerimoniarios"]:
            if str(c.get("nome", "")).strip():
                db.execute("UPDATE cerimoniarios SET ativo = ? WHERE id = ?",
                           (1 if c.get("ativo", 1) else 0, id_de(c["nome"])))

        db.execute("DELETE FROM missas")          # a exclusão em cascata limpa escalas e disponíveis
        total = 0
        for m in dados["missas"]:
            data, hora = str(m.get("data", "")), str(m.get("hora", ""))
            date.fromisoformat(data)
            if not re.fullmatch(r"\d{2}:\d{2}", hora):
                raise ValueError("hora")
            funcoes = [" ".join(str(f).split())[:30] for f in (m.get("funcoes") or [])][:6]
            qtd = max(1, min(30, int(m.get("quantidade", 1))))
            cur = db.execute(
                "INSERT INTO missas (nome, data, hora, quantidade, funcoes, recado, publicada) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (str(m.get("nome", "Missa")).strip()[:80] or "Missa", data, hora, qtd,
                 json.dumps(funcoes, ensure_ascii=False), str(m.get("recado", ""))[:300],
                 1 if m.get("publicada", 1) else 0),
            )
            mid = cur.lastrowid
            vistos = []
            for nome in m.get("disponiveis") or []:
                cid = id_de(nome)
                if cid not in vistos:
                    vistos.append(cid)
            db.executemany("INSERT INTO missa_disponiveis (missa_id, cerimoniario_id) VALUES (?, ?)",
                           [(mid, c) for c in vistos])
            db.executemany(
                "INSERT INTO escala (missa_id, cerimoniario_id, funcao, ordem) VALUES (?, ?, ?, ?)",
                [(mid, id_de(e["nome"]), " ".join(str(e.get("funcao", "")).split())[:30] or FUNCAO_PADRAO, i)
                 for i, e in enumerate(m.get("escala") or [])],
            )
            total += 1
        db.commit()
    except Exception:
        db.rollback()
        flash("Não foi possível restaurar: o arquivo parece estar incompleto ou corrompido. "
              "Nada foi alterado.", "erro")
        return redirect(url_for("painel"))
    flash(f"Backup restaurado: {total} missa(s) recuperada(s).", "ok")
    return redirect(url_for("painel"))


# ------------------------------------------------------------ cerimoniários

@app.route("/admin/cerimoniarios")
@login_obrigatorio
def cerimoniarios():
    db = get_db()
    recentes, totais = contagens_para_painel(db, hoje_iso())
    lista = db.execute("SELECT * FROM cerimoniarios ORDER BY ativo DESC, nome COLLATE NOCASE").fetchall()
    return render_template("cerimoniarios.html", lista=lista, recentes=recentes, totais=totais)


@app.route("/admin/cerimoniarios/<int:cid>", methods=["POST"])
@login_obrigatorio
def atualizar_cerimoniario(cid):
    db = get_db()
    row = db.execute("SELECT * FROM cerimoniarios WHERE id = ?", (cid,)).fetchone()
    if not row:
        abort(404)
    acao = request.form.get("acao")
    if acao in ("ativar", "desativar"):
        db.execute("UPDATE cerimoniarios SET ativo = ? WHERE id = ?", (1 if acao == "ativar" else 0, cid))
        db.commit()
        flash(f"{row['nome']} {'voltou a aparecer' if acao == 'ativar' else 'saiu'} da lista de disponíveis.", "ok")
    return redirect(url_for("cerimoniarios"))


if __name__ == "__main__":
    app.run(debug=bool(os.environ.get("DEBUG")), host="0.0.0.0",
            port=int(os.environ.get("PORT", 5000)))
