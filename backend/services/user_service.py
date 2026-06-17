# backend/services/user_service.py
import sqlite3
from pathlib import Path

# Ajustado para buscar exatamente o "its.db" na mesma pasta onde o banco for gerado
# Se o seu arquivo de banco fica na pasta "database", usamos o .parent correspondente.
DB_PATH = Path(__file__).resolve().parent.parent / "database" / "its.db"

class UserService:

    @staticmethod
    def get_connection():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row # Garante acesso por nome de coluna
        return conn

    @staticmethod
    def login_simplificado(email: str):
        """
        Verifica se o e-mail existe na tabela 'usuarios'.
        Retorna os dados e se o aluno precisa ou não fazer o diagnóstico.
        """
        conn = UserService.get_connection()
        cursor = conn.cursor()

        # 1. Busca o usuário pelo e-mail (usando a tabela 'usuarios' que você criou)
        cursor.execute("""
            SELECT id, nome, email 
            FROM usuarios 
            WHERE email = ?
        """, (email.strip().lower(),))
        
        user_row = cursor.fetchone()

        if user_row is None:
            conn.close()
            return {"status": "error", "message": "Usuário não encontrado com este e-mail."}

        user_id = user_row["id"]

        # 2. Verifica se o usuário já tem notas na tabela 'proficiencia'
        cursor.execute("""
            SELECT COUNT(*) as total 
            FROM proficiencia 
            WHERE usuario_id = ?
        """, (user_id,))
        
        has_proficiency = cursor.fetchone()["total"] > 0

        conn.close()

        return {
            "status": "success",
            "user": {
                "id": user_id,
                "nome": user_row["nome"],
                "email": user_row["email"]
            },
            "precisa_diagnostico": not has_proficiency
        }

    @staticmethod
    def obter_status_progresso(user_id: int):
        """
        Gera as regras do Grafo baseadas nos dados reais das tabelas 
        'conceitos' e 'proficiencia' criadas no seu banco.
        """
        conn = UserService.get_connection()
        cursor = conn.cursor()

        # Busca os conceitos (IDs de 1 a 8) exatamente como você populou
        cursor.execute("SELECT id, nome FROM conceitos ORDER BY id ASC")
        conceitos_rows = cursor.fetchall()

        # Busca a tabela de proficiência granular por conceito
        cursor.execute("SELECT conceito_id, nivel FROM proficiencia WHERE usuario_id = ?", (user_id,))
        proficiencias = {row["conceito_id"]: row["nivel"] for row in cursor.fetchall()}

        conn.close()

        progresso_grafo = []
        liberado = True # O primeiro conceito (ID 1 - SELECT) começa sempre aberto

        for row in conceitos_rows:
            c_id = row["id"]
            c_nome = row["nome"]
            nivel_atual = proficiencias.get(c_id, 0.0)

            # Suas regras pedagógicas de bloqueio/desbloqueio
            ganhou_trofeu = nivel_atual >= 70.0
            pode_pular = nivel_atual >= 50.0

            progresso_grafo.append({
                "conceito_id": c_id,
                "nome": c_nome,
                "nivel": round(nivel_atual, 2),
                "liberado": liberado,
                "ganhou_trofeu": ganhou_trofeu,
                "pode_pular": pode_pular
            })

            # Regra de avanço em cascata do Grafo:
            # O próximo item só estará liberado se o atual passou de 70% ou o aluno escolheu pular (>=50%)
            liberado = liberado and (ganhou_trofeu or pode_pular)

        return {
            "user_id": user_id,
            "progresso": progresso_grafo
        }