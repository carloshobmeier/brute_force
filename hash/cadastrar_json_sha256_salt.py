
import json
import os
import bcrypt
import time
from colorama import init, Style, Fore

init(autoreset=True)

# Hash a senha utilizando bcrypt com salt.
def hash_senha(senha):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(senha.encode(), salt)

# Retorna o caminho completo do arquivo JSON no diretório do script.
def pegar_caminho_arquivo(nome_arquivo):
    caminho_diretorio = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(caminho_diretorio, nome_arquivo)

# Salva a lista de usuários em um arquivo JSON.
def salvar_usuarios(usuarios):
    caminho_arquivo = pegar_caminho_arquivo('users.json')
    with open(caminho_arquivo, 'w') as arquivo:
        json.dump(usuarios, arquivo)

# Carrega a lista de usuários de um arquivo JSON.
def carregar_usuarios():
    caminho_arquivo = pegar_caminho_arquivo('users.json')
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'r') as arquivo:
            return json.load(arquivo)
    else:
        return {}

# Cadastra um novo usuário.
def registrar_usuario(usuarios):
    print("\nO nome e a senha devem, respectivamente, ter 4 caracteres cada.")
    nome = input("Digite o nome: ")
    if len(nome) != 4:
        print(f"{Fore.RED}O nome escolhido não tem exatamente 4 caracteres.")
        return
    
    if nome in usuarios:
        print(f"{Fore.RED}Este nome de usuário já está em uso. Por favor, escolha outro nome.")
        return

    senha = input("Digite a senha: ")
    if len(senha) != 4:
        print(f"{Fore.RED}A senha escolhida não tem exatamente 4 caracteres.")
        return

    # Cria uma hash para a senha
    senha_hash = hash_senha(senha).decode()
    
    # Salva o usuário
    usuarios[nome] = senha_hash
    salvar_usuarios(usuarios)
    print(f"{Fore.GREEN}Usuário cadastrado com sucesso.")

# Autentica um usuário existente.
def autenticar_usuario(usuarios):
    nome = input("\nDigite seu nome: ")
    senha = input("Digite sua senha: ")
    
    # Verifica se o usuário existe e compara a hash da senha
    if nome in usuarios and bcrypt.checkpw(senha.encode(), usuarios[nome].encode()):
        print(f"{Fore.GREEN}Autenticação bem-sucedida.")
        print(f"{Fore.GREEN}Bem-vindo, {Style.BRIGHT}{nome}.")
    else:
        print(f"{Fore.RED}Falha na autenticação.")

def main():
    usuarios = carregar_usuarios()
    
    while True:
        print("\nMENU")
        print("1 - Cadastrar usuário")
        print("2 - Autenticar usuário")
        print("3 - Sair")
        escolha = input("Escolha uma opção: ")
        
        if escolha == '1':
            registrar_usuario(usuarios)
        elif escolha == '2':
            autenticar_usuario(usuarios)
        elif escolha == '3':
            break
        else:
            print(f"{Fore.YELLOW}Opção inválida.")

if __name__ == "__main__":
    main()
