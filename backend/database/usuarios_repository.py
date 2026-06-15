from connection import get_connection


def criar_usuario(nome, email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO usuarios(nome,email)
    VALUES (?,?)
    """, (nome, email))

    conn.commit()
    conn.close()


def buscar_usuario(id_usuario):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM usuarios
    WHERE id = ?
    """, (id_usuario,))

    usuario = cursor.fetchone()

    conn.close()

    return usuario