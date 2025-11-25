'''Curso de FastAPI - Rest API com Python (Backend Completo)'''

from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao
from main import bcrypt_context
from shemas import UsuarioShema, LoginShema
from sqlalchemy.orm import Session
from dependencies import pegar_sessao

auth_router = APIRouter(prefix='/auth', tags=['auth'])


def gerar_token(id_usuario):
    base_token = f'nGaIxvXeFZPlTkpF{id_usuario}v4YP2rHJRO7PZQRc'
    return base_token


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
    usuario_shema: UsuarioShema, session: Session = Depends(pegar_sessao)
):
    # busca informações na base usando UsuarioShema
    usuario_db = (
        session.query(Usuario).filter(Usuario.email == usuario_shema.email).first()
    )

    # valida usuario se existe com HTTPException
    if usuario_db:
        raise HTTPException(status_code=400, detail='E-mail do Usuário, já cadastrado!')

    # criptografia (versão que funciona [bcrypt==4.0.1])
    # pip uninstall bcrypt
    # pip install bcrypt==4.0.1
    senha_hash = bcrypt_context.hash(usuario_shema.senha)

    # cria Usuário usando UsuarioShema
    usuario_novo = Usuario(usuario_shema.nome, usuario_shema.email, senha_hash)
    # adiciona na base
    session.add(usuario_novo)
    # commit na base e encerra a sessão
    session.commit()

    # pega e-mail do novo usario criado
    return {
        'mensagem': f'Usuário com e-mail: {usuario_novo.email}, Cadastrado com Sucesso!'
    }


@auth_router.post('/login')
async def login(login_shema: LoginShema, session: Session = Depends(pegar_sessao)):
    # checagem se já existe
    usuario = session.query(Usuario).filter(Usuario.email == login_shema.email).first()

    if not usuario:
        raise HTTPException(status_code=400, detail='Usuário não encontrado!')

    access_token = gerar_token(usuario.id)

    return {'access_token': access_token, 'token_type': 'Bearer'}

    # token gerado nGaIxvXeFZPlTkpF1v4YP2rHJRO7PZQRc

    # JWT Bearer
    # headers = {'Access-Token': 'Bearer token}
