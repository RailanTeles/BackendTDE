from utils.comandos_sql import Comandos
from models.atendimento import Atendimento
from datetime import datetime

class AtendimentoDao(Comandos):
    def obterQtdAtendimentosUsuario(self, id: int):
        """Verifica se um usuário tem atendimentos pelo id. Retorna a quantidade de atendimentos."""
        self.conectar()
        atends = self.obterRegistro("SELECT COUNT(idUsuario) as total FROM atendimentos WHERE idUsuario=?", (id,))
        self.desconectar()
        return atends.get('total')

    def criarAtendimento(self, data, paciente_id, procedimentos, tipo, numero_plano, usuario_id):
        if not procedimentos or len(procedimentos) == 0:
            raise Exception("O atendimento deve possuir pelo menos um procedimento.")
        if tipo == 'plano' and not numero_plano:
            raise Exception("Número do plano de saúde é obrigatório para atendimentos do tipo plano.")
        if tipo == 'particular' and numero_plano:
            raise Exception("Número do plano de saúde não deve ser informado para atendimentos particulares.")
        self.conectar()
        valor_total = 0
        for proc in procedimentos:
            if tipo == 'plano':
                valor_total += proc['valorPlano']
            else:
                valor_total += proc['valorParticular']
        atendimento_query = """
            INSERT INTO atendimentos (data, idPaciente, tipo, numeroPlano, idUsuario, valorTotal)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(atendimento_query, (data, paciente_id, tipo, numero_plano, usuario_id, valor_total))
        atendimento_id = self.cursor.lastrowid
        for proc in procedimentos:
            self.cursor.execute(
                "INSERT INTO Atendimento_Procedimento (idAtendimento, idProcedimento) VALUES (?, ?)",
                (atendimento_id, proc['id'])
            )
        self.comitar()
        self.desconectar()
        return atendimento_id

    def listarAtendimentos(self):
        self.conectar()
        query = '''
            SELECT a.*, GROUP_CONCAT(ap.idProcedimento) as procedimentos
            FROM atendimentos a
            LEFT JOIN Atendimento_Procedimento ap ON a.id = ap.idAtendimento
            GROUP BY a.id
        '''
        atendimentos = self.obterRegistros(query)
        self.desconectar()
        return atendimentos

    def obterAtendimentoPorId(self, atendimento_id):
        self.conectar()
        query = '''
            SELECT a.*, GROUP_CONCAT(ap.idProcedimento) as procedimentos
            FROM atendimentos a
            LEFT JOIN Atendimento_Procedimento ap ON a.id = ap.idAtendimento
            WHERE a.id = ?
            GROUP BY a.id
        '''
        atendimento = self.obterRegistro(query, (atendimento_id,))
        self.desconectar()
        return atendimento

    def atualizarAtendimento(self, atendimento_id, data, paciente_id, procedimentos, tipo, numero_plano, usuario_id, usuario_tipo):
        atendimento = self.obterAtendimentoPorId(atendimento_id)
        if not atendimento:
            raise Exception("Atendimento não encontrado.")
        if usuario_tipo != 'admin' and atendimento['idUsuario'] != usuario_id:
            raise Exception("Você não tem permissão para editar este atendimento.")
        if not procedimentos or len(procedimentos) == 0:
            raise Exception("O atendimento deve possuir pelo menos um procedimento.")
        if tipo == 'plano' and not numero_plano:
            raise Exception("Número do plano de saúde é obrigatório para atendimentos do tipo plano.")
        if tipo == 'particular' and numero_plano:
            raise Exception("Número do plano de saúde não deve ser informado para atendimentos particulares.")
        self.conectar()
        valor_total = 0
        for proc in procedimentos:
            if tipo == 'plano':
                valor_total += proc['valorPlano']
            else:
                valor_total += proc['valorParticular']
        update_query = '''
            UPDATE atendimentos SET data=?, idPaciente=?, tipo=?, numeroPlano=?, idUsuario=?, valorTotal=? WHERE id=?
        '''
        self.cursor.execute(update_query, (data, paciente_id, tipo, numero_plano, usuario_id, valor_total, atendimento_id))
        self.cursor.execute("DELETE FROM Atendimento_Procedimento WHERE idAtendimento=?", (atendimento_id,))
        for proc in procedimentos:
            self.cursor.execute(
                "INSERT INTO Atendimento_Procedimento (idAtendimento, idProcedimento) VALUES (?, ?)",
                (atendimento_id, proc['id'])
            )
        self.comitar()
        self.desconectar()
        return True

    def removerAtendimento(self, atendimento_id, usuario_id, usuario_tipo):
        atendimento = self.obterAtendimentoPorId(atendimento_id)
        if not atendimento:
            raise Exception("Atendimento não encontrado.")
        if usuario_tipo != 'admin' and atendimento['idUsuario'] != usuario_id:
            raise Exception("Você não tem permissão para remover este atendimento.")
        self.conectar()
        self.cursor.execute("DELETE FROM Atendimento_Procedimento WHERE idAtendimento=?", (atendimento_id,))
        self.cursor.execute("DELETE FROM atendimentos WHERE id=?", (atendimento_id,))
        self.comitar()
        self.desconectar()
        return True
