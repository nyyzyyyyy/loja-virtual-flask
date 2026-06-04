from database import conectar_banco

conexao = conectar_banco()

imagens = [
    ("camiseta.jpg", 1),
    ("tenis.jpg", 2),
    ("mochila.jpg", 3),
    ("relogio.jpg", 4),
]

for imagem, produto_id in imagens:
    conexao.execute(
        "UPDATE produtos SET imagem = ? WHERE id = ?",
        (imagem, produto_id)
    )

conexao.commit()
conexao.close()

print("Imagens atualizadas com sucesso.")