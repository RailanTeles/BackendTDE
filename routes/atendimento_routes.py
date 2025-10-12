from flask import Blueprint, request, jsonify
from dao.atendimento_dao import AtendimentoDao
from security.notations import token_required
from service.atendimento_service import AtendimentoService

atendimento_routes = Blueprint('atendimento_routes', __name__)
atendimentoDao = AtendimentoDao()
atendimentoService = AtendimentoService()

# Criar atendimento
@atendimento_routes.route('/api/v1/atendimentos', methods=['POST'])
@token_required
def criar_atendimento():
    data = request.get_json()
    try:
        data_atendimento = data.get('data')
        paciente_id = data.get('paciente_id')
        procedimentos = data.get('procedimentos')
        tipo = data.get('tipo')
        numero_plano = data.get('numero_plano')
        usuario_id = data.get('usuario_id')
        response, status = atendimentoService.criarAtendimento(
            data_atendimento, paciente_id, procedimentos, tipo, numero_plano, usuario_id
        )
        return jsonify(response), status
    except Exception as e:
        return jsonify({'msg': str(e)}), 400

# Listar atendimentos
@atendimento_routes.route('/api/v1/atendimentos', methods=['GET'])
@token_required
def listar_atendimentos():
    try:
        usuario_id = request.args.get('usuario_id', type=int)
        usuario_tipo = request.args.get('usuario_tipo', type=str)
        if usuario_tipo == 'admin':
            atendimentos = atendimentoDao.listarAtendimentos()
        else:
            atendimentos = [a for a in atendimentoDao.listarAtendimentos() if a['idUsuario'] == usuario_id]
        return jsonify(atendimentos), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 400

# Obter atendimento por ID
@atendimento_routes.route('/api/v1/atendimentos/<int:atendimento_id>', methods=['GET'])
@token_required
def obter_atendimento(atendimento_id):
    try:
        atendimento = atendimentoDao.obterAtendimentoPorId(atendimento_id)
        if not atendimento:
            return jsonify({'msg': 'Atendimento não encontrado'}), 404
        return jsonify(atendimento), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 400

# Atualizar atendimento
@atendimento_routes.route('/api/v1/atendimentos/<int:atendimento_id>', methods=['PUT'])
@token_required
def atualizar_atendimento(atendimento_id):
    data = request.get_json()
    try:
        data_atendimento = data.get('data')
        paciente_id = data.get('paciente_id')
        procedimentos = data.get('procedimentos')
        tipo = data.get('tipo')
        numero_plano = data.get('numero_plano')
        usuario_id = data.get('usuario_id')
        usuario_tipo = data.get('usuario_tipo')
        response, status = atendimentoService.atualizarAtendimento(
            atendimento_id, data_atendimento, paciente_id, procedimentos, tipo, numero_plano, usuario_id, usuario_tipo
        )
        return jsonify(response), status
    except Exception as e:
        return jsonify({'msg': str(e)}), 400

# Remover atendimento
@atendimento_routes.route('/api/v1/atendimentos/<int:atendimento_id>', methods=['DELETE'])
@token_required
def remover_atendimento(atendimento_id):
    data = request.get_json()
    try:
        usuario_id = data.get('usuario_id')
        usuario_tipo = data.get('usuario_tipo')
        response, status = atendimentoService.removerAtendimento(
            atendimento_id, usuario_id, usuario_tipo
        )
        return jsonify(response), status
    except Exception as e:
        return jsonify({'msg': str(e)}), 400
