from flask import Flask, render_template, request

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
@app.route("/produtos")
def catalogo():
    busca = request.args.get("busca", "").lower()
    categoria = request.args.get("categoria", "")
    preco_maximo = request.args.get("preco_maximo", "")

    produtos_filtrados = produtos

    if busca:
        produtos_filtrados = [
            produto for produto in produtos_filtrados
            if busca in produto["nome"].lower()
        ]

    if categoria:
        produtos_filtrados = [
            produto for produto in produtos_filtrados
            if produto["categoria"] == categoria
        ]

    if preco_maximo:
        produtos_filtrados = [
            produto for produto in produtos_filtrados
            if produto["preco"] <= float(preco_maximo)
        ]

    categorias = sorted(set(produto["categoria"] for produto in produtos))

    return render_template(
        "catalogo.html",
        produtos=produtos_filtrados,
        categorias=categorias,
        busca=busca,
        categoria_selecionada=categoria,
        preco_maximo=preco_maximo,
    )
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