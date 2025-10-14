from flask import Flask, jsonify, request, Blueprint
from service.paciente_service import PacienteService
from security.notations import token_required

paciente_routes = Blueprint('paciente_routes', __name__)

pacienteService = PacienteService()

#Rota para obter paciente por id
@paciente_routes.route("/api/v1/paciente/<id>", methods=["GET"])
@token_required
def obterPaciente(id):
    """
    Rota para obter paciente por id
    Exemplo: /api/v1/paciente/1
    """

    try:
        return pacienteService.obterPaciente(id)

    except Exception as e:
        return{
            "msg" : f"{str(e)}"
        }, 500
    
#Rota para obter paciente por id
@paciente_routes.route("/api/v1/paciente", methods=["GET"])
@token_required
def obterPacientes():
    """
    Rota para obter todos os pacientes com paginação. Parâmetros de query: pagina (padrão 1) e itensPorPagina (padrão 2)
    Exemplo: /api/v1/paciente?pagina=1&itensPorPagina=2
    """
    try:
        pagina = request.args.get('pagina', default=1, type=int)
        itensPorPagina = request.args.get('itensPorPagina', default=2, type=int)

        return pacienteService.obterPacientes(itensPorPagina, pagina)
    
    except Exception as e:
        return {
            "msg": f"{str(e)}"
        }, 500

#Rota para adicionar paciente
@paciente_routes.route("/api/v1/paciente", methods=["POST"])
def adicionarPaciente():
    """
    Rota para adicionar um novo paciente. Json:
    {
        "paciente": {
            "cpf": "12345678900",
            "nome": "Nome do Paciente",
            "email": "email@exemplo.com",
            "telefone": "11987654321",
            "dataNascimento": "2000-01-01"
        },
        "responsavel": {
            "cpf": "12345678901",
            "nome": "Nome do Responsável",
            "email": "responsavel@exemplo.com",
            "telefone": "11987654322",
            "dataNascimento": "1980-01-01"
        },
        "endereco": {
            "estado": "SP",
            "cidade": "São Paulo",
            "bairro": "Centro",
            "cep": "01000-000",
            "rua": "Rua Exemplo",
            "numeroCasa": "123"
        }
    """
    try:
        data = request.get_json()
        return pacienteService.adicionarPaciente(data)
    
    except Exception as e:
        return {
            "msg": f"{str(e)}"
        }, 500

#Rota para alterar paciente
@paciente_routes.route("/api/v1/paciente/<id>", methods=["PUT"])
@token_required
def alterarPaciente(id):
    """
    Rota para alterar um paciente. Json:{
        "paciente": {
            "cpf": "12345678900",
            "nome": "Nome do Paciente",
            "email": "email@exemplo.com",
            "telefone": "11987654321",
            "dataNascimento": "2000-01-01"
        },
        "responsavel": {
            "cpf": "12345678901",
            "nome": "Nome do Responsável",
            "email": "responsavel@exemplo.com",
            "telefone": "11987654322",
            "dataNascimento": "1980-01-01"
        },
        "endereco": {
            "estado": "SP",
            "cidade": "São Paulo",
            "bairro": "Centro",
            "cep": "01000-000",
            "rua": "Rua Exemplo",
            "numeroCasa": "123"
        }
    """
    try:
        data = request.get_json()
        return pacienteService.alterarPaciente(id, data)
    
    except Exception as e:
        return {
            "msg": f"{str(e)}"
        }, 500
    

#Rota para deletar paciente
@paciente_routes.route("/api/v1/paciente/<id>", methods=["DELETE"])
@token_required
def deletarPaciente(id):
    """
    Rota para deletar um paciente por id.
    Um paciente com atendimentos não pode ser deletado.
    Exemplo: /api/v1/paciente/1
    """
    try:
        return pacienteService.deletarPaciente(id)
    
    except Exception as e:
        return {
            "msg": f"{str(e)}"
        }, 500
    

#Rota para deletar apenas o responsavel do paciente
@paciente_routes.route("/api/v1/paciente/<id>/responsavel", methods=["DELETE"])
@token_required
def deletarResponsavel(id):
    """
    Rota para deletar apenas o responsável do paciente por id.
    Caso o paciente seja menor de idade, o responsável não pode ser deletado.
    Exemplo: /api/v1/paciente/1/responsavel
    """
    try:
        return pacienteService.deletarResponsavel(id)
    
    except Exception as e:
        return {
            "msg": f"{str(e)}"
        }, 500