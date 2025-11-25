'''
Curso de FastAPI - Rest API com Python (Backend Completo)

- Aula 01: Apresentação do Projeto
- Aula 02: Requisições e Roteamento da API
- Aula 03: Banco de Dados, Modelos e Migrações
- Aula 04: Criar conta de usuário, Schemas e Criptografia
'''

from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
from os import getenv

load_dotenv()  # carrega do arquivo .env

SECRET_KEY = getenv('SECRET_KEY')

app = FastAPI()

# usará pra criptografia usando hash
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

from auth_routes import auth_router
from orders_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)

# uvicorn main:app --reload
