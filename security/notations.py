from functools import wraps
from flask import request, jsonify, g
from utils.jwt_util import decode_token
from dao.usuario_dao import UsuarioDao

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        usuarioDao = UsuarioDao()
        token = request.headers.get('Authorization')

        # Verifica se há token
        if not token:
            return jsonify({"msg": "Não autorizado"}), 401

        # Verifica se o formato é válido
        if not token.startswith('Bearer '):
            return jsonify({"msg": "Formato de token inválido"}), 401

        user_id = decode_token(token)
        if not user_id:
            return jsonify({"msg": "Token inválido"}), 401

        # Verifica se o usuário existe
        user = usuarioDao.obterUsuarioId(user_id)
        if not user:
            return jsonify({"msg": "Token inválido"}), 404

        # SALVA O USER_ID NO CONTEXTO GLOBAL
        g.user_id = user_id
        print(f"✅ User ID autenticado: {user_id}")

        return f(*args, **kwargs)

    return decorated