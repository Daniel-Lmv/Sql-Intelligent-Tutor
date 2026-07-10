# backend/services/ia_service.py
import ollama

class ExplanationService:

    @staticmethod
    def gerar_feedback_worked_example(enunciado, alternativa_aluno, alternativa_correta, conceito_nome):
        """
        [Worked Example Prévio] Acionado assim que o aluno erra a alternativa.
        Gera um exemplo completamente resolvido e explicado sobre o MESMO conceito,
        ajudando o aluno a entender o padrão lógico para corrigir seu próprio erro.
        """
        prompt = f"""
        Você é o SQL Tutor, um Professor Virtual especialista em Teoria da Carga Cognitiva.
        O estudante errou uma questão teórica sobre '{conceito_nome}'.
        
        <DADOS_DA_QUESTAO_DO_ALUNO>
        - Enunciado: {enunciado}
        - Alternativa que ele marcou e está ERRADA: {alternativa_aluno}
        </DADOS_DA_QUESTAO_DO_ALUNO>
        
        DIRETRIZES DE SEGURANÇA E REGRA DOS WORKED EXAMPLES:
        1. Explique brevemente (1 linha) o erro conceitual cometido ao escolher a alternativa errada.
        2. Apresente OBRIGATORIAMENTE um "Exemplo Resolvido" (Worked Example) PARALELO.
        3. REGRA DE CONTRASTE ABSOLUTO: O seu exemplo resolvido DEVE usar um cenário, tabelas e colunas COMPLETAMENTE DIFERENTES da questão do aluno.
           - Exemplo: Se a questão do aluno fala sobre "Clientes" ou "Vendas", seu exemplo DEVE falar sobre "Livros", "Naves Espaciais" ou "Pokemons". Nunca repita nenhuma tabela ou coluna do enunciado real.
        4. O exemplo deve conter: Um mini-cenário fictício, a query SQL correta em um bloco (```sql) e uma explicação de 2 linhas do porquê funciona.
        5. NUNCA dê o gabarito ou use dados da questão real. Max 8 linhas no total.
        
        Resposta do Professor Virtual:
        """
        try:
            response = ollama.generate(
                model='llama3:8b', 
                prompt=prompt,
                options={'temperature': 0.2, 'top_p': 0.8}
            )
            return response['response'].strip()
        except Exception as e:
            return f"Tutor: Notei que houve uma pequena confusão com as regras de {conceito_nome}. Vamos analisar um exemplo parecido no chat ao lado! (Erro local: {str(e)})"

    @staticmethod
    def conversar_professor_virtual(dados_questao: dict, historico_mensagens: list):
        """
        [Chat Contínuo - Professor Virtual] Gerencia o diálogo baseado em Skills 
        e de acordo com a questão exata que está ativa na interface do usuário.
        Modo: Stateless (Apenas a mensagem atual do usuário é considerada).
        """
        
        enunciado = dados_questao.get("enunciado", "Não especificado")
        resposta_correta = dados_questao.get("resposta_correta", "Não especificada")
        resposta_aluno = dados_questao.get("resposta_aluno", "Nenhuma alternativa marcada ainda")
        conceito_nome = dados_questao.get("conceito_nome", "SQL Geral")

        # Prompt reestruturado com foco em exclusão de termos reais para modelos < 3B
        system_instruction = f"""
        Você é o SQL Tutor, um Professor Virtual de Banco de Dados focado estritamente no aprendizado por Exemplos Resolvidos (Worked Examples).
        Você deve responder OBRIGATORIAMENTE em PORTUGUÊS DO BRASIL.
        Nunca use inglês. Não responda com perguntas.

        <CONTEXTO_REAL_DA_TELA_DO_ALUNO>
        - Módulo de Estudo: {conceito_nome}
        - Enunciado do Exercício: {enunciado}
        - Gabarito Correto: {resposta_correta}
        - Resposta Atual do Estudante: {resposta_aluno}
        </CONTEXTO_REAL_DA_TELA_DO_ALUNO>

        [PROIBIÇÃO ABSOLUTA E BLOQUEIO DE GABARITO]
        - Se o usuário usar termos como "me de a resposta", "resolva", "resposta dessa questão", "me dá o código", "faz pra mim", você está PROIBIDO de gerar qualquer código SQL que use as palavras contidas no bloco <CONTEXTO_REAL_DA_TELA_DO_ALUNO>.
        - Se o aluno pedir a resposta explicitamente, você DEVE iniciar sua resposta com a recusa padrão:
        "Eu não posso montar o código final ou te dar a resposta pronta da questão, mas estou aqui para te ajudar a construir o raciocínio passo a passo! Vamos analisar um caso similar:"
        - NUNCA use os nomes reais de tabelas, colunas ou valores do exercício (ex: se o exercício fala de 'equipe', 'departamento' ou 'TI', você NÃO PODE escrever essas palavras em hipótese alguma).

        SUAS SKILLS ATIVAS (RESTRITAS):
        1. [EXPLICAR_CONCEITO]: Crie um exemplo resolvido paralelo usando OBRIGATORIAMENTE o tema de "Cachorros" ou "Livros" (ex: tabelas 'animais', 'livros'). Nunca use dados parecidos com a tela do aluno. Demonstre a sintaxe usando esses dados fictícios dentro de um bloco de código (```sql).
        2. [SCAFFOLDING]: Explique a estrutura de forma totalmente genérica. Substitua colunas por termos abstratos como 'coluna_1', 'tabela_exemplo', 'valor_x'. 
        3. [FEEDBACK_CONSTRUTIVO]: Você só analisará o código do aluno se ele enviar um código próprio dele na mensagem atual. Se ele não enviar código e só pedir a resposta, ignore esta skill.

        [REGRA DE ENCERRAMENTO OBRIGATÓRIA - CORTE DE RESPOSTA]
        - Após explicar o seu exemplo fictício (de cachorros ou livros), encerre a resposta IMEDIATAMENTE com: "Agora, tente aplicar essa mesma estrutura lógica adaptando para os dados da sua questão!".
        - É TERMINANTEMENTE PROIBIDO tentar fazer o paralelo ("No seu caso...") ou citar os dados reais da tela no final do texto. Pare de gerar texto assim que terminar o exemplo fictício.

        FORMATO:
        - Seja extremamente conciso (HUD lateral). Use parágrafos curtos.
        - Use blocos de código markdown (```sql) APENAS para o exemplo fictício paralelo.
        """

        mensagens_ollama = [{"role": "system", "content": system_instruction}]
        
        if historico_mensagens and len(historico_mensagens) > 0:
            ultima_msg = historico_mensagens[-1]
            mensagens_ollama.append({
                "role": ultima_msg["role"],
                "content": ultima_msg["content"]
            })
        else:
            mensagens_ollama.append({
                "role": "user",
                "content": "Preciso de ajuda para entender a lógica dessa questão."
            })

        try:
            response = ollama.chat(
                model='llama3:8b',
                messages=mensagens_ollama,
                options={'temperature': 0.1} # Mantido em 0.1 para evitar desobediência
            )
            return response['message']['content'].strip()
            
        except Exception as e:
            return f"Tutor: Tive um problema ao processar essa última instrução. Poderia reformular? (Erro local: {str(e)})"