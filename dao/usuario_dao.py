import math
from utils.comandos_sql import Comandos
from models.usuario import Usuario

class UsuarioDao(Comandos):
    def obterUsuarioId(self, id: int):
        """Obter usuários com base no id"""
        self.conectar()
        usuario = self.obterRegistro("SELECT * FROM usuarios WHERE id=?", (id, ))
        self.desconectar()
        return usuario
    
    def obterUsuarioEmail(self, email: str):
        """Obter usuários com base no email"""
        self.conectar()
        usuario = self.obterRegistro("SELECT * FROM usuarios WHERE email=?", (email, ))
        self.desconectar()
        return usuario
    
    def obterListaUsuarios(self, itensPorPagina: int, pagina: int):
        """Obter todos os usuários paginação"""
        self.conectar()
        desvio = itensPorPagina * (pagina - 1)
        usuarios = self.obterRegistros("SELECT * FROM usuarios ORDER BY id DESC LIMIT ? OFFSET ?", (itensPorPagina, desvio))
        usuariosTotais = self.obterRegistro("SELECT COUNT(id) as total FROM usuarios")
        usuariosTotais = usuariosTotais.get('total')
        totalPaginas = math.ceil(usuariosTotais / itensPorPagina) if usuariosTotais else 1
        self.desconectar()

        if pagina > totalPaginas:
            return None

        return {
            "pagina": pagina,
            "totalPaginas": totalPaginas,
            "itensPorPagina" : itensPorPagina,
            "usuariosTotais" : usuariosTotais,
            "usuarios" : usuarios
        }
    
    def adicionarUsuario(self, usuario: Usuario):
        """Adicionar um usuário"""
        self.conectar()
        self.obterRegistro("INSERT INTO usuarios (nome, email, tipo, senha) VALUES (?, ?, ?, ?)", (usuario.nome, usuario.email, usuario.tipo, usuario.senha))
        self.comitar()
        self.desconectar()
        return {
            "msg": "Usuário adicionado com sucesso"
        }

    def editarUsuario(self, usuario: Usuario):
        """Editar um usuário com base no id"""
        self.conectar()
        self.obterRegistro("UPDATE usuarios SET email = ?, nome = ? WHERE id = ?", (usuario.email, usuario.nome, usuario.id))
        self.comitar()
        self.desconectar()
        return {
            "msg" : "Usuário editado com sucesso"
        }
    
    def resetarSenhaUsuario(self, usuario: Usuario):
        """Usuário admin resetar a senha para padrão com base no e-mail"""
        self.conectar()
        senhaPadrao = "123456"
        self.obterRegistro("UPDATE usuarios SET senha = ? WHERE email = ?", (senhaPadrao, usuario.email))
        self.comitar()
        self.desconectar()
        return {
            "msg" : "Senha resetada com sucesso"
        }
    
    def redefinirSenha(self, novaSenha: str, id: int):
        """Próprio usuário editando sua senha com base no id"""
        self.conectar()
        self.obterRegistro("UPDATE usuarios SET senha = ? WHERE id = ?", (novaSenha, id))
        self.comitar()
        self.desconectar()
        return {
            "msg" : "Senha alterada com sucesso"
        }
    
    def removerUsuario(self, usuario: Usuario):
        """Usuário admin removendo um usuário com base no e-mail"""
        self.conectar()
        self.obterRegistro("DELETE FROM usuarios WHERE email = ?", (usuario.email,))
        self.comitar()
        self.desconectar()
        return {
            "msg" : "Usuário deletado com sucesso"
        }