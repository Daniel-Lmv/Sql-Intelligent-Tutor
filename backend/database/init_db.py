import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "its.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ==========================
# TABELA USUARIOS
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE
)
""")

# ==========================
# TABELA CONCEITOS
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS conceitos (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    descricao TEXT
)
""")

# ==========================
# TABELA QUESTOES
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS questoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    conceito_id INTEGER,

    enunciado TEXT NOT NULL,

    sql_gabarito TEXT NOT NULL,

    FOREIGN KEY(conceito_id)
        REFERENCES conceitos(id)
)
""")

# ==========================
# TABELA PROFICIENCIA
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS proficiencia (
    usuario_id INTEGER,

    conceito_id INTEGER,

    nivel REAL DEFAULT 0,

    PRIMARY KEY(usuario_id, conceito_id),

    FOREIGN KEY(usuario_id)
        REFERENCES usuarios(id),

    FOREIGN KEY(conceito_id)
        REFERENCES conceitos(id)
)
""")

# ==========================
# TABELA RESPOSTAS
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS respostas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER,

    questao_id INTEGER,

    resposta_sql TEXT,

    correta INTEGER,

    data_resposta DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(usuario_id)
        REFERENCES usuarios(id),

    FOREIGN KEY(questao_id)
        REFERENCES questoes(id)
)
""")

# ==========================
# POPULAR CONCEITOS
# ==========================

cursor.execute("DELETE FROM conceitos")

conceitos = [
    (1, "SELECT", "Selecionar colunas"),
    (2, "WHERE", "Filtrar registros"),
    (3, "ORDER BY", "Ordenar resultados"),
    (4, "AGREGACOES", "COUNT SUM AVG"),
    (5, "GROUP BY", "Agrupar registros"),
    (6, "HAVING", "Filtrar grupos"),
    (7, "JOINS", "Combinar tabelas"),
    (8, "SUBQUERIES", "Consultas aninhadas")
]

cursor.executemany("""
INSERT INTO conceitos
VALUES (?, ?, ?)
""", conceitos)

conn.commit()
conn.close()

print("its.db criado e populado com sucesso!")