from utils.comandos_sql import Comandos
from models.paciente import Paciente
from models.endereco import Endereco
from models.reponsavel import Reponsavel

class EnderecoDao(Comandos):
    def obterEnderecoId(self, idPaciente: int):
        self.conectar()
        enderecoPaciente = self.obterRegistro("SELECT * FROM Enderecos WHERE idPaciente=?", (idPaciente, ))
        self.desconectar()
        return enderecoPaciente