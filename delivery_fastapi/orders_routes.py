'''Curso de FastAPI - Rest API com Python (Backend Completo)'''

import json
from fastapi import APIRouter

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
