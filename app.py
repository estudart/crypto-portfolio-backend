from flask import Flask, jsonify, redirect, request
from flasgger import Swagger
from flask_restful import Api, Resource

from model import *
from schemas import *

from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)


class HomeResource(Resource):
    def get(self):
        """
        Welcome to the home page!

        ---
        tags:
            - Welcome
        responses:
            200:
                description: A welcome message
        """
        return {"message": "Welcome to the home page"}


# Essa rota fica responsavel por adicionar novos lugares na base do site
@app.post('/exec_order', tags=[lugar_tag],
          responses={"200": ExecOrderViewSchema 
                     #"409": ErrorSchemaLugarExiste, 
                     #"422": ErrorSchemaLugar
                     })
def add_exec_order(form: ExecOrderSchema):
    """Nesse endpoint é possível adicionar um novo lugar à base de dados
    """
    order = ExecOrder(
        symbol=form.symbol,
        quantity=form.quantity,
        price = form.price,
        side = form.side,
        currency = form.currency
    )

    try:
        session = Session()
        # adicionando order
        session.add(order)
        symbol = form.symbol
        portfolio = session.query(Portfolio).filter(Portfolio.symbol == symbol).first()
        if portfolio:
            if form.side == "BUY":
                portfolio.price += form.price
                portfolio.quantity += form.quantity
                session.commit()
            elif form.side == "SELL":
                portfolio.price -= form.price
                portfolio.quantity -= form.quantity
                session.commit()
            return show_exec_order(order), 200
        else:
            portfolio_add = Portfolio(
                symbol=form.symbol,
                quantity=form.quantity,
                price=form.price
            )
            session.add(portfolio_add)
            session.commit()
        # efetivando o camando de adição de novo item na tabela
        return show_exec_order(order), 200
    except IntegrityError as e:
        error_msg = "lugar de mesmo nome já salvo na base :/"
        return {"message": error_msg}, 409
    except Exception as e:
        error_msg = "Não foi possível salvar novo lugar :/"
        return {"message": error_msg}, 422

@app.get('/exec_order', tags=[exec_tag])
def get_exec_order():
    """In this route, you can get all the orders executed."""
    try:
        with Session() as session:
            orders = session.query(ExecOrder).all()

            if not orders:
                error_msg = 'There no excuted orders in the database'
                return {"message": error_msg}, 422

            # Convert orders to a list of dictionaries
            orders_data = [show_exec_order(order) for order in orders]

            # Return the list of dictionaries as JSON
            return jsonify(orders_data), 200
    except Exception as e:
        error_msg = f"Erro inesperado: {e}"
        return {"message": error_msg}, 500

@app.get('/portfolio', tags=[portfolio_tag])
def get_portfolio():
    try:
        with Session() as session:
            portfolio = session.query(Portfolio).all()
            portfolio_data = [show_portfolio(port) for port in portfolio]
            return jsonify(portfolio_data), 200
    except Exception as e:
        error_msg = f"Internal server error: {e}"
        return {"message": error_msg}, 500

