import math
from utils.comandos_sql import Comandos
from models.paciente import Paciente
from models.endereco import Endereco
from models.responsavel import Responsavel

class PacienteDao(Comandos):
    def obterPacientePorId(self, id: int):
        """Obter paciente com base no id"""
        self.conectar()
        paciente = self.obterRegistro("SELECT * FROM Pacientes WHERE id=?", (id, ))
        self.desconectar()
        return paciente
    
    def obterPacientePorCpf(self, cpf: str):
        """Obter paciente com base no cpf"""
        self.conectar()
        paciente = self.obterRegistro("SELECT * FROM Pacientes WHERE cpf=?", (cpf, ))
        self.desconectar()
        return paciente
    
    def obterPacientePorEmail(self, email: str):
        """Obter paciente com base no email"""
        self.conectar()
        paciente = self.obterRegistro("SELECT * FROM Pacientes WHERE email=?", (email, ))
        self.desconectar()
        return paciente
    
    def obterPacientes(self, itensPorPagina: int, pagina: int):
        """Obter todos os usuários paginação"""
        self.conectar()
        desvio = itensPorPagina * (pagina - 1)
        pacientes = self.obterRegistros("SELECT * FROM Pacientes ORDER BY id DESC LIMIT ? OFFSET ?", (itensPorPagina, desvio))
        pacientesTotais = self.obterRegistro("SELECT COUNT(id) as total FROM Pacientes")
        pacientesTotais = pacientesTotais.get('total')
        totalPaginas = math.ceil(pacientesTotais / itensPorPagina) if pacientesTotais else 1
        self.desconectar()

        if pagina > totalPaginas:
            return None

        return {
            "pagina": pagina,
            "totalPaginas": totalPaginas,
            "itensPorPagina" : itensPorPagina,
            "pacientesTotais" : pacientesTotais,
            "pacientes" : pacientes
        }
    
    def adicionarPaciente(self, paciente: Paciente):
        self.conectar()
        self.obterRegistro("INSERT INTO Pacientes (cpf, nome, email, telefone, dataNascimento) VALUES (?, ?, ?, ?, ?)", (paciente.cpf, paciente.nome, paciente.email, paciente.telefone, paciente.dataNascimento))
        self.comitar()
        self.desconectar()
        return {
            "msg": "Usuário adicionado com sucesso"
        }

    def alterarPaciente(self, paciente: Paciente):
        self.conectar()
        self.obterRegistro("UPDATE Pacientes SET cpf=?, nome=?, email=?, telefone=?, dataNascimento=? WHERE id=?", (paciente.cpf, paciente.nome, paciente.email, paciente.telefone, paciente.dataNascimento, paciente.id))
        self.comitar()
        self.desconectar()
        return {
            "msg": "Usuário alterado com sucesso"
        }
    
