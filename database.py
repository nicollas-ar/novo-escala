"""Banco de dados (SQLite) da Escala cerimoniarios do Limão."""
import os
import re
import shutil
import sqlite3
from pathlib import Path

from werkzeug.security import generate_password_hash

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.environ.get("DATA_DIR", BASE_DIR / "instance"))
DB_PATH = DATA_DIR / "escala.db"
FOTOS_DIR = DATA_DIR / "fotos"
SEED_FOTOS = BASE_DIR / "static" / "seed_fotos"

# (nome exibido, arquivo da foto), na ordem em que foram enviados
CERIMONIARIOS_INICIAIS = [
    ("Julio", "julio.jpg"),
    ("Pedro", "pedro.jpg"),
    ("Luana", "luana.jpg"),
    ("Thabata", "thabata.jpg"),
    ("Nicollas Augusto", "nicollas-augusto.jpg"),
    ("Bernardo", "bernardo.jpg"),
    ("Gabriel", "gabriel.jpg"),
    ("Dennys", "dennys.jpg"),
    ("Eguiberto", "eguiberto.jpg"),
    ("Guilherme", "guilherme.jpg"),
    ("Henrique", "henrique.jpg"),
    ("Nicolas", "nicolas.jpg"),
    ("Kauan", "kauan.jpg"),
    ("Larissa", "larissa.jpg"),
    ("Leonardo Oliveira", "leonardo-oliveira.jpg"),
    ("Manuela Navarro", "manuela-navarro.jpg"),
    ("Manuela", "manuela.jpg"),
    ("Rafaela", "rafaela.jpg"),
    ("Ruan", "ruan.jpg"),
    ("Maria Sofia", "maria-sofia.jpg"),
    ("Nicole Sophia", "nicole-sophia.jpg"),
    ("Layla", "layla.jpg"),
    ("Gustavo", "gustavo.jpg"),
    ("Leonardo", "leonardo.jpg"),
    ("Malu", "malu.jpg"),
    ("Vitor", "vitor.jpg"),
]

SCHEMA = """
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS cerimoniarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    foto TEXT,
    ativo INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS missas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    data TEXT NOT NULL,          -- AAAA-MM-DD
    hora TEXT NOT NULL,          -- HH:MM
    quantidade INTEGER NOT NULL,
    funcoes TEXT NOT NULL DEFAULT '[]',  -- lista JSON com as funções do sorteio
    publicada INTEGER NOT NULL DEFAULT 1, -- 0 = rascunho (só o coordenador vê)
    recado TEXT NOT NULL DEFAULT ''      -- aviso opcional exibido abaixo do horário
);
CREATE TABLE IF NOT EXISTS missa_disponiveis (
    missa_id INTEGER NOT NULL REFERENCES missas(id) ON DELETE CASCADE,
    cerimoniario_id INTEGER NOT NULL REFERENCES cerimoniarios(id) ON DELETE CASCADE,
    PRIMARY KEY (missa_id, cerimoniario_id)
);
CREATE TABLE IF NOT EXISTS escala (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    missa_id INTEGER NOT NULL REFERENCES missas(id) ON DELETE CASCADE,
    cerimoniario_id INTEGER NOT NULL REFERENCES cerimoniarios(id) ON DELETE CASCADE,
    funcao TEXT NOT NULL,
    ordem INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_missas_data ON missas(data, hora);
CREATE INDEX IF NOT EXISTS idx_escala_missa ON escala(missa_id);
CREATE INDEX IF NOT EXISTS idx_escala_cer ON escala(cerimoniario_id);
"""


# ---------------------------------------------------------------- PostgreSQL
# Se a variável DATABASE_URL existir (ex.: banco gratuito do Neon), o app usa PostgreSQL.
# Sem ela, usa o arquivo SQLite local (instance/escala.db), como antes.
def _limpar_url(texto):
    """Aceita a string do Neon mesmo se vier com aspas ou com o prefixo "psql" copiado junto."""
    texto = texto.strip().strip("\"'").strip()
    if texto.lower().startswith("psql "):
        texto = texto[5:].strip().strip("\"'").strip()
    return texto


DATABASE_URL = _limpar_url(os.environ.get("DATABASE_URL", ""))
USA_PG = bool(DATABASE_URL)
if USA_PG and not DATABASE_URL.startswith(("postgres://", "postgresql://")):
    # em vez de cair em silêncio no SQLite (e perder os dados a cada deploy), para com um erro claro
    raise RuntimeError(
        "DATABASE_URL está definida, mas não começa com postgresql://. "
        "Copie a connection string completa do Neon (botão Connect)."
    )
if os.environ.get("PRODUCAO") and not USA_PG and not os.environ.get("DATA_DIR"):
    # em produção, SQLite sem disco persistente perde os dados a cada deploy: melhor parar do que perder em silêncio
    raise RuntimeError(
        "Banco temporário em produção. Defina DATABASE_URL (banco externo, ex.: Neon) "
        "ou DATA_DIR apontando para um disco persistente."
    )
MODO_BANCO = "postgresql" if USA_PG else "sqlite"
try:
    from urllib.parse import urlparse
    _HOST = urlparse(DATABASE_URL).hostname if USA_PG else "arquivo local"
