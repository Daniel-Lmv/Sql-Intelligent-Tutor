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
        Retorna todas as questões da tabela 'questoes_diagnostico' ordenadas.
        """
        conn = ProficiencyService.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, ordem, conceito_id, enunciado, 
                   alternativa_a, alternativa_b, alternativa_c, alternativa_d,
                   dificuldade
            FROM questoes_diagnostico 
            ORDER BY ordem ASC
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        questoes = []
        for row in rows:
            questoes.append({
                "id": row["id"],
                "ordem": row["ordem"],
                "conceito_id": row["conceito_id"],
                "enunciado": row["enunciado"],
                "alternativas": {
                    "A": row["alternativa_a"],
                    "B": row["alternativa_b"],
                    "C": row["alternativa_c"],
                    "D": row["alternativa_d"]
                },
                "dificuldade": row["dificuldade"]
            })
            
        return questoes
    
    @staticmethod
    def processar_respostas_diagnostico(user_id: int, answers: dict):
        """
        Recebe as respostas do aluno no formato de dicionário:
        answers = { "1": "A", "2": "C", ... }
        
        Calcula a proficiência inicial por conceito de forma híbrida/multitópico,
        salva na tabela 'proficiencia' e retorna o resultado.
        """
        conn = DiagnosticService.get_connection()
        cursor = conn.cursor()

        # Puxa o gabarito estruturado
        cursor.execute("""
            SELECT id, conceito_id, resposta_correta 
            FROM questoes_diagnostico
        """)
        questions_gabarito = cursor.fetchall()
        conn.close()

        # MATRIZ DE CORRELAÇÃO: Mapeia cada Questão ID aos conceitos que ela impacta
        # Formato: question_id: [lista_de_conceito_ids_afetados]
        MATRIZ_CONCEITOS = {
            1: [1],        # Q1 (SELECT/WHERE) afeta Conceito 1
            2: [1, 2],     # Q2 (BETWEEN/NULL) afeta Conceito 1 e 2
            3: [1, 3, 4],  # Q3 (Agregação/Ordenação) afeta Conceito 1, 3 e 4
            4: [1, 6],     # Q4 (INNER JOIN) afeta Conceito 1 e 6
            5: [1, 3, 4, 5], # Q5 (HAVING) afeta Conceito 1 (SELECT), 3 (Agregação), 4 (GROUP BY) e 5 (HAVING)
            6: [1, 6, 7],  # Q6 (LEFT JOIN) afeta Conceito 1, 6 e 7
            7: [1, 8],     # Q7 (Subqueries) afeta Conceito 1 e 8
            8: [1, 2]      # Q8 (DISTINCT/LIMIT) afeta Conceito 1 e 2
        }

        # Inicializa os contadores para TODOS os 8 conceitos do sistema
        concept_stats = {i: {"correct": 0, "total": 0} for i in range(1, 9)}

        for question in questions_gabarito:
            question_id = question["id"]
            correct_answer = question["resposta_correta"]

            # Descobre quais conceitos essa questão avalia (usa o da matriz, ou o ID padrão se não mapeado)
            conceitos_afetados = MATRIZ_CONCEITOS.get(question_id, [question["conceito_id"]])

            # Captura a resposta enviada pelo front-end
            student_answer = answers.get(str(question_id)) or answers.get(question_id)

            if student_answer is not None:
                is_correct = student_answer.strip().upper() == correct_answer.strip().upper()
                
                # Distribui o peso da questão para todos os conceitos envolvidos nela!
                for c_id in conceitos_afetados:
                    concept_stats[c_id]["total"] += 1
                    if is_correct:
                        concept_stats[c_id]["correct"] += 1

        # Calcula a proficiência final de 0 a 100 por conceito de forma ponderada
        proficiency = {}
        for concept_id, stats in concept_stats.items():
            total = stats["total"]
            if total == 0:
                proficiency[concept_id] = 0.0
                continue

            score = (stats["correct"] / total) * 100
            proficiency[concept_id] = round(score, 2)

        # Invoca o seu salvamento que já funciona perfeitamente!
        ProficiencyService.save_initial_proficiency(user_id, proficiency)

        return {
            "status": "success",
            "message": "Diagnóstico multitópico processado com sucesso!",
            "proficiencia_calculada": proficiency
        }