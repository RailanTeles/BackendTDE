from utils.comandos_sql import Comandos

class ProcedimentoDao(Comandos):
    """DAO para operações relacionadas a procedimentos."""

    def listar_procedimentos(self, offset=0, limit=10):
        """Lista procedimentos com paginação."""
        self.conectar()
        query = '''
            SELECT id, nome, desc, valorPlano, valorParticular
            FROM Procedimentos
            ORDER BY nome ASC
            LIMIT ? OFFSET ?
        '''
        procedimentos = self.obterRegistros(query, (limit, offset))
        self.desconectar()
        return procedimentos

    def obter_total_procedimentos(self):
        """Retorna total de procedimentos."""
        self.conectar()
        result = self.obterRegistro("SELECT COUNT(*) as total FROM Procedimentos")
        self.desconectar()
        return result.get('total') if result else 0

    def obter_procedimento_por_id(self, procedimento_id):
        """Obtém um procedimento pelo ID."""
        self.conectar()
        procedimento = self.obterRegistro(
            "SELECT * FROM Procedimentos WHERE id = ?",
            (procedimento_id,)
        )
        self.desconectar()
        return procedimento

    def obter_procedimento_por_nome(self, nome: str):
        """Obtém um procedimento pelo nome (case insensitive)."""
        self.conectar()
        procedimento = self.obterRegistro(
            "SELECT * FROM Procedimentos WHERE LOWER(nome) = LOWER(?)",
            (nome,)
        )
        self.desconectar()
        return procedimento

    def criar_procedimento_db(self, nome: str, desc: str, valor_plano: float, valor_particular: float):
        """Cria um novo procedimento."""
        self.conectar()
        self.cursor.execute(
            """
            INSERT INTO Procedimentos (nome, desc, valorPlano, valorParticular)
            VALUES (?, ?, ?, ?)
            """,
            (nome, desc, valor_plano, valor_particular)
        )
        procedimento_id = self.cursor.lastrowid
        self.comitar()
        self.desconectar()
        return procedimento_id

    def atualizar_procedimento_db(self, procedimento_id: int, nome: str, desc: str, valor_plano: float, valor_particular: float):
        """Atualiza um procedimento existente."""
        self.conectar()
        self.cursor.execute(
            """
            UPDATE Procedimentos
            SET nome = ?, desc = ?, valorPlano = ?, valorParticular = ?
            WHERE id = ?
            """,
            (nome, desc, valor_plano, valor_particular, procedimento_id)
        )
        self.comitar()
        self.desconectar()

    def remover_procedimento_db(self, procedimento_id: int):
        """Remove um procedimento existente."""
        self.conectar()
        self.cursor.execute("DELETE FROM Procedimentos WHERE id = ?", (procedimento_id,))
        rowcount = self.cursor.rowcount
        self.comitar()
        self.desconectar()

        if rowcount == 0:
            raise Exception(f"Procedimento com ID {procedimento_id} não encontrado")

        return True

    def verificar_procedimento_em_uso(self, procedimento_id: int):
        """Verifica se o procedimento está em uso em atendimentos."""
        self.conectar()
        registro = self.obterRegistro(
            "SELECT 1 AS existe FROM Atendimento_Procedimento WHERE idProcedimento = ? LIMIT 1",
            (procedimento_id,)
        )
        self.desconectar()
        return bool(registro)