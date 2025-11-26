'''Curso de FastAPI - Rest API com Python (Backend Completo)'''

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from dotenv import load_dotenv
from os import getenv

load_dotenv()  # carrega do arquivo .env

SECRET_KEY = getenv('SECRET_KEY')
ALGORITHM = getenv('ALGORITHM')
# converte em inteiro pra data da expiração do Token
ACCESS_TOKEN_EXP_MIN = int(getenv('ACCESS_TOKEN_EXP_MIN', 15))
REFRESH_TOKEN_EXP_DAY = int(getenv('REFRESH_TOKEN_EXP_DAY', 7)) # Extra

app = FastAPI()

# usará pra criptografia usando hash
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
# authentic OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

from auth_routes import auth_router
from orders_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)

# uvicorn main:app --reload
