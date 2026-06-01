from database import conectar_banco

conexao = conectar_banco()

conexao.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    categoria TEXT NOT NULL,
    preco REAL NOT NULL,
    descricao TEXT NOT NULL,
    estoque INTEGER NOT NULL
)
""")

conexao.execute("""
INSERT INTO produtos (nome, categoria, preco, descricao, estoque)
VALUES
('Camiseta Basica', 'Roupas', 59.90, 'Camiseta confortavel para o dia a dia.', 20),
('Tenis Esportivo', 'Calcados', 199.90, 'Tenis ideal para caminhadas e atividades fisicas.', 12),
('Mochila Urbana', 'Acessorios', 129.90, 'Mochila resistente para trabalho, estudo e viagens curtas.', 8),
('Relogio Digital', 'Acessorios', 89.90, 'Relogio digital resistente e moderno.', 15)
""")

conexao.commit()
conexao.close()

print("Banco de dados criado com sucesso.")