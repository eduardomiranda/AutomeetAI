# Certifique-se de que o pacote `assemblyai` esteja instalado. 
# Você pode instalá-lo facilmente com o comando `pip install -U assemblyai`.
#
# Nota para usuários macOS: use `pip3` se `pip` estiver associado a outra versão do Python.

import assemblyai as aai


# Função para converter um arquivo de áudio MP3 em texto usando o serviço AssemblyAI.
def mp3_to_text(aai, filename, s_labels, s_expected, l_code):
    try:
        # Configura as opções de transcrição, incluindo rótulos de falantes,
        # o número esperado de falantes e o código de idioma do áudio.
        config = aai.TranscriptionConfig(
            speaker_labels=s_labels,  # Define se os rótulos dos falantes devem ser incluídos.
            speakers_expected=s_expected,  # Número esperado de falantes no áudio.
            language_code=l_code  # Define o código de idioma, como 'pt' para português.
        )

        # Cria uma instância do Transcriber, que será usada para realizar a transcrição.
        transcriber = aai.Transcriber()

        # Transcreve o arquivo MP3 usando as configurações especificadas.
        transcript = transcriber.transcribe(
            filename,
            config=config
        )

        # Retorna a transcrição gerada pela API.
        return transcript

    except FileNotFoundError:
        # Captura o erro se o arquivo de áudio não for encontrado.
        print("Erro: o arquivo especificado não foi encontrado.")
    except Exception as e:
        # Captura quaisquer outras exceções ocorridas durante a execução.
        print(f"Ocorreu um erro: {e}")



# Verifica se este script Python está sendo executado diretamente, não importado.
if __name__ == "__main__":

    # Defina sua chave de API fornecida pelo AssemblyAI. Isso é essencial para autenticação.
    aai.settings.api_key = ""

    # Especifique o caminho para o arquivo MP3 que deseja transcrever.
    mp3_local_filename = "d4fc6a25adeb464ca69a72072b7dff50.mp3"

    # Chama a função de transcrição com as configurações desejadas.
    transcript = mp3_to_text(
        aai, 
        filename=mp3_local_filename, 
        s_labels=True,  # Habilita os rótulos dos falantes no resultado da transcrição.
        s_expected=2,   # Espera que o áudio contenha 2 falantes.
        l_code='pt'     # Define o idioma do áudio como português.
    )

    # Se a transcrição foi bem-sucedida, exibe as falas dos falantes.
    if transcript:
        # Itera sobre as fala transcritas e imprime cada fala com o número do falante.
        for utterance in transcript.utterances:
            # Exibe o número do falante e o texto correspondente.
            print(f"Speaker {utterance.speaker}: {utterance.text}")