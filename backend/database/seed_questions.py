import sqlite3
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = BASE_DIR / "its.db"
JSON_PATH = BASE_DIR / "questions.json"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

with open(JSON_PATH, "r", encoding="utf-8") as f:
    questions = json.load(f)

for q in questions:

    cursor.execute("""
        INSERT OR REPLACE INTO questoes (
            conceito_id,
            enunciado,
            alternativa_a,
            alternativa_b,
            alternativa_c,
            alternativa_d,
            resposta_correta,
            dificuldade
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        q["conceito_id"],
        q["enunciado"],
        q["alternativa_a"],
        q["alternativa_b"],
        q["alternativa_c"],
        q["alternativa_d"],
        q["resposta_correta"],
        q["dificuldade"]
    ))

conn.commit()
conn.close()

print(f"{len(questions)} questões inseridas com sucesso!")