from flask import Blueprint, request, jsonify
from service.procedimento_service import ProcedimentoService
from security.notations import token_required
from utils.jwt_util import decode_token
from dao.usuario_dao import UsuarioDao

procedimento_routes = Blueprint('procedimento_routes', __name__)
procedimentoService = ProcedimentoService()
usuarioDao = UsuarioDao()  # Para checar permissões de admin

# Rota para obter um procedimento por id
@procedimento_routes.route("/api/v1/procedimento/<int:id>", methods=["GET"])
@token_required
def obter_procedimento(id):
    """
    Rota para obter um procedimento pelo id
    Exemplo: /api/v1/procedimento/1
    """
    try:
        return procedimentoService.obterProcedimento(id)
    except Exception as e:
        return {"msg": f"{str(e)}"}, 500

# Rota para obter todos os procedimentos com paginação
@procedimento_routes.route("/api/v1/procedimento", methods=["GET"])
@token_required
def obter_procedimentos():
    """
    Rota para listar procedimentos com paginação
    Parâmetros de query: pagina (padrão 1) e itensPorPagina (padrão 10)
    Exemplo: /api/v1/procedimento?pagina=1&itensPorPagina=10
    """
    try:
        pagina = request.args.get('pagina', default=1, type=int)
        itensPorPagina = request.args.get('itensPorPagina', default=10, type=int)
        return procedimentoService.obterProcedimentos(itensPorPagina, pagina)
    except Exception as e:
        return {"msg": f"{str(e)}"}, 500

# Rota para adicionar um novo procedimento (apenas admin)
@procedimento_routes.route("/api/v1/procedimento", methods=["POST"])
@token_required
def adicionar_procedimento():
    """
    Rota para adicionar um procedimento
    JSON esperado:
    {
        "nome": "Exame de Sangue",
        "desc": "Descrição do procedimento",
        "valorPlano": 100.0,
        "valorParticular": 150.0
    }
    """
    try:
        token = request.headers.get('Authorization')
        user_id = decode_token(token)
        user = usuarioDao.obterUsuarioId(user_id)
        if not user or user.get('role') != 'admin':
            return {"msg": "Acesso negado: permissão insuficiente!"}, 403

        data = request.get_json()
        return procedimentoService.adicionarProcedimento(data)
    except Exception as e:
        return {"msg": f"{str(e)}"}, 500

# Rota para alterar um procedimento existente (apenas admin)
@procedimento_routes.route("/api/v1/procedimento/<int:id>", methods=["PUT"])
@token_required
def alterar_procedimento(id):
    """
    Rota para alterar um procedimento existente
    JSON esperado:
    {
        "nome": "Exame Atualizado",
        "desc": "Nova descrição",
        "valorPlano": 120.0,
        "valorParticular": 170.0
    }
    Exemplo: /api/v1/procedimento/1
    """
    try:
        token = request.headers.get('Authorization')
        user_id = decode_token(token)
        user = usuarioDao.obterUsuarioId(user_id)
        if not user or user.get('role') != 'admin':
            return {"msg": "Acesso negado: permissão insuficiente!"}, 403

        data = request.get_json()
        return procedimentoService.alterarProcedimento(id, data)
    except Exception as e:
        return {"msg": f"{str(e)}"}, 500

# Rota para deletar um procedimento (apenas admin)
@procedimento_routes.route("/api/v1/procedimento/<int:id>", methods=["DELETE"])
@token_required
def deletar_procedimento(id):
    """
    Rota para deletar um procedimento por id
    Um procedimento vinculado a atendimentos não pode ser deletado
    Exemplo: /api/v1/procedimento/1
    """
    try:
        token = request.headers.get('Authorization')
        user_id = decode_token(token)
        user = usuarioDao.obterUsuarioId(user_id)
        if not user or user.get('role') != 'admin':
            return {"msg": "Acesso negado: permissão insuficiente!"}, 403

        return procedimentoService.deletarProcedimento(id)
    except Exception as e:
        return {"msg": f"{str(e)}"}, 500
