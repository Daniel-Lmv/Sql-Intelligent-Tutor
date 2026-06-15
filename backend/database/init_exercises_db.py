import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "exercises.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ==========================
# CLIENTES
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY,
    nome TEXT,
    idade INTEGER,
    cidade TEXT
)
""")

# ==========================
# PRODUTOS
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY,
    nome TEXT,
    preco REAL
)
""")

# ==========================
# PEDIDOS
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY,

    cliente_id INTEGER,

    produto_id INTEGER,

    quantidade INTEGER,

    FOREIGN KEY(cliente_id)
        REFERENCES clientes(id),

    FOREIGN KEY(produto_id)
        REFERENCES produtos(id)
)
""")

# ==========================
# DEPARTAMENTOS
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS departamentos (
    id INTEGER PRIMARY KEY,
    nome TEXT
)
""")

# ==========================
# FUNCIONARIOS
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS funcionarios (
    id INTEGER PRIMARY KEY,

    nome TEXT,

    salario REAL,

    departamento_id INTEGER,

    FOREIGN KEY(departamento_id)
        REFERENCES departamentos(id)
)
""")

# ==========================
# LIMPAR TABELAS
# ==========================

cursor.execute("DELETE FROM pedidos")
cursor.execute("DELETE FROM clientes")
cursor.execute("DELETE FROM produtos")
cursor.execute("DELETE FROM funcionarios")
cursor.execute("DELETE FROM departamentos")

# ==========================
# CLIENTES
# ==========================

cursor.executemany("""
INSERT INTO clientes
VALUES (?, ?, ?, ?)
""", [

    (1, "Ana", 15, "Recife"),
    (2, "João", 20, "Recife"),
    (3, "Maria", 25, "Olinda"),
    (4, "Pedro", 17, "Jaboatao"),
    (5, "Lucas", 30, "Recife"),
    (6, "Davi", 22, "Natal"),
    (7, "Alberto", 18, "São Paulo"),
    (8, "Rafaela", 28, "João Pessoa")

])

# ==========================
# PRODUTOS
# ==========================

cursor.executemany("""
INSERT INTO produtos
VALUES (?, ?, ?)
""", [

    (1, "Notebook", 3500),
    (2, "Mouse", 50),
    (3, "Teclado", 150),
    (4, "Monitor", 900),
    (5, "Headset", 250),
    (6, "PC Gamer", 4000),
    (7, "Xbox One", 2000),
    (8, "Playstation 5", 3500),

])

# ==========================
# PEDIDOS
# ==========================

cursor.executemany("""
INSERT INTO pedidos
VALUES (?, ?, ?, ?)
""", [

    (1, 1, 2, 1),
    (2, 2, 1, 1),
    (3, 3, 4, 2),
    (4, 2, 3, 1),
    (5, 5, 5, 3),
    (6, 6, 7, 1),
    (7, 7, 6, 1),
    (8, 8, 8, 2),
    (9, 6, 5, 4),
    (10, 5, 8, 1)

])

# ==========================
# DEPARTAMENTOS
# ==========================

cursor.executemany("""
INSERT INTO departamentos
VALUES (?, ?)
""", [

    (1, "TI"),
    (2, "RH"),
    (3, "Vendas"),
    (4, "Financeiro"),
    (5, "Diretoria")

])

# ==========================
# FUNCIONARIOS
# ==========================

cursor.executemany("""
INSERT INTO funcionarios
VALUES (?, ?, ?, ?)
""", [

    (1, "Carlos", 5000, 1),
    (2, "Fernanda", 3000, 2),
    (3, "Roberto", 7000, 1),
    (4, "Juliana", 4000, 3),
    (5, "Paulo", 3500, 3),
    (6, "Roberto", 5000, 4),
    (7, "Aparecida", 4000, 5),
    (8, "Handerson", 5500, 5),

])

conn.commit()
conn.close()

print("exercises.db criado e populado com sucesso!")