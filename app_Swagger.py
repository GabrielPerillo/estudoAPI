from flask import Flask, request
from flask_restx import Api, Resource, fields

# ===============================
# Configuração da aplicação
# ===============================
app = Flask(__name__)

api = Api(
    app,
    title="Biblioteca de Livros",
    version="1.0",
    description="API para consulta, criação, edição e exclusão de livros"
)

# ===============================
# Namespace
# ===============================
ns_livros = api.namespace("livros", description="Operações CRUD com livros")

# ===============================
# Model (Swagger / OpenAPI)
# ===============================
livro_model = api.model("Livro", {
    "id": fields.Integer(required=True, description="ID do livro"),
    "titulo": fields.String(required=True, description="Título do livro"),
    "autor": fields.String(required=True, description="Autor do livro"),
})

# ===============================
# Fonte de dados (mock)
# ===============================
livros = [
    {
        "id": 1,
        "titulo": "O Senhor dos Anéis - A Sociedade do Anel",
        "autor": "J.R.R. Tolkien"
    },
    {
        "id": 2,
        "titulo": "Harry Potter e a Pedra Filosofal",
        "autor": "J.K. Rowling"
    },
    {
        "id": 3,
        "titulo": "Hábitos Atômicos",
        "autor": "James Clear"
    }
]

# ===============================
# Endpoints /livros
# ===============================
@ns_livros.route("/")
class Livros(Resource):

    @ns_livros.marshal_list_with(livro_model)
    def get(self):
        """Consultar todos os livros"""
        return livros

    @ns_livros.expect(livro_model)
    @ns_livros.marshal_list_with(livro_model)
    def post(self):
        """Cadastrar um novo livro"""
        novo_livro = request.json
        livros.append(novo_livro)
        return livros, 201

# ===============================
# Endpoints /livros/{id}
# ===============================
@ns_livros.route("/<int:id>")
class Livro(Resource):

    @ns_livros.marshal_with(livro_model)
    def get(self, id):
        """Consultar livro por ID"""
        for livro in livros:
            if livro["id"] == id:
                return livro
        api.abort(404, "Livro não encontrado")

    @ns_livros.expect(livro_model)
    @ns_livros.marshal_with(livro_model)
    def put(self, id):
        """Editar livro por ID"""
        dados = request.json
        for livro in livros:
            if livro["id"] == id:
                livro.update(dados)
                return livro
        api.abort(404, "Livro não encontrado")

    @ns_livros.marshal_list_with(livro_model)
    def delete(self, id):
        """Excluir livro por ID"""
        for indice, livro in enumerate(livros):
            if livro["id"] == id:
                del livros[indice]
                return livros
        api.abort(404, "Livro não encontrado")

# ===============================
# Inicialização
# ===============================
if __name__ == "__main__":
    app.run(port=5000, host="localhost", debug=True)
