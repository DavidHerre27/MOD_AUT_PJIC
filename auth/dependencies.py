from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from auth.security import verificar_token
from auth.database import get_usuario_por_nombre

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verificar_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    
    usuario = get_usuario_por_nombre(payload["sub"])
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")

    return usuario