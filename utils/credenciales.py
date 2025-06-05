import psycopg2
import os
from fastapi import APIRouter
from auth import database

router = APIRouter()

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )
    
@router.post("/actualizar_credenciales_gt")
async def obtener_credenciales_gt(usuario_sistema: str):
    query = """
        SELECT gt_usuario, gt_clave_encriptada
        FROM credenciales_gt
        WHERE usuario_sistema = :usuario_sistema
    """
    fila = await database.fetch_one(query=query, values={"usuario_sistema": usuario_sistema})

    if fila:
        return fila["gt_usuario"], fila["gt_clave_encriptada"]

    return None, None