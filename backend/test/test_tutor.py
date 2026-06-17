import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from services.proficiency_service import ProficiencyService
from services.tutor_service import TutorService
from backend.services.ia_service import ExplanationService # ⬅️ Nova Importação

def simular_fluxo_its_com_ia():
    user_id = 1
    
    print("=" * 70)
    print("🤖 SIMULAÇÃO DO ITS-SQL COM INTELIGÊNCIA ARTIFICIAL LOCAL (LLAMA 3) 🤖")
    print("=" * 70)

    # Inicializando proficiência simulada do diagnóstico
    diagnostic_result = {1: 80.0, 2: 100.0, 3: 33.33, 4: 66.67, 5: 100.0, 6: 33.33, 7: 66.67, 8: 100.0}
    ProficiencyService.save_initial_proficiency(user_id, diagnostic_result)

    # Tutor escolhe a questão
    proxima_questao = TutorService.get_next_question(user_id)
    
    if proxima_questao["status"] == "success":
        q = proxima_questao["question"]
        print(f"\n🎯 [Tutor]: Selecionei uma questão de {proxima_questao['concept_name']} para você.")
        print(f"   Enunciado: {q['enunciado']}")
        print(f"   A) {q['alternativa_a']}")
        print(f"   B) {q['alternativa_b']}")
        print(f"   C) {q['alternativa_c']}")
        print(f"   D) {q['alternativa_d']}")
    else:
        print("Erro ao buscar questão.")
        return

    # Simulando o Aluno Respondendo Errado
    # Vamos supor que a correta era 'C' e ele marcou 'A'
    alternativa_errada_marcada = "A" 
    print(f"\n⌨️ [Aluno]: Marcou a alternativa: {alternativa_errada_marcada}")
    
    # Atualiza a nota no banco (-5)
    ProficiencyService.update_proficiency(user_id=user_id, concept_id=q["conceito_id"], correct=False)
    
    # -------------------------------------------------------------------------
    # O PULO DO GATO: Acionando o Modelo de IA Local para explicar o erro
    # -------------------------------------------------------------------------
    print("\n🧠 [Tutor IA] Analisando o seu erro... Gerando feedback personalizado...")
    
    feedback = ExplanationService.gerar_feedback_erro(
        enunciado=q["enunciado"],
        alternativa_aluno=alternativa_errada_marcada,
        alternativa_correta=q["resposta_correta"],
        conceito_nome=proxima_questao["concept_name"]
    )
    
    print("-" * 70)
    print(f"💬 FEEDBACK DA IA:\n{feedback}")
    print("-" * 70)

if __name__ == "__main__":
    simular_fluxo_its_com_ia()