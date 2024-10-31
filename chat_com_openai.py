# Importe os pacotes necessários.
# Na verdade, você deve importar apenas as partes necessárias de uma biblioteca,
# mas para este código, assumimos que OpenAI é importado corretamente.
from openai import OpenAI


def generate_response(openai_client, system_prompt_text, user_prompt_text):
    """
    Esta função envia uma solicitação para a API do OpenAI com um prompt dado e retorna a resposta do modelo.

    Argumentos:
    - prompt_text: Uma string contendo o texto do prompt para o qual você deseja uma completude da IA.

    Retorna:
    - O conteúdo da resposta gerada pelo modelo.
    """

    try:

        # Cria uma resposta usando o cliente da API OpenAI para o chat
        response = openai_client.chat.completions.create(
            model="gpt-4o-2024-08-06",  # Especifica o modelo de linguagem a ser utilizado. 
                                        # Neste caso, é uma variante do GPT-4 otimizada para chat. 
                                        # Modelos diferentes podem ter capacidades e custos diferentes.
            messages=[
                {"role": "system", "content": system_prompt_text},
                {"role": "user", "content": user_prompt_text}
            ],
            # A lista 'messages' contém a sequência de mensagens que compõem o contexto da conversa.
            # Cada mensagem tem um papel ('role') e um conteúdo ('content').
            # 'role': 'system' fornece instruções gerais ou estabelece o tom para o assistente.
            # 'role': 'user' contém a interação entrada pelo usuário, geralmente uma pergunta ou comando.

            # max_tokens=150,  # Define o número máximo de tokens (palavras ou fragmentos de palavras) que a resposta gerada pode ter. 
                             # Limitar tokens ajuda a controlar custos e evita respostas excessivamente longas. 
                             # Um 'token' aqui é uma unidade básica que compõe o texto.

            temperature=0.7  # Controla o nível de "criatividade" ou "aleatoriedade" na resposta gerada.
                             # Valores mais baixos (como 0.2) resultam em respostas mais determinísticas e retilíneas.
                             # Valores mais altos (próximo de 1) tornam a saída mais variada e imprevisível.
                             # Um valor como 0.7 geralmente equilibra bem qualidade e diversidade nas respostas.
        )

        # Extraia o texto gerado da resposta
        # Navegar através da estrutura do objeto de resposta para encontrar o conteúdo relevante
        returned_text = response.choices[0].message.content.strip()

        # Retorne a resposta do modelo para outros usos no programa
        return returned_text

    except Exception as e:
        # Lidar com exceções que podem ocorrer durante a solicitação da API
        # Isso pode incluir problemas de rede, chave de API inválida, etc.
        print("Ocorreu um erro:", str(e))
        return None



# Verifica se o script está sendo executado como o programa principal
if __name__ == "__main__":

    # Inicialize o cliente OpenAI com sua chave de API.
    # Isso permite que você use vários modelos fornecidos pelo OpenAI.
    openai_client = OpenAI(api_key='')  # Certifique-se de substituir por uma chave de API válida.

    # Defina os prompts para testar a função
    system_prompt_text = "Você é um assistente prestativo."
    user_prompt_text = "Explique a teoria da relatividade em termos simples."

    # Chame a função de geração de resposta e capture seu resultado
    result = generate_response(openai_client, system_prompt_text, user_prompt_text)

    # Verifique se obtivemos uma resposta válida e imprima um resultado final
    if result:
        print("Resultado Final:", result)
    else:
        print("Falha ao obter uma resposta do modelo.")