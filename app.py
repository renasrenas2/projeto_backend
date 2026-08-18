from flask import Flask,jsonify

app = Flask(__name__)

@app.route("/")
def start():
    return "Primeiro Projeto"

@app.route("/curso")
def curso():
    return jsonify({
        "curso": "Engenharia de Software"
    })

@app.route("/aluno")
def aluno():
    return jsonify({
        "aluno": "Renato"
    })

@app.route("/aluno/<nome>")
def alunoX(nome):
    return jsonify ({
        "nome": nome,
        "curso": "Engenharia de Software",
        "Numero": "1"
    })

if __name__ == "__main__":
    app.run(debug=True)