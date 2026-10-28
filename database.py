"""Banco de dados (SQLite) da Escala cerimoniarios do Limão."""
import os
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


def conectar():
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
