from flask import Blueprint, request, jsonify, g
from security.notations import token_required

procedimento_routes = Blueprint('procedimento_routes', __name__)

def get_procedimento_service():
    """SEMPRE importar localmente para evitar circular imports"""
    from service.procedimento_service import ProcedimentoService
    return ProcedimentoService()

def verificar_admin():
    try:
        # O token contém apenas o ID, então precisamos buscar o usuário no banco
        user_id = g.get("user_id")
        if not user_id:
            print("❌ Nenhum user_id encontrado no contexto")
            return False
        
        # Buscar informações do usuário no banco - usando SEU método
        from dao.usuario_dao import UsuarioDao
        usuario_dao = UsuarioDao()
        usuario = usuario_dao.obterUsuarioId(user_id)  # SEU MÉTODO obterUsuarioId
        
        if not usuario:
            print("❌ Usuário não encontrado no banco de dados")
            return False
        
        print(f"🔍 Tipo de usuário: {usuario.get('tipo')}")
        return usuario.get("tipo") == "admin"
        
    except Exception as e:
        print(f"❌ Erro ao verificar admin: {str(e)}")
        return False

@procedimento_routes.route("/api/v1/procedimentos", methods=["GET"])
@token_required
def obter_procedimentos():
    try:
        pagina = request.args.get('pagina', default=1, type=int)
        itens_por_pagina = request.args.get('itensPorPagina', default=10, type=int)

        service = get_procedimento_service()
        resultado, status = service.obterProcedimentos(itens_por_pagina, pagina)
        return jsonify(resultado), status

    except Exception as e:
        return jsonify({"msg": f"Erro interno do servidor: {str(e)}"}), 500

@procedimento_routes.route("/api/v1/procedimentos/<int:id>", methods=["GET"])
@token_required
def obter_procedimento(id):
    try:
        service = get_procedimento_service()
        resultado, status = service.obterProcedimento(id)
        return jsonify(resultado), status

    except Exception as e:
        return jsonify({"msg": f"Erro interno do servidor: {str(e)}"}), 500

@procedimento_routes.route("/api/v1/procedimentos", methods=["POST"])
@token_required
def adicionar_procedimento():
    try:
        if not verificar_admin():
            return jsonify({"msg": "Apenas administradores podem realizar esta ação."}), 403

        dados = request.get_json()
        if not dados:
            return jsonify({"msg": "Dados JSON são obrigatórios."}), 400

        service = get_procedimento_service()
        resultado, status = service.adicionarProcedimento(dados)
        return jsonify(resultado), status

    except Exception as e:
        return jsonify({"msg": f"Erro interno do servidor: {str(e)}"}), 500

@procedimento_routes.route("/api/v1/procedimentos/<int:id>", methods=["PUT"])
@token_required
def alterar_procedimento(id):
    try:
        if not verificar_admin():
            return jsonify({"msg": "Apenas administradores podem realizar esta ação."}), 403

        dados = request.get_json()
        if not dados:
            return jsonify({"msg": "Dados JSON são obrigatórios."}), 400

        service = get_procedimento_service()
        resultado, status = service.alterarProcedimento(id, dados)
        return jsonify(resultado), status

    except Exception as e:
        return jsonify({"msg": f"Erro interno do servidor: {str(e)}"}), 500

@procedimento_routes.route("/api/v1/procedimentos/<int:id>", methods=["DELETE"])
@token_required
def deletar_procedimento(id):
    try:
        if not verificar_admin():
            return jsonify({"msg": "Apenas administradores podem realizar esta ação."}), 403

        service = get_procedimento_service()
        resultado, status = service.deletarProcedimento(id)
        return jsonify(resultado), status

    except Exception as e:
        return jsonify({"msg": f"Erro interno do servidor: {str(e)}"}), 500