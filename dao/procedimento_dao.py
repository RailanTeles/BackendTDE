import math
from utils.comandos_sql import Comandos

class ProcedimentoDao(Comandos):
    def __init__(self):
        super().__init__()

    def obterProcedimentoPorId(self, id: int):
        """Obtém um procedimento pelo ID"""
        try:
            self.conectar()
            return self.obterRegistro(
                "SELECT * FROM Procedimentos WHERE id = ?",
                (id,)
            )
        except Exception as e:
            raise Exception(f"Erro ao buscar procedimento por ID: {str(e)}")
        finally:
            self.desconectar()

    def obterProcedimentoPorNome(self, nome: str):
        """Obtém um procedimento pelo nome"""
        try:
            self.conectar()
            return self.obterRegistro(
                "SELECT * FROM Procedimentos WHERE LOWER(nome) = LOWER(?)",
                (nome,)
            )
        except Exception as e:
            raise Exception(f"Erro ao buscar procedimento por nome: {str(e)}")
        finally:
            self.desconectar()

    def contarProcedimentos(self):
        """Conta o total de procedimentos"""
        try:
            self.conectar()
            linha = self.obterRegistro("SELECT COUNT(id) AS total FROM Procedimentos")
            return linha.get("total", 0) if linha else 0
        except Exception as e:
            raise Exception(f"Erro ao contar procedimentos: {str(e)}")
        finally:
            self.desconectar()

    def obterProcedimentos(self, itensPorPagina: int = 10, pagina: int = 1):
        """Lista procedimentos com paginação"""
        try:
            self.conectar()
            
            itens_por_pagina = max(1, int(itensPorPagina)) if itensPorPagina else 10
            pagina_atual = max(1, int(pagina)) if pagina else 1
            
            # Obter total
            total_row = self.obterRegistro("SELECT COUNT(id) AS total FROM Procedimentos")
            total = total_row.get("total", 0) if total_row else 0

            # Calcular paginação
            offset = itens_por_pagina * (pagina_atual - 1)
            totalPaginas = math.ceil(total / itens_por_pagina) if total > 0 else 1

            # Verificar se a página existe
            if pagina_atual > totalPaginas and totalPaginas > 0:
                return {
                    "pagina": pagina_atual,
                    "totalPaginas": totalPaginas,
                    "itensPorPagina": itens_por_pagina,
                    "procedimentosTotais": total,
                    "procedimentos": []
                }

            # Obter registros
            registros = self.obterRegistros(
                "SELECT * FROM Procedimentos ORDER BY nome ASC LIMIT ? OFFSET ?",
                (itens_por_pagina, offset)
            ) or []

            return {
                "pagina": pagina_atual,
                "totalPaginas": totalPaginas,
                "itensPorPagina": itens_por_pagina,
                "procedimentosTotais": total,
                "procedimentos": registros
            }
            
        except Exception as e:
            raise Exception(f"Erro ao listar procedimentos: {str(e)}")
        finally:
            self.desconectar()

    def adicionarProcedimento(self, dados: dict):
        """Adiciona um novo procedimento"""
        try:
            self.conectar()
            print(f" Dados recebidos no DAO: {dados}")
            
            self.cursor.execute(
                """
                INSERT INTO Procedimentos
                (nome, desc, valorPlano, valorParticular)
                VALUES (?, ?, ?, ?)
                """,
                (
                    dados["nome"],
                    dados["desc"],
                    dados["valorPlano"],
                    dados["valorParticular"]
                )
            )
            
            inserted_id = self.cursor.lastrowid
            self.comitar()
            
            print(f" Procedimento adicionado com ID: {inserted_id}")
            return {"msg": "Procedimento adicionado com sucesso", "id": inserted_id}
            
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Erro ao adicionar procedimento: {str(e)}")
        finally:
            self.desconectar()

    def alterarProcedimento(self, id: int, dados: dict):
        """Altera um procedimento existente"""
        try:
            self.conectar()
            print(f" Dados recebidos no DAO para alteração: {dados}")
            
            self.cursor.execute(
                """
                UPDATE Procedimentos
                SET nome = ?, desc = ?, valorPlano = ?, valorParticular = ?
                WHERE id = ?
                """,
                (
                    dados["nome"],
                    dados["desc"],
                    dados["valorPlano"],
                    dados["valorParticular"],
                    id
                )
            )
            
            if self.cursor.rowcount == 0:
                raise Exception("Nenhum procedimento foi alterado - ID não encontrado")
            
            self.comitar()
            print(f" Procedimento ID {id} alterado com sucesso")
            return {"msg": "Procedimento alterado com sucesso"}
            
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Erro ao alterar procedimento: {str(e)}")
        finally:
            self.desconectar()

    def deletarProcedimento(self, id: int):
        """Deleta um procedimento"""
        try:
            self.conectar()
            print(f" DELETANDO procedimento ID: {id}")
            
            # Verificar se o procedimento existe
            procedimento = self.obterRegistro("SELECT id FROM Procedimentos WHERE id = ?", (id,))
            if not procedimento:
                raise Exception(f"Procedimento com ID {id} não encontrado")
            print(f" Procedimento ID {id} encontrado")
            
            # Verificar se está em uso
            em_uso = self.obterRegistro(
                "SELECT 1 AS existe FROM Atendimento_Procedimento WHERE idProcedimento = ? LIMIT 1",
                (id,)
            )
            if em_uso:
                raise Exception("Não é possível excluir: procedimento está em uso em atendimentos")
            print(" Procedimento não está em uso")
            
            # Executar DELETE
            self.cursor.execute("DELETE FROM Procedimentos WHERE id = ?", (id,))
            
            print(f" DELETE executado. Linhas afetadas: {self.cursor.rowcount}")
            
            if self.cursor.rowcount == 0:
                raise Exception(f"Nenhum procedimento foi deletado - ID {id} não encontrado")
            
            self.comitar()
            print(" COMMIT realizado com sucesso!")
            
            return {"msg": "Procedimento deletado com sucesso"}
            
        except Exception as e:
            self.conn.rollback()
            print(f" ERRO no delete: {str(e)}")
            raise Exception(f"Erro ao deletar procedimento: {str(e)}")
        finally:
            self.desconectar()

    def verificarProcedimentoEmUso(self, id: int):
        """Verifica se o procedimento está em uso"""
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