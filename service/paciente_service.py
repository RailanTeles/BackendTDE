from dao.paciente_dao import PacienteDao
from dao.endereco_dao import EnderecoDao
from dao.responsavel_dao import ResponsavelDao
from dao.atendimento_dao import AtendimentoDao
from models.paciente import Paciente
from models.endereco import Endereco
from models.responsavel import Responsavel

class PacienteService:
    def __init__(self):
        self.pacienteDao = PacienteDao()
        self.enderecoDao = EnderecoDao()
        self.responsavelDao = ResponsavelDao()
        self.atendimentoDao = AtendimentoDao()

    def obterPaciente(self, idPaciente: int):
        pacienteProcurado = self.pacienteDao.obterPacientePorId(idPaciente)

        if not pacienteProcurado:
            return {
                "msg" : "Paciente não encontrado"
            }, 404
        
        enderecoProcurado = self.enderecoDao.obterEnderecoId(idPaciente)

        responsavelProcurado = self.responsavelDao.obterResponsavelId(idPaciente)

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
            responsavel = self.responsavelDao.obterResponsavelId(id_paciente)

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
    
    def adicionarPaciente(self, data: str):
        paciente_data = data.get('paciente')

        if not paciente_data:
            return {
                "msg": "Dados do paciente não fornecidos"
            }, 400

        cpf = paciente_data.get('cpf')
        nome = paciente_data.get('nome')
        email = paciente_data.get('email')
        telefone = paciente_data.get('telefone')
        dataNascimento = paciente_data.get('dataNascimento')

        if not cpf or not nome or not email or not telefone or not dataNascimento:
            return {
                "msg": "Dados do paciente incompletos"
            }, 400

        pacienteCPF = self.pacienteDao.obterPacientePorCpf(cpf)
        if pacienteCPF:
            return {
                "msg": "CPF já cadastrado"
            }, 409
        
        pacienteEmail = self.pacienteDao.obterPacientePorEmail(email)
        if pacienteEmail:
            return {
                "msg": "Email já cadastrado"
            }, 409

        paciente = Paciente(id=0, cpf=cpf, nome=nome, email=email, telefone=telefone, dataNascimento=dataNascimento)
        
        deMaior = paciente.verificarMaiorIdade()

        responsavel_data = data.get('responsavel')

        if not deMaior and not responsavel_data:
            return {
                "msg": "Paciente menor de idade, responsável deve ser informado"
            }, 400
        
        if responsavel_data:
            cpf_resp = responsavel_data.get('cpf')
            nome_resp = responsavel_data.get('nome')
            email_resp = responsavel_data.get('email')
            telefone_resp = responsavel_data.get('telefone')
            dataNascimento_resp = responsavel_data.get('dataNascimento')

            if not cpf_resp or not nome_resp or not email_resp or not telefone_resp or not dataNascimento_resp:
                return {
                    "msg": "Dados do responsável incompletos"
                }, 400

            responsavel = Responsavel(id=0, cpf=cpf_resp, nome=nome_resp, email=email_resp, telefone=telefone_resp, dataNascimento=dataNascimento_resp, idPaciente=paciente.id)

            respDeMaior = responsavel.verificarMaiorIdade()
            if not respDeMaior:
                return {
                    "msg": "Responsável deve ser maior de idade"
                }, 400

        
        endereco_data = data.get('endereco')
        
        if not endereco_data:
            return {
                "msg": "Endereço deve ser informado"
            }, 400
        
        if endereco_data:
            estado = endereco_data.get('estado')
            cidade = endereco_data.get('cidade')
            bairro = endereco_data.get('bairro')
            cep = endereco_data.get('cep')
            rua = endereco_data.get('rua')
            numeroCasa = endereco_data.get('numeroCasa')

            if not estado or not cidade or not bairro or not cep or not rua or not numeroCasa:
                return {
                    "msg": "Dados do endereço incompletos"
                }, 400
            endereco = Endereco(id=0, estado=estado, cidade=cidade, bairro=bairro, cep=cep, rua=rua, numeroCasa=numeroCasa, idPaciente=paciente.id)

        self.pacienteDao.adicionarPaciente(paciente)
        pacienteCadastrado = self.pacienteDao.obterPacientePorCpf(paciente.cpf)
        idPacienteCadastrado = pacienteCadastrado.get("id")

        endereco.idPaciente = idPacienteCadastrado
        self.enderecoDao.adicionarEndereco(endereco)

        if responsavel_data:
            responsavel.idPaciente = idPacienteCadastrado
            self.responsavelDao.adicionarResponsavel(responsavel)

        return {
            "msg": "Paciente adicionado com sucesso",
        }, 200
    

    def alterarPaciente(self, idPaciente: int, data: str):
        idPaciente = int(idPaciente)
        pacienteBD = self.pacienteDao.obterPacientePorId(idPaciente)
        if not pacienteBD:
            return {
                "msg": "Paciente não encontrado"
            }, 404

        paciente_data = data.get('paciente')

        if not paciente_data:
            return {
                "msg": "Todos os dados do paciente devem ser fornecidos"
            }, 400

        cpf = paciente_data.get('cpf')
        nome = paciente_data.get('nome')
        email = paciente_data.get('email')
        telefone = paciente_data.get('telefone')
        dataNascimento = paciente_data.get('dataNascimento')

        if not cpf or not nome or not email or not telefone or not dataNascimento:
            return {
                "msg": "Todos os dados do paciente devem ser fornecidos (cpf, nome, email, telefone, dataNascimento)"
            }, 400
        
        pacienteCPF = self.pacienteDao.obterPacientePorCpf(cpf)
        if pacienteCPF and pacienteCPF.get("id") != idPaciente:
            return {
                "msg": "CPF já cadastrado"
            }, 409
        
        pacienteEmail = self.pacienteDao.obterPacientePorEmail(email)
        if pacienteEmail and pacienteEmail.get("id") != idPaciente:
            return {
                "msg": "Email já cadastrado"
            }, 409
        
        pacienteEditado = Paciente(id=idPaciente, cpf=cpf, nome=nome, email=email, telefone=telefone, dataNascimento=dataNascimento)

        deMaior = pacienteEditado.verificarMaiorIdade()

        responsavel_data = data.get('responsavel')

        if not deMaior and not responsavel_data:
            return {
                "msg": "Paciente menor de idade, os dados do responsável devem ser informados, pois são obrigatórios"
            }, 400
        
        if responsavel_data:
            cpf_resp = responsavel_data.get('cpf')
            nome_resp = responsavel_data.get('nome')
            email_resp = responsavel_data.get('email')
            telefone_resp = responsavel_data.get('telefone')
            dataNascimento_resp = responsavel_data.get('dataNascimento')

            if not cpf_resp or not nome_resp or not email_resp or not telefone_resp or not dataNascimento_resp:
                return {
                    "msg": "Dados do responsável incompletos (cpf, nome, email, telefone, dataNascimento)"
                }, 400
            
            responsavelEditado = Responsavel(id=0, cpf=cpf_resp, nome=nome_resp, email=email_resp, telefone=telefone_resp, dataNascimento=dataNascimento_resp, idPaciente=idPaciente)
            respDeMaior = responsavelEditado.verificarMaiorIdade()
            if not respDeMaior:
                return {
                    "msg": "Responsável deve ser maior de idade"
                }, 400
            
        
        endereco_data = data.get('endereco')
        
        if not endereco_data:
            return {
                "msg": "Endereço deve ser informado"
            }, 400
        
        if endereco_data:
            estado = endereco_data.get('estado')
            cidade = endereco_data.get('cidade')
            bairro = endereco_data.get('bairro')
            cep = endereco_data.get('cep')
            rua = endereco_data.get('rua')
            numeroCasa = endereco_data.get('numeroCasa')

            if not estado or not cidade or not bairro or not cep or not rua or not numeroCasa:
                return {
                    "msg": "Dados do endereço incompletos (estado, cidade, bairro, cep, rua, numeroCasa)"
                }, 400
            enderecoEditado = Endereco(id=0, estado=estado, cidade=cidade, bairro=bairro, cep=cep, rua=rua, numeroCasa=numeroCasa, idPaciente=pacienteEditado.id)

        self.pacienteDao.alterarPaciente(pacienteEditado)
        self.enderecoDao.alterarEndereco(enderecoEditado)

        if responsavel_data:
            responsavelExistente = self.responsavelDao.obterResponsavelId(idPaciente)
            if responsavelExistente:
                responsavelEditado.id = responsavelExistente.get("id")
                self.responsavelDao.alterarResponsavel(responsavelEditado)
            else:
                self.responsavelDao.adicionarResponsavel(responsavelEditado)

        return {
            "msg": "Paciente alterado com sucesso",
        }, 200
    

    def deletarPaciente(self, idPaciente: int):
        idPaciente = int(idPaciente)
        pacienteBD = self.pacienteDao.obterPacientePorId(idPaciente)
        if not pacienteBD:
            return {
                "msg": "Paciente não encontrado"
            }, 404

        qtdAtendimentos = self.atendimentoDao.obterQtdAtendimentosPaciente(idPaciente)
        if qtdAtendimentos and qtdAtendimentos > 0:
            return {
                "msg": "Paciente possui atendimentos vinculados e não pode ser deletado"
            }, 409
        
        self.pacienteDao.deletarPaciente(idPaciente)
        self.enderecoDao.deletarEndereco(idPaciente)
        self.responsavelDao.deletarResponsavel(idPaciente)

        return {
            "msg": "Dados do paciente deletados com sucesso",
        }, 200
