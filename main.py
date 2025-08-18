from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

# Mostrar a lista de rotas
print("Lista de Rotas:")
for rule in app.url_map.iter_rules():
    print(rule)

app.run(port=5000, host="localhost")