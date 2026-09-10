# Importamos o módulo streamlit com o alias 'st'.
# Isso nos permite usar 'st' para acessar as funcionalidades do Streamlit,
# que é uma estrutura de aplicação web para Python.
import streamlit as st

# Importamos a função annotated_text para destaque de texto na aplicação.
from annotated_text import annotated_text

# Importamos bibliotecas específicas para integração com serviços de IA e manipulação de mídia.
import assemblyai as aai
from openai import OpenAI

import uuid

# Importamos funções personalizadas para converter arquivos e manusear dados.
from mp4_to_mp3 import mp4_to_mp3, audio_to_mp3
from mp3_to_text import mp3_to_text
from misc import deletar_arquivo_se_existir
from chat_com_openai import generate_response

# Importamos um dicionário com códigos de idiomas para processamento de áudio.
from assemblyai_language_codes import *


# Usamos a função title() do Streamlit para colocar um título na nossa aplicação web.
st.title('🤖 AutomeetAI')

# Usamos a função write() para exibir um texto simples na página.
# Esta função é bastante versátil e pode também mostrar dados e exibir gráficos.
st.write('Automação de atas de reunião com tecnologia de IA com Python.')



# Verifica se as chaves de API para AssemblyAI e OpenAI estão disponíveis nos segredos (st.secrets).
if 'assemblyai' in st.secrets and 'api_key' in st.secrets['assemblyai'] and \
   'openai'     in st.secrets and 'api_key' in st.secrets['openai'] :

	# Recupera a chave de API para AssemblyAI dos segredos armazenados e a atribui à variável `aai_api_key`.
	aai_api_key = st.secrets['assemblyai']['api_key']

	# Recupera a chave de API para OpenAI dos segredos armazenados e a atribui à variável `openai_api_key`.
	openai_api_key = st.secrets['openai']['api_key']


else:

	# Caso as chaves não estejam disponíveis, cria uma interface de usuário para entrada manual das chaves.

	# Adiciona uma linha horizontal para separar seções no layout da aplicação.
	st.divider()

	# Divide a página em duas colunas para entrada de API keys.
	col11, col12 = st.columns(2)

	with col11:
		# O método `text_input` é usado para criar uma caixa de texto onde o usuário pode inserir a chave de API.
		aai_api_key = st.text_input("AssemblyAI   •   API key")

	with col12:
		# Outro método `text_input` semelhante ao anterior, mas desta vez para a chave de API do OpenAI.
		openai_api_key = st.text_input("OpenAI   •   API key")




# Outra linha divisória para organização visual.
st.divider()

# Área de texto para o prompt do sistema: o comportamento e papel do "assistente".
prompt_system = st.text_area("Forneça instruções gerais ou estabeleça o tom para o \"assistente\" de IA:", "Você é um ótimo gerente de projetos com grandes capacidades de criação de atas de reunião.")

# Área de texto para o prompt do usuário: o que o usuário deseja que o assistente faça.
prompt_text = st.text_area("O que o usuário deseja que o assistente faça?", """Em uma redação de nível especializado, resuma as notas da reunião em um único parágrafo.
Em seguida, escreva uma lista de cada um de seus pontos-chaves tratados na reunião.
Por fim, liste as próximas etapas ou itens de ação sugeridos pelos palestrantes, se houver.""")


# Mais uma linha divisória para clareza visual.
st.divider()

# Novamente divide a página em duas colunas para configurações adicionais.
col21, col22 = st.columns(2)

# Entrada numérica para o número de falantes estimados no áudio.
with col21:
	speakers_expected = st.number_input("Total de pessoas falantes:", 1, 15)

# Seleção do idioma falado, usando a lista de códigos de idiomas importados.
with col22:
	language = st.selectbox("Selecione o idioma falado:", tuple(language_codes.keys()))

# Componente de upload de arquivo para que o usuário possa enviar arquivos de áudio/vídeo.
uploaded_file = st.file_uploader("Selecione o seu arquivo", accept_multiple_files=False)

