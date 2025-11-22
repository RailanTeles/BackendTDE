class ProcedimentoService:
    def __init__(self):
        print(" ProcedimentoService inicializado!")

    def _get_dao(self):
        """Método interno para obter DAO"""
        from dao.procedimento_dao import ProcedimentoDao
        return ProcedimentoDao()

    def _verificar_admin(self, token: str) -> bool:
        """Verifica se o usuário é admin usando o contexto do Flask"""
        try:
            from flask import g
            from dao.usuario_dao import UsuarioDao
            
            print(" Verificando admin via contexto Flask...")
            
            user_id = g.get("user_id")
            print(f" User ID do contexto: {user_id}")
            
            if not user_id:
                print(" User ID não encontrado no contexto")
                return False
            
            # Buscar usuário no banco
            usuario_dao = UsuarioDao()
            usuario = usuario_dao.obterUsuarioId(user_id)
            
            if not usuario:
                print(" Usuário não encontrado no banco")
                return False
            
            tipo_usuario = usuario.get("tipo")
            print(f" Tipo do usuário: {tipo_usuario}")
            
            is_admin = tipo_usuario == "admin"
            print(f" É admin? {is_admin}")
            
            return is_admin
            
        except Exception as e:
            print(f" Erro ao verificar admin: {str(e)}")
            return False

    def obterProcedimentos(self, token: str, itensPorPagina: int = 10, pagina: int = 1):
        """
        Lista procedimentos de forma paginada.
        Qualquer usuário autenticado pode acessar.
        """
        try:
            print(f" Listando procedimentos - Página: {pagina}, Itens por página: {itensPorPagina}")
            dao = self._get_dao()
            resultado = dao.obterProcedimentos(itensPorPagina, pagina)
            return resultado, 200
        except Exception as e:
            return {"msg": f"Erro ao listar procedimentos: {str(e)}"}, 500

    def obterProcedimento(self, token: str, id: int):
        """
        Obtém um procedimento específico pelo ID.
        Qualquer usuário autenticado pode acessar.
        """
        try:
            print(f" Buscando procedimento ID: {id}")
            if not id or id <= 0:
                return {"msg": "ID do procedimento é obrigatório."}, 400

            dao = self._get_dao()
            proc = dao.obterProcedimentoPorId(id)
            if not proc:
                return {"msg": f"Procedimento com ID {id} não encontrado."}, 404
            return proc, 200
        except Exception as e:
            return {"msg": f"Erro ao buscar procedimento: {str(e)}"}, 500

    def adicionarProcedimento(self, token: str, dados: dict):
        """
        Adiciona um novo procedimento.
        Apenas administradores podem realizar esta ação.
        """
        try:
            print(f" Tentando adicionar procedimento...")
            print(f" Dados recebidos: {dados}")
            
            # Verificar se é admin
            if not self._verificar_admin(token):
                return {"msg": "Apenas administradores podem realizar esta ação."}, 403

            print(" Usuário é admin, continuando...")
            
            # Validações básicas
            nome = dados.get("nome", "").strip()
            desc = dados.get("desc", "").strip()
            valorPlano = dados.get("valorPlano")
            valorParticular = dados.get("valorParticular")

            if not nome:
                return {"msg": "O campo 'nome' é obrigatório."}, 400

            if valorPlano is None or valorParticular is None:
                return {"msg": "Campos 'valorPlano' e 'valorParticular' são obrigatórios."}, 400

            try:
                valorPlano = float(valorPlano)
                valorParticular = float(valorParticular)
                if valorPlano < 0 or valorParticular < 0:
                    return {"msg": "Valores não podem ser negativos."}, 400
            except (ValueError, TypeError):
                return {"msg": "Campos 'valorPlano' e 'valorParticular' devem ser números válidos."}, 400

            dao = self._get_dao()

            # Verificar se já existe procedimento com mesmo nome
            existente = dao.obterProcedimentoPorNome(nome)
            if existente:
                return {"msg": "Já existe um procedimento com esse nome."}, 409

            # Adicionar procedimento
            dados_para_dao = {
                "nome": nome,
                "desc": desc,
                "valorPlano": valorPlano,
                "valorParticular": valorParticular
            }
            
            print(f" Enviando dados para DAO: {dados_para_dao}")
            resultado = dao.adicionarProcedimento(dados_para_dao)
            return resultado, 201

        except Exception as e:
            return {"msg": f"Erro ao adicionar procedimento: {str(e)}"}, 500

    def alterarProcedimento(self, token: str, id: int, dados: dict):
        """
        Altera um procedimento existente.
        Apenas administradores podem realizar esta ação.
        """
        try:
            print(f" Tentando alterar procedimento ID: {id}")
            print(f" Dados recebidos: {dados}")
            
            # Verificar se é admin
            if not self._verificar_admin(token):
                return {"msg": "Apenas administradores podem realizar esta ação."}, 403

            print("✅ Usuário é admin, continuando...")
            
            if not id or id <= 0:
                return {"msg": "ID do procedimento é obrigatório."}, 400

            dao = self._get_dao()
            existente = dao.obterProcedimentoPorId(id)
            if not existente:
                return {"msg": f"Procedimento ID {id} não encontrado."}, 404

            nome_novo = dados.get("nome", "").strip()
            desc_novo = dados.get("desc", "").strip()
            valorPlano_novo = dados.get("valorPlano")
            valorParticular_novo = dados.get("valorParticular")

            if not nome_novo:
                nome_novo = existente.get("nome", "").strip()
            if not desc_novo:
                desc_novo = existente.get("desc", "").strip()
            if valorPlano_novo is None:
                valorPlano_novo = existente.get("valorPlano")
            if valorParticular_novo is None:
                valorParticular_novo = existente.get("valorParticular")

            if not nome_novo:
                return {"msg": "O campo 'nome' não pode estar vazio."}, 400

            try:
                valorPlano_novo = float(valorPlano_novo)
                valorParticular_novo = float(valorParticular_novo)
                if valorPlano_novo < 0 or valorParticular_novo < 0:
                    return {"msg": "Valores não podem ser negativos."}, 400
            except (ValueError, TypeError):
                return {"msg": "Campos 'valorPlano' e 'valorParticular' devem ser números válidos."}, 400

            outro_procedimento = dao.obterProcedimentoPorNome(nome_novo)
            if outro_procedimento and outro_procedimento.get("id") != id:
                return {"msg": "Já existe outro procedimento com esse nome."}, 409

            dados_para_dao = {
                "nome": nome_novo,
                "desc": desc_novo,
                "valorPlano": valorPlano_novo,
                "valorParticular": valorParticular_novo
            }
            
            print(f" Enviando dados para DAO: {dados_para_dao}")
            dao.alterarProcedimento(id, dados_para_dao)
            return {"msg": "Procedimento alterado com sucesso."}, 200

        except Exception as e:
            return {"msg": f"Erro ao alterar procedimento: {str(e)}"}, 500

    def deletarProcedimento(self, token: str, id: int):
        """
        Deleta um procedimento existente.
        Apenas administradores podem realizar esta ação.
        """
        try:
            print(f" Tentando deletar procedimento ID: {id}")
            
            # Verificar se é admin
            if not self._verificar_admin(token):
                return {"msg": "Apenas administradores podem realizar esta ação."}, 403

            print(" Usuário é admin, continuando...")
            
            if not id or id <= 0:
                return {"msg": "ID do procedimento é obrigatório."}, 400

            dao = self._get_dao()
            
            # O DAO faz todas as verificações internamente
            resultado = dao.deletarProcedimento(id)
            return {"msg": "Procedimento deletado com sucesso."}, 200

        except Exception as e:
            error_msg = str(e)
            print(f" Erro no delete: {error_msg}")
            
            # Tratamento específico de erros baseado nas mensagens do DAO
            if "não encontrado" in error_msg.lower():
                return {"msg": f"Procedimento ID {id} não encontrado."}, 404
            elif "em uso" in error_msg.lower():
                return {"msg": "Não é possível excluir: procedimento está em uso em atendimentos."}, 409
            else:
                return {"msg": f"Erro ao deletar procedimento: {error_msg}"}, 500