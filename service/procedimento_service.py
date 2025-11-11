from dao.procedimento_dao import ProcedimentoDao
from dao.atendimento_dao import AtendimentoDao
from models.procedimento import Procedimento

class ProcedimentoService:
    def __init__(self):
        self.procedimentoDao = ProcedimentoDao()
        self.atendimentoDao = AtendimentoDao()

    def obter_procedimento(self, id: int):
        procedimento = self.procedimentoDao.obterProcedimentoPorId(id)
        if not procedimento:
            raise ValueError(f"Procedimento com ID {id} não encontrado.")
        return procedimento

    def obter_procedimento_por_nome(self, nome: str):
        procedimento = self.procedimentoDao.obterProcedimentoPorNome(nome)
        if not procedimento:
            raise ValueError(f"Procedimento com nome '{nome}' não encontrado.")
        return procedimento

    def listar_procedimentos(self, itens_por_pagina: int = 10, pagina: int = 1):
        resultado = self.procedimentoDao.obterProcedimentos(itens_por_pagina, pagina)
        if not resultado:
            raise ValueError(f"A página {pagina} está fora do limite de resultados disponíveis.")
        return resultado

    def adicionar_procedimento(self, dados: dict):
        procedimento = Procedimento(**dados)
        return self.procedimentoDao.adicionarProcedimento(procedimento)

    def alterar_procedimento(self, id: int, dados: dict):
        procedimento_existente = self.procedimentoDao.obterProcedimentoPorId(id)
        if not procedimento_existente:
            raise ValueError(f"Procedimento com ID {id} não encontrado.")

        procedimento = Procedimento(
            id=id,
            nome=dados.get("nome", procedimento_existente["nome"]),
            desc=dados.get("desc", procedimento_existente["desc"]),
            valorPlano=dados.get("valorPlano", procedimento_existente["valorPlano"]),
            valorParticular=dados.get("valorParticular", procedimento_existente["valorParticular"])
        )

        return self.procedimentoDao.alterarProcedimento(procedimento)

    def deletar_procedimento(self, id: int):
        procedimento = self.procedimentoDao.obterProcedimentoPorId(id)
        if not procedimento:
            raise ValueError(f"Procedimento com ID {id} não encontrado.")
        return self.procedimentoDao.deletarProcedimento(id)

    def listar_procedimentos_por_atendimento(self, atendimento_id: int):
        atendimento = self.atendimentoDao.obter_atendimento_por_id(atendimento_id)
        if not atendimento:
            raise ValueError(f"Atendimento com ID {atendimento_id} não encontrado.")

        procedimentos_ids = []
        if atendimento.get("procedimentos"):
            procedimentos_ids = [int(pid) for pid in atendimento["procedimentos"].split(",")]

        procedimentos = [
            self.procedimentoDao.obterProcedimentoPorId(proc_id)
            for proc_id in procedimentos_ids
        ]

        return [p for p in procedimentos if p]
