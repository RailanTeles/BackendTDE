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
    
    """
    try:
        pagina = request.args.get('pagina', default=1, type=int)
        itensPorPagina = request.args.get('itensPorPagina', default=2, type=int)

        return pacienteService.obterPacientes(itensPorPagina, pagina)
    
    except Exception as e:
        return {
            "msg": f"{str(e)}"
        }, 500
