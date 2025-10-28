from cryptography.fernet import Fernet
import os
import shutil

def carregar_chave():
    try:
        return open("chave.key", "rb").read()
    except FileNotFoundError:
        print("Erro: Arquivo 'chave.key' não encontrado. Certifique-se de que o ransomware foi executado primeiro.")
        return None

def descriptografar_arquivo(arquivo, chave):
    # Verificar se o arquivo está criptografado (inicia com 'gAAAAA' do Fernet)
    try:
        with open(arquivo, "rb") as file:
            primeiros_bytes = file.read(6)
        if primeiros_bytes != b'gAAAAA':
            print(f"Arquivo {arquivo} não está criptografado. Pulando...")
            return
    except Exception as e:
        print(f"Erro ao verificar {arquivo}: {e}")
        return

    # Criar backup antes de descriptografar
    backup = arquivo + ".bak"
    try:
        shutil.copy(arquivo, backup)
        print(f"Backup criado: {backup}")
    except Exception as e:
        print(f"Erro ao criar backup para {arquivo}: {e}")
        return

    # Descriptografar com tratamento de erros
    f = Fernet(chave)
    try:
        with open(arquivo, "rb") as file:
            dados = file.read()
        dados_descritografados = f.decrypt(dados)
        with open(arquivo, "wb") as file:
            file.write(dados_descritografados)
        print(f"Arquivo {arquivo} descriptografado com sucesso.")
    except Exception as e:
        print(f"Erro ao descriptografar {arquivo}: {e}. Restaurando do backup...")
        try:
            shutil.copy(backup, arquivo)
            print(f"Arquivo {arquivo} restaurado do backup.")
        except Exception as e2:
            print(f"Erro ao restaurar backup: {e2}")

def encontrar_arquivos(diretorio):
    lista = []
    for raiz, _, arquivos in os.walk(diretorio):
        for nome in arquivos:
            caminho = os.path.join(raiz, nome)
            if nome != "Ransonware.py" and not nome.endswith(".key") and not nome.endswith(".bak"):
                lista.append(caminho)
    return lista

def main():
    chave = carregar_chave()
    if chave is None:
        return
    arquivos = encontrar_arquivos("test_files")
    if not arquivos:
        print("Nenhum arquivo encontrado para descriptografar em 'test_files'.")
        return
    for arquivo in arquivos:
        descriptografar_arquivo(arquivo, chave)
    print("Processo de descriptografia concluído!!!")

if __name__ == "__main__":
    main()
