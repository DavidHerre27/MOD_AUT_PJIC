import sqlite3
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
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    usuario = form_data.username
    clave = form_data.password

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT clave_hash, dependencia FROM usuarios WHERE usuario = ?", (usuario,))
    fila = cursor.fetchone()
    conn.close()

    if not fila:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")

    clave_hash, dependencia = fila
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
def guardar_credenciales(datos: Credenciales):
    try:
        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()

        clave_hash = hashear_clave(datos.clave)

        # Asegúrate de que el usuario exista antes de actualizar
        cursor.execute("SELECT id FROM usuarios WHERE usuario = ?", (datos.usuario,))
        if cursor.fetchone() is None:
            return {"error": "Usuario no encontrado"}, 404

        cursor.execute("UPDATE usuarios SET clave_hash = ? WHERE usuario = ?", (clave_hash, datos.usuario))
        conn.commit()
        return {"mensaje": "Credenciales actualizadas correctamente"}
    except Exception as e:
        print("❌ Error:", e)
        return {"error": str(e)}, 500
    finally:
        conn.close()