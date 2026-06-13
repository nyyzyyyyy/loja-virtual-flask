from database import conectar_banco

email = input("Digite o e-mail do usuario que sera admin: ")

conexao = conectar_banco()

conexao.execute(
    "UPDATE usuarios SET tipo = 'admin' WHERE email = ?",
    (email,)
)

conexao.commit()
conexao.close()

print("Usuario atualizado para admin.")