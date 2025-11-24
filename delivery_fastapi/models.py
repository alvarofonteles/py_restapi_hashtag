'''Curso de FastAPI - Rest API com Python (Backend Completo)'''

from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    Boolean,
    Float,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import ChoiceType

# cria sua conexão com a base
db = create_engine(url='sqlite:///banco.db')

# Cria a base do banco
Base = declarative_base()


# Classe Usuario das tabelas do banco
class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String)
    email = Column('email', String, nullable=False)
    senha = Column('senha', String)
    ativo = Column('ativo', Boolean)
    admin = Column('admin', Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin


# Classe Pedido
class Pedido(Base):
    __tablename__ = 'pedidos'

    # STATUS_PEDIDO = (
    #     ('PENDENTE', 'PENDENTE'),
    #     ('CANCELADO', 'CANCELADO'),
    #     ('FINALIZADO', 'FINALIZADO'),
    # )

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    status = Column(
        'status',
        String,  # ChoiceType(STATUS_PEDIDO)
    )  # PENDENTE, CANCELADO, FINALIZADO

    # nome e campo(PK) da tabela Usuario no banco (chave estrangeira)
    usuario = Column('usuario', ForeignKey('usuarios.id'))
    preco = Column('preco', Float)
    # itens =

    def __init__(self, usuario, status='PENDENTE', preco=0):
        self.usuario = usuario
        self.status = status
        self.preco = preco


class ItensPedido(Base):
    __tablename__ = 'itens_pedido'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    quantidade = Column('quantidade', Integer)
    sabor = Column('sabor', String)
    tamanho = Column('tamanho', String)
    preco_unitario = Column('preco_unitario', Float)
    pedido = Column('pedido', ForeignKey('pedidos.id'))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido
