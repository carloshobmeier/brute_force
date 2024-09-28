
import json
import hashlib
import os
from colorama import init, Fore, Style

init(autoreset=True)

# Hash a senha utilizando SHA-256.
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

#Retorna o caminho completo do arquivo no diretório do script.
def pegar_caminho_arquivo(nome_arquivo):
    caminho_diretorio = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(caminho_diretorio, nome_arquivo)

# Salva a lista de usuários no arquivo JSON.
def salvar_usuarios(usuarios):
    caminho_arquivo = pegar_caminho_arquivo('users.json')
    with open(caminho_arquivo, 'w') as arquivo:
        json.dump(usuarios, arquivo)

# Carrega a lista de usuários no arquivo JSON.
def carregar_usuarios():
    caminho_arquivo = pegar_caminho_arquivo('users.json')
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'r') as arquivo:
            return json.load(arquivo)
    else:
        return {}

# Cadastra novo usuário.
def registrar_usuario(usuarios):
    print("\nA senha deve ter 5 caracteres.")
    nome = input("Digite o nome: ")

    
    if nome in usuarios:
        print(f"{Fore.RED}Este nome de usuário já está em uso. Por favor, escolha outro nome.")
        return

    senha = input("Digite a senha: ")
    if len(senha) != 5:
        print(f"{Fore.RED}A senha escolhida não tem exatamente 4 caracteres.")
        return

    # Cria uma hash para a senha
    senha_hash = hash_senha(senha)
    
    # Salva o usuário
    usuarios[nome] = senha_hash
    salvar_usuarios(usuarios)
    print(f"{Fore.GREEN}Usuário cadastrado com sucesso.")

# Autentica um usuário existente.
def autenticar_usuario(usuarios):
    nome = input("\nDigite seu nome: ")
    senha = input("Digite sua senha: ")
    
    # Verifica se o usuário existe e compara a hash da senha
    if nome in usuarios and usuarios[nome] == hash_senha(senha):
        print(f"{Fore.GREEN}Autenticação bem-sucedida.")
        print(f"{Fore.GREEN}Bem-vindo, {Style.BRIGHT}{nome}.")
    else:
        print(f"{Fore.RED}Falha na autenticação.")

def main():
    usuarios = carregar_usuarios()
    while True:
        print("\nMENU INICIAL")
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
