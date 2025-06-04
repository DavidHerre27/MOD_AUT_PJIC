from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import os

# Configuración básica
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "clave_default_segura")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_clave(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def generar_hash_clave(password):
    return pwd_context.hash(password)

def crear_token_acceso(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decodificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
    
from fastapi import HTTPException, status

def verificar_token_y_extraer_usuario(token: str) -> str:
    payload = decodificar_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        )
    usuario = payload.get("sub")
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: sin usuario",
        )
    return usuario