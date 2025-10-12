# Serviço de regras de negócio para Atendimentos
from utils.jwt_util import decode_token
from dao.atendimento_dao import AtendimentoDao
from models.usuario import TipoUsuario


class AtendimentoService:

    def obterAtendimentosPorData(self, token: str, data_inicio: str, data_fim: str, pagina: int = 1, itens_por_pagina: int = 10):
        """
        Retorna lista paginada de atendimentos entre duas datas informadas (inclusive).
        Apenas usuários autenticados. Admin vê todos, default vê apenas os próprios.
        """
        try:
            usuario_id = decode_token(token)
            if not usuario_id:
                return {"msg": "Token inválido"}, 401
            from dao.usuario_dao import UsuarioDao
            usuarioDao = UsuarioDao()
            usuario = usuarioDao.obterUsuarioId(usuario_id)
            if not usuario:
                return {"msg": "Usuário não encontrado"}, 404
            # Validação simples das datas (YYYY-MM-DD)
            from datetime import datetime
            try:
                dt_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
                dt_fim = datetime.strptime(data_fim, "%Y-%m-%d")
            except Exception:
                return {"msg": "Formato de data inválido. Use YYYY-MM-DD."}, 400
            if dt_inicio > dt_fim:
                return {"msg": "Data inicial não pode ser maior que a final."}, 400
            offset = (pagina - 1) * itens_por_pagina
            atendimentos = self.atendimentoDao.listarAtendimentosPorData(data_inicio, data_fim, offset, itens_por_pagina)
            # Se não for admin, filtra só os próprios
            if usuario.get('tipo') != TipoUsuario.ADMIN.value:
                atendimentos = [a for a in atendimentos if a['idUsuario'] == usuario_id]
            total = len(atendimentos)
            total_paginas = (total // itens_por_pagina) + (1 if total % itens_por_pagina else 0)
            resposta = {
                'pagina': pagina,
                'itens_por_pagina': itens_por_pagina,
                'total': total,
                'total_paginas': total_paginas,
                'atendimentos': atendimentos
            }
            return resposta, 200
        except Exception as e:
            return {"msg": str(e)}, 500
    def __init__(self):
        """Inicializa o service com o DAO de atendimento."""
        self.atendimentoDao = AtendimentoDao()

    def obterAtendimento(self, token: str, atendimento_id: int):
        """
        Retorna um atendimento pelo ID, se o usuário for admin ou dono.
        """
        try:
            usuario_id = decode_token(token)
            if not usuario_id:
                return {"msg": "Token inválido"}, 401
            from dao.usuario_dao import UsuarioDao
            usuarioDao = UsuarioDao()
            usuario = usuarioDao.obterUsuarioId(usuario_id)
            if not usuario:
                return {"msg": "Usuário não encontrado"}, 404
            atendimento = self.atendimentoDao.obterAtendimentoPorId(atendimento_id)
            if not atendimento:
                return {"msg": "Atendimento não encontrado"}, 404
            # Permissão: admin ou dono
            if usuario.get('tipo') != TipoUsuario.ADMIN.value and atendimento['idUsuario'] != usuario_id:
                return {"msg": "Você não tem permissão para ver este atendimento."}, 403
            return atendimento, 200
        except Exception as e:
            return {"msg": str(e)}, 500

    def obterAtendimentos(self, token: str, pagina: int = 1, itens_por_pagina: int = 10):
        """
        Retorna lista paginada de atendimentos do usuário logado (ou todos se admin).
        """
        try:
            usuario_id = decode_token(token)
            if not usuario_id:
                return {"msg": "Token inválido"}, 401
            from dao.usuario_dao import UsuarioDao
            usuarioDao = UsuarioDao()
            usuario = usuarioDao.obterUsuarioId(usuario_id)
            if not usuario:
                return {"msg": "Usuário não encontrado"}, 404
            todos = self.atendimentoDao.listarAtendimentos()
            if usuario.get('tipo') != TipoUsuario.ADMIN.value:
                todos = [a for a in todos if a['idUsuario'] == usuario_id]
            total = len(todos)
            total_paginas = (total // itens_por_pagina) + (1 if total % itens_por_pagina else 0)
            inicio = (pagina - 1) * itens_por_pagina
            fim = inicio + itens_por_pagina
            atendimentos_pagina = todos[inicio:fim]
            resposta = {
                'pagina': pagina,
                'itens_por_pagina': itens_por_pagina,
                'total': total,
                'total_paginas': total_paginas,
                'atendimentos': atendimentos_pagina
            }
            return resposta, 200
        except Exception as e:
            return {"msg": str(e)}, 500

    def criarAtendimento(self, token: str, data_request):
        """
        Cria um novo atendimento. Apenas admin pode criar para outro usuário (usuario_id no JSON).
        """
        try:
            usuario_id = decode_token(token)
            if not usuario_id:
                return {"msg": "Token inválido"}, 401
            from dao.usuario_dao import UsuarioDao
            usuarioDao = UsuarioDao()
            usuario = usuarioDao.obterUsuarioId(usuario_id)
            if not usuario:
                return {"msg": "Usuário não encontrado"}, 404
            usuario_id_destino = data_request.get('usuario_id')
            eh_admin = usuario.get('tipo') == TipoUsuario.ADMIN.value
            if usuario_id_destino is not None:
                if not eh_admin:
                    return {"msg": "Apenas administradores podem criar atendimentos para outros usuários."}, 403
                usuario_destino = usuarioDao.obterUsuarioId(usuario_id_destino)
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
            from dao.paciente_dao import PacienteDao
            pacienteDao = PacienteDao()
            paciente = pacienteDao.obterPacientePorId(paciente_id)
            if not paciente:
                return {"msg": f"Paciente com ID {paciente_id} não encontrado."}, 404
            valor_total = 0
            for proc in procedimentos:
                if tipo == 'plano':
                    valor_total += proc['valorPlano']
                else:
                    valor_total += proc['valorParticular']
            atendimento_id = self.atendimentoDao.criarAtendimentoDB(data, paciente_id, procedimentos, tipo, numero_plano, usuario_id_destino, valor_total)
            return {"msg": "Atendimento criado com sucesso", "id": atendimento_id}, 201
        except Exception as e:
            return {"msg": str(e)}, 500

    def atualizarAtendimento(self, token: str, atendimento_id: int, data_request):
        try:
            usuario_id = decode_token(token)
            if not usuario_id:
                return {"msg": "Token inválido"}, 401
            
            from dao.usuario_dao import UsuarioDao
            usuarioDao = UsuarioDao()
            usuario = usuarioDao.obterUsuarioId(usuario_id)
            
            if not usuario:
                return {"msg": "Usuário não encontrado"}, 404
            
            atendimento = self.atendimentoDao.obterAtendimentoPorId(atendimento_id)
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
                from dao.usuario_dao import UsuarioDao
                usuarioDao = UsuarioDao()
                usuario_destino = usuarioDao.obterUsuarioId(novo_usuario_id)
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
            from dao.paciente_dao import PacienteDao
            pacienteDao = PacienteDao()
            paciente = pacienteDao.obterPacientePorId(paciente_id)
            if not paciente:
                return {"msg": f"Paciente com ID {paciente_id} não encontrado."}, 404
            
            valor_total = 0
            for proc in procedimentos:
                if tipo == 'plano':
                    valor_total += proc['valorPlano']
                else:
                    valor_total += proc['valorParticular']
                    
            self.atendimentoDao.atualizarAtendimentoDB(atendimento_id, data, paciente_id, procedimentos, tipo, numero_plano, novo_usuario_id, valor_total)
            
            # Mensagem personalizada se houve transferência
            if novo_usuario_id != atendimento.get('idUsuario'):
                return {"msg": f"Atendimento transferido para usuário {novo_usuario_id} e atualizado com sucesso"}, 200
            else:
                return {"msg": "Atendimento atualizado com sucesso"}, 200
        except Exception as e:
            return {"msg": str(e)}, 500

    def removerAtendimento(self, token: str, atendimento_id: int):
        try:
            # Extrai automaticamente o ID do usuário do token
            usuario_id = decode_token(token)
            if not usuario_id:
                return {"msg": "Token inválido"}, 401
            
            from dao.usuario_dao import UsuarioDao
            usuarioDao = UsuarioDao()
            usuario = usuarioDao.obterUsuarioId(usuario_id)
            
            if not usuario:
                return {"msg": "Usuário não encontrado"}, 404
            
            # Busca o atendimento
            atendimento = self.atendimentoDao.obterAtendimentoPorId(atendimento_id)
            if not atendimento:
                return {"msg": "Atendimento não encontrado."}, 404
            
            # Verifica permissões automaticamente
            eh_admin = usuario.get('tipo') == TipoUsuario.ADMIN.value
            eh_dono = atendimento.get('idUsuario') == usuario_id
            
            if not eh_admin and not eh_dono:
                return {
                    "msg": f"Acesso negado. Você (ID: {usuario_id}) não pode deletar o atendimento do usuário {atendimento.get('idUsuario')}."
                }, 403
                
            self.atendimentoDao.removerAtendimentoDB(atendimento_id)
            return {"msg": "Atendimento removido com sucesso"}, 200
            
        except Exception as e:
            return {"msg": str(e)}, 500
