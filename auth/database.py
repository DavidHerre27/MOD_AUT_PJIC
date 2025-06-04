import sqlite3
import os

DATABASE = "usuarios.db"
print(f"📍 [DEBUG] Cargando usuarios.db desde: {os.path.abspath('usuarios.db')}")

def get_connection():
    return sqlite3.connect(os.path.join(os.path.dirname(__file__), "..", "usuarios.db"))

def get_usuario_por_nombre(nombre: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT usuario, clave_hash, dependencia FROM usuarios WHERE usuario = ?", (nombre,))
    fila = cursor.fetchone()
    conn.close()
    if fila:
        return {
            "usuario": fila[0],
            "clave_hash": fila[1],
            "dependencia": fila[2]
        }
    return None