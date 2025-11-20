import math
from utils.comandos_sql import Comandos
from models.procedimento import Procedimento

class ProcedimentoDao(Comandos):
    def __init__(self):
        super().__init__()

    def obterProcedimentoPorId(self, id: int):
        try:
            self.conectar()
            procedimento = self.obterRegistro(
                "SELECT * FROM Procedimentos WHERE id = ?",
                (id,)
            )
            return procedimento
        except Exception as e:
            raise Exception(f"Erro ao buscar procedimento por ID: {str(e)}")
        finally:
            self.desconectar()

    def obterProcedimentoPorNome(self, nome: str):
        try:
            self.conectar()
            procedimento = self.obterRegistro(
                "SELECT * FROM Procedimentos WHERE LOWER(nome) = LOWER(?)",
                (nome,)
            )
            return procedimento
        except Exception as e:
            raise Exception(f"Erro ao buscar procedimento por nome: {str(e)}")
        finally:
            self.desconectar()

    def contarProcedimentos(self):
        try:
            self.conectar()
            linha = self.obterRegistro("SELECT COUNT(id) AS total FROM Procedimentos")
            return linha.get("total", 0) if linha else 0
        except Exception as e:
            raise Exception(f"Erro ao contar procedimentos: {str(e)}")
        finally:
            self.desconectar()

    def obterProcedimentos(self, itensPorPagina: int = 10, pagina: int = 1):
        try:
            self.conectar()

            total_row = self.obterRegistro("SELECT COUNT(id) AS total FROM Procedimentos")
            total = total_row.get("total", 0) if total_row else 0

            itensPorPagina = max(1, int(itensPorPagina)) if itensPorPagina else 10
            pagina = max(1, int(pagina)) if pagina else 1
            offset = itensPorPagina * (pagina - 1)

            totalPaginas = math.ceil(total / itensPorPagina) if total > 0 else 1

            if pagina > totalPaginas and totalPaginas > 0:
                return None

            registros = self.obterRegistros(
                "SELECT * FROM Procedimentos ORDER BY nome ASC LIMIT ? OFFSET ?",
                (itensPorPagina, offset)
            ) or []

            return {
                "pagina": pagina,
                "totalPaginas": totalPaginas,
                "itensPorPagina": itensPorPagina,
                "procedimentosTotais": total,
                "procedimentos": registros
            }
        except Exception as e:
            raise Exception(f"Erro ao listar procedimentos: {str(e)}")
        finally:
            self.desconectar()

    def adicionarProcedimento(self, dados: dict):
        try:
            self.conectar()
            self.cursor.execute(
                """
                INSERT INTO Procedimentos
                (nome, desc, valorPlano, valorParticular)  -- ⭐ MUDOU: descricao → desc
                VALUES (?, ?, ?, ?)
                """,
                (
                    dados["nome"],
                    dados["descricao"],  # ⭐ Mantém o mesmo nome no dicionário
                    dados["valorPlano"],
                    dados["valorParticular"]
                )
            )
            self.comitar()
            inserted_id = self.cursor.lastrowid
            return {"msg": "Procedimento adicionado com sucesso", "id": inserted_id}
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Erro ao adicionar procedimento: {str(e)}")
        finally:
            self.desconectar()

    def alterarProcedimento(self, id: int, dados: dict):
        try:
            self.conectar()
            self.cursor.execute(
                """
                UPDATE Procedimentos
                SET nome = ?, desc = ?, valorPlano = ?, valorParticular = ?  -- ⭐ MUDOU: descricao → desc
                WHERE id = ?
                """,
                (
                    dados["nome"],
                    dados["descricao"],  # ⭐ Mantém o mesmo nome no dicionário
                    dados["valorPlano"],
                    dados["valorParticular"],
                    id
                )
            )
            self.comitar()
            return {"msg": "Procedimento alterado com sucesso"}
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Erro ao alterar procedimento: {str(e)}")
        finally:
            self.desconectar()

    def deletarProcedimento(self, id: int):
        try:
            self.conectar()
            self.cursor.execute(
                "DELETE FROM Procedimentos WHERE id = ?",
                (id,)
            )
            self.comitar()
            return {"msg": 'Procedimento deletado com sucesso'}
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Erro ao deletar procedimento: {str(e)}")
        finally:
            self.desconectar()

    def verificarProcedimentoEmUso(self, id: int):
        try:
            self.conectar()
            registro = self.obterRegistro(
                "SELECT 1 AS existe FROM Atendimento_Procedimento WHERE idProcedimento = ? LIMIT 1",
                (id,)
            )
            return bool(registro)
        except Exception as e:
            raise Exception(f"Erro ao verificar procedimento em uso: {str(e)}")
        finally:
            self.desconectar()