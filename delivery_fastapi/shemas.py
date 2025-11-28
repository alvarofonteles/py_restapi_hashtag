'''Curso de FastAPI - Rest API com Python (Backend Completo)'''

from pydantic import BaseModel
from typing import Optional, List


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


class ItensPedidoShema(BaseShema):
    quantidade: int
    sabor: str
    tamanho: str
    preco_unitario: float


class ResponsePedidoShema(BaseShema):
    id: int
    status: str
    preco: float
    itens: List[ItensPedidoShema]
