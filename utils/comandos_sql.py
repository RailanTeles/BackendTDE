import sqlite3

DATABASE = "./database/data.db"

class Comandos:
    def conectar(self):
        """Abre a conexão com o banco e configura para retornar dicionários"""
        self.conn = sqlite3.connect(DATABASE)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def desconectar(self):
        """Fecha cursor e conexão"""
        self.cursor.close()
        self.conn.close()

    def comitar(self):
        self.conn.commit()

    def obterRegistros(self, comando, parametros = None):
        """
        Executa um comando no mysql com ou sem parãmetros. Deve ser usado para comandos que retornam lista
        """
        if parametros is None:
            self.cursor.execute(comando)
        else:
            self.cursor.execute(comando, parametros)
        linhas = self.cursor.fetchall()
        resultado = [dict(linha) for linha in linhas]
        return resultado
    
    def obterRegistro(self, comando, parametros = None):
        """
        Executa um comando no mysql com ou sem parãmetros. Deve ser usado para comandos que retornam uma única lista
        """
        if parametros is None:
            self.cursor.execute(comando)
        else:
            self.cursor.execute(comando, parametros)
        resultado = self.cursor.fetchone()[0]
        return resultado
        
        
