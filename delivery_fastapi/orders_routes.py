'''Curso de FastAPI - Rest API com Python (Backend Completo)'''

from fastapi import APIRouter, Depends, HTTPException
from shemas import PedidoShema, ItensPedidoShema
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verifica_token
from models import Pedido, Usuario, ItensPedido

# roteador da rota pedidos
order_router = APIRouter(
    prefix='/pedidos', tags=['pedidos'], dependencies=[Depends(verifica_token)]
)


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


@order_router.post('/pedido')
async def criar_pedido(
    pedido_shema: PedidoShema, session: Session = Depends(pegar_sessao)
):
    '''criar pedido'''
    pedido_novo = Pedido(usuario=pedido_shema.id_usuario)

    session.add(pedido_novo)
    session.commit()

    return {'mensagem': f'Pedido {pedido_novo.id}, criado com Sucesso!'}


@order_router.post('/cancelar/{id_pedido}')
async def cancelar_pedido(
    id_pedido: int,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verifica_token),
):
    '''cancelar pedido'''
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail='Pedido não encontrado.')

    if not usuario.admin and usuario.id != pedido.id_usuario:
        raise HTTPException(
            status_code=401,
            detail='Você não tem autorização para fazer esse cancelamento.',
        )

    pedido.status = 'CANCELADO'
    session.commit()

    return {
        'mensagem': f'Pedido número: {pedido.id}, cancelado com sucesso!',
        'pedido': pedido,
    }


@order_router.get('/listar')
async def listar_pedidos(
    session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verifica_token)
):
    '''
    listar pedidos
    - funcionando
      - top
    '''

    # checagem se ele é administrador
    if not usuario.admin:
        raise HTTPException(
            status_code=401, detail='Você não tem autorização para fazer essa operação.'
        )

    # retorna todos os pedidos
    pedidos = session.query(Pedido).all()

    # devolve a lista de todos os pedidos
    return {'pedidos': pedidos}


@order_router.post('/adicionar-item/{id_pedido}')
async def adicionar_item_pedido(
    id_pedido: int,
    itens_shema: ItensPedidoShema,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verifica_token),
):
    '''Adiciona item pedido e atualiza preço do pedido'''
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()

    if not pedido:
        raise HTTPException(status_code=400, detail='Pedido não encontrado.')

    if not usuario.admin and usuario.id != pedido.id_usuario:
        raise HTTPException(
            status_code=401, detail='Você não tem autorização para fazer essa operação.'
        )

    item_pedido = ItensPedido(
        itens_shema.quantidade,
        itens_shema.sabor,
        itens_shema.tamanho,
        itens_shema.preco_unitario,
        id_pedido,
    )

    # adiciona itens pedido
    session.add(item_pedido)

    # atualiza preço no Pedido (Mocado)
    pedido.calcula_preco()

    # commit na sessão
    session.commit()

    return {
        'mensagem': f'Item: {item_pedido.id}, com valor total: {pedido.preco}, criado com Sucesso!',
        'pedido': pedido,
    }
