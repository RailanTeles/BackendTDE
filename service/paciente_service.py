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