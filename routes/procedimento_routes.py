

from flask import Blueprint, jsonify, request
from service.procedimento_service import ProcedimentoService
from security.notations import token_required

procedimento_routes = Blueprint('procedimento_routes', __name__)
procedimentoService = ProcedimentoService()


@procedimento_routes.route("/api/v1/procedimento", methods=["POST"])
@token_required
def adicionar_procedimento():

    try:
        data = request.get_json()
        return procedimentoService.adicionarProcedimento(data)
    except Exception as e:
        return {"msg": str(e)}, 500

@procedimento_routes.route("/api/v1/procedimento/<int:id>", methods=["PUT"])
@token_required
def alterar_procedimento(id):
    try:
        data = request.get_json()
        return procedimentoService.alterarProcedimento(id, data)
    except Exception as e:
        return {"msg": str(e)}, 500


@procedimento_routes.route("/api/v1/procedimento/<int:id>", methods=["GET"])
@token_required
def obter_procedimento(id):
    try:
        return procedimentoService.obterProcedimento(id)
    except Exception as e:
        return {"msg": str(e)}, 500

@procedimento_routes.route("/api/v1/procedimento", methods=["GET"])
@token_required
def obter_procedimentos():
    try:
        pagina = request.args.get('pagina', default=1, type=int)
        itensPorPagina = request.args.get('itensPorPagina', default=10, type=int)
        return procedimentoService.obterProcedimentos(itensPorPagina, pagina)
    except Exception as e:
        return {"msg": str(e)}, 500

@procedimento_routes.route("/api/v1/procedimento/<int:id>", methods=["DELETE"])
@token_required
def deletar_procedimento(id):
    try:
        return procedimentoService.deletarProcedimento(id)
    except Exception as e:
        return {"msg": str(e)}, 500