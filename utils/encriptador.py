from cryptography.fernet import Fernet, InvalidToken
import os
from dotenv import load_dotenv

load_dotenv()
FERNET_KEY = os.getenv("FERNET_KEY")
if not FERNET_KEY:
    raise ValueError("❌ No se encontró FERNET_KEY en el entorno.")
fernet = Fernet(FERNET_KEY)
print(f"🔑 usando FERNET_KEY: {FERNET_KEY}")

def encriptar(texto):
    return fernet.encrypt(texto.encode()).decode()

def desencriptar(token):
    try:
        print("🧩 Token recibido para desencriptar:", token)
        return fernet.decrypt(token.encode()).decode()
    except InvalidToken:
        print("❌ Token inválido. ¿Está encriptado con otra clave?")
        raise