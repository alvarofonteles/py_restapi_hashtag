'''Curso de FastAPI - Rest API com Python (Backend Completo)'''

from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao, verifica_token
from main import (
    bcrypt_context,
    ALGORITHM,
    ACCESS_TOKEN_EXP_MIN,
    SECRET_KEY,
    REFRESH_TOKEN_EXP_DAY,
)
from shemas import UsuarioShema, LoginShema
from sqlalchemy.orm import Session
from dependencies import pegar_sessao
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

auth_router = APIRouter(prefix='/auth', tags=['auth'])


def gerar_token(id_usuario, refresh=timedelta(minutes=ACCESS_TOKEN_EXP_MIN)):
    # data da expiração do Token
    # se passar o refresh, é atualizado, senao segue default
    data_exp = datetime.now(timezone.utc) + refresh

    # dicionario de informação para o encode
    dict_info = {'sub': str(id_usuario), 'exp': data_exp}

    # GERA O TOKEN
    jwt_encode = jwt.encode(dict_info, SECRET_KEY, ALGORITHM)

    # retorna o Token
    return jwt_encode


# validação de email (reaproveita)
def verifica_email_existente(email: str, session: Session) -> Usuario | None:
    '''Retorna o usuário se existir.'''
    return session.query(Usuario).filter(Usuario.email == email).first()


# validação de usario e senha na base de dados
def autentica_login(shema: LoginShema, session: Session) -> Usuario | bool:
    '''Autentica usuário com e-mail e senha'''
    usuario = verifica_email_existente(shema.email, session)

    if not usuario:
        return False

    # verifica a senha hash na base
    if not bcrypt_context.verify(shema.senha, usuario.senha):
        return False

    return usuario  # retorna autenticado


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
    # valida email existe com HTTPException usando a função para registro
    if verifica_email_existente(usuario_shema.email, session):
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
    # checagem se já existe usando a função para autenticação
    usuario = autentica_login(shema=login_shema, session=session)

    if not usuario:
        raise HTTPException(status_code=400, detail='Credenciais inválidas!')

    # gera token de 15 min
    access_token = gerar_token(usuario.id)

    # gera o refresh token de 7 dias
    refresh = timedelta(days=REFRESH_TOKEN_EXP_DAY)
    refresh_token = gerar_token(id_usuario=usuario.id, refresh=refresh)

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'Bearer',
    }

    # JWT Bearer
    # headers = {'Access-Token': 'Bearer token}


# já com usuário validado
@auth_router.get('/refresh')
async def refresh_token(usuario: Usuario = Depends(verifica_token)):

    # No refresh endpoint - SÓ GERA ACCESS NOVO
    new_access_token = gerar_token(usuario.id)
    # refresh_token continua o MESMO com os 7 dias originais

    return {
        'access_token': new_access_token,
        'token_type': 'Bearer',
    }
