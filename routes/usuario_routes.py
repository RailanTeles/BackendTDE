from flask import Flask, jsonify, request, Blueprint
from controller.usuario_controller import UsuarioController
from security.notations import token_required

usuario_routes = Blueprint('usuario_routes', __name__)

usuarioController = UsuarioController()

# Rota para Login
@usuario_routes.route("/api/v1/usuarios/login", methods=['POST'])
def login():
    """Endpoint que recebe o e-mail e a senha, e retorna o token"""
    try:
        data = request.get_json()
        return usuarioController.login(data)

    except Exception as e:
        return {
            "msg": f"{str(e)}"
        }, 500
