from models import db
from sqlalchemy.orm import sessionmaker


def pegar_sessao():
    try:
        # abre uma sessão no banco
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        # se tudo der errado fecha a sessão
        session.close()
