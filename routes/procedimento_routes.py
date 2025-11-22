from flask import Blueprint, request, jsonify
from security.notations import token_required
from service.procedimento_service import ProcedimentoService

procedimento_routes = Blueprint('procedimento_routes', __name__)
procedimento_service = ProcedimentoService()

@procedimento_routes.route("/api/v1/procedimentos", methods=["GET"])
@token_required
def obter_procedimentos():
    """
    Lista procedimentos de forma paginada.
    Requer autenticação via token JWT.
    Permite filtros de paginação via query params.
    """
    try:
        token = request.headers.get('Authorization')
        pagina = request.args.get('pagina', default=1, type=int)
        itens_por_pagina = request.args.get('itensPorPagina', default=10, type=int)

        resposta, status = procedimento_service.obterProcedimentos(token, itens_por_pagina, pagina)
        return jsonify(resposta), status

    except Exception as e:
        return jsonify({"msg": f"Erro interno do servidor: {str(e)}"}), 500

@procedimento_routes.route("/api/v1/procedimentos/<int:id>", methods=["GET"])
@token_required
def obter_procedimento(id):
    """
    Obtém um procedimento específico pelo ID.
    Requer autenticação via token JWT.
    """
    try:
        token = request.headers.get('Authorization')
        resposta, status = procedimento_service.obterProcedimento(token, id)
        return jsonify(resposta), status

    except Exception as e:
        return jsonify({"msg": f"Erro interno do servidor: {str(e)}"}), 500

@procedimento_routes.route("/api/v1/procedimentos", methods=["POST"])
@token_required
def adicionar_procedimento():
    """
    Cria um novo procedimento.
    Requer autenticação via token JWT.
    Apenas administradores podem criar procedimentos.
    """
    try:
        token = request.headers.get('Authorization')
        dados = request.get_json()
        
        if not dados:
            return jsonify({"msg": "Dados JSON são obrigatórios."}), 400

        resposta, status = procedimento_service.adicionarProcedimento(token, dados)
        return jsonify(resposta), status

    except Exception as e:
        return jsonify({"msg": f"Erro interno do servidor: {str(e)}"}), 500

@procedimento_routes.route("/api/v1/procedimentos/<int:id>", methods=["PUT"])
@token_required
def alterar_procedimento(id):
    """
    Atualiza um procedimento existente.
    Requer autenticação via token JWT.
    Apenas administradores podem editar procedimentos.
    """
    try:
        token = request.headers.get('Authorization')
        dados = request.get_json()
        
        if not dados:
            return jsonify({"msg": "Dados JSON são obrigatórios."}), 400

        resposta, status = procedimento_service.alterarProcedimento(token, id, dados)
        return jsonify(resposta), status

    except Exception as e:
        return jsonify({"msg": f"Erro interno do servidor: {str(e)}"}), 500

@procedimento_routes.route("/api/v1/procedimentos/<int:id>", methods=["DELETE"])
@token_required
def deletar_procedimento(id):
    """
    Remove um procedimento existente.
    Requer autenticação via token JWT.
    Apenas administradores podem remover procedimentos.
    Procedimentos em uso não podem ser removidos.
    """
    try:
        token = request.headers.get('Authorization')
        resposta, status = procedimento_service.deletarProcedimento(token, id)
        return jsonify(resposta), status

    except Exception as e:
        return jsonify({"msg": f"Erro interno do servidor: {str(e)}"}), 500