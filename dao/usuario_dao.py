import math
from utils.comandos_sql import Comandos

class daoUsuario(Comandos):
    def obterUsuarioId(self, id: int):
        """Obter usuários com base no id"""
        self.conectar()
        usuarios = self.obterRegistros("SELECT * FROM usuarios WHERE id=?", (id, ))
        self.desconectar()
        return {
            "usuarios": usuarios
        }
    
    def obterUsuarios(self, qtdUsuariosPorPagina: int, paginaAtual: int):
        """Obter todos os usuários paginação"""
        self.conectar()
        desvio = qtdUsuariosPorPagina * (paginaAtual - 1)
        usuarios = self.obterRegistros("SELECT * FROM usuarios ORDER BY id DESC LIMIT ? OFFSET ?", (qtdUsuariosPorPagina, desvio))
        usuariosTotais = self.obterRegistro("SELECT COUNT(id) FROM usuarios")
        totalPaginas = math.ceil(usuariosTotais / qtdUsuariosPorPagina) if usuariosTotais else 1
        self.desconectar()
        return {
            "paginaAtual": paginaAtual,
            "totalPaginas": totalPaginas,
            "qtdUsuariosPorPagina" : qtdUsuariosPorPagina,
            "usuariosTotais" : usuariosTotais,
            "usuarios" : usuarios
        }

