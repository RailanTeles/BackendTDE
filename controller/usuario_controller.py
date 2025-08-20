from flask import request
from utils.jwt_util import generate_token, decode_token
from dao.usuario_dao import UsuarioDao
from models.usuario import Usuario, TipoUsuario

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

        if esseUsuario.get('id') != usuario.get('id') and esseUsuario.get('tipo') != TipoUsuario.ADMIN.value:
            return {
                "msg": "Acesso negado"
            }, 403

        return {
            "usuario" : usuario
        }, 200

    def obterUsuarios(self, token: str, itensPorPagina: int, pagina: int):
        idUsuario = decode_token(token)

        usuario = self.usuarioDao.obterUsuarioId(idUsuario)

        if usuario.get('tipo') != TipoUsuario.ADMIN.value:
            return {
                "msg": "Acesso negado"
            }, 403
        
        response = self.usuarioDao.obterListaUsuarios(itensPorPagina, pagina)

        if not response:
            return{
                "msg" : "Index indiponível"
            }, 404
        
        return response, 200
    
    def adicionarUsuario(self, token: str, data):
        idUsuario = decode_token(token)
        usuario = self.usuarioDao.obterUsuarioId(idUsuario)

        if usuario.get('tipo') != TipoUsuario.ADMIN.value:
            return {
                "msg": "Acesso negado"
            }, 403
        
        email = data.get('email')
        nome = data.get('nome')
        tipo = data.get('tipo')
        senha = '123456'

        if not email or not nome or not tipo:
            return {
                "msg" : "Os campos nome, email e tipo devem ser informados"
            }, 400

        existeUsuario = self.usuarioDao.obterUsuarioEmail(email)

        if existeUsuario:
            return {
                "msg" : "Email já cadastrado"
            }, 409
        
        if tipo not in (TipoUsuario.ADMIN.value, TipoUsuario.DEFAULT.value):
            return {
                "msg" : "O usuário deve ser do tipo admin ou default"
            }, 400

        novoUsuario = Usuario(0, email, nome, tipo, senha)

        resposta = self.usuarioDao.adicionarUsuario(novoUsuario)

        return resposta, 200

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
    
    def alterarSenha(self, token: str, data):
        idUsuario = decode_token(token)

        senha = data.get('senha')
        novaSenha = data.get('novaSenha')

        if not senha or not novaSenha:
            return {
                "msg" : "A senha antiga e a nova devem ser informadas"
            }, 400
        
        usuario = self.usuarioDao.obterUsuarioId(idUsuario)

        if usuario.get('senha') != senha:
            return {
                "msg" : "Senha incorreta"
            }, 401
        
        response = self.usuarioDao.redefinirSenha(novaSenha, idUsuario)

        return response, 200