# auth/database.py
from databases import Database
import os

# Usa la variable de entorno DATABASE_URL definida en Render
DATABASE_URL = os.getenv("DATABASE_URL")
database = Database(DATABASE_URL)

async def get_usuario_por_nombre(nombre: str):
    query = """
        SELECT usuario, clave_hash, dependencia
        FROM usuarios
        WHERE usuario = :nombre
    """
    fila = await database.fetch_one(query=query, values={"nombre": nombre})
    
    if fila:
        return {
            "usuario": fila["usuario"],
            "clave_hash": fila["clave_hash"],
            "dependencia": fila["dependencia"]
        }
    return None