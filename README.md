# Suiyuu - Loja Virtual

Sistema de loja virtual desenvolvido com Python, Flask, HTML5, CSS3 e SQLite.

## Funcionalidades

- Página inicial com produtos em destaque
- Catálogo de produtos
- Busca por produtos
- Filtro por categoria
- Filtro por faixa de preço
- Página individual de produto
- Carrinho de compras
- Cadastro de usuários
- Login e logout
- Área do cliente
- Histórico de pedidos
- Painel administrativo protegido
- Cadastro, edição e exclusão de produtos
- Gerenciamento de categorias
- Controle de estoque
- Visualização e atualização de pedidos

## Tecnologias Utilizadas

- Python
- Flask
- HTML5
- CSS3
- SQLite
- Git
- GitHub

## Como Executar O Projeto

### 1. Clonar o repositório

```powershell
git clone https://github.com/nyyzyyyyy/loja-virtual-flask.git

Entre na pasta: cd loja-virtual-flask
Criar Ambiente Virtual: python -m venv venv
Ativar ambiente virtual: venv\Scripts\activate
Instalar dependencias: pip install -r requirements.txt
Criar Banco de dados:
python init_db.py
python migrar_imagens.py
python atualizar_imagens.py
python migrar_categorias.py
python migrar_usuarios.py
python migrar_pedidos.py

Rodar o projeto python app.py
Acessar: http://127.0.0.1:5000

Usuário Administrador
Para transformar um usuário cadastrado em administrador, execute:
python criar_admin.py
Digite o e-mail do usuário cadastrado.