except Exception:  # pragma: no cover
    _HOST = "?"
print(f"[banco] usando {MODO_BANCO} ({_HOST})", flush=True)

SCHEMA_PG = SCHEMA.replace("INTEGER PRIMARY KEY AUTOINCREMENT", "SERIAL PRIMARY KEY")


class Linha:
    """Linha de resultado que se comporta como sqlite3.Row: aceita linha["coluna"] e linha[0]."""
    __slots__ = ("_idx", "_vals")

    def __init__(self, idx, vals):
        self._idx = idx
        self._vals = vals

    def __getitem__(self, k):
        if isinstance(k, str):
            return self._vals[self._idx[k]]
        return self._vals[k]

    def keys(self):
        return list(self._idx)

    def __iter__(self):
        return iter(self._vals)

    def __len__(self):
        return len(self._vals)


def _fabrica_linhas(cur):
    idx = {d.name: i for i, d in enumerate(cur.description or [])}
    return lambda valores: Linha(idx, tuple(valores))


class _Cursor:
    def __init__(self, cur, lastrowid=None):
        self._cur = cur
        self.lastrowid = lastrowid

    def fetchone(self):
        return self._cur.fetchone()

    def fetchall(self):
        return self._cur.fetchall()

    def __iter__(self):
        return iter(self._cur)


_RE_NOCASE = re.compile(r"([\w.]+)\s+COLLATE\s+NOCASE", re.I)
_RE_INSERT = re.compile(r"\s*INSERT\s+INTO\s+(\w+)", re.I)
_TABELAS_COM_ID = {"admins", "cerimoniarios", "missas", "escala"}


def _traduzir(sql):
    """Converte o SQL escrito para SQLite no equivalente de PostgreSQL."""
    sql = _RE_NOCASE.sub(r"LOWER(\1)", sql)
    return sql.replace("?", "%s")


class ConexaoPG:
    """Dá à conexão do PostgreSQL a mesma interface usada com o SQLite (execute, executemany, commit, close)."""

    def __init__(self, conn):
        self._conn = conn

    def execute(self, sql, params=()):
        sql_pg = _traduzir(sql)
        m = _RE_INSERT.match(sql)
        quer_id = bool(m and m.group(1).lower() in _TABELAS_COM_ID and "returning" not in sql.lower())
        if quer_id:
            sql_pg += " RETURNING id"
        cur = self._conn.execute(sql_pg, tuple(params))
        ultimo = None
        if quer_id:
            linha = cur.fetchone()
            ultimo = linha[0] if linha else None
        return _Cursor(cur, ultimo)

    def executemany(self, sql, linhas):
        with self._conn.cursor() as cur:
            cur.executemany(_traduzir(sql), [tuple(l) for l in linhas])

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def close(self):
        self._conn.close()


def _conectar_pg():
    import psycopg  # só é necessário quando DATABASE_URL está definida
    conn = psycopg.connect(
        DATABASE_URL,
        row_factory=_fabrica_linhas,
        prepare_threshold=None,   # compatível com o "pooler" do Neon
        connect_timeout=15,
    )
    return ConexaoPG(conn)


def conectar():
    if USA_PG:
        return _conectar_pg()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    FOTOS_DIR.mkdir(parents=True, exist_ok=True)

    # copia as fotos iniciais para a pasta de dados (onde ficam também os uploads)
    if SEED_FOTOS.exists():
        for arq in SEED_FOTOS.glob("*.jpg"):
            destino = FOTOS_DIR / arq.name
            if not destino.exists():
                shutil.copy(arq, destino)

    conn = conectar()
    if USA_PG:
        for comando in SCHEMA_PG.split(";"):
            if comando.strip():
                conn.execute(comando)
        conn.execute("ALTER TABLE missas ADD COLUMN IF NOT EXISTS publicada INTEGER NOT NULL DEFAULT 1")
        conn.execute("ALTER TABLE missas ADD COLUMN IF NOT EXISTS recado TEXT NOT NULL DEFAULT ''")
    else:
        conn.executescript(SCHEMA)
        colunas = [r["name"] for r in conn.execute("PRAGMA table_info(missas)")]
        if "publicada" not in colunas:  # bancos criados em versões anteriores: missas já existentes ficam publicadas
            conn.execute("ALTER TABLE missas ADD COLUMN publicada INTEGER NOT NULL DEFAULT 1")
        if "recado" not in colunas:  # bancos criados antes do recado: as missas existentes continuam, sem recado
            conn.execute("ALTER TABLE missas ADD COLUMN recado TEXT NOT NULL DEFAULT ''")

    if conn.execute("SELECT COUNT(*) FROM admins").fetchone()[0] == 0:
        usuario = os.environ.get("ADMIN_USER", "juliomalu")
        senha = os.environ.get("ADMIN_PASSWORD", "12345")
        conn.execute(
            "INSERT INTO admins (usuario, senha_hash) VALUES (?, ?)",
            (usuario, generate_password_hash(senha)),
        )

    if conn.execute("SELECT COUNT(*) FROM cerimoniarios").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO cerimoniarios (nome, foto) VALUES (?, ?)",
            CERIMONIARIOS_INICIAIS,
        )

    conn.commit()
    conn.close()
