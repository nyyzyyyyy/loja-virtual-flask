from flask import Flask, render_template, request, redirect, url_for, session
from database import conectar_banco
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "chave-secreta-suiyuu"

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


def cadastrar_produto(nome, categoria, preco, descricao, estoque, imagem):
    conexao = conectar_banco()
    conexao.execute(
        """
        INSERT INTO produtos (nome, categoria, preco, descricao, estoque, imagem)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (nome, categoria, preco, descricao, estoque, imagem)
    )
    conexao.commit()
    conexao.close()


@app.context_processor
def dados_globais():
    try:
        categorias = listar_categorias()
    except Exception:
        categorias = []
    return {"categorias_menu": categorias}

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


@app.route("/admin/produtos/novo", methods=["GET", "POST"])
def admin_novo_produto():
    if request.method == "POST":
        nome = request.form["nome"]
        categoria = request.form["categoria"]
        preco = float(request.form["preco"])
        descricao = request.form["descricao"]
        estoque = int(request.form["estoque"])
        imagem = request.form["imagem"]

        cadastrar_produto(nome, categoria, preco, descricao, estoque, imagem)

        return redirect(url_for("admin_produtos"))

    return render_template("admin_novo_produto.html")

@app.route("/admin/produtos/<int:produto_id>/editar", methods=["GET", "POST"])
def admin_editar_produto(produto_id):
    produto = buscar_produto_por_id(produto_id)

    if produto is None:
        return "Produto nao encontrado", 404

    if request.method == "POST":
        nome = request.form["nome"]
        categoria = request.form["categoria"]
        preco = float(request.form["preco"])
        descricao = request.form["descricao"]
        estoque = int(request.form["estoque"])
        imagem = request.form["imagem"]

        atualizar_produto(produto_id, nome, categoria, preco, descricao, estoque, imagem)

        return redirect(url_for("admin_produtos"))

    return render_template("admin_editar_produto.html", produto=produto)

def atualizar_produto(produto_id, nome, categoria, preco, descricao, estoque, imagem):
    conexao = conectar_banco()
    conexao.execute(
        """
        UPDATE produtos
        SET nome = ?, categoria = ?, preco = ?, descricao = ?, estoque = ?, imagem = ?
        WHERE id = ?
        """,
        (nome, categoria, preco, descricao, estoque, imagem, produto_id)
    )
    conexao.commit()
    conexao.close()


def excluir_produto(produto_id):
    conexao = conectar_banco()
    conexao.execute(
        "DELETE FROM produtos WHERE id = ?",
        (produto_id,)
    )
    conexao.commit()
    conexao.close()

def listar_categorias():
    conexao = conectar_banco()
    categorias = conexao.execute(
        "SELECT * FROM categorias ORDER BY nome"
    ).fetchall()
    conexao.close()
    return categorias


def cadastrar_categoria(nome):
    conexao = conectar_banco()
    conexao.execute(
        "INSERT INTO categorias (nome) VALUES (?)",
        (nome,)
    )
    conexao.commit()
    conexao.close()

def buscar_categoria_por_id(categoria_id):
    conexao = conectar_banco()
    categoria = conexao.execute(
        "SELECT * FROM categorias WHERE id = ?",
        (categoria_id,)
    ).fetchone()
    conexao.close()
    return categoria


def atualizar_categoria(categoria_id, nome):
    conexao = conectar_banco()
    conexao.execute(
        "UPDATE categorias SET nome = ? WHERE id = ?",
        (nome, categoria_id)
    )
    conexao.commit()
    conexao.close()


def excluir_categoria(categoria_id):
    conexao = conectar_banco()
    conexao.execute(
        "DELETE FROM categorias WHERE id = ?",
        (categoria_id,)
    )
    conexao.commit()
    conexao.close()

def cadastrar_usuario(nome, email, senha):
    senha_hash = generate_password_hash(senha)

    conexao = conectar_banco()
    conexao.execute(
        """
        INSERT INTO usuarios (nome, email, senha)
        VALUES (?, ?, ?)
        """,
        (nome, email, senha_hash)
    )
    conexao.commit()
    conexao.close()


def buscar_usuario_por_email(email):
    conexao = conectar_banco()
    usuario = conexao.execute(
        "SELECT * FROM usuarios WHERE email = ?",
        (email,)
    ).fetchone()
    conexao.close()
    return usuario    

@app.route("/admin/produtos/<int:produto_id>/excluir", methods=["POST"])
def admin_excluir_produto(produto_id):
    excluir_produto(produto_id)
    return redirect(url_for("admin_produtos"))

@app.route("/admin/categorias", methods=["GET", "POST"])
def admin_categorias():
    if request.method == "POST":
        nome = request.form["nome"]
        cadastrar_categoria(nome)
        return redirect(url_for("admin_categorias"))

    categorias = listar_categorias()
    return render_template("admin_categorias.html", categorias=categorias)

@app.route("/admin/categorias/<int:categoria_id>/editar", methods=["GET", "POST"])
def admin_editar_categoria(categoria_id):
    categoria = buscar_categoria_por_id(categoria_id)

    if categoria is None:
        return "Categoria nao encontrada", 404

    if request.method == "POST":
        nome = request.form["nome"]
        atualizar_categoria(categoria_id, nome)
        return redirect(url_for("admin_categorias"))

    return render_template("admin_editar_categoria.html", categoria=categoria)

@app.route("/admin/categorias/<int:categoria_id>/excluir", methods=["POST"])
def admin_excluir_categoria(categoria_id):
    excluir_categoria(categoria_id)
    return redirect(url_for("admin_categorias"))

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    erro = None

    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        usuario_existente = buscar_usuario_por_email(email)

        if usuario_existente:
            erro = "Este e-mail ja esta cadastrado."
        else:
            cadastrar_usuario(nome, email, senha)
            return redirect(url_for("login"))

    return render_template("cadastro.html", erro=erro)

@app.route("/login", methods=["GET", "POST"])
def login():
    erro = None

    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        usuario = buscar_usuario_por_email(email)

        if usuario and check_password_hash(usuario["senha"], senha):
            session["usuario_id"] = usuario["id"]
            session["usuario_nome"] = usuario["nome"]
            session["usuario_tipo"] = usuario["tipo"]
            return redirect(url_for("home"))

        erro = "E-mail ou senha invalidos."

    return render_template("login.html", erro=erro)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))



if __name__ == "__main__":
    print("Iniciando o servidor Flask...")
    app.run(debug=True)