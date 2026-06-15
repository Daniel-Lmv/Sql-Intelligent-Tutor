import sqlite3
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = BASE_DIR / "its.db"
JSON_PATH = BASE_DIR / "diagnostic_questions.json"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS questoes_diagnostico (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    ordem INTEGER NOT NULL UNIQUE,

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

if not JSON_PATH.exists():
    raise FileNotFoundError(
        f"Arquivo não encontrado: {JSON_PATH}"
    )

with open(JSON_PATH, "r", encoding="utf-8") as file:
    questions = json.load(file)


cursor.execute("""
DELETE FROM questoes_diagnostico
""")


cursor.execute("""
DELETE FROM sqlite_sequence
WHERE name='questoes_diagnostico'
""")

for ordem, question in enumerate(questions, start=1):

    required_fields = [
        "conceito_id",
        "enunciado",
        "alternativa_a",
        "alternativa_b",
        "alternativa_c",
        "alternativa_d",
        "resposta_correta",
        "dificuldade"
    ]

    for field in required_fields:

        if field not in question:

            raise ValueError(
                f"Campo obrigatório ausente: {field}"
            )

    cursor.execute("""
    INSERT INTO questoes_diagnostico (

        ordem,
        conceito_id,

        enunciado,

        alternativa_a,
        alternativa_b,
        alternativa_c,
        alternativa_d,

        resposta_correta,

        dificuldade

    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        ordem,

        question["conceito_id"],

        question["enunciado"],

        question["alternativa_a"],
        question["alternativa_b"],
        question["alternativa_c"],
        question["alternativa_d"],

        question["resposta_correta"].upper(),

        question["dificuldade"]

    ))

conn.commit()

cursor.execute("""
SELECT COUNT(*)
FROM questoes_diagnostico
""")

total = cursor.fetchone()[0]

conn.close()

print("=" * 50)
print("QUESTÕES DE DIAGNÓSTICO IMPORTADAS")
print(f"Total de questões: {total}")
print("Banco atualizado com sucesso.")
print("=" * 50)