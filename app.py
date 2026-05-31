from flask import Flask, render_template

app = Flask(__name__)

produtos = [
    {
        "id": 1,
        "nome": "Camiseta Basica",
        "categoria": "Roupas",
        "preco": 59.90,
        "descricao": "Camiseta confortavel para o dia a dia.",
        "estoque": 20,
    },
    {
        "id": 2,
        "nome": "Tenis Esportivo",
        "categoria": "Calcados",
        "preco": 199.90,
        "descricao": "Tenis ideal para caminhadas e atividades fisicas.",
        "estoque": 12,
    },
    {
        "id": 3,
        "nome": "Mochila Urbana",
        "categoria": "Acessorios",
        "preco": 129.90,
        "descricao": "Mochila resistente para trabalho, estudo e viagens curtas.",
        "estoque": 8,
    },
    {
    "id": 4,
    "nome": "Relogio Digital",
    "categoria": "Acessorios",
    "preco": 89.90,
    "descricao": "Relogio digital resistente e moderno.",
    "estoque": 15,
},
]

@app.route("/")
def home():
    return render_template("index.html", produtos=produtos)

@app.route("/produto/<int:produto_id>")
def produto_detalhe(produto_id):
    produto_encontrado = None

    for produto in produtos:
        if produto["id"] == produto_id:
            produto_encontrado = produto
            break

    if produto_encontrado is None:
        return "Produto nao encontrado", 404

    return render_template("produto_detalhe.html", produto=produto_encontrado)

if __name__ == "__main__":
    print("Iniciando o servidor Flask...")
    app.run(debug=True)