from utils.comandos_sql import Comandos
from models.paciente import Paciente
from models.endereco import Endereco
from models.responsavel import Responsavel

class EnderecoDao(Comandos):
    def obterEnderecoId(self, idPaciente: int):
        self.conectar()
        enderecoPaciente = self.obterRegistro("SELECT * FROM Enderecos WHERE idPaciente=?", (idPaciente, ))
        self.desconectar()
        return enderecoPaciente
    
    def adicionarEndereco(self, endereco: Endereco):
        self.conectar()
        self.obterRegistro("INSERT INTO Enderecos (estado, cidade, bairro, cep, rua, numeroCasa, idPaciente) VALUES (?, ?, ?, ?, ?, ?, ?)", (endereco.estado, endereco.cidade, endereco.bairro, endereco.cep, endereco.rua, endereco.numeroCasa, endereco.idPaciente))
        self.comitar()
        self.desconectar()
        return {
            "msg": "Endereço adicionado com sucesso"
        }