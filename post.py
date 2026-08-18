from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/produto", methods=["POST"])
def produto():

    id = request.get_json()

    return jsonify({
        "Produto": "Produto cadastro",
        "id": id
    })

if __name__ == "__main__":
    app.run(debug=True)
