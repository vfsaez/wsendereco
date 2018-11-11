#!/usr/bin/python3
from os import system

from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from secrets import *

db_connect = create_engine('sqlite:///enderecodb.db')
app = Flask(__name__)
api = Api(app)

tokenDictionary = {}

class Enderecos(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from endereco") # This line performs query and returns json result
        return {'Ceps cadastrados': [i[1] for i in query.cursor.fetchall()]} # Fetches first column that is Employee ID
    
    def post(self):

        conn = db_connect.connect()
        print(request.json)
        id = request.json['id']
        cep = request.json['cep']
        logradouro = request.json['logradouro']
        inicio = request.json['inicio']
        fim = request.json['fim']

        query = conn.execute("insert into endereco values(null,'{0}','{1}','{2}','{3}')".format(cep, logradouro, inicio, fim))
        return {'status':'success'}

class Pedidos_id(Resource):
    def get(self, id):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from pedido where idCliente = "+id) # This line performs query and returns json result
        return jsonify([dict(zip(tuple (query.keys()) ,i)) for i in query.cursor])



class Pedidos(Resource):
    def post(self):

        conn = db_connect.connect()
        print(request.json)
        idCliente = request.json['idCliente']
        nomeCliente = request.json['nomeCliente']
        logradouroEntrega = request.json['logradouroEntrega']
        numeroEntrega = request.json['numeroEntrega']
        complementoEntrega = request.json['complementoEntrega']
        cepEntrega = request.json['cepEntrega']
        valorProdutos = request.json['valorProdutos']
        FreteTotal = request.json['FreteTotal']
        valorTotal = request.json['valorTotal']
        prazoEntrega = request.json['prazoEntrega']
        idPagamento = request.json['idPagamento']
        formaPagamento = request.json['formaPagamento']
        statusPagamento = request.json['statusPagamento']
        statusEntrega = request.json['statusEntrega']
        statusPedido = request.json['statusPedido']
        query = conn.execute("insert into pedido values(null,'{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}')".format(idCliente,cpfCliente,nomeCliente,logradouroEntrega,numeroEntrega,complementoEntrega,cepEntrega,valorProdutos,FreteTotal,valorTotal,prazoEntrega,idPagamento,formaPagamento,statusPagamento,statusEntrega,statusPedido))
        return {'status':'success'}


class ProdutosPedido_id(Resource):
    def get(self, id):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from produtosPedido where idPedido = "+id) # This line performs query and returns json result
        return jsonify([dict(zip(tuple (query.keys()) ,i)) for i in query.cursor])

class ProdutosPedido(Resource):
    def post(self):

        conn = db_connect.connect()
        print(request.json)
        idPedido = request.json['idPedido']
        idProduto = request.json['idProduto']
        quantidade = request.json['quantidade']
        valorUnitario = request.json['valorUnitario']
        valorSoma = request.json['valorSoma']
    
        query = conn.execute("insert into produtosPedido values('{0}','{1}','{2}','{3}','{4}')".format(idPedido,idProduto,quantidade,valorUnitario,valorSoma))
        return {'status':'success'}

class Enderecos_Id(Resource):
    def get(self, id):

        conn = db_connect.connect()
        query = conn.execute("select * from endereco where id ="+id)
        result = {'Endereco': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

class Enderecos_Logradouro(Resource):
    def get(self, logradouro):

        conn = db_connect.connect()
        consult = "select * from endereco where "
        for index, item in enumerate(logradouro.split('+')):
            if index == 0:
                consult +=  "logradouro like '%"+item+"%'"
            else:
                consult +=  " and logradouro like '%"+item+"%'"
        query = conn.execute(consult)
        result = {'Enderecos Compativeis': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

class Enderecos_Cep(Resource):
    def get(self, cep):

        conn = db_connect.connect()
        query = conn.execute("select * from endereco where cep ='"+cep+"'")
        result = {'Endereco': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

class Authenticate_Login(Resource):
    def post(self, username, password):
        if (username is None or password is None):
            return False

        # TODO: validate username and password
        token = self.generateToken()
        tokenDictionary[token] = username
        result = {'TOKEN': token}
        return jsonify(result)

    def generateToken(self):
        return token_hex(16)

    def validateRequest(self, request):
        if request.headers.get('TOKEN') is None:
            return False

        return request.headers.get('TOKEN') in tokenDictionary

class Authenticate_Logout(Resource):
    def post(self, username):
        for key, value in dict(tokenDictionary).items():
            if value == username:
                del tokenDictionary[key]
        return True


@app.route('/end')
def student():
   return render_template('end.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      return render_template("result.html",result = result)

api.add_resource(Enderecos_Cep, '/api/enderecos/cep/<cep>') # Route_3
api.add_resource(Enderecos_Id, '/api/enderecos/id/<id>') # Route_3
api.add_resource(Enderecos_Logradouro, '/api/enderecos/logradouro/<logradouro>') # Route_3
api.add_resource(Enderecos, '/api/enderecos') # Route_1
api.add_resource(Pedidos, '/site/pedidos/')
api.add_resource(Pedidos_id, '/site/pedidos/id/<id>') # Route_1
api.add_resource(ProdutosPedido_id, '/site/produtospedido/id/<id>') # Route_1
api.add_resource(Authenticate_Login, '/api/login/<username>/<password>')
api.add_resource(Authenticate_Logout, '/api/logout/<username>')


if __name__ == '__main__':
     app.run(host='0.0.0.0', port='80')