'''
# Essa rota fica responsável por adicionar novos clientes na base do sistema
@app.post('/cliente', tags=[cliente_tag],
          responses={"200": ClienteViewSchema, 
                     "409": ErrorSchemaClienteExiste,
                     "422": ErrorSchemaCliente})
def add_cliente(form: ClienteSchema):
    """Nesse endpoint é possivel adicionar um novo cliente à base
    """
    cliente = Cliente(
        nome=form.nome,
        telefone=form.telefone,
        email=form.email
    )

    try:
        # abrindo uma conexão com a base
        session = Session()
        # adicionando cliente
        session.add(cliente)
        session.commit()
        return apresenta_cliente(cliente), 200
    except IntegrityError as e:
        error_msg = "cliente de mesmo nome já salvo na base :/"
        return {"message": error_msg}, 409
    except Exception as e:
        error_msg = "Não foi possível salvar novo cliente :/"
        return {"message": error_msg}, 422

# Essa rota fica responsável por adicionar novos guias na base do sistema
@app.post('/guia', tags=[guia_tag],
          responses={"200": GuiaViewSchema, 
                     "409": ErrorSchemaGuiaExiste,
                     "422": ErrorSchemaGuia})
def add_guia(form: GuiaSchema):
    """Nesse endpoint é possivel adicionar um novo guia à base
    """
    guia = Guia(
        nome=form.nome,
        telefone=form.telefone,
        email=form.email,
        transporte=form.transporte
    )

    try:
        session = Session()
        # adicionando guia
        session.add(guia)
        session.commit()
        return apresenta_guia(guia), 200
    except IntegrityError as e:
        error_msg = "Guia de mesmo nome já salvo na base :/"
        return {"message": error_msg}, 409
    except Exception as e:
        error_msg = "Não foi possível salvar novo Guia :/"
        return {"message": error_msg}, 422


# Essa rota é responsável por adicionar um novo passeio na base
@app.post('/passeio', tags=[passeio_tag],
          responses={"200": PasseioViewSchema,
                     "409": ErrorSchemaGuia, "404": ErrorSchemaLugar,
                     "407": ErrorSchemaCliente, "422": ErrorSchema})
def add_passeio(form: PasseioSchema):
    """Nesse endpoint é possivel criar um novo passeio
    """
    session = Session()
    
    passeio = Passeio(
        guia_nome=form.guia_nome,
        lugar_nome=form.lugar_nome,
        cliente_nome=form.cliente_nome,
        n_estrela=form.n_estrela
    )
 
    try:
        # adicionando passeio
        session.add(passeio)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        return apresenta_passeio(passeio), 200
    except IntegrityError as e:
        error_msg = "ForeignKeyConstraint ERROR :/"
        return {"message": error_msg}, 422
    except Exception as e:
        # error_msg = "Não foi possível salvar novo item :/"
        return {"message": str(e)}, 424


# Essa rota fica responsável por adicionar novos comentarios a respeito de passeios
@app.post('/comentario', tags=[comentario_tag],
          responses={"200": ComentarioViewSchema, 
                     "422": ErrorSchema, 
                     "422": ErrorSchema})
def add_comentario(form: ComentarioSchema):
    """Nesse endpoint é possivel criar um novo comentário para a plataforma
    """
    session = Session()
    passeio_id = form.passeio_id
    passeio = session.query(Passeio).filter(Passeio.id == passeio_id).first()

    # criando um comentário
    comentario = Comentario(
        cliente_nome=form.cliente_nome,
        texto=form.texto
    )
    # adicionando comentario
    passeio.adiciona_comentario(comentario)
    # efetivando o camando de adição de novo item na tabela
    session.commit()
    return apresenta_passeio(passeio), 200

        

# Nessa rota, conseguimos fazer a requisição dos passeios que aconteceram
@app.get('/passeio', tags=[passeio_tag],
         responses={"200": PasseioViewSchema, 
                    "422": ErrorSchemaPasseio})
def get_passeio(query: PasseioGetSchema):
    """Nessa rota é possivel fazer uma busca de um passeio especifico, através do seu id.
    """
    passeio_id=query.id
    session = Session()
    passeio = session.query(Passeio).filter(Passeio.id == passeio_id).first()
    print(passeio)
    
    if not passeio:
        error_msg = 'Passeio não foi encontrado na base'
        return {"message": error_msg}, 422
    else:
        return apresenta_passeio(passeio), 200


@app.delete('/passeio', tags=[passeio_tag],
            responses={"200": PasseioDelSchema, 
                       "422": ErrorSchemaPasseio})
# Nessa rota, conseguimos deletar um passeio (talvez não seja bom tê-la)
def del_passeio(form: PasseioDelSchema):
    """Nesse endpoint é possivel deletar um passeio da base.
    """
    session = Session()
    passeio_id=form.id
    passeio = session.query(Passeio).filter(Passeio.id == passeio_id).first()

    if not passeio:
        error_msg = 'Passeio não foi encontrado na base'
        return {"message": error_msg}, 422
    else:
        count = session.query(Passeio).filter(Passeio.id == passeio_id).delete()
        session.commit()
        msg = f'Passeio de id: {passeio_id}, foi deletado'
        return {"message": msg}, 200


# Nessa rota, é possivel excluir um comentário da tabela
@app.delete('/comentario', 
            tags=[comentario_tag],
            responses={"200": ComentarioDelSchema, 
                       "422": ErrorSchema})
def del_comentario(form: ComentarioDelSchema):
    """Através desse comando é possivel excluir um comentario"""
    session = Session()
    comentario_id=form.id
    comentario = session.query(Comentario).filter(Comentario.id == comentario_id).first()

    if not comentario:
        error_msg = 'Comentario não foi encontrado na base'
        return {"message": error_msg}, 422
    else:
        count = session.query(Comentario).filter(Comentario.id == comentario_id).delete()
        session.commit()
        msg = f'Comentario de id: {comentario_id}, foi deletado'
        return {"message": msg}, 200
'''