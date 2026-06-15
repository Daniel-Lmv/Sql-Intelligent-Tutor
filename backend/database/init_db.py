import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "its.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# USUÁRIOS
cursor.execute("""
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE
)
""")


# CONCEITOS
cursor.execute("""
CREATE TABLE conceitos (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    descricao TEXT
)
""")

# QUESTÕES
cursor.execute("""
CREATE TABLE questoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    conceito_id INTEGER NOT NULL,

    enunciado TEXT NOT NULL UNIQUE,

    alternativa_a TEXT NOT NULL,
    alternativa_b TEXT NOT NULL,
    alternativa_c TEXT NOT NULL,
    alternativa_d TEXT NOT NULL,

    resposta_correta TEXT NOT NULL,

    dificuldade INTEGER DEFAULT 1,

    FOREIGN KEY (conceito_id)
        REFERENCES conceitos(id)
)
""")


# PROFICIÊNCIA
cursor.execute("""
CREATE TABLE proficiencia (
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

# RESPOSTAS
cursor.execute("""
CREATE TABLE respostas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER NOT NULL,

    questao_id INTEGER NOT NULL,

    resposta_aluno TEXT NOT NULL,

    acertou INTEGER NOT NULL,

    data_resposta DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(usuario_id)
        REFERENCES usuarios(id),

    FOREIGN KEY(questao_id)
        REFERENCES questoes(id)
)
""")

# POPULAR CONCEITOS
conceitos = [
    (
        1,
        "SELECT",
        "Seleção de colunas e registros"
    ),
    (
        2,
        "WHERE",
        "Filtragem de registros"
    ),
    (
        3,
        "ORDER BY",
        "Ordenação de resultados"
    ),
    (
        4,
        "AGREGACOES",
        "COUNT, SUM, AVG, MIN e MAX"
    ),
    (
        5,
        "GROUP BY",
        "Agrupamento de registros"
    ),
    (
        6,
        "HAVING",
        "Filtragem de grupos"
    ),
    (
        7,
        "JOINS",
        "Junção entre tabelas"
    ),
    (
        8,
        "SUBQUERIES",
        "Consultas aninhadas"
    )
]

cursor.executemany("""
INSERT INTO conceitos
VALUES (?, ?, ?)
""", conceitos)

# USUÁRIO DE TESTE
cursor.execute("""
INSERT INTO usuarios
(nome, email)
VALUES (?, ?)
""", (
    "Aluno Teste",
    "teste@gmail.com"
))

conn.commit()
conn.close()

print("Banco its.db criado com sucesso!")