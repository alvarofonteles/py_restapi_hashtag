'''Curso de FastAPI - Rest API com Python (Backend Completo)'''

from models import db
from sqlalchemy.orm import sessionmaker, Session
from jose import jwt, JWTError
from main import ALGORITHM, SECRET_KEY, oauth2_scheme
from fastapi import Depends, HTTPException
from models import Usuario


def pegar_sessao():
    try:
        # abre uma sessão no banco
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        # se tudo der errado fecha a sessão
        session.close()


# com OAuth2 para verificação
def verifica_token(
    token: str = Depends(oauth2_scheme), session: Session = Depends(pegar_sessao)
):

    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        # Extrai o user_id do payload e converte pra int
        id_usuario = int(payload.get('sub'))
    except JWTError:
        raise HTTPException(status_code=401, detail='Token inválido ou expirado')

    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    # trata o erro de verdade
    if not usuario:
        raise HTTPException(status_code=401, detail='Acesso Negado')

    return usuario
