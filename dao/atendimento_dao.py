from utils.comandos_sql import Comandos

class AtendimentoDao(Comandos):
    def obterQtdAtendimentosUsuario(self, id: int):
        """Verifica se um usuário tem atendimentos pelo id. Retorna a quantidade de atendimentos."""
        self.conectar()
        atends = self.obterRegistro("SELECT COUNT(idUsuario) as total FROM atendimentos WHERE idUsuario=?", (id,))
        self.desconectar()
        return atends.get('total')
