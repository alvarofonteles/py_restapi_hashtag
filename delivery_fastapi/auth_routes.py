'''Curso de FastAPI - Rest API com Python (Backend Completo)'''

from fastapi import APIRouter, Depends
from models import Usuario
from dependencies import pegar_sessao

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


@auth_router.post('/criar_conta')
async def criar_conta(
    email: str, senha: str, nome: str, session=Depends(pegar_sessao)
):
    # busca informações na base
    usuario_db = session.query(Usuario).filter(Usuario.email == email).first()
    # valida usuario se existe
    if usuario_db:
        return {'mensagem': 'Usuário já cadastrado na base!'}

    # cria Usuário
    usuario = Usuario(nome, email, senha)
    # adiciona na base
    session.add(usuario)
    # commit na base e encerra a sessão
    session.commit()
    return {'mensagem': 'Usuário cadastrado com Sucesso!'}
