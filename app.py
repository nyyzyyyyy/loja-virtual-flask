import os

from flask import Flask, render_template, request, redirect, url_for, session
from database import conectar_banco, inicializar_banco
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "chave-secreta-suiyuu")

inicializar_banco()

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
    if not usuario_admin_logado():
        return redirect(url_for("login"))
    produtos = listar_produtos()
    return render_template("admin_produtos.html", produtos=produtos)


@app.route("/admin/produtos/novo", methods=["GET", "POST"])
def admin_novo_produto():
    if not usuario_admin_logado():
        return redirect(url_for("login"))

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
    if not usuario_admin_logado():
        return redirect(url_for("login"))

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

def obter_carrinho():
    return session.get("carrinho", {})

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

def buscar_usuario_por_id(usuario_id):
    conexao = conectar_banco()
    usuario = conexao.execute(
        "SELECT * FROM usuarios WHERE id = ?",
        (usuario_id,)
    ).fetchone()
    conexao.close()
    return usuario

def usuario_admin_logado():
    return session.get("usuario_tipo") == "admin"

def criar_pedido(usuario_id, itens, total):
    conexao = conectar_banco()

    cursor = conexao.execute(
        """
        INSERT INTO pedidos (usuario_id, total, status)
        VALUES (?, ?, ?)
        """,
        (usuario_id, total, "Pendente")
    )

    pedido_id = cursor.lastrowid

    for item in itens:
        produto = item["produto"]
        quantidade = item["quantidade"]
        subtotal = item["subtotal"]

        conexao.execute(
            """
            INSERT INTO pedido_itens (
                pedido_id, produto_id, quantidade, preco_unitario, subtotal
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                pedido_id,
                produto["id"],
                quantidade,
                produto["preco"],
                subtotal,
            )
        )

        conexao.execute(
            """
            UPDATE produtos
            SET estoque = estoque - ?
            WHERE id = ?
            """,
            (quantidade, produto["id"])
        )

    conexao.commit()
    conexao.close()

    return pedido_id

def listar_pedidos_usuario(usuario_id):
    conexao = conectar_banco()
    pedidos = conexao.execute(
        """
        SELECT * FROM pedidos
        WHERE usuario_id = ?
        ORDER BY criado_em DESC
        """,
        (usuario_id,)
    ).fetchall()
    conexao.close()
    return pedidos

def listar_todos_pedidos():
    conexao = conectar_banco()
    pedidos = conexao.execute(
        """
        SELECT pedidos.*, usuarios.nome AS usuario_nome, usuarios.email AS usuario_email
        FROM pedidos
        JOIN usuarios ON usuarios.id = pedidos.usuario_id
        ORDER BY pedidos.criado_em DESC
        """
    ).fetchall()
    conexao.close()
    return pedidos

def listar_itens_pedido(pedido_id):
    conexao = conectar_banco()
    itens = conexao.execute(
        """
        SELECT
            pedido_itens.*,
            produtos.nome AS produto_nome
        FROM pedido_itens
        JOIN produtos ON produtos.id = pedido_itens.produto_id
        WHERE pedido_itens.pedido_id = ?
        """,
        (pedido_id,)
    ).fetchall()
    conexao.close()
    return itens

def atualizar_status_pedido(pedido_id, status):
    conexao = conectar_banco()
    conexao.execute(
        "UPDATE pedidos SET status = ? WHERE id = ?",
        (status, pedido_id)
    )
    conexao.commit()
    conexao.close()

@app.route("/admin/produtos/<int:produto_id>/excluir", methods=["POST"])
def admin_excluir_produto(produto_id):
    if not usuario_admin_logado():
        return redirect(url_for("login"))
    excluir_produto(produto_id)
    return redirect(url_for("admin_produtos"))

@app.route("/admin/categorias", methods=["GET", "POST"])

def admin_categorias():
    if not usuario_admin_logado():
        return redirect(url_for("login"))

    if request.method == "POST":
        nome = request.form["nome"]
        cadastrar_categoria(nome)
        return redirect(url_for("admin_categorias"))

    categorias = listar_categorias()
    return render_template("admin_categorias.html", categorias=categorias)

@app.route("/admin/categorias/<int:categoria_id>/editar", methods=["GET", "POST"])
def admin_editar_categoria(categoria_id):
    if not usuario_admin_logado():
        return redirect(url_for("login"))

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
    if not usuario_admin_logado():
        return redirect(url_for("login"))

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

@app.route("/minha-conta")
def minha_conta():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    usuario = buscar_usuario_por_id(session["usuario_id"])
    pedidos = listar_pedidos_usuario(session["usuario_id"])

    return render_template("minha_conta.html", usuario=usuario, pedidos=pedidos)

@app.route("/carrinho/adicionar/<int:produto_id>", methods=["POST"])
def adicionar_carrinho(produto_id):
    produto = buscar_produto_por_id(produto_id)

    if produto is None:
        return "Produto nao encontrado", 404

    carrinho = obter_carrinho()
    produto_id_texto = str(produto_id)

    if produto_id_texto in carrinho:
        carrinho[produto_id_texto] += 1
    else:
        carrinho[produto_id_texto] = 1

    session["carrinho"] = carrinho

    return redirect(url_for("ver_carrinho"))

@app.route("/carrinho")
def ver_carrinho():
    itens, total = montar_itens_carrinho()
    return render_template("carrinho.html", itens=itens, total=total)

@app.route("/carrinho/atualizar/<int:produto_id>", methods=["POST"])
def atualizar_carrinho(produto_id):
    acao = request.form["acao"]
    carrinho = obter_carrinho()
    produto_id_texto = str(produto_id)

    if produto_id_texto in carrinho:
        if acao == "aumentar":
            carrinho[produto_id_texto] += 1
        elif acao == "diminuir":
            carrinho[produto_id_texto] -= 1

            if carrinho[produto_id_texto] <= 0:
                carrinho.pop(produto_id_texto)

    session["carrinho"] = carrinho

    return redirect(url_for("ver_carrinho"))

@app.route("/carrinho/remover/<int:produto_id>", methods=["POST"])
def remover_carrinho(produto_id):
    carrinho = obter_carrinho()
    produto_id_texto = str(produto_id)

    if produto_id_texto in carrinho:
        carrinho.pop(produto_id_texto)

    session["carrinho"] = carrinho

    return redirect(url_for("ver_carrinho"))

@app.route("/carrinho/limpar", methods=["POST"])
def limpar_carrinho():
    session["carrinho"] = {}
    return redirect(url_for("ver_carrinho"))

def montar_itens_carrinho():
    carrinho = obter_carrinho()
    itens = []
    total = 0

    for produto_id, quantidade in carrinho.items():
        produto = buscar_produto_por_id(int(produto_id))

        if produto:
            subtotal = produto["preco"] * quantidade
            total += subtotal

            itens.append({
                "produto": produto,
                "quantidade": quantidade,
                "subtotal": subtotal,
            })

    return itens, total

@app.route("/pedido/finalizar", methods=["POST"])
def finalizar_pedido():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    itens, total = montar_itens_carrinho()

    if not itens:
        return redirect(url_for("ver_carrinho"))

    pedido_id = criar_pedido(session["usuario_id"], itens, total)

    session["carrinho"] = {}

    return redirect(url_for("pedido_confirmado", pedido_id=pedido_id))

@app.route("/pedido/<int:pedido_id>/confirmado")
def pedido_confirmado(pedido_id):
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    return render_template("pedido_confirmado.html", pedido_id=pedido_id)

@app.route("/admin/pedidos")
def admin_pedidos():
    if not usuario_admin_logado():
        return redirect(url_for("login"))

    pedidos = listar_todos_pedidos()
    return render_template("admin_pedidos.html", pedidos=pedidos)

@app.route("/admin/pedidos/<int:pedido_id>")
def admin_pedido_detalhe(pedido_id):
    if not usuario_admin_logado():
        return redirect(url_for("login"))

    itens = listar_itens_pedido(pedido_id)

    return render_template("admin_pedido_detalhe.html", pedido_id=pedido_id, itens=itens)

@app.route("/admin/pedidos/<int:pedido_id>/status", methods=["POST"])
def admin_atualizar_status_pedido(pedido_id):
    if not usuario_admin_logado():
        return redirect(url_for("login"))

    status = request.form["status"]
    status_permitidos = ["Pendente", "Pago", "Enviado", "Entregue"]

    if status in status_permitidos:
        atualizar_status_pedido(pedido_id, status)

    return redirect(url_for("admin_pedidos"))

@app.route("/promover-admin/<email>/<chave>")
def promover_admin(email, chave):
    chave_admin = os.environ.get("ADMIN_SETUP_KEY", "")

    if not chave_admin or chave != chave_admin:
        return "Acesso negado", 403

    conexao = conectar_banco()
    conexao.execute(
        "UPDATE usuarios SET tipo = 'admin' WHERE email = ?",
        (email,)
    )
    conexao.commit()
    conexao.close()

    return "Usuario promovido para admin com sucesso."

if __name__ == "__main__":
    print("Iniciando o servidor Flask...")
    app.run(debug=True)

