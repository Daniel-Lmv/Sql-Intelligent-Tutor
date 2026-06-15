from backend.database.connection import get_connection

def obter_proficiencia(
    usuario_id,
    conceito_id
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT nivel
    FROM proficiencia
    WHERE usuario_id = ?
      AND conceito_id = ?
    """,
    (
        usuario_id,
        conceito_id
    ))

    resultado = cursor.fetchone()

    conn.close()

    return resultado


def atualizar_proficiencia(
    usuario_id,
    conceito_id,
    novo_nivel
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE proficiencia
    SET nivel = ?
    WHERE usuario_id = ?
      AND conceito_id = ?
    """,
    (
        novo_nivel,
        usuario_id,
        conceito_id
    ))

    conn.commit()

    conn.close()