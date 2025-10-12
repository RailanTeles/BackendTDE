
from flask import Blueprint, request, jsonify
from security.notations import token_required
from service.atendimento_service import AtendimentoService

# Blueprint para rotas de atendimentos
atendimento_routes = Blueprint('atendimento_routes', __name__)
atendimentoService = AtendimentoService()

# =========================
# Rotas de Atendimento
# =========================

@atendimento_routes.route('/api/v1/atendimentos', methods=['POST'])
@token_required
def criar_atendimento():
    """
    Cria um novo atendimento.
    Requer autenticação via token JWT.
    Apenas administradores podem criar para outros usuários.
    Valida existência do paciente e regras de negócio no service.
    """
    try:
        token = request.headers.get('Authorization')
        data = request.get_json()
        response, status = atendimentoService.criarAtendimento(token, data)
        return jsonify(response), status
    except Exception as e:
        return jsonify({'msg': str(e)}), 500

@atendimento_routes.route('/api/v1/atendimentos', methods=['GET'])
@token_required
def listar_atendimentos():
    """
    Lista atendimentos de forma paginada.
    Requer autenticação via token JWT.
    Permite filtros de paginação via query params.
    """
    try:
        token = request.headers.get('Authorization')
        pagina = request.args.get('pagina', default=1, type=int)
        itens_por_pagina = request.args.get('itens_por_pagina', default=10, type=int)
        response, status = atendimentoService.obterAtendimentos(token, pagina, itens_por_pagina)
        return jsonify(response), status
    except Exception as e:
        return jsonify({'msg': str(e)}), 500

@atendimento_routes.route('/api/v1/atendimentos/<int:atendimento_id>', methods=['GET'])
@token_required
def obter_atendimento(atendimento_id):
    """
    Obtém um atendimento específico pelo ID.
    Requer autenticação via token JWT.
    Apenas o dono ou admin pode visualizar.
    """
    try:
        token = request.headers.get('Authorization')
        response, status = atendimentoService.obterAtendimento(token, atendimento_id)
        return jsonify(response), status
    except Exception as e:
        return jsonify({'msg': str(e)}), 500

@atendimento_routes.route('/api/v1/atendimentos/<int:atendimento_id>', methods=['PUT'])
@token_required
def atualizar_atendimento(atendimento_id):
    """
    Atualiza um atendimento existente.
    Requer autenticação via token JWT.
    Apenas o dono ou admin pode editar.
    Valida existência do paciente e regras de negócio no service.
    """
    try:
        token = request.headers.get('Authorization')
        data = request.get_json()
        response, status = atendimentoService.atualizarAtendimento(token, atendimento_id, data)
        return jsonify(response), status
    except Exception as e:
        return jsonify({'msg': str(e)}), 500

@atendimento_routes.route('/api/v1/atendimentos/<int:atendimento_id>', methods=['DELETE'])
@token_required
def remover_atendimento(atendimento_id):
    """
    Remove um atendimento existente.
    Requer autenticação via token JWT.
    Apenas o dono ou admin pode remover.
    """
    try:
        token = request.headers.get('Authorization')
        response, status = atendimentoService.removerAtendimento(token, atendimento_id)
        return jsonify(response), status
    except Exception as e:
        return jsonify({'msg': str(e)}), 500


# Endpoint para listar atendimentos entre datas
@atendimento_routes.route('/api/v1/atendimentos/<data_inicio>/<data_fim>', methods=['GET'])
@token_required
def listar_atendimentos_por_data_paginado(data_inicio, data_fim):
    """
    Lista atendimentos entre duas datas informadas (inclusive), paginado.
    Parâmetros via path:
      - data_inicio: data inicial (YYYY-MM-DD)
      - data_fim: data final (YYYY-MM-DD)
    Parâmetros via query string:
      - pagina: número da página (opcional, padrão=1)
      - itens_por_pagina: itens por página (opcional, padrão=10)
    Exemplo de uso: /api/v1/atendimentos/2025-10-01/2025-10-20?pagina=1&itens_por_pagina=10
    """
    try:
        token = request.headers.get('Authorization')
        pagina = request.args.get('pagina', default=1, type=int)
        itens_por_pagina = request.args.get('itens_por_pagina', default=10, type=int)
        if not data_inicio or not data_fim:
            return jsonify({'msg': 'Parâmetros data_inicio e data_fim são obrigatórios.'}), 400
        response, status = atendimentoService.obterAtendimentosPorData(token, data_inicio, data_fim, pagina, itens_por_pagina)
        return jsonify(response), status
    except Exception as e:
        return jsonify({'msg': str(e)}), 500