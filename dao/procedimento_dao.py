import math
from utils.comandos_sql import Comandos
from models.procedimento import Procedimento

class ProcedimentoDao(Comandos):

    def obterProcedimentoPorId(self, id: int):
        self.conectar()
        procedimento = self.obterRegistro("SELECT * FROM Procedimentos WHERE id=?", (id, ))
        self.desconectar()
        return procedimento
    
    def obterProcedimentoPorNome(self, nome: str):
        self.conectar()
        procedimento = self.obterRegistro("SELECT * FROM Procedimentos WHERE nome=?", (nome, ))
        self.desconectar()
        return procedimento
    
    def obterProcedimentos(self, itensPorPagina: int, pagina: int):
        self.conectar()
        desvio = itensPorPagina * (pagina - 1)
        procedimentos = self.obterRegistros("SELECT * FROM Procedimentos ORDER BY nome ASC LIMIT ? OFFSET ?", (itensPorPagina, desvio))
        procedimentosTotais = self.obterRegistro("SELECT COUNT(id) as total FROM Procedimentos")
        procedimentosTotais = procedimentosTotais.get('total') if procedimentosTotais else 0
        totalPaginas = math.ceil(procedimentosTotais / itensPorPagina) if procedimentosTotais else 1
        self.desconectar()

        if pagina > totalPaginas and totalPaginas > 0:
            return None

        return {
            "pagina": pagina,
            "totalPaginas": totalPaginas,
            "itensPorPagina": itensPorPagina,
            "procedimentosTotais": procedimentosTotais,
            "procedimentos": procedimentos
        }
    
    def adicionarProcedimento(self, procedimento: Procedimento):
        """Adiciona um novo procedimento ao banco de dados"""
        self.conectar()
        
        self.obterRegistro("INSERT INTO Procedimentos (nome, desc, valorPlano, valorParticular) VALUES (?, ?, ?, ?)", 
                           (procedimento.nome, procedimento.desc, procedimento.valorPlano, procedimento.valorParticular))
        self.comitar()
        self.desconectar()
        return {"msg": "Procedimento adicionado com sucesso"}

    def alterarProcedimento(self, procedimento: Procedimento):
        """Altera os dados de um procedimento existente"""
        self.conectar()
        
        self.obterRegistro("UPDATE Procedimentos SET nome=?, desc=?, valorPlano=?, valorParticular=? WHERE id=?", 
                           (procedimento.nome, procedimento.desc, procedimento.valorPlano, procedimento.valorParticular, procedimento.id))
        self.comitar()
        self.desconectar()
        return {"msg": "Procedimento alterado com sucesso"}
    
    def deletarProcedimento(self, id: int):
        """Deleta um procedimento do banco de dados pelo seu id"""
        self.conectar()
        self.obterRegistro("DELETE FROM Procedimentos WHERE id=?", (id, ))
        self.comitar()
        self.desconectar()
        return {"msg": "Procedimento deletado com sucesso"}