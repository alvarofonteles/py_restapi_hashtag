'''Curso de FastAPI - Rest API com Python (Backend Completo)'''

from pydantic import BaseModel
from typing import Optional


# pra não ficar redundante
class BaseShema(BaseModel):
    class Config:
        from_attributes = True


# todos herdam a mesma Config
class UsuarioShema(BaseShema):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]


class PedidoShema(BaseShema):
    id_usuario: int


class LoginShema(BaseShema):
    email: str
    senha: str
