from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Minha loja virtual está funcionando!"

if __name__ == "__main__":
    print("Iniciando o servidor Flask...")
    app.run(debug=True)