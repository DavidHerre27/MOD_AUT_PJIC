from pydantic import BaseModel

class UsuarioBase(BaseModel):
    usuario: str
    dependencia: str

class UsuarioDB(UsuarioBase):
    clave_hash: str