from utils.comandos_sql import Comandos
from models.atendimento import Atendimento
from datetime import datetime
class AtendimentoDao(Comandos):
    def listarAtendimentosPorData(self, data_inicio, data_fim, offset=0, limit=10):
        self.conectar()
        query = '''
            SELECT a.*, GROUP_CONCAT(ap.idProcedimento) as procedimentos
            FROM atendimentos a
            LEFT JOIN Atendimento_Procedimento ap ON a.id = ap.idAtendimento
            WHERE date(a.data) BETWEEN date(?) AND date(?)
            GROUP BY a.id
            ORDER BY a.data
            LIMIT ? OFFSET ?
        '''
        atendimentos = self.obterRegistros(query, (data_inicio, data_fim, limit, offset))
        self.desconectar()
        return atendimentos
    def obterQtdAtendimentosUsuario(self, id: int):
        """Retorna a quantidade de atendimentos de um usuário."""
        self.conectar()
        atends = self.obterRegistro("SELECT COUNT(idUsuario) as total FROM atendimentos WHERE idUsuario=?", (id,))
        self.desconectar()
        return atends.get('total')
    
    def obterQtdAtendimentosPaciente(self, id: int):
        """Retorna a quantidade de atendimentos de um paciente."""
        self.conectar()
        atends = self.obterRegistro("SELECT COUNT(idPaciente) as total FROM atendimentos WHERE idPaciente=?", (id,))
        self.desconectar()
        return atends.get('total')
    
    def criarAtendimentoDB(self, data, paciente_id, procedimentos, tipo, numero_plano, usuario_id, valor_total):
        """Cria um atendimento e vincula procedimentos."""
        try:
            self.conectar()
            self.cursor.execute(
                "INSERT INTO atendimentos (data, idPaciente, tipo, numeroPlano, idUsuario, valorTotal) VALUES (?, ?, ?, ?, ?, ?)",
                (data, paciente_id, tipo, numero_plano, usuario_id, valor_total)
            )
            atendimento_id = self.cursor.lastrowid
            ids_vistos = set()
            for proc in procedimentos:
                proc_id = proc['id']
                if proc_id not in ids_vistos:
                    self.cursor.execute(
                        "INSERT INTO Atendimento_Procedimento (idAtendimento, idProcedimento) VALUES (?, ?)",
                        (atendimento_id, proc_id)
                    )
                    ids_vistos.add(proc_id)
            self.comitar()
            return atendimento_id
        finally:
            self.desconectar()
    def listarAtendimentos(self):
        """Lista todos os atendimentos."""
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
        """Obtém um atendimento pelo ID."""
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
        """Atualiza um atendimento."""
        try:
            self.conectar()
            self.cursor.execute(
                "UPDATE atendimentos SET data=?, idPaciente=?, tipo=?, numeroPlano=?, idUsuario=?, valorTotal=? WHERE id=?",
                (data, paciente_id, tipo, numero_plano, usuario_id, valor_total, atendimento_id)
            )
            self.cursor.execute("DELETE FROM Atendimento_Procedimento WHERE idAtendimento=?", (atendimento_id,))
            ids_vistos = set()
            for proc in procedimentos:
                proc_id = proc['id']
                if proc_id not in ids_vistos:
                    self.cursor.execute(
                        "INSERT INTO Atendimento_Procedimento (idAtendimento, idProcedimento) VALUES (?, ?)",
                        (atendimento_id, proc_id)
                    )
                    ids_vistos.add(proc_id)
            self.comitar()
            return True
        finally:
            self.desconectar()
    def removerAtendimentoDB(self, atendimento_id):
        """Remove um atendimento."""
        try:
            self.conectar()
            self.cursor.execute("DELETE FROM Atendimento_Procedimento WHERE idAtendimento=?", (atendimento_id,))
            self.cursor.execute("DELETE FROM atendimentos WHERE id=?", (atendimento_id,))
            self.comitar()
            return True
        finally:
            self.desconectar()