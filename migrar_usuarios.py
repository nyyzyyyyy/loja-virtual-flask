from database import conectar_banco

conexao = conectar_banco()

conexao.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    tipo TEXT NOT NULL DEFAULT 'cliente'
)
""")

conexao.commit()
conexao.close()

print("Tabela de usuarios criada com sucesso.")