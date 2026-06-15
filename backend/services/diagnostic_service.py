import sqlite3
from pathlib import Path

DB_PATH = (
    Path(__file__).resolve().parent.parent
    / "database"
    / "its.db"
)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_diagnostic_questions():
    """
    Retorna as questões do diagnóstico
    na ordem definida pelo campo 'ordem'.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM questoes_diagnostico
        ORDER BY ordem
    """)

    questions = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return questions


def evaluate_diagnostic(answers, questions):
    """
    answers:

    {
        "1": "A",
        "2": "C",
        "3": "D"
    }

    questions:

    retorno de get_diagnostic_questions()

    Retorna:

    {
        1: 66.67,
        2: 100.0,
        3: 33.33
    }
    """

    concept_stats = {}

    for question in questions:

        question_id = question["id"]
        concept_id = question["conceito_id"]
        correct_answer = question["resposta_correta"]

        if concept_id not in concept_stats:

            concept_stats[concept_id] = {
                "correct": 0,
                "total": 0
            }

        concept_stats[concept_id]["total"] += 1

        student_answer = (
            answers.get(str(question_id))
            or answers.get(question_id)
        )

        if student_answer is not None:

            if student_answer.upper() == correct_answer.upper():

                concept_stats[concept_id]["correct"] += 1

    proficiency = {}

    for concept_id, stats in concept_stats.items():

        total = stats["total"]

        if total == 0:

            proficiency[concept_id] = 0.0
            continue

        score = (
            stats["correct"] / total
        ) * 100

        proficiency[concept_id] = round(score, 2)

    return proficiency


def get_concept_names():
    """
    Retorna um dicionário:

    {
        1: "SELECT",
        2: "WHERE",
        ...
    }
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome
        FROM conceitos
    """)

    concepts = {
        row["id"]: row["nome"]
        for row in cursor.fetchall()
    }

    conn.close()

    return concepts


def evaluate_diagnostic_with_names(
    answers,
    questions
):
    """
    Retorna resultado usando
    o nome do conceito.

    Exemplo:

    {
        "SELECT": 66.67,
        "WHERE": 100.0,
        "ORDER BY": 33.33
    }
    """

    proficiency = evaluate_diagnostic(
        answers,
        questions
    )

    concepts = get_concept_names()

    result = {}

    for concept_id, score in proficiency.items():

        concept_name = concepts.get(
            concept_id,
            f"CONCEITO_{concept_id}"
        )

        result[concept_name] = score

    return result