# Linha divisória abaixo do componente de upload.
st.divider()

# Validação de tipo de arquivo suportado
if uploaded_file:
	extensoes_suportadas = ['mp4', 'ogg', 'oga', 'opus', 'mp3', 'wav', 'flac', 'm4a']
	extensao_arquivo = uploaded_file.name.split('.')[-1].lower()
	
	if extensao_arquivo not in extensoes_suportadas:
		st.error(f"❌ Arquivo não suportado! Use um destes formatos: {', '.join(extensoes_suportadas)}")
		uploaded_file = None
	else:
		st.success(f"✅ Arquivo {extensao_arquivo.upper()} detectado")


# Se um arquivo foi carregado, executa o processamento.
if uploaded_file:

	# Obtém o nome do arquivo carregado
	uploaded_filename = uploaded_file.name
	
	# Detecta a extensão do arquivo
	file_extension = uploaded_filename.split('.')[-1].lower()

	with st.spinner('Convertendo áudio para mp3...'):

		# Gera um nome único para o arquivo MP3 usando uuid (pseudônimo universalmente único).
		mp3_filename = '{nome_arquivo}.mp3'.format(nome_arquivo=uuid.uuid4().hex)

		# Abre o arquivo temporariamente para leitura e escrita binária.
		tempfile = open(uploaded_filename, 'wb')
		tempfile.write(uploaded_file.read())
		tempfile.close()

		# Converte o arquivo para MP3 (suporta MP4, OGG e outros formatos)
		audio_to_mp3(uploaded_filename, mp3_filename)
		
		# Remove o arquivo temporário
		deletar_arquivo_se_existir(uploaded_filename)

	# Indica sucesso da conversão.
	st.success("Conversão para MP3 realizada!")



	with st.spinner('Convertendo de mp3 para texto...'):

		# Configura a chave da API para o AssemblyAI.
		aai.settings.api_key = aai_api_key

		# Converte o áudio MP3 para texto.
		transcript = mp3_to_text(
			aai, 
			filename=mp3_filename,
			s_labels=True,  # Ativa os rótulos para falantes.
			s_expected=speakers_expected,
			l_code=language_codes[language]
		)

		# Indica que o áudio foi transcrito com sucesso.
		st.success("Transcrição de áudio para texto realizada!")


		# Inicializa variáveis para armazenar o texto transcrito e anotado.
		texto_transcrito = ''
		texto_anotado = []

		# Se a transcrição foi bem-sucedida, exibe as falas dos falantes.
		if transcript:
			# Itera sobre as falas transcritas e imprime cada fala com o número do falante.
			for utterance in transcript.utterances:
				# Exibe o número do falante e o texto correspondente.
				texto_transcrito += f"Speaker {utterance.speaker}: {utterance.text}"
				texto_transcrito += '\n'

				# Adiciona o texto da fala junto com a identificação do falante.
				texto_anotado.append((utterance.text, f"Speaker {utterance.speaker}"))


	with st.spinner('Gerando ata de reunião...'):

		# Inicializa o cliente OpenAI com sua chave de API.
		client = OpenAI(api_key=openai_api_key)

		# Inclui a transcrição do áudio no prompt de texto.
		prompt_text += '\n===========\n'
		prompt_text += texto_transcrito

		# Gera uma resposta com base nos prompts e na transcrição.
		texto_retorno = generate_response(client, prompt_system, prompt_text)

		# Indica sucesso na geração da ata.
		st.success("Ata gerada com sucesso!")


	# Exibe a seção de transcrição original.
	st.subheader('Transcrição original')

	# Mostra o texto anotado com os falantes diferenciados.
	annotated_text(texto_anotado)

	# Display da ata gerada na aplicação.
	st.subheader('Ata gerada')
	st.markdown(texto_retorno)

	# Remove o arquivo MP3 temporário criado.
	deletar_arquivo_se_existir(mp3_filename)