from utils.comandos_sql import Comandos
from models.reponsavel import Reponsavel

class ResponsavelDao(Comandos):
    def obterReponsavelId(self, idPaciente):
        """Obter responsável do paciente com base no id do Paciente"""
        self.conectar()
        responsavel = self.obterRegistro("SELECT * FROM Responsaveis WHERE id=?", (idPaciente, ))
        self.desconectar()
        return responsavel