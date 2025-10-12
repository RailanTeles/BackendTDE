from utils.comandos_sql import Comandos
from models.responsavel import Responsavel

class ResponsavelDao(Comandos):
    def obterResponsavelId(self, idPaciente):
        """Obter responsável do paciente com base no id do Paciente"""
        self.conectar()
        responsavel = self.obterRegistro("SELECT * FROM Responsaveis WHERE idPaciente=?", (idPaciente, ))
        self.desconectar()
        return responsavel
    
    def adicionarResponsavel(self, responsavel: Responsavel):
        self.conectar()
        self.obterRegistro("INSERT INTO Responsaveis (cpf, nome, email, telefone, dataNascimento, idPaciente) VALUES (?, ?, ?, ?, ?, ?)", (responsavel.cpf, responsavel.nome, responsavel.email, responsavel.telefone, responsavel.dataNascimento, responsavel.idPaciente))
        self.comitar()
        self.desconectar()
        return {
            "msg": "Responsável adicionado com sucesso"
        }