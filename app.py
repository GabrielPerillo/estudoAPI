# API - Um lugar para dipsonibilizar recursos e/ou funcionalidades 
# 1. Objetivo - Criar uma API que disponibiliza a consulta, criação, edição, exclusão de livros 
# 2. URL Base (Lugar onde faremos as requisições) - localhost - ex: youtube.com/api
# 3. Endpoints - Quais são os tipos de funcionalidade que vamos disponibilizar na API 
#    - localhost/livros (GET) - Consultar Livros 
#    - localhost/livros (GET) - Cadastrar novos Livros 
#    - localhost/livros/id (GET) - Consultar livro específico por ID 
#    - localhost/livros/id (PUT) - Editar livro por ID 
#    - localhost/livros/id (DELETE) - Deletar livro por ID 
# 4. Quais recursos/funcionalidades queremos disponibilizar - Livros  

from flask import Flask, jsonify, request 
#from flask_restx import Api, Resource

# Flask - servidor 
# jsonify - o que nos permite retornar no formato .json, formato esperado de uma API
# request - que nos permite acessar os dados que estão indo/vindo das nossas requsições 

app = Flask(__name__)  # criando aplicação flask com nome do arquivo atual 
# api = Api(
#     app,
#     title="Biblioteca de Livros",
#     version="1.0",
#     description="API documentada com Swagger"
# )

# ns = api.namespace("health", description="Health check")

# @ns.route("/")
# class Health(Resource):
#     def get(self):
#         return {"status": "ok"}

# Agora precisamos de uma fonte de dados 

livros = [      # lista 
    {           # dicionário
        'id': 1,
        'título': 'O Senhor dos Anpeis - A Sociedade do Anel',
        'autor': 'J.R.R Tolkien'
    },
    {
        'id': 2,
        'título': 'Harry Potter e a Pedra Filosofal',
        'autor': 'J.K Howling'
    },
    {
        'id': 3,
        'título': 'Hábitos Atômicos',
        'autor': 'James Clear'
    }
]

# Agora vamos criar a API



# para ser cosniderado uma API, é preciso decorá-la com 
@app.route('/livros',methods=['GET']) 

# Consultar (todos)
def obterLivros():
    return jsonify(livros)


@app.route('/livros/<int:id>',methods=['GET']) 

# Consultar (id)
def obterLivroId(id):
    for livro in livros:
        if livro.get('id') == id:
            return jsonify(livro)


# Editar 
@app.route('/livros/<int:id>',methods=['PUT'])

def editarLivroId(id):
    livro_alterado = request.get_json()
    for indice,livro in enumerate(livros):
        if livro.get('id') == id:
            livros[indice].update(livro_alterado)
            return jsonify(livros[indice])


# Criar 
@app.route('/livros',methods=['POST'])

def cadastrarLivro():
    novo_livro = request.get_json()
    livros.append(novo_livro)

    return jsonify(livros)


# Excluir 

@app.route('/livros/<int:id>',methods=['DELETE'])
def excluir_livro(id):
    for indice, livro in enumerate(livros):
        if livro.get('id') == id:
            del livros[indice]
        
    return jsonify(livros) 



# agora vamos inicializar essa aplicação 
app.run(port=5000,host='localhost',debug=True) 

