import subprocess
from itertools import product
import string
import tempfile
import shutil

SEVEN_ZIP_PATH = r"C:\Program Files\7-Zip\7z.exe"  # Caminho completo para o executável 7z

def brute_force_decrypt(rar_path, max_length, character_set):
    """Tenta descompactar o arquivo RAR usando brute force chamando o 7z via subprocess."""
    for length in range(1, max_length + 1):
        for password_tuple in product(character_set, repeat=length):
            password = ''.join(password_tuple)
            try:
                # Chama o 7z via subprocess, especificando o caminho completo
                result = subprocess.run(
                    [SEVEN_ZIP_PATH, 'x', '-p{}'.format(password), '-y', rar_path],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )
                # Verifica se a senha foi bem-sucedida verificando a saída
                if 'Everything is Ok' in result.stdout:
                    print(f"Senha encontrada: {password}")
                    return password
            except subprocess.CalledProcessError as e:
                continue  # Senha incorreta, continua tentando

    print("Senha não encontrada.")
    return None

def get_character_set():
    characters = ""
    if input("Incluir letras maiúsculas? (s/n) ").lower() == 's':
        characters += string.ascii_uppercase
    if input("Incluir letras minúsculas? (s/n) ").lower() == 's':
        characters += string.ascii_lowercase
    if input("Incluir caracteres numéricos? (s/n) ").lower() == 's':
        characters += string.digits
    if input("Incluir caracteres especiais? (s/n) ").lower() == 's':
        characters += string.punctuation
    
    return characters

if __name__ == "__main__":
    rar_path = input("Digite o caminho do arquivo RAR criptografado: ")
    max_length = int(input("Digite o comprimento máximo da senha a testar: "))
    character_set = get_character_set()

    if character_set:
        result = brute_force_decrypt(rar_path, max_length, character_set)
        if result:
            print(f"A senha do RAR é: {result}")
        else:
            print("Não foi possível descriptografar o RAR com as combinações testadas.")
    else:
        print("Nenhum conjunto de caracteres foi selecionado para o teste.")
