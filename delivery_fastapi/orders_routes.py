'''Curso de FastAPI - Rest API com Python (Backend Completo)'''

from fastapi import APIRouter, Depends
from shemas import PedidoShema
from sqlalchemy.orm import Session
from dependencies import pegar_sessao
from models import Pedido

# roteador da rota pedidos
order_router = APIRouter(prefix='/pedidos', tags=['pedidos'])


# rota padrão
# decorador do tipo get (nesse raso na raiz '/')
@order_router.get('/')
# cria uma função assincrona (pedidos)
async def pedidos():
    '''
    Essa é a rota padrão de Pedidos do nosso Software.
    - Todas as rotas dos Pedidos, precisam de Autenticação.
    '''
    # sua implementação
    ...

    # retorna um json (dict '{}')
    return {
        'mensagem': 'Você está acessando a rota Pedidos',
    }


@order_router.post('/pedido')
async def criar_pedido(
    pedido_shema: PedidoShema, session: Session = Depends(pegar_sessao)
):
    pedido_novo = Pedido(usuario=pedido_shema.id_usuario)

    session.add(pedido_novo)
    session.commit()

    return {'mensagem': f'Pedido {pedido_novo.id}, criado com Sucesso!'}
    ...
