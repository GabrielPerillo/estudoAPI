from flask import Flask, request
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, title="Biblioteca de Livros", version="1.0",
          description="API para consulta, criação, edição e exclusão de livros")

ns = api.namespace("livros", description="Operações CRUD com livros")

livro_input = api.model("LivroInput", {
    "titulo": fields.String(required=True, description="Título do livro"),
    "autor": fields.String(required=True, description="Autor do livro"),
})

livro_model = api.model("Livro", {
    "id": fields.Integer(required=True, description="ID do livro"),
    "titulo": fields.String(required=True, description="Título do livro"),
    "autor": fields.String(required=True, description="Autor do livro"),
})

# mock em memória
livros_by_id = {
    1: {"id": 1, "titulo": "O Senhor dos Anéis - A Sociedade do Anel", "autor": "J.R.R. Tolkien"},
    2: {"id": 2, "titulo": "Harry Potter e a Pedra Filosofal", "autor": "J.K. Rowling"},
    3: {"id": 3, "titulo": "Hábitos Atômicos", "autor": "James Clear"},
}
next_id = 4


def get_livro_or_404(id_: int):
    livro = livros_by_id.get(id_)
    if not livro:
        api.abort(404, f"Livro não encontrado (id={id_})")
    return livro


@ns.route("/")
class Livros(Resource):
    @ns.marshal_list_with(livro_model)
    def get(self):
        return list(livros_by_id.values())

    @ns.expect(livro_input, validate=True)
    @ns.marshal_with(livro_model, code=201)
    def post(self):
        global next_id
        payload = api.payload

        novo = {"id": next_id, "titulo": payload["titulo"], "autor": payload["autor"]}
        livros_by_id[next_id] = novo
        next_id += 1

        return novo, 201


@ns.route("/<int:id>")
class Livro(Resource):
    @ns.marshal_with(livro_model)
    def get(self, id):
        return get_livro_or_404(id)

    @ns.expect(livro_input, validate=True)
    @ns.marshal_with(livro_model)
    def put(self, id):
        livro = get_livro_or_404(id)
        payload = api.payload

        livro["titulo"] = payload["titulo"]
        livro["autor"] = payload["autor"]
        return livro, 200

    @ns.response(204, "Excluído com sucesso")
    def delete(self, id):
        get_livro_or_404(id)
        del livros_by_id[id]
        return "", 204


if __name__ == "__main__":
    app.run(port=5000, host="127.0.0.1", debug=True)
