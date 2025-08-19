from functools import wraps
from flask import request, jsonify
from utils.jwt_util import decode_token
from dao.usuario_dao import UsuarioDao


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        usuarioDao = UsuarioDao()
        token = request.headers.get('Authorization')

        # Verifica se há token
        if not token:
            return {"msg": "Não autorizado"}, 401
        
        # Verifica se o formato é válido
        if not token.startswith('Bearer '):
            return {"msg": "Formato de token inválido"}, 401

        id = decode_token(token)
        if not id:
            return {"msg": "Token inválido"}, 401
        
        # Verifica se o usuário existe
        user = usuarioDao.obterUsuarioId(id)
        if not user:
            return {"msg": "Token inválido"}, 404
        
        return f(*args, **kwargs)

    return decorated