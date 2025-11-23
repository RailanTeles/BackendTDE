from flask import Blueprint, request
from security.notations import token_required
from service.procedimento_service import ProcedimentoService

# Blueprint para rotas de procedimentos
procedimento_routes = Blueprint('procedimento_routes', __name__)
procedimento_service = ProcedimentoService()

@procedimento_routes.route('/api/v1/procedimentos', methods=['POST'])
@token_required
def criar_procedimento():
    """
    Cria um novo procedimento.
    Requer autenticação via token JWT.
    Apenas administradores podem criar procedimentos.
    """
    token = request.headers.get('Authorization')
    data = request.get_json()
    return procedimento_service.criar_procedimento(token, data)

@procedimento_routes.route('/api/v1/procedimentos', methods=['GET'])
@token_required
def listar_procedimentos():
    """
    Lista procedimentos de forma paginada.
    Requer autenticação via token JWT.
    Permite filtros de paginação via query params.
    """
    token = request.headers.get('Authorization')
    pagina = request.args.get('pagina', default=1, type=int)
    itensPorPagina = request.args.get('itensPorPagina', default=None, type=int)
    itens_por_pagina_legacy = request.args.get('itens_por_pagina', default=None, type=int)
    itens = itensPorPagina if itensPorPagina is not None else (itens_por_pagina_legacy if itens_por_pagina_legacy is not None else 2)
    return procedimento_service.obter_procedimentos(token, pagina, itens)

@procedimento_routes.route('/api/v1/procedimentos/<int:procedimento_id>', methods=['GET'])
@token_required
def obter_procedimento(procedimento_id):
    """
    Obtém um procedimento específico pelo ID.
    Requer autenticação via token JWT.
    """
    token = request.headers.get('Authorization')
    return procedimento_service.obter_procedimento(token, procedimento_id)

@procedimento_routes.route('/api/v1/procedimentos/<int:procedimento_id>', methods=['PUT'])
@token_required
def atualizar_procedimento(procedimento_id):
    """
    Atualiza um procedimento existente.
    Requer autenticação via token JWT.
    Apenas administradores podem editar procedimentos.
    """
    token = request.headers.get('Authorization')
    data = request.get_json()
    return procedimento_service.atualizar_procedimento(token, procedimento_id, data)

@procedimento_routes.route('/api/v1/procedimentos/<int:procedimento_id>', methods=['DELETE'])
@token_required
def remover_procedimento(procedimento_id):
    """
    Remove um procedimento existente.
    Requer autenticação via token JWT.
    Apenas administradores podem remover procedimentos.
    Procedimentos em uso não podem ser removidos.
    """
    token = request.headers.get('Authorization')
    return procedimento_service.remover_procedimento(token, procedimento_id)