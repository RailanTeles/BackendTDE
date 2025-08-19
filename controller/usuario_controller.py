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

        usuario = self.usuarioDao.obterUsuarioEmail(email)

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
    
    def obterUsuario(self, email: str, token: str):
        idEsseUsuario = decode_token(token)

        esseUsuario = self.usuarioDao.obterUsuarioId(idEsseUsuario)

        usuario = self.usuarioDao.obterUsuarioEmail(email)

        if not usuario:
            return {
                "msg": "Usuário não encontrado"
            }, 404

        if esseUsuario.get('id') != usuario.get('id') and esseUsuario.get('tipo') != 'admin':
            return {
                "msg": "Acesso negado"
            }, 403

        return {
            "usuario" : usuario
        }, 200

    def obterUsuarios(self, token: str, itensPorPagina: int, pagina: int):
        idUsuario = decode_token(token)

        usuario = self.usuarioDao.obterUsuarioId(idUsuario)

        if usuario.get('tipo') != 'admin':
            return {
                "msg": "Acesso negado"
            }, 403
        
        response = self.usuarioDao.obterListaUsuarios(itensPorPagina, pagina)

        if not response:
            return{
                "msg" : "Index indiponível"
            }, 404
        
        return response, 200

    def editarMe(self, token: str, data):
        idUsuario = decode_token(token)

        email = data.get('email')
        nome = data.get('nome')

        if not email or not nome:
            return {
                "msg" : "Os novos nome e email devem ser informados"
            }, 400

        usuario = self.usuarioDao.obterUsuarioEmail(email)

        if usuario.get('id') != idUsuario:
            return {
                "msg" : "Email já cadastrado"
            }, 409

        novasInfos = Usuario(idUsuario, email, nome, "", "")

        response = self.usuarioDao.editarUsuario(novasInfos)

        return response, 200