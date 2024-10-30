# Start by making sure the `assemblyai` package is installed.
# If not, you can install it by running the following command:
# pip install -U assemblyai
#
# Note: Some macOS users may need to use `pip3` instead of `pip`.

import assemblyai as aai

# Replace with your API key
aai.settings.api_key = ""

def mp3_to_text(aai, filename, s_labels, s_expected, l_code):

    config = aai.TranscriptionConfig(speaker_labels=s_labels, speakers_expected=s_expected, language_code=l_code)

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(
        filename,
        config=config
    )

    return transcript



# Verifica se o script está sendo executado como o programa principal
if __name__ == "__main__":

    # Define o caminho do arquivo MP3 local que será convertido
    mp3_local_filename = "d4fc6a25adeb464ca69a72072b7dff50.mp3"

    transcript = mp3_to_text(aai, filename=mp3_local_filename, s_labels=True, s_expected=2, l_code='pt')

    for utterance in transcript.utterances:
        print(f"Speaker {utterance.speaker}: {utterance.text}")
