from flask import Flask, render_template, request
from database import conectar_banco

app = Flask(__name__)

def listar_produtos():
    conexao = conectar_banco()
    produtos = conexao.execute("SELECT * FROM produtos").fetchall()
    conexao.close()
    return produtos


def buscar_produto_por_id(produto_id):
    conexao = conectar_banco()
    produto = conexao.execute(
        "SELECT * FROM produtos WHERE id = ?",
        (produto_id,)
    ).fetchone()
    conexao.close()
    return produto

@app.route("/")
def home():
    produtos = listar_produtos()
    return render_template("index.html", produtos=produtos)
@app.route("/produtos")
def catalogo():
    busca = request.args.get("busca", "").lower()
    categoria = request.args.get("categoria", "")
    preco_maximo = request.args.get("preco_maximo", "")

    produtos_filtrados = listar_produtos()

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

    todos_produtos = listar_produtos()
    categorias = sorted(set(produto["categoria"] for produto in todos_produtos))

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
    produto = buscar_produto_por_id(produto_id)

    if produto is None:
        return "Produto nao encontrado", 404

    return render_template("produto_detalhe.html", produto=produto)

@app.route("/admin/produtos")
def admin_produtos():
    produtos = listar_produtos()
    return render_template("admin_produtos.html", produtos=produtos)

if __name__ == "__main__":
    print("Iniciando o servidor Flask...")
    app.run(debug=True)