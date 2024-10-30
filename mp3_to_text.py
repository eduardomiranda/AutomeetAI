# Inicie garantindo que o pacote `assemblyai` esteja instalado.
# Caso contrário, você pode instalá-lo executando o seguinte comando:
# pip install -U assemblyai
#
# Nota: Alguns usuários de macOS podem precisar usar `pip3` em vez de `pip`.

import assemblyai as aai

# Substitua pela sua chave de API fornecida pelo AssemblyAI
aai.settings.api_key = ""

# Função para converter um arquivo MP3 em texto
def mp3_to_text(aai, filename, s_labels, s_expected, l_code):

    # Configura as opções de transcrição, como rotulagem de falantes,
    # número esperado de falantes e o código de linguagem
    config = aai.TranscriptionConfig(
        speaker_labels=s_labels,  # Define se os rótulos dos falantes devem ser incluídos
        speakers_expected=s_expected,  # Número esperado de falantes no áudio
        language_code=l_code  # Código do idioma do áudio (por exemplo, 'pt' para português)
    )

    # Cria uma instância do Transcriber que fará a transcrição do arquivo MP3
    transcriber = aai.Transcriber()

    # Realiza a transcrição do arquivo MP3 com as configurações especificadas
    transcript = transcriber.transcribe(
        filename,
        config=config
    )

    # Retorna a transcrição gerada pela API
    return transcript


# Verifica se o script está sendo executado como o programa principal
if __name__ == "__main__":

    # Define o caminho do arquivo MP3 local que será convertido
    mp3_local_filename = "d4fc6a25adeb464ca69a72072b7dff50.mp3"

    # Chama a função para transcrever o arquivo MP3, passando os parâmetros necessários
    transcript = mp3_to_text(
        aai, 
        filename=mp3_local_filename, 
        s_labels=True,  # Ativa os rótulos dos falantes
        s_expected=2,   # Espera-se que haja 2 falantes no áudio
        l_code='pt'     # Define o idioma como português
    )

    # Percorre as falas transcritas e imprime o texto de cada falante
    for utterance in transcript.utterances:
        # Exibe o número do falante e o texto correspondente
        print(f"Speaker {utterance.speaker}: {utterance.text}")