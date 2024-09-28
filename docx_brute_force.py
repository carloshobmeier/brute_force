import msoffcrypto
import io
from itertools import product
import string

def brute_force_decrypt(docx_path, max_length, character_set):
    file = msoffcrypto.OfficeFile(open(docx_path, "rb"))

    # Tenta senhas de diferentes comprimentos
    for length in range(1, max_length + 1):
        for password_tuple in product(character_set, repeat=length):
            # Converte a tupla de caracteres em string
            password = ''.join(password_tuple)
            try:
                # Tenta desbloquear o documento com a senha
                file.load_key(password=password)
                decrypted_stream = io.BytesIO()
                file.decrypt(decrypted_stream)
                print(f"Senha encontrada: {password}")
                return password
            except Exception as e:
                continue  # Se a senha estiver errada, continua tentando
    
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
    docx_path = input("Digite o caminho do arquivo DOCX criptografado: ")
    max_length = int(input("Digite o comprimento máximo da senha a testar: "))
    character_set = get_character_set()

    if character_set:
        result = brute_force_decrypt(docx_path, max_length, character_set)
        if result:
            print(f"A senha do DOCX é: {result}")
        else:
            print("Não foi possível descriptografar o DOCX com as combinações testadas.")
    else:
        print("Nenhum conjunto de caracteres foi selecionado para o teste.")
