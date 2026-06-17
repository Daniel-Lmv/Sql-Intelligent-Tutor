# backend/services/explanation_service.py
import ollama

class ExplanationService:

    @staticmethod
    def gerar_feedback_erro(enunciado, alternativa_aluno, alternativa_correta, conceito_nome):
        """
        [Método Estático Clássico] Gera o primeiro balão de fala do tutor 
        assim que o aluno erra a questão.
        """
        prompt = f"""
        Você é um Tutor Inteligente de Banco de Dados SQL, especialista em IA na Educação (IAED).
        Um estudante acabou de errar uma questão sobre o conceito de '{conceito_nome}'.
        
        [Questão Proposta]: {enunciado}
        [Resposta Correta]: Alternativa {alternativa_correta}
        [Resposta que o Aluno Marcou]: Alternativa {alternativa_aluno}
        
        Instruções Pedagógicas:
        1. Explique de forma muito curta (máximo 4 linhas) por que a alternativa que o aluno marcou ({alternativa_aluno}) está incorreta para este cenário específico.
        2. Dê uma pista conceitual sobre '{conceito_nome}' para ajudá-lo a refletir sobre o erro.
        3. Nunca dê a resposta correta de bandeja e nem escreva o código SQL correto.
        4. Fale diretamente com o aluno em português, de forma amigável e instigante.
        
        Explicação Inicial do Tutor:
        """
        try:
            response = ollama.generate(
                model='llama3', 
                prompt=prompt,
                options={'temperature': 0.3, 'top_p': 0.9}
            )
            return response['response'].strip()
        except Exception as e:
            return f"Tutor: Notei que você se confundiu nas regras de {conceito_nome}. Dê uma olhada no enunciado novamente! (Erro local: {str(e)})"

    @staticmethod
    def conversar_tutor_socratico(dados_questao: dict, historico_mensagens: list):
        """
        [Método de Chat Contínuo] Gerencia o diálogo interativo entre o aluno e o Llama 3.
        Usa o método Socrático para guiar o aluno a descobrir a resposta correta por conta própria.
        
        'dados_questao' deve conter: { 'enunciado', 'resposta_correta', 'resposta_aluno', 'conceito_nome' }
        'historico_mensagens' deve vir do frontend no formato: 
        [
            {"role": "user", "content": "Texto do aluno"},
            {"role": "assistant", "content": "Texto da IA"}
        ]
        """
        
        # O "System Prompt" dita as regras comportamentais da IA para toda a conversa
        system_instruction = f"""
        Você é um Tutor Socrático de SQL especializado em Banco de Dados. 
        O aluno está tentando resolver a seguinte questão sobre '{dados_questao['conceito_nome']}':
        "{dados_questao['enunciado']}"
        A resposta correta é a alternativa '{dados_questao['resposta_correta']}', e o aluno errou ao marcar a alternativa '{dados_questao['resposta_aluno']}'.
        
        Suas DIRETRIZES RÍGIDAS de IAED (Inteligência Artificial na Educação):
        1. Atue estritamente usando o Método Socrático: Não dê respostas prontas, não diga qual alternativa é a correta e jamais escreva a query SQL correta para o aluno.
        2. Responda às dúvidas do aluno fazendo novas perguntas reflexivas que o guiem a perceber a própria falha ou lógica incorreta.
        3. Se o aluno pedir a resposta ou tentar fazer você escrever o código, recuse educadamente e dê uma pista conceitual simples.
        4. Suas respostas devem ser curtas, diretas (no máximo 3 ou 4 linhas) e motivadoras.
        5. Fale em português de forma natural.
        """

        # Monta o pacote de mensagens injetando a instrução do sistema no topo
        mensagens_ollama = [{"role": "system", "content": system_instruction}]
        
        # Alimenta o Ollama com o histórico real da conversa que veio da tela do usuário
        for msg in historico_mensagens:
            mensagens_ollama.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        try:
            # Chama a API de chat mantendo a coerência da conversa
            response = ollama.chat(
                model='llama3',
                messages=mensagens_ollama,
                options={'temperature': 0.5} # Levemente maior para o diálogo parecer natural
            )
            return response['message']['content'].strip()
            
        except Exception as e:
            return f"Tutor: Estou com dificuldades para processar seu pensamento agora. Pode repetir? (Erro local: {str(e)})"