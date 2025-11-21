class ProcedimentoService:
    def __init__(self):
        print("✅ ProcedimentoService inicializado!")

    def _get_dao(self):
        """Método interno para obter DAO"""
        from dao.procedimento_dao import ProcedimentoDao
        return ProcedimentoDao()

    def obterProcedimentos(self, itensPorPagina: int = 10, pagina: int = 1):
        try:
            dao = self._get_dao()
            resultado = dao.obterProcedimentos(itensPorPagina, pagina)
            if resultado is None:
                return {"msg": f"A página {pagina} não possui resultados."}, 404
            return resultado, 200
        except Exception as e:
            return {"msg": f"Erro ao listar procedimentos: {str(e)}"}, 500

    def obterProcedimento(self, id: int):
        try:
            if not id or id <= 0:
                return {"msg": "ID do procedimento é obrigatório."}, 400

            dao = self._get_dao()
            proc = dao.obterProcedimentoPorId(id)
            if not proc:
                return {"msg": f"Procedimento com ID {id} não encontrado."}, 404
            return proc, 200
        except Exception as e:
            return {"msg": f"Erro ao buscar procedimento: {str(e)}"}, 500

    def adicionarProcedimento(self, dados: dict):
        try:
            # Validações básicas
            nome = dados.get("nome", "").strip()
            desc = dados.get("desc", "").strip()  # CORRETO: "desc"
            valorPlano = dados.get("valorPlano")
            valorParticular = dados.get("valorParticular")

            print(f"📥 Dados recebidos no Service: {dados}")  # DEBUG
            print(f"📥 Descrição recebida: '{desc}'")  # DEBUG

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

            # Adicionar procedimento - CORRETO: usando "desc"
            dados_para_dao = {
                "nome": nome,
                "desc": desc,  # CORRETO: "desc"
                "valorPlano": valorPlano,
                "valorParticular": valorParticular
            }
            
            print(f"📤 Dados enviados para DAO: {dados_para_dao}")  # DEBUG
            
            resultado = dao.adicionarProcedimento(dados_para_dao)

            return resultado, 201

        except Exception as e:
            return {"msg": f"Erro ao adicionar procedimento: {str(e)}"}, 500

    def alterarProcedimento(self, id: int, dados: dict):
        try:
            if not id or id <= 0:
                return {"msg": "ID do procedimento é obrigatório."}, 400

            dao = self._get_dao()
            existente = dao.obterProcedimentoPorId(id)
            if not existente:
                return {"msg": f"Procedimento ID {id} não encontrado."}, 404

            nome_novo = dados.get("nome", "").strip()
            desc_novo = dados.get("desc", "").strip()  # CORRETO: "desc"
            valorPlano_novo = dados.get("valorPlano")
            valorParticular_novo = dados.get("valorParticular")

            if not nome_novo:
                nome_novo = existente.get("nome", "").strip()
            if not desc_novo:
                desc_novo = existente.get("desc", "").strip()  # CORRETO: "desc"
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
                "desc": desc_novo,  # CORRETO: "desc"
                "valorPlano": valorPlano_novo,
                "valorParticular": valorParticular_novo
            }
            
            dao.alterarProcedimento(id, dados_para_dao)

            return {"msg": "Procedimento alterado com sucesso."}, 200

        except Exception as e:
            return {"msg": f"Erro ao alterar procedimento: {str(e)}"}, 500

    def deletarProcedimento(self, id: int):
        try:
            if not id or id <= 0:
                return {"msg": "ID do procedimento é obrigatório."}, 400

            dao = self._get_dao()
            existente = dao.obterProcedimentoPorId(id)
            if not existente:
                return {"msg": f"Procedimento ID {id} não encontrado."}, 404

            em_uso = dao.verificarProcedimentoEmUso(id)
            if em_uso:
                return {"msg": "Não é possível excluir: procedimento está em uso em atendimentos."}, 409

            dao.deletarProcedimento(id)
            return {"msg": "Procedimento deletado com sucesso."}, 200

        except Exception as e:
            return {"msg": f"Erro ao deletar procedimento: {str(e)}"}, 500