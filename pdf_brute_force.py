import pypdf
from itertools import product
import string

def brute_force_decrypt(pdf_path, max_length, character_set):
    pdf_reader = pypdf.PdfReader(pdf_path)
    
    # Tenta senhas de diferentes comprimentos
    for length in range(1, max_length + 1):
        for password_tuple in product(character_set, repeat=length):
            # Converte a tupla de caracteres em string
            password = ''.join(password_tuple)
            
            if pdf_reader.decrypt(password):
                print(f"Senha encontrada: {password}")
                return password
    
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
    pdf_path = input("Digite o caminho do arquivo PDF criptografado: ")
    max_length = int(input("Digite o comprimento máximo da senha a testar: "))
    character_set = get_character_set()

    if character_set:
        result = brute_force_decrypt(pdf_path, max_length, character_set)
        if result:
            print(f"A senha do PDF é: {result}")
        else:
            print("Não foi possível descriptografar o PDF com as combinações testadas.")
    else:
        print("Nenhum conjunto de caracteres foi selecionado para o teste.")
