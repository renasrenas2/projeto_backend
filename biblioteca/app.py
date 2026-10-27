from flask import Flask, jsonify

from routes.autores import autores_bp
from routes.livros import livros_bp

app = Flask(__name__)

app.register_blueprint(autores_bp)
app.register_blueprint(livros_bp)

@app.route("/", methods=["GET"]) 
def inicio():

    return jsonify({
        "Informações": "API de Biblioteca",
        "Versao": "3.0"
    })

if __name__ == "__main__":
    app.run(debug=True)