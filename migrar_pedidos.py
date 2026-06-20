from database import conectar_banco

conexao = conectar_banco()

conexao.execute("""
CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    total REAL NOT NULL,
    status TEXT NOT NULL DEFAULT 'Pendente',
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
)
""")

conexao.execute("""
CREATE TABLE IF NOT EXISTS pedido_itens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    preco_unitario REAL NOT NULL,
    subtotal REAL NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
)
""")

conexao.commit()
conexao.close()

print("Tabelas de pedidos criadas com sucesso.")