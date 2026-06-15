from connection import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS conceitos (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    descricao TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS questoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conceito_id INTEGER,
    enunciado TEXT,
    sql_gabarito TEXT,

    FOREIGN KEY(conceito_id)
        REFERENCES conceitos(id)
)
""")

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
INSERT OR IGNORE INTO conceitos
VALUES (?, ?, ?)
""", conceitos)

conn.commit()
conn.close()

print("Banco inicializado.")