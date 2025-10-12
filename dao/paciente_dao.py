from utils.comandos_sql import Comandos
from models.paciente import Paciente
from models.endereco import Endereco
from models.reponsavel import Reponsavel

class PacienteDao(Comandos):
    def obterPacientePorId(self, id: int):
        """Obter paciente com base no id"""
        self.conectar()
        paciente = self.obterRegistro("SELECT * FROM Pacientes WHERE id=?", (id, ))
        self.desconectar()
        return paciente
    
