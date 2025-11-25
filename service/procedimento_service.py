from utils.jwt_util import decode_token
from dao.procedimento_dao import ProcedimentoDao
from models.usuario import TipoUsuario

class ProcedimentoService:
    def __init__(self):
        self.procedimento_dao = ProcedimentoDao()
        # ✅ UsuarioDao REMOVIDO conforme barema

    def _verificar_admin(self, token: str):
        """Verifica se o usuário é administrador usando apenas decode_token"""
        if not token:
            return {"msg": "Token não fornecido"}, 401
            
        # Remove 'Bearer ' se presente
        if token.startswith('Bearer '):
            token = token[7:]
        
        payload = decode_token(token)
        
        if not payload:
            return {"msg": "Token inválido ou expirado"}, 401
        
        # Verifica se o payload contém as informações de tipo de usuário
        if isinstance(payload, dict) and 'tipo' in payload:
            # Token retorna payload completo com tipo
            if payload.get('tipo') != TipoUsuario.ADMIN.value:
                return {"msg": "Acesso negado. Apenas administradores podem realizar esta ação."}, 403
        else:
            # Se o decode_token não retornar um payload com 'tipo', 
            # precisamos de uma abordagem alternativa
            return {"msg": "Token não contém informações de permissão adequadas"}, 401
        
        return None

    def _verificar_token_valido(self, token: str):
        """Verifica se o token é válido para operações básicas"""
        if not token:
            return {"msg": "Token não fornecido"}, 401
            
        if token.startswith('Bearer '):
            token = token[7:]
        
        payload = decode_token(token)
        if not payload:
            return {"msg": "Token inválido ou expirado"}, 401
            
        return None

    def obter_procedimentos(self, token: str, pagina: int = 1, itens_por_pagina: int = 2):
        # Verificar token válido
        erro_token = self._verificar_token_valido(token)
        if erro_token:
            return erro_token

        total = self.procedimento_dao.obter_total_procedimentos()
        total_paginas = (total // itens_por_pagina) + (1 if total % itens_por_pagina else 0)

        offset = (pagina - 1) * itens_por_pagina
        procedimentos_pagina = self.procedimento_dao.listar_procedimentos(offset, itens_por_pagina)

        resposta = {
            'pagina': pagina,
            'totalPaginas': total_paginas,
            'itensPorPagina': itens_por_pagina,
            'registrosTotais': total,
            'procedimentos': procedimentos_pagina or []
        }
        return resposta, 200

    def obter_procedimento(self, token: str, procedimento_id: int):
        erro_token = self._verificar_token_valido(token)
        if erro_token:
            return erro_token

        procedimento = self.procedimento_dao.obter_procedimento_por_id(procedimento_id)
        if not procedimento:
            return {"msg": "Procedimento não encontrado"}, 404

        return procedimento, 200

    def criar_procedimento(self, token: str, data_request):
        erro_admin = self._verificar_admin(token)
        if erro_admin:
            return erro_admin

        nome = data_request.get('nome', '').strip()
        desc = data_request.get('desc', '').strip()
        valor_plano = data_request.get('valorPlano')
        valor_particular = data_request.get('valorParticular')

        if not nome:
            return {"msg": "O campo 'nome' é obrigatório."}, 400

        if valor_plano is None or valor_particular is None:
            return {"msg": "Campos 'valorPlano' e 'valorParticular' são obrigatórios."}, 400

        if not isinstance(valor_plano, (int, float)) or not isinstance(valor_particular, (int, float)):
            return {"msg": "Campos 'valorPlano' e 'valorParticular' devem ser números válidos."}, 400

        if valor_plano < 0 or valor_particular < 0:
            return {"msg": "Valores não podem ser negativos."}, 400

        existente = self.procedimento_dao.obter_procedimento_por_nome(nome)
        if existente:
            return {"msg": "Já existe um procedimento com esse nome."}, 409

        procedimento_id = self.procedimento_dao.criar_procedimento_db(
            nome, desc, float(valor_plano), float(valor_particular)
        )

        return {
            "msg": "Procedimento criado com sucesso",
            "id": procedimento_id
        }, 201

    def atualizar_procedimento(self, token: str, procedimento_id: int, data_request):
        erro_admin = self._verificar_admin(token)
        if erro_admin:
            return erro_admin

        procedimento_existente = self.procedimento_dao.obter_procedimento_por_id(procedimento_id)
        if not procedimento_existente:
            return {"msg": f"Procedimento ID {procedimento_id} não encontrado."}, 404

        nome = data_request.get('nome', '').strip()
        desc = data_request.get('desc', '').strip()
        valor_plano = data_request.get('valorPlano')
        valor_particular = data_request.get('valorParticular')

        if not nome:
            nome = procedimento_existente.get('nome', '').strip()
        if not desc:
            desc = procedimento_existente.get('desc', '').strip()
        if valor_plano is None:
            valor_plano = procedimento_existente.get('valorPlano')
        if valor_particular is None:
            valor_particular = procedimento_existente.get('valorParticular')

        if not nome:
            return {"msg": "O campo 'nome' não pode estar vazio."}, 400

        if not isinstance(valor_plano, (int, float)) or not isinstance(valor_particular, (int, float)):
            return {"msg": "Campos 'valorPlano' e 'valorParticular' devem ser números válidos."}, 400

        if valor_plano < 0 or valor_particular < 0:
            return {"msg": "Valores não podem ser negativos."}, 400

        outro_procedimento = self.procedimento_dao.obter_procedimento_por_nome(nome)
        if outro_procedimento and outro_procedimento.get('id') != procedimento_id:
            return {"msg": "Já existe outro procedimento com esse nome."}, 409

        self.procedimento_dao.atualizar_procedimento_db(
            procedimento_id, nome, desc, float(valor_plano), float(valor_particular)
        )

        return {"msg": "Procedimento atualizado com sucesso"}, 200

    def remover_procedimento(self, token: str, procedimento_id: int):
        erro_admin = self._verificar_admin(token)
        if erro_admin:
            return erro_admin

        procedimento = self.procedimento_dao.obter_procedimento_por_id(procedimento_id)
        if not procedimento:
            return {"msg": f"Procedimento ID {procedimento_id} não encontrado."}, 404

        em_uso = self.procedimento_dao.verificar_procedimento_em_uso(procedimento_id)
        if em_uso:
            return {"msg": "Não é possível excluir: procedimento está em uso em atendimentos."}, 409

        self.procedimento_dao.remover_procedimento_db(procedimento_id)

        return {"msg": "Procedimento removido com sucesso"}, 200