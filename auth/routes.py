from auth.database import database
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from auth.security import verificar_clave, crear_token
from pydantic import BaseModel
from auth.security import hashear_clave

router = APIRouter()

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    usuario: str
    dependencia: str

@router.post("/login", response_model=LoginResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    usuario = form_data.username
    clave = form_data.password

    query = """
        SELECT clave_hash, dependencia 
        FROM usuarios 
        WHERE usuario = :usuario
    """
    result = await database.fetch_one(query=query, values={"usuario": usuario})

    if not result:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")

    clave_hash = result["clave_hash"]
    dependencia = result["dependencia"]

    if not verificar_clave(clave, clave_hash):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    token = crear_token({"sub": usuario})
    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": usuario,
        "dependencia": dependencia
    }
    
class Credenciales(BaseModel):
    usuario: str
    clave: str

@router.post("/guardar_credenciales")
async def guardar_credenciales(datos: Credenciales):
    try:
        # Verificar si el usuario existe
        query_verificar = "SELECT id FROM usuarios WHERE usuario = :usuario"
        existe = await database.fetch_one(query=query_verificar, values={"usuario": datos.usuario})

        if not existe:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Hashear la nueva clave
        clave_hash = hashear_clave(datos.clave)

        # Actualizar la clave
        query_actualizar = """
            UPDATE usuarios
            SET clave_hash = :clave_hash
            WHERE usuario = :usuario
        """
        await database.execute(query=query_actualizar, values={
            "clave_hash": clave_hash,
            "usuario": datos.usuario
        })

        return {"mensaje": "✅ Credenciales actualizadas correctamente"}
    
    except Exception as e:
        print("❌ Error:", e)
        raise HTTPException(status_code=500, detail="Error interno al actualizar credenciales")