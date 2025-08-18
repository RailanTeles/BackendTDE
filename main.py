from flask import Flask, request
from flask_cors import CORS
from routes.usuario_routes import usuario_routes

app = Flask(__name__)

CORS(app)

app.register_blueprint(usuario_routes)

# Mostrar a lista de rotas
print("Lista de Rotas:")
for rule in app.url_map.iter_rules():
    print(rule)

app.run(host="0.0.0.0", port=5000)