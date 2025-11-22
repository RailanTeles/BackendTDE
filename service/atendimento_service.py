from utils.jwt_util import decode_token
from dao.atendimento_dao import AtendimentoDao
from dao.usuario_dao import UsuarioDao
from dao.paciente_dao import PacienteDao
from dao.procedimento_dao import ProcedimentoDao
from models.usuario import TipoUsuario
from datetime import datetime, date
import calendar

class AtendimentoService:
    def __init__(self):
        self.atendimento_dao = AtendimentoDao()
        self.usuario_dao = UsuarioDao()
        self.paciente_dao = PacienteDao()
        self.procedimento_dao = ProcedimentoDao()

    @staticmethod
    def _parse_date_safe(value: str):
        """Valida e retorna um date no formato YYYY-MM-DD sem usar try/except; retorna None se inválido."""
        if not isinstance(value, str) or len(value) != 10:
            return None
        if value[4] != '-' or value[7] != '-':
            return None
        parts = value.split('-')
        if len(parts) != 3:
            return None
        y, m, d = parts
        if not (y.isdigit() and m.isdigit() and d.isdigit()):
            return None
        year = int(y)
        month = int(m)
        day = int(d)
        if month < 1 or month > 12:
            return None
        max_day = calendar.monthrange(year, month)[1]
        if day < 1 or day > max_day:
            return None
        return date(year, month, day)

    def obter_atendimentos_por_data(self, token: str, data_inicio: str, data_fim: str, pagina: int = 1, itens_por_pagina: int = 10):
        """
        Retorna lista paginada de atendimentos entre duas datas informadas (inclusive).
        Apenas usuários autenticados. Admin vê todos, default vê apenas os próprios.
        """
        usuario_id = decode_token(token)
        if not usuario_id:
            return {"msg": "Token inválido"}, 401

        usuario = self.usuario_dao.obterUsuarioId(usuario_id)
        if not usuario:
            return {"msg": "Usuário não encontrado"}, 404

        # Validação simples das datas (YYYY-MM-DD)
        dt_inicio = self._parse_date_safe(data_inicio)
        dt_fim = self._parse_date_safe(data_fim)
        if not dt_inicio or not dt_fim:
            return {"msg": "Formato de data inválido. Use YYYY-MM-DD."}, 400

        if dt_inicio > dt_fim:
            return {"msg": "Data inicial não pode ser maior que a final."}, 400

        # Se não for admin, filtra apenas os próprios atendimentos
        usuario_filtro = None if usuario.get('tipo') == TipoUsuario.ADMIN.value else usuario_id
        
        # Obter total de registros
        total = self.atendimento_dao.obter_total_atendimentos_por_data(data_inicio, data_fim, usuario_filtro)
        total_paginas = (total // itens_por_pagina) + (1 if total % itens_por_pagina else 0)
        
        # Obter página específica
        offset = (pagina - 1) * itens_por_pagina
        atendimentos = self.atendimento_dao.listar_atendimentos_por_data(data_inicio, data_fim, offset, itens_por_pagina, usuario_filtro)
        resposta = {
            'pagina': pagina,
            'totalPaginas': total_paginas,
            'itensPorPagina': itens_por_pagina,
            'registrosTotais': total,
            'itens': atendimentos
        }
        return resposta, 200

    def obter_atendimento(self, token: str, atendimento_id: int):
        """
        Retorna um atendimento pelo ID, se o usuário for admin ou dono.
        """
        usuario_id = decode_token(token)
        if not usuario_id:
            return {"msg": "Token inválido"}, 401

        usuario = self.usuario_dao.obterUsuarioId(usuario_id)
        if not usuario:
            return {"msg": "Usuário não encontrado"}, 404

        atendimento = self.atendimento_dao.obter_atendimento_por_id(atendimento_id)
        if not atendimento:
            return {"msg": "Atendimento não encontrado"}, 404

        # Permissão: admin ou dono
        if usuario.get('tipo') != TipoUsuario.ADMIN.value and atendimento['idUsuario'] != usuario_id:
            return {"msg": "Você não tem permissão para ver este atendimento."}, 403

        return atendimento, 200

    def obter_atendimentos(self, token: str, pagina: int = 1, itens_por_pagina: int = 10):
        """
        Retorna lista paginada de atendimentos do usuário logado (ou todos se admin).
        """
        usuario_id = decode_token(token)
        if not usuario_id:
            return {"msg": "Token inválido"}, 401

        usuario = self.usuario_dao.obterUsuarioId(usuario_id)
        if not usuario:
            return {"msg": "Usuário não encontrado"}, 404

        # Se não for admin, filtra apenas os próprios atendimentos
        usuario_filtro = None if usuario.get('tipo') == TipoUsuario.ADMIN.value else usuario_id
        
        # Obter total de registros
        total = self.atendimento_dao.obter_total_atendimentos(usuario_filtro)
        total_paginas = (total // itens_por_pagina) + (1 if total % itens_por_pagina else 0)
        
        # Obter página específica
        offset = (pagina - 1) * itens_por_pagina
        atendimentos_pagina = self.atendimento_dao.listar_atendimentos(usuario_filtro, offset, itens_por_pagina)
        resposta = {
            'pagina': pagina,
            'totalPaginas': total_paginas,
            'itensPorPagina': itens_por_pagina,
            'registrosTotais': total,
            'itens': atendimentos_pagina
        }
        return resposta, 200

    def criar_atendimento(self, token: str, data_request):
        """
        Cria um novo atendimento. Apenas admin pode criar para outro usuário (usuario_id no JSON).
        """
        usuario_id = decode_token(token)
        if not usuario_id:
            return {"msg": "Token inválido"}, 401

        usuario = self.usuario_dao.obterUsuarioId(usuario_id)
        if not usuario:
            return {"msg": "Usuário não encontrado"}, 404

        usuario_id_destino = data_request.get('usuario_id')
        eh_admin = usuario.get('tipo') == TipoUsuario.ADMIN.value

        if usuario_id_destino is not None:
            if not eh_admin:
                return {"msg": "Apenas administradores podem criar atendimentos para outros usuários."}, 403
            usuario_destino = self.usuario_dao.obterUsuarioId(usuario_id_destino)
            if not usuario_destino:
                return {"msg": f"Usuário destino com ID {usuario_id_destino} não encontrado."}, 404
        else:
            usuario_id_destino = usuario_id

        # Validação dos campos obrigatórios
        data = data_request.get('data')
        paciente_id = data_request.get('paciente_id')
        procedimentos = data_request.get('procedimentos')
        tipo = data_request.get('tipo')
        numero_plano = data_request.get('numero_plano')

        if not all([data, paciente_id, tipo]):
            return {"msg": "Data, paciente_id e tipo são campos obrigatórios"}, 400

        if not procedimentos or len(procedimentos) == 0:
            return {"msg": "O atendimento deve possuir pelo menos um procedimento."}, 400

        ids_procedimentos = [proc.get('id') for proc in procedimentos if proc.get('id')]
        if len(ids_procedimentos) != len(set(ids_procedimentos)):
            return {"msg": "Não é permitido duplicar procedimentos no mesmo atendimento."}, 400

        for proc in procedimentos:
            if not proc.get('id'):
                return {"msg": "Todos os procedimentos devem ter um ID válido."}, 400

        if tipo not in ['plano', 'particular']:
            return {"msg": "Tipo deve ser 'plano' ou 'particular'"}, 400

        if tipo == 'plano' and not numero_plano:
            return {"msg": "Número do plano de saúde é obrigatório para atendimentos do tipo plano."}, 400

        if tipo == 'particular' and numero_plano:
            return {"msg": "Número do plano de saúde não deve ser informado para atendimentos particulares."}, 400

        # Validar se o paciente existe
        paciente = self.paciente_dao.obterPacientePorId(paciente_id)
        if not paciente:
            return {"msg": f"Paciente com ID {paciente_id} não encontrado."}, 404

        # Validar existência dos procedimentos (apenas IDs são necessários)
        for proc in procedimentos:
            proc_id = proc.get('id')
            procedimento = self.procedimento_dao.obterProcedimentoPorId(proc_id)
            if not procedimento:
                return {"msg": f"Procedimento com ID {proc_id} não encontrado."}, 404

        # Criar atendimento (valorTotal será consultado dinamicamente nas consultas)
        atendimento_id = self.atendimento_dao.criar_atendimento_db(
            data, paciente_id, procedimentos, tipo, numero_plano, usuario_id_destino, 0
        )

        # Recuperar atendimento recém-criado com valorTotal calculado por SUM
        new_id = atendimento_id["id"] if isinstance(atendimento_id, dict) else atendimento_id
        atendimento = self.atendimento_dao.obter_atendimento_por_id(new_id)
        return {"msg": "Atendimento criado com sucesso", "id": new_id, "atendimento": atendimento}, 201

    def atualizar_atendimento(self, token: str, atendimento_id: int, data_request):
        usuario_id = decode_token(token)
        if not usuario_id:
            return {"msg": "Token inválido"}, 401

        usuario = self.usuario_dao.obterUsuarioId(usuario_id)
        if not usuario:
            return {"msg": "Usuário não encontrado"}, 404

        atendimento = self.atendimento_dao.obter_atendimento_por_id(atendimento_id)
        if not atendimento:
            return {"msg": "Atendimento não encontrado."}, 404

        if usuario.get('tipo') != TipoUsuario.ADMIN.value and atendimento['idUsuario'] != usuario_id:
            return {"msg": "Você não tem permissão para editar este atendimento."}, 403

        # Validar campos obrigatórios
        data = data_request.get('data')
        paciente_id = data_request.get('paciente_id')
        procedimentos = data_request.get('procedimentos')
        tipo = data_request.get('tipo')
        numero_plano = data_request.get('numero_plano')
        novo_usuario_id = data_request.get('usuario_id')  # Permitir especificar usuário destino

        # REGRA: Apenas ADMIN pode transferir atendimentos
        eh_admin = usuario.get('tipo') == TipoUsuario.ADMIN.value

        if novo_usuario_id is not None:
            # Se especificou usuario_id mas não é admin, bloquear
            if not eh_admin:
                return {"msg": "Apenas administradores podem transferir atendimentos para outros usuários."}, 403

            # Validar se o usuário destino existe
            usuario_destino = self.usuario_dao.obterUsuarioId(novo_usuario_id)
            if not usuario_destino:
                return {"msg": f"Usuário destino com ID {novo_usuario_id} não encontrado."}, 404
        else:
            # Se não especificou usuário destino, mantém o original
            novo_usuario_id = atendimento.get('idUsuario')

        # Verificar permissão de edição (admin ou dono original)
        if not eh_admin and atendimento.get('idUsuario') != usuario_id:
            return {"msg": "Você não tem permissão para editar este atendimento."}, 403

        if not all([data, paciente_id, tipo]):
            return {"msg": "Data, paciente_id e tipo são campos obrigatórios"}, 400

        if not procedimentos or len(procedimentos) == 0:
            return {"msg": "O atendimento deve possuir pelo menos um procedimento."}, 400

        if tipo not in ['plano', 'particular']:
            return {"msg": "Tipo deve ser 'plano' ou 'particular'"}, 400

        if tipo == 'plano' and not numero_plano:
            return {"msg": "Número do plano de saúde é obrigatório para atendimentos do tipo plano."}, 400

        if tipo == 'particular' and numero_plano:
            return {"msg": "Número do plano de saúde não deve ser informado para atendimentos particulares."}, 400

        # Validar se o paciente existe
        paciente = self.paciente_dao.obterPacientePorId(paciente_id)
        if not paciente:
            return {"msg": f"Paciente com ID {paciente_id} não encontrado."}, 404

        # Validar existência dos procedimentos (apenas IDs são necessários)
        for proc in procedimentos:
            proc_id = proc.get('id')
            procedimento = self.procedimento_dao.obterProcedimentoPorId(proc_id)
            if not procedimento:
                return {"msg": f"Procedimento com ID {proc_id} não encontrado."}, 404

        self.atendimento_dao.atualizar_atendimento_db(
            atendimento_id, data, paciente_id, procedimentos, tipo, numero_plano, novo_usuario_id, 0
        )

        # Recuperar atendimento atualizado com valorTotal calculado por SUM
        atendimento_atualizado = self.atendimento_dao.obter_atendimento_por_id(atendimento_id)

        # Mensagem personalizada se houve transferência
        if novo_usuario_id != atendimento.get('idUsuario'):
            return {"msg": f"Atendimento transferido para usuário {novo_usuario_id} e atualizado com sucesso", "atendimento": atendimento_atualizado}, 200
        else:
            return {"msg": "Atendimento atualizado com sucesso", "atendimento": atendimento_atualizado}, 200

    def remover_atendimento(self, token: str, atendimento_id: int):
        # Extrai automaticamente o ID do usuário do token
        usuario_id = decode_token(token)
        if not usuario_id:
            return {"msg": "Token inválido"}, 401

        usuario = self.usuario_dao.obterUsuarioId(usuario_id)
        if not usuario:
            return {"msg": "Usuário não encontrado"}, 404

        # Busca o atendimento
        atendimento = self.atendimento_dao.obter_atendimento_por_id(atendimento_id)
        if not atendimento:
            return {"msg": "Atendimento não encontrado."}, 404

        # Verifica permissões automaticamente
        eh_admin = usuario.get('tipo') == TipoUsuario.ADMIN.value
        eh_dono = atendimento.get('idUsuario') == usuario_id

        if not eh_admin and not eh_dono:
            return {
                "msg": f"Acesso negado. Você (ID: {usuario_id}) não pode deletar o atendimento do usuário {atendimento.get('idUsuario')}."
            }, 403

        self.atendimento_dao.remover_atendimento_db(atendimento_id)
        return {"msg": "Atendimento removido com sucesso"}, 200
