from flask import Blueprint, jsonify, request
from database import conectar_banco

livros_bp = Blueprint("livros", __name__)

@livros_bp.route("/livros", methods=["GET"]) # listar livros
def listar_livros():
    
    conexao = conectar_banco()

    livros = conexao.execute(
        """
        SELECT livros.id, livros.titulo, livros.ano, livros.autorid, autores.nome AS autor,
        autores.nacionalidade
        FROM livros
        JOIN autores
        ON livros.autorid = autores.id
        ORDER BY livros.id
        """
    ).fetchall() # busca todos os itens do cadastro
    
    conexao.close()
    
    resultado = []

    for livro in livros:
        resultado.append({
            "id": livro["id"],
            "titulo": livro["titulo"],
            "ano": livro["ano"]
        })
    
    return jsonify(resultado)