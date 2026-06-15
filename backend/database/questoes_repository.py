from backend.database.connection import get_connection


def criar_questao(
    conceito_id,
    enunciado,
    sql_gabarito
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO questoes(
        conceito_id,
        enunciado,
        sql_gabarito
    )
    VALUES (?, ?, ?)
    """,
    (
        conceito_id,
        enunciado,
        sql_gabarito
    ))

    conn.commit()

    conn.close()


def buscar_questao(id_questao):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM questoes
    WHERE id = ?
    """, (id_questao,))

    questao = cursor.fetchone()

    conn.close()

    return questao