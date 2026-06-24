import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "its.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# USUÁRIO DE TESTE
# cursor.execute("""
# INSERT INTO usuarios
# (nome, email)
# VALUES (?, ?)
# """, (
#     "DANIEL Teste",
#     "daniel@gmail.com"
# ))



conn.commit()
conn.close()
