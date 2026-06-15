import sqlite3

conn = sqlite3.connect("its.db")

cursor = conn.cursor()

print("Banco criado com sucesso!")

conn.close()