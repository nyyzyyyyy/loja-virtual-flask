from database import conectar_banco

conexao = conectar_banco()

conexao.execute("""
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE
)
""")

categorias_iniciais = ["Roupas", "Calcados", "Acessorios", "Casa"]

for categoria in categorias_iniciais:
    try:
        conexao.execute(
            "INSERT INTO categorias (nome) VALUES (?)",
            (categoria,)
        )
    except Exception:
        pass

conexao.commit()
conexao.close()

print("Tabela de categorias criada com sucesso.")