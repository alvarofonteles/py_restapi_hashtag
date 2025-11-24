'''Curso de FastAPI - Rest API com Python (Backend Completo)'''

from fastapi import APIRouter

auth_router = APIRouter(prefix='/auth', tags=['auth'])


@auth_router.get('/')
# decorador do tipo get (nesse raso na raiz '/')
async def autenticar():
    '''Essa é a rota padrão de Autenticação do nosso Software.'''
    ...

    # retorna um json (dict '{}')
    return {
        'mensagem': 'Você acessou a rota padrão de Autenticação',
        'autenticado': False,
    }
