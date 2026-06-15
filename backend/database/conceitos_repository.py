from backend.database.connection import get_connection


def listar_conceitos():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM conceitos
    ORDER BY id
    """)

    conceitos = cursor.fetchall()

    conn.close()

    return conceitos