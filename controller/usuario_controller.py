from flask import request
from utils.jwt_util import generate_token, decode_token
from dao.usuario_dao import UsuarioDao
from models.usuario import Usuario

class UsuarioController:
    def __init__(self):
        self.usuarioDao = UsuarioDao()
    
    def login(self, data):
        email = data.get('email')
        senha = data.get('senha')

        resultado = self.usuarioDao.obterUsuarioEmail(email)
        usuario = resultado.get('usuario')

        if not usuario:
            return {
                "msg": "E-mail ou senha incorretas"
            }, 404
        
        if senha != usuario.get('senha'):
            return {
                "msg": "E-mail ou senha incorretas"
            }, 404
        
        token = generate_token(usuario.get('id'))

        return {
            "token": token,
            "msg": "Logado com sucesso"
        }, 200
        