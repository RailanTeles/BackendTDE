from dao.procedimento_dao import ProcedimentoDao
from dao.atendimento_dao import AtendimentoDao
from models.procedimento import Procedimento

class ProcedimentoService:
    def _init_(self):
        self.procedimentoDao = ProcedimentoDao()
        self.atendimentoDao = AtendimentoDao()

    def obterProcedimento(self, id: int):
        procedimento = self.procedimentoDao.obterProcedimentoPorId(id)
        if not procedimento:
            return {"msg": "Procedimento não encontrado"}, 404
        return procedimento, 200

    def obterProcedimentos(self, itensPorPagina: int, pagina: int):
        resposta = self.procedimentoDao.obterProcedimentos(itensPorPagina, pagina)
        if not resposta:
            return {"msg": "Página não disponível"}, 404
        return resposta, 200

    def adicionarProcedimento(self, data: dict):
        nome = data.get('nome')
        desc = data.get('desc')
        valorPlano = data.get('valorPlano')
        valorParticular = data.get('valorParticular')

        if not ([nome, desc, valorPlano is not None, valorParticular is not None]):
            return {"msg": "Os campos 'nome', 'desc', 'valorPlano' e 'valorParticular' são obrigatórios"}, 400
        
        valor_plano_float = float(valorPlano)
        valor_particular_float = float(valorParticular)
        
        if valor_plano_float < 0 or valor_particular_float < 0:
            return {"msg": "Os valores não podem ser negativos"}, 400

        procedimento_existente = self.procedimentoDao.obterProcedimentoPorNome(nome)
        if procedimento_existente:
            return {"msg": f"O procedimento com o nome '{nome}' já existe"}, 409

        procedimento = Procedimento(id=0, nome=nome, desc=desc, valorPlano=valor_plano_float, valorParticular=valor_particular_float)
        self.procedimentoDao.adicionarProcedimento(procedimento)
        
        return {"msg": "Procedimento adicionado com sucesso"}, 201

    def alterarProcedimento(self, id: int, data: dict):
        procedimento_atual = self.procedimentoDao.obterProcedimentoPorId(id)
        if not procedimento_atual:
            return {"msg": "Procedimento não encontrado"}, 404

        nome = data.get('nome')
        desc = data.get('desc')
        valorPlano = data.get('valorPlano')
        valorParticular = data.get('valorParticular')

        if not ([nome, desc, valorPlano is not None, valorParticular is not None]):
            return {"msg": "Os campos 'nome', 'desc', 'valorPlano' e 'valorParticular' são obrigatórios"}, 400
            
        valor_plano_float = float(valorPlano)
        valor_particular_float = float(valorParticular)
        
        if valor_plano_float < 0 or valor_particular_float < 0:
            return {"msg": "Os valores não podem ser negativos"}, 400

        procedimento_existente = self.procedimentoDao.obterProcedimentoPorNome(nome)
        if procedimento_existente and procedimento_existente.get("id") != id:
            return {"msg": f"Já existe outro procedimento com o nome '{nome}'"}, 409

        procedimento_editado = Procedimento(id=id, nome=nome, desc=desc, valorPlano=valor_plano_float, valorParticular=valor_particular_float)
        self.procedimentoDao.alterarProcedimento(procedimento_editado)
        
        return {"msg": "Procedimento alterado com sucesso"}, 200

    def deletarProcedimento(self, id: int):
        procedimento = self.procedimentoDao.obterProcedimentoPorId(id)
        if not procedimento:
            return {"msg": "Procedimento não encontrado"}, 404

        atendimento_com_procedimento = self.atendimentoDao.verificarProcedimentoEmUso(id)
        if atendimento_com_procedimento:
            return {"msg": "Não é possível remover um procedimento que foi utilizado em algum atendimento"}, 409

        self.procedimentoDao.deletarProcedimento(id)
        return {"msg": "Procedimento deletado com sucesso"}, 200