#!/usr/bin/python3
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

db_connect = create_engine('sqlite:///enderecodb.db')
app = Flask(__name__)
api = Api(app)


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

        query = conn.execute("insert into employees values(null,'{0}','{1}','{2}','{3}')".format(cep, logradouro, inicio, fim))
        return {'status':'success'}

class Enderecos_Id(Resource):
    def get(self, id):
        conn = db_connect.connect()
        query = conn.execute("select * from endereco where id ="+id)
        result = {'Endereco': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

class Enderecos_Cep(Resource):
    def get(self, cep):
        conn = db_connect.connect()
        query = conn.execute("select * from endereco where cep ="+cep)
        result = {'Endereco': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)


api.add_resource(Enderecos_Cep, '/enderecos/cep/<cep>') # Route_3
api.add_resource(Enderecos_Id, '/enderecos/id/<id>') # Route_3
api.add_resource(Enderecos, '/enderecos') # Route_1


if __name__ == '__main__':
     app.run()
