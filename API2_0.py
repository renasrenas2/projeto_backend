from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# API geral de livros, versão 2.0
def conectar_banco():
    conexao = sqlite3.connect("biblioteca2_0.db")
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao

def criar_tabelas():
    conexao = conectar_banco()
    
    # Criação da tabela de autores
    conexao.execute("""
        CREATE TABLE IF NOT EXISTS autores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL, 
        nacionalidade TEXT NOT NULL
    )
    """)
    
    # CORREÇÃO: Alterado o nome da tabela de 'autores' para 'livros'
    conexao.execute("""
        CREATE TABLE IF NOT EXISTS livros (
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

@app.route("/", methods=["GET"]) # CORREÇÃO: Ajustado de {"GET"} para ["GET"]
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
    INSERT INTO autores (nome, nacionalidade)
    VALUES (?, ?)
    """, 
    (nome, nacionalidade)
    )
    
    conexao.commit()
    idautor = cursor.lastrowid
    conexao.close()
    
    # CORREÇÃO: Ajustada a indentação do retorno que estava desalinhada
    return jsonify({
        "Aviso": "Autor cadastrado com sucesso!!!",
        "Autor": {
            "id": idautor,
            "nome": nome,
            "nacionalidade": nacionalidade
        }
    }), 201

@app.route("/autores", methods=["GET"]) # listar autores
def listarautores():
    
    conexao = conectar_banco()

    autores = conexao.execute(
        """
        SELECT * FROM autores 
        ORDER BY id 
        """
    ).fetchall() # busca todos os itens do cadastro
    
    conexao.close()
    
    return jsonify([
        dict(autor)
        for autor in autores
    ])



@app.route("/autores/<int:id>", methods=["GET"]) # listar autor por id
def buscarautor(id):
    
    conexao = conectar_banco()

    autor = conexao.execute(
        """
        SELECT * FROM autores 
        WHERE id = ? 
        """, (id,)
    ).fetchone() # um dado só
    
    conexao.close()

    if autor is None:
        return jsonify({
            "Aviso": "Autor não encontrado!!!"
        })
    
    return jsonify(dict(autor))



@app.route("/autores/<int:id>", methods=["PUT"]) # alterar autor
def atualizarautor(id):

    dados = request.get_json()

    nome = dados["nome"]
    nacionalidade = dados["nacionalidade"]

    conexao = conectar_banco()

    resultado = conexao.execute(
        """
        UPDATE autores
        SET nome = ?,
        nacionalidade = ?
        WHERE id = ?
        """, (nome, nacionalidade, id,)
    )

    conexao.commit()
    conexao.close()

    if resultado.rowcount == 0:
        return jsonify({
            "Aviso": "Autor não encontrado!!!"
        }), 404
    
    return jsonify({
        "Aviso": "Autor atualizado com sucesso!!!"
    })

@app.route("/autores/<int:id>", methods=["DELETE"]) # excluir autor
def excluirautor(id):

    conexao = conectar_banco()

    resultado = conexao.execute(
        """
        DELETE FROM autores
        WHERE id = ?
        """, (id,)
    )

    conexao.commit()
    conexao.close()

    if resultado.rowcount == 0:
        return jsonify({
            "Aviso": "Autor não encontrado!!!"
        }), 404
    
    return jsonify({
        "Aviso": "Autor excluído com sucesso!!!"
    })

# Livros

@app.route("/livros", methods=["POST"])
def cadastrar_livro():
    dados = request.get_json()
    titulo = dados["titulo"]
    ano = dados["ano"]
    autorid = dados["autorid"]
    
    conexao = conectar_banco()
    
    autor = conexao.execute(
        """
        SELECT id FROM autores
        WHERE id = ?
        """, (autorid,)
    ).fetchone()
    
    if autor is None:
        conexao.close()
        return jsonify({
            "Aviso": "Autor não encontrado!!!"
        }), 404

    cursor = conexao.execute(
        """
        INSERT INTO livros
        (titulo, ano, autorid)
        VALUES (?, ?, ?)
        """, (titulo, ano, autorid)
    )

    conexao.commit()
    idlivro = cursor.lastrowid
    conexao.close()
    
    return jsonify({
        "Aviso": "Livro cadastrado com sucesso!!!",
        "Livro": {
            "id": idlivro,
            "titulo": titulo,
            "ano": ano,
            "autorId": autorid
        }
    }), 201


@app.route("/livros", methods=["GET"]) # listar livros
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
    
    return jsonify([
        dict(livro)
        for livro in livros
    ])


@app.route("/livros/<int:id>", methods=["GET"]) # listar livro por id
def buscarlivro(id):
    
    conexao = conectar_banco()

    livro = conexao.execute(
        """
        SELECT livros.id, livros.titulo, livros.ano, livros.autorid, autores.nome AS autor,
        autores.nacionalidade
        FROM livros
        JOIN autores
        ON livros.autorid = autores.id
        WHERE livros.id = ? 
        """, (id,)
    ).fetchone() # um dado só
    
    conexao.close()

    if livro is None:
        return jsonify({
            "Aviso": "Livro não encontrado!!!"
        }), 404
    
    return jsonify(dict(livro)) # função do dicionário é buscar os elementos da tabela como um todo


# fazer tudo para a tabela livros também

if __name__ == "__main__":
    criar_tabelas()
    app.run(debug=True)