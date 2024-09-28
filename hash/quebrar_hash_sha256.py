import json
import hashlib
import os
import itertools
import time
from tqdm import tqdm  # Importa tqdm para a barra de progresso
from colorama import Fore, Style, init

init(autoreset=True)

# Hash a senha utilizando SHA-256.
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# Carrega a lista de usuários de um arquivo JSON.
def carregar_usuarios():
    caminho_arquivo = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'users.json')
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'r') as arquivo:
            return json.load(arquivo)
    else:
        return {}

# Tenta quebrar a hash usando força bruta para senhas de até um certo tamanho.
def brute_force_hash(objetivo_hash, max_length):
    caracteres = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789Çç!@#$%&*()\\/|áãõóúÁÃÓÔÚ'
    for length in range(1, max_length + 1):
        total_combinacoes = len(caracteres) ** length
        for senha_tuple in tqdm(itertools.product(caracteres, repeat=length), total=total_combinacoes, desc=f"Testando senhas com {length} caracteres", unit="comb"):
            senha = ''.join(senha_tuple)
            if hash_senha(senha) == objetivo_hash:
                return senha
    return None

def main():
    max_length = int(input("Digite o tamanho máximo da senha que deseja testar: "))
    usuarios = carregar_usuarios()
    start_time = time.time()
    
    # Limita o número de usuários para quebrar a senha aos 10 primeiros
    usuarios_testar = {k: usuarios[k] for k in list(usuarios)[:10]}
    
    for name, senha_com_hash in usuarios_testar.items():
        print(f"\nQuebrando senha para {Fore.BLUE}{name}{Style.RESET_ALL}...")
        usuario_start = time.time()
        senha_encontrada = brute_force_hash(senha_com_hash, max_length)
        usuario_end = time.time()
        
        if senha_encontrada:
            print(f"{Fore.GREEN}Senha encontrada para {Style.BRIGHT}{name}{Style.RESET_ALL}: {Fore.YELLOW}{senha_encontrada}{Style.RESET_ALL} (Tempo: {usuario_end - usuario_start:.2f} segundos)")
        else:
            print(f"{Fore.RED}Senha não encontrada para {Style.BRIGHT}{name}")

    end_time = time.time()
    total_time = end_time - start_time
    print(f"\nTempo total: {Fore.YELLOW}{total_time:.2f} segundos")
    print(f"Tempo médio por senha: {Fore.YELLOW}{total_time / len(usuarios_testar):.2f} segundos")

if __name__ == "__main__":
    main()
