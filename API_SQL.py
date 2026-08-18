from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def conectar_banco():
    conexao = sqlite3.connect("biblioteca.db")
    conexao.row_factory = sqlite3.Row
    return conexao

def criar_tabela():
    conexao = conectar_banco()

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS livros(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL
        )   
    """)

    conexao.commit()
    conexao.close()

@app.route("/", methods=["GET"])
def inicio():

    return jsonify({
        "Informações": "API Geral de Livros",
        "Versao": "1.0"
    })

@app.route("/livros", methods=["POST"])
def cadastrar_livro():
    
    dados = request.get_json()

    titulo = dados["titulo"]
    autor = dados["autor"]

    conexao = conectar_banco()

    cursor = conexao.execute(
        """
        INSERT INTO livros (titulo, autor)
        VALUES(?, ?)
        """,
        (titulo, autor)
    )

    conexao.commit()

    id_livro = cursor.lastrowid

    conexao.close()

    return jsonify({
        "Aviso": "Livro cadastrado com sucesso!!!",
        "id": id_livro,
        "titulo": titulo,
        "autor": autor
    }), 200

@app.route("/livros", methods=["GET"])
def listar_livros():
    conexao = conectar_banco()

    livros = conexao.execute(
        "SELECT * FROM livros"
    ).fetchall()

    conexao.close()
    
    return jsonify([
        dict(livro)
        for livro in livros
    ])

@app.route("/livros/<int:id>", methods={"GET"})
def buscar_livro(id):

    conexao = conectar_banco()

    livro = conexao.execute(
        "SELECT * FROM livros WHERE id = ?",
        (id,)
    ).fetchone()

    conexao.close()

    if livro is None:

        return jsonify({
            "Aviso": "Livro não encontrado!!!"
        }), 404
    
    return jsonify(dict(livro))

if __name__ == "__main__":

    criar_tabela()
    
    app.run(debug=True)