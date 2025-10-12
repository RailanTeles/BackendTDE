from utils.jwt_util import generate_token, decode_token
from dao.paciente_dao import PacienteDao
from dao.endereco_dao import EnderecoDao
from dao.responsavel_dao import ResponsavelDao
from models.paciente import Paciente
from models.endereco import Endereco
from models.reponsavel import Reponsavel

class PacienteService:
    def __init__(self):
        self.pacienteDao = PacienteDao()
        self.enderecoDao = EnderecoDao()
        self.responsavelDao = ResponsavelDao()

    def obterPaciente(self, idPaciente: int):
        pacienteProcurado = self.pacienteDao.obterPacientePorId(idPaciente)

        if not pacienteProcurado:
            return {
                "msg" : "Paciente não encontrado"
            }, 404
        
        enderecoProcurado = self.enderecoDao.obterEnderecoId(idPaciente)

        responsavelProcurado = self.responsavelDao.obterReponsavelId(idPaciente)

        return {
            "paciente" : pacienteProcurado,
            "endereco" : enderecoProcurado,
            "responsavel" : responsavelProcurado
        }, 200
    
    def obterPacientes(self, itensPorPagina: int, pagina: int):
        resposta = self.pacienteDao.obterPacientes(itensPorPagina, pagina)

        if not resposta:
            return{
                "msg" : "Index indiponível"
            }, 404

        pacientes = resposta.get("pacientes")

        dicionario_geral = []
        for paciente in pacientes:
            id_paciente = paciente.get("id")
            endereco = self.enderecoDao.obterEnderecoId(id_paciente)
            responsavel = self.responsavelDao.obterReponsavelId(id_paciente)

            dicionario_geral.append({
                "dados": paciente,
                "endereco": endereco,
                "responsavel": responsavel
            })

        return {
            "pagina": resposta.get("pagina"),
            "totalPaginas": resposta.get("totalPaginas"),
            "itensPorPagina" : resposta.get("itensPorPagina"),
            "pacientesTotais" : resposta.get("pacientesTotais"),
            "pacientes" : dicionario_geral,
        }, 200
