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

@usuario_routes.route("/api/v1/usuarios/<email>", methods=["GET"])
@token_required
def obterUsuario(email):
    """Endpoint que recebe o e-mail por meio da url, e só retorna os dados se ou é o próprio usuário ou é admin"""
    try:
        token = request.headers.get('Authorization')
        return usuarioController.obterUsuario(email, token)
    
    except Exception as e:
        return {
            "msg": f"{str(e)}"
        }, 500

@usuario_routes.route("/api/v1/usuarios", methods=["GET"])
@token_required
def obterUsuarios():
    """Endpoint que retorna os usuários de forma paginada, por meio dos queryparams: pagina e itensPorPagina"""
    try:
        token = request.headers.get('Authorization')
        pagina = request.args.get('pagina', default=1, type=int)
        itensPorPagina = request.args.get('itensPorPagina', default=2, type=int)

        return usuarioController.obterUsuarios(token, itensPorPagina, pagina)
    
    except Exception as e:
        return {
            "msg": f"{str(e)}"
        }, 500

@usuario_routes.route("/api/v1/usuarios/adicionar", methods=['POST'])
@token_required
def adicionarUsuario():
    """Endpoint que adiciona um usuário"""
    try:
        token = request.headers.get('Authorization')
        data = request.get_json()

        return usuarioController.adicionarUsuario(token, data)
    
    except Exception as e:
        return {
            "msg": f"{str(e)}"
        }, 500

@usuario_routes.route("/api/v1/usuarios/editar", methods=['PUT'])
@token_required
def editarMe():
    """Endpoint que o usuário edita suas próprias informações"""
    try:
        token = request.headers.get('Authorization')
        data = request.get_json()
        return usuarioController.editarMe(token, data)

    except Exception as e:
        return {
            "msg": f"{str(e)}"
        }, 500
    
@usuario_routes.route("/api/v1/usuarios/alterarSenha", methods=['PUT'])
@token_required
def alterarSenha():
    """Usuário alterando a própria senha, informando a antiga e a nova"""
    try: 
        token = request.headers.get('Authorization')
        data = request.get_json()
        return usuarioController.alterarSenha(token, data)
    
    except Exception as e:
        return {
            "msg": f"{str(e)}"
        }, 500
    
@usuario_routes.route("/api/v1/usuarios/resetarSenha", methods=['PUT'])
@token_required
def resetarSenha():
    """Usuário admin resetando a senha"""
    try:
        token = request.headers.get('Authorization')
        data = request.get_json()
        return usuarioController.resetarSenha(token, data)
    
    except Exception as e:
        return {
            "msg": f"{str(e)}"
        }, 500