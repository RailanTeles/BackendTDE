from utils.comandos_sql import Comandos
from models.atendimento import Atendimento
from datetime import datetime


class AtendimentoDao(Comandos):
    """DAO para operações relacionadas a atendimentos."""

    def listar_atendimentos_por_data(self, data_inicio, data_fim, offset=0, limit=10, usuario_id=None):
        """Lista atendimentos entre datas, com paginação e filtro opcional por usuário."""
        self.conectar()
        query = '''
            SELECT a.*, GROUP_CONCAT(ap.idProcedimento) as procedimentos
            FROM atendimentos a
            LEFT JOIN Atendimento_Procedimento ap ON a.id = ap.idAtendimento
            WHERE date(a.data) BETWEEN date(?) AND date(?)'''
        params = [data_inicio, data_fim]
        if usuario_id is not None:
            query += ' AND a.idUsuario = ?'
            params.append(usuario_id)
        query += '''
            GROUP BY a.id
            ORDER BY a.data
            LIMIT ? OFFSET ?
        '''
        params.extend([limit, offset])
        itens = self.obterRegistros(query, tuple(params))
        self.desconectar()
        return itens

    def obter_qtd_atendimentos_usuario(self, id_usuario: int):
        """Retorna a quantidade de atendimentos de um usuário."""
        self.conectar()
        atends = self.obterRegistro("SELECT COUNT(idUsuario) as total FROM atendimentos WHERE idUsuario=?", (id_usuario,))
        self.desconectar()
        return atends.get('total')
<<<<<<< HEAD

    def obter_total_atendimentos(self, usuario_id=None):
        """Retorna total de atendimentos, opcionalmente filtrados por usuário."""
        self.conectar()
        if usuario_id is not None:
            result = self.obterRegistro("SELECT COUNT(*) as total FROM atendimentos WHERE idUsuario=?", (usuario_id,))
        else:
            result = self.obterRegistro("SELECT COUNT(*) as total FROM atendimentos")
        self.desconectar()
        return result.get('total') if result else 0

    def obter_total_atendimentos_por_data(self, data_inicio, data_fim, usuario_id=None):
        """Retorna total de atendimentos entre datas, opcionalmente filtrados por usuário."""
        self.conectar()
        query = "SELECT COUNT(*) as total FROM atendimentos WHERE date(data) BETWEEN date(?) AND date(?)"
        params = [data_inicio, data_fim]
        if usuario_id is not None:
            query += " AND idUsuario=?"
            params.append(usuario_id)
        result = self.obterRegistro(query, tuple(params))
        self.desconectar()
        return result.get('total') if result else 0
    def criar_atendimento_db(self, data, paciente_id, procedimentos, tipo, numero_plano, usuario_id, valor_total):
=======
    
    def obterQtdAtendimentosPaciente(self, id: int):
        """Retorna a quantidade de atendimentos de um paciente."""
        self.conectar()
        atends = self.obterRegistro("SELECT COUNT(idPaciente) as total FROM atendimentos WHERE idPaciente=?", (id,))
        self.desconectar()
        return atends.get('total')
    
    def criarAtendimentoDB(self, data, paciente_id, procedimentos, tipo, numero_plano, usuario_id, valor_total):
>>>>>>> 118647b4325a230f311a867af23cc26e7e9ab662
        """Cria um atendimento e vincula procedimentos."""
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
        self.desconectar()
        return {
            "msg": "Atendimento criado com sucesso",
            "id": atendimento_id
        }
    def listar_atendimentos(self, usuario_id=None, offset=0, limit=None):
        """Lista atendimentos com paginação opcional, opcionalmente filtrados por usuário."""
        self.conectar()
        query = '''
            SELECT a.*, GROUP_CONCAT(ap.idProcedimento) as procedimentos
            FROM atendimentos a
            LEFT JOIN Atendimento_Procedimento ap ON a.id = ap.idAtendimento'''
        params = []
        if usuario_id is not None:
            query += ' WHERE a.idUsuario = ?'
            params.append(usuario_id)
        query += ' GROUP BY a.id'
        if limit is not None:
            query += ' LIMIT ? OFFSET ?'
            params.extend([limit, offset])
        itens = self.obterRegistros(query, tuple(params)) if params else self.obterRegistros(query)
        self.desconectar()
        return itens

    def obter_atendimento_por_id(self, atendimento_id):
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

    def atualizar_atendimento_db(self, atendimento_id, data, paciente_id, procedimentos, tipo, numero_plano, usuario_id, valor_total):
        """Atualiza um atendimento e seus procedimentos."""
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
        self.desconectar()
        return {
            "msg": "Atendimento atualizado com sucesso"
        }

    def remover_atendimento_db(self, atendimento_id):
        """Remove um atendimento e seus procedimentos associados."""
        self.conectar()
        self.cursor.execute("DELETE FROM Atendimento_Procedimento WHERE idAtendimento=?", (atendimento_id,))
        self.cursor.execute("DELETE FROM atendimentos WHERE id=?", (atendimento_id,))
        self.comitar()
        self.desconectar()
        return {
            "msg": "Atendimento removido com sucesso"
        }