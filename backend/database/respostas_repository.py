from connection import get_connection


def registrar_resposta(
    usuario_id,
    questao_id,
    resposta_sql,
    correta
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO respostas(
        usuario_id,
        questao_id,
        resposta_sql,
        correta
    )
    VALUES (?, ?, ?, ?)
    """,
    (
        usuario_id,
        questao_id,
        resposta_sql,
        correta
    ))

    conn.commit()

    conn.close()