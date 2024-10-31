import os

def deletar_arquivo_se_existir(nome_do_arquivo):
    """
    Deleta um arquivo caso ele exista.

    :param nome_do_arquivo: O caminho para o arquivo a ser deletado.
    """
    # Verifica se o arquivo existe no caminho especificado
    if os.path.exists(nome_do_arquivo):
        # Remove o arquivo
        os.remove(nome_do_arquivo)
        # Informa ao usuário que o arquivo foi deletado com sucesso
        print(f"{nome_do_arquivo} foi deletado.")
    else:
        # Informa ao usuário que o arquivo não existe
        print(f"O arquivo {nome_do_arquivo} não existe.")