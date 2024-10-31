# Importamos o módulo streamlit com o alias 'st'
# Dessa forma, podemos usar 'st' para acessar as funcionalidades do Streamlit
import streamlit as st
from annotated_text import annotated_text

import assemblyai as aai
from openai import OpenAI
import uuid

from mp4_to_mp3 import mp4_to_mp3
from mp3_to_text import mp3_to_text
from misc import deletar_arquivo_se_existir
from chat_com_openai import generate_response
from assemblyai_language_codes import *




# Usamos a função title() do Streamlit para colocar um título na nossa aplicação web
st.title('🤖 AutomeetAI')

# Usamos a função write() para exibir um texto simples na página
# Esta função é bastante versátil e pode também mostrar dados e exibir gráficos
st.write('Automação de atas de reunião com tecnologia de IA com Python.')


st.divider()  # 👈 Draws a horizontal rule


col11, col12 = st.columns(2)

with col11:
	aai_api_key = st.text_input("AssemblyAI   •   API key", "")

with col12:
	openai_api_key = st.text_input("OpenAI   •   API key", "")


st.divider()  # 👈 Draws a horizontal rule


prompt_system = st.text_area("System prompt:", "Você é um ótimo gerente de projetos com grandes capacidades de criação de atas de reunião.")
prompt_text = st.text_area("User prompt:", """Em uma redação de nível especializado, resuma as notas da reunião em um único parágrafo.\nEm seguida, escreva uma lista de cada um de seus pontos-chaves tratados na reunião.\nPor fim, liste as próximas etapas ou itens de ação sugeridos pelos palestrantes, se houver.""")


st.divider()  # 👈 Draws a horizontal rule

col21, col22 = st.columns(2)

with col21:
	speakers_expected = st.number_input("Total de pessoas falantes:", 1, 15)

with col22:
	language = st.selectbox("Selecione o idioma falado:", tuple(language_codes.keys()))


uploaded_file = st.file_uploader("Selecione o seu arquivo", accept_multiple_files=False, type = ['mp4'])


st.divider()  # 👈 Draws a horizontal rule


if uploaded_file:

	with st.spinner('Convertendo de mp4 para mp3'):
	
		mp4_filename = uploaded_file.name
		mp3_filename = '{nome_arquivo}.mp3'.format(nome_arquivo = uuid.uuid4().hex)

		tempfile = open(mp4_filename, 'wb')
		tempfile.write(uploaded_file.read())

		mp4_to_mp3(mp4_filename, mp3_filename)

	st.success("Conversão de MP4 para MP3 realizada!")



	with st.spinner('Convertendo de mp3 para texto'):

		aai.settings.api_key = aai_api_key

		transcript = mp3_to_text(
			aai, 
			filename=mp3_filename, #"d4fc6a25adeb464ca69a72072b7dff50.mp3", 
			s_labels=True,  
			s_expected=speakers_expected,
			l_code=language_codes[language]
		)

		st.success("Transcrição de áudio para texto realizada!")

		texto_transcrito = ''
		texto_anotado = []

		# Se a transcrição foi bem-sucedida, exibe as falas dos falantes.
		if transcript:
			# Itera sobre as fala transcritas e imprime cada fala com o número do falante.
			for utterance in transcript.utterances:
				# Exibe o número do falante e o texto correspondente.
				texto_transcrito += f"Speaker {utterance.speaker}: {utterance.text}"
				texto_transcrito += '\n'

				texto_anotado.append((utterance.text, f"Speaker {utterance.speaker}"))



	with st.spinner('Gerando ata de reunião'):
		
		# Inicialize o cliente OpenAI com sua chave de API.
		client = OpenAI(api_key=openai_api_key)

		prompt_text += '\n===========\n'
		prompt_text += texto_transcrito

		texto_retorno = generate_response(client, prompt_system, prompt_text)

		st.success("Ata gerada com sucesso!")


	st.subheader('Transcrição original')
	annotated_text(texto_anotado)
	
	# st.markdown(texto_transcrito)
	st.subheader('Ata gerada')
	st.markdown(texto_retorno)


	deletar_arquivo_se_existir(mp3_filename)