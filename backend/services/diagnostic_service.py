# backend/services/diagnostic_service.py
import sqlite3
from pathlib import Path
from services.proficiency_service import ProficiencyService

DB_PATH = Path(__file__).resolve().parent.parent / "database" / "its.db"

class DiagnosticService:

    @staticmethod
    def get_connection():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def obter_questoes_diagnostico():
        """
        Retorna as questões do diagnóstico para renderização no Frontend.
        OCULTA a coluna 'resposta_correta' por segurança contra trapaças.
        """
        conn = DiagnosticService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, ordem, conceito_id, enunciado, alternativa_a, alternativa_b, alternativa_c, alternativa_d, dificuldade
            FROM questoes_diagnostico
            ORDER BY ordem ASC
        """)

        questions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return questions

    @staticmethod
    def processar_respostas_diagnostico(user_id: int, answers: dict):
        """
        Recebe as respostas do aluno no formato de dicionário:
        answers = { "1": "A", "2": "C", ... }
        
        Calcula a proficiência inicial por conceito, salva automaticamente
        na tabela 'proficiencia' e retorna o resultado.
        """
        conn = DiagnosticService.get_connection()
        cursor = conn.cursor()

        # Puxa o gabarito completo (id, conceito e resposta certa) para validação interna no backend
        cursor.execute("""
            SELECT id, conceito_id, resposta_correta 
            FROM questoes_diagnostico
        """)
        questions_gabarito = cursor.fetchall()
        conn.close()

        concept_stats = {}

        # Usa a sua lógica fantástica de mapeamento dinâmico
        for question in questions_gabarito:
            question_id = question["id"]
            concept_id = question["conceito_id"]
            correct_answer = question["resposta_correta"]

            if concept_id not in concept_stats:
                concept_stats[concept_id] = {
                    "correct": 0,
                    "total": 0
                }

            concept_stats[concept_id]["total"] += 1

            # Sua lógica flexível de captura de respostas (String ou Int)
            student_answer = answers.get(str(question_id)) or answers.get(question_id)

            if student_answer is not None:
                if student_answer.strip().upper() == correct_answer.strip().upper():
                    concept_stats[concept_id]["correct"] += 1

        # Calcula a proficiência final de 0 a 100 por conceito
        proficiency = {}
        for concept_id, stats in concept_stats.items():
            total = stats["total"]
            if total == 0:
                proficiency[concept_id] = 0.0
                continue

            score = (stats["correct"] / total) * 100
            proficiency[concept_id] = round(score, 2)

        # Invoca o seu ProficiencyService para salvar os dados na tabela 'proficiencia'
        ProficiencyService.save_initial_proficiency(user_id, proficiency)

        return {
            "status": "success",
            "message": "Diagnóstico processado com sucesso!",
            "proficiencia_calculada": proficiency
        }