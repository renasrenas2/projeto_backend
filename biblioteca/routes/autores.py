from flask import Blueprint, jsonify, request
from database import conectar_banco

autores_bp = Blueprint("autores", __name__)

@autores_bp.route("/autores", methods=["GET"]) # listar autores
def listarautores():
    
    conexao = conectar_banco()

    autores = conexao.execute(
        """
        SELECT *
        FROM autores 
        ORDER BY id 
        """
    ).fetchall() # busca todos os itens do cadastro
    
    conexao.close()
    
    resultado = []

    for autor in autores:
        resultado.append({
            "id": autor["id"],
            "nome": autor["nome"],
            "nacionalidade": autor["nacionalidade"]
        })
    
    return jsonify(resultado)