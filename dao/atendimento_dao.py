from utils.comandos_sql import Comandos
from models.atendimento import Atendimento
from datetime import datetime

class AtendimentoDao(Comandos):
    def obterQtdAtendimentosUsuario(self, id: int):
        self.conectar()
        atends = self.obterRegistro("SELECT COUNT(idUsuario) as total FROM atendimentos WHERE idUsuario=?", (id,))
        self.desconectar()
        return atends.get('total')

    def criarAtendimentoDB(self, data, paciente_id, procedimentos, tipo, numero_plano, usuario_id, valor_total):
        self.conectar()
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

    def atualizarAtendimentoDB(self, atendimento_id, data, paciente_id, procedimentos, tipo, numero_plano, usuario_id, valor_total):
        self.conectar()
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

    def removerAtendimentoDB(self, atendimento_id):
        self.conectar()
        self.cursor.execute("DELETE FROM Atendimento_Procedimento WHERE idAtendimento=?", (atendimento_id,))
        self.cursor.execute("DELETE FROM atendimentos WHERE id=?", (atendimento_id,))
        self.comitar()
        self.desconectar()
        return True
