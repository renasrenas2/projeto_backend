from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def conectar_banco():
    conexao = sqlite3.connect("biblioteca2_0.db")
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao

def criar_tabelas():
    conexao = conectar_banco()

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS autores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL, 
        nacionalidade TEXT NOT NULL
        )
    """)

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS autores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        ano TEXT NOT NULL,
        autorid INTEGER NOT NULL,
        FOREIGN KEY (autorid)
            REFERENCES autores(id)
        )
    """)

    conexao.commit()
    conexao.close()

@app.route("/", methods={"GET"})
def inicio():

    return jsonify({
        "Informações": "API Geral de Livros",
        "Versao": "2.0"
    })


@app.route("/autores", methods=["POST"])
def cadastrar_autor():

    dados = request.get_json()
    nome = dados["nome"]
    nacionalidade = dados["nacionalidade"]

    conexao = conectar_banco()

    cursor = conexao.execute("""
        INSERT INTO autores 
        (nome, nacionalidade)
        VALUES (?, ?)
    """, 
        (nome, nacionalidade)
    )

    conexao.commit()
    idautor = cursor.lastrowid
    conexao.close()
    
    return jsonify({
        "Aviso": "Autor cadastrado com sucesso!!!",

        "Autor":{
            "id": idautor,
            "nome": nome,
            "nacionalidade": nacionalidade
        }
    }), 201
if __name__ == "__main__":
    
    criar_tabelas()

    app.run(debug=True)