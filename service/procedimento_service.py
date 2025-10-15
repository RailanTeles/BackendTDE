# service/procedimento_service.py

from dao.procedimento_dao import ProcedimentoDao
from models.procedimento import Procedimento
from dao.atendimento_dao import AtendimentoDao

class ProcedimentoService:
    def __init__(self):
        self.procedimentoDao = ProcedimentoDao()
        self.atendimentoDao = AtendimentoDao()

    def _validar_dados(self, data: dict, id_existente: int = None):
        """
        Método auxiliar privado para validar e processar os dados de um procedimento.
        Levanta ValueError em caso de qualquer problema.
        Retorna os dados limpos e convertidos se tudo estiver correto.
        """
        nome = data.get('nome')
        desc = data.get('desc')
        valorPlano = data.get('valorPlano')
        valorParticular = data.get('valorParticular')

        # 1. Validação de campos obrigatórios
        if not all([nome, desc, valorPlano is not None, valorParticular is not None]):
            raise ValueError("Todos os campos são obrigatórios: 'nome', 'desc', 'valorPlano', 'valorParticular'")
        
        # 2. Validação e conversão dos valores numéricos
        try:
            valor_plano_float = float(valorPlano)
            valor_particular_float = float(valorParticular)
        except (TypeError, ValueError):
            raise ValueError("Os campos 'valorPlano' e 'valorParticular' devem ser números válidos")

        # 3. Validação de valores negativos
        if valor_plano_float < 0 or valor_particular_float < 0:
            raise ValueError("Os valores não podem ser negativos")

        # 4. Validação de nome único
        procedimento_existente = self.procedimentoDao.obterProcedimentoPorNome(nome)
        # Se um procedimento com esse nome existe E não é o mesmo que estamos editando
        if procedimento_existente and (id_existente is None or procedimento_existente.get("id") != id_existente):
            raise ValueError(f"O procedimento com o nome '{nome}' já existe")
            
        return nome, desc, valor_plano_float, valor_particular_float

    def obterProcedimento(self, id: int):
        procedimento = self.procedimentoDao.obterProcedimentoPorId(id)
        if not procedimento:
            raise ValueError("Procedimento não encontrado")
        return procedimento

    def obterProcedimentos(self, itensPorPagina: int, pagina: int):
        resposta = self.procedimentoDao.obterProcedimentos(itensPorPagina, pagina)
        if not resposta:
            raise ValueError("Página não disponível")
        return resposta

    def adicionarProcedimento(self, data: dict):
        # Chama o método de validação. Se algo estiver errado, ele levantará um erro.
        nome, desc, valor_plano, valor_particular = self._validar_dados(data)

        procedimento = Procedimento(id=0, nome=nome, desc=desc, valorPlano=valor_plano, valorParticular=valor_particular)
        return self.procedimentoDao.adicionarProcedimento(procedimento)

    def alterarProcedimento(self, id: int, data: dict):
        if not self.procedimentoDao.obterProcedimentoPorId(id):
            raise ValueError("Procedimento não encontrado")

        # Chama o método de validação, passando o ID do procedimento que estamos editando
        nome, desc, valor_plano, valor_particular = self._validar_dados(data, id_existente=id)

        procedimento_editado = Procedimento(id=id, nome=nome, desc=desc, valorPlano=valor_plano, valorParticular=valor_particular)
        return self.procedimentoDao.alterarProcedimento(procedimento_editado)

    def deletarProcedimento(self, id: int):
        if not self.procedimentoDao.obterProcedimentoPorId(id):
            raise ValueError("Procedimento não encontrado")

        atendimentos_usando = self.atendimentoDao.verificarUsoDoProcedimento(id)
        if atendimentos_usando > 0:
            raise ValueError("Este procedimento está vinculado a atendimentos e não pode ser removido.")

        return self.procedimentoDao.deletarProcedimento(id)