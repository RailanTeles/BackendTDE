from functools import wraps
from flask import request, jsonify
from utils.jwt_util import decode_token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        # Verifica se há token
        if not token:
            return {"msg": "Não autorizado"}, 401
        
        # Verifica se o formato é válido
        if not token.startswith('Bearer '):
            return {"msg": "Formato de token inválido"}, 401

        id = decode_token(token)
        if not id:
            return {"msg": "Usuário não encontrado"}, 401
        
        # Verifica se o usuário existe
        # user = 
        # if not user:
        #     return {"msg": "Usuário não encontrado"}, 404

        return decorated