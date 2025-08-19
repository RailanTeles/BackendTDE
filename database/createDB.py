import sqlite3

DATABASE_FILE="./database/data.db"

conn = sqlite3.connect(DATABASE_FILE)

cursor = conn.cursor()

# cursor.execute("""
#     CREATE TABLE Usuarios(
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         email VARCHAR(255) UNIQUE NOT NULL,
#         nome VARCHAR(255) NOT NULL,
#         tipo TEXT CHECK(tipo IN ('admin', 'default')) NOT NULL,
#         senha VARCHAR(255) NOT NULL
#     )
# """)

# cursor.execute("INSERT INTO usuarios (email, nome, tipo, senha) VALUES ('admin@consultorio.com', 'admin123', 'admin', 'admin123')")
# cursor.execute("INSERT INTO usuarios (email, nome, tipo, senha) VALUES ('default@consultorio.com', 'default', 'default', 'default123')")

# cursor.execute("""
#     CREATE TABLE Pacientes(
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         cpf VARCHAR(11) UNIQUE NOT NULL,
#         nome VARCHAR(255) NOT NULL,
#         email VARCHAR(255) UNIQUE NOT NULL,
#         telefone VARCHAR(20) NOT NULL,
#         dataNascimento DATE NOT NULL
#     )
# """)

# cursor.execute("""
#     CREATE TABLE Enderecos(
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         estado VARCHAR(255) NOT NULL,
#         cidade VARCHAR(255) NOT NULL,
#         bairro VARCHAR(255) NOT NULL,
#         cep VARCHAR(10) NOT NULL,
#         rua VARCHAR(255) NOT NULL,
#         numeroCasa INTEGER NOT NULL,
#         idPaciente INTEGER NOT NULL,
               
#         FOREIGN KEY (idPaciente) REFERENCES pacientes(id)
#     )
# """)

# cursor.execute("""
#     CREATE TABLE Responsaveis(
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         cpf VARCHAR(11) UNIQUE NOT NULL,
#         nome VARCHAR(255) NOT NULL,
#         dataNascimento DATE NOT NULL,
#         email VARCHAR(255) UNIQUE NOT NULL,
#         telefone VARCHAR(20) NOT NULL,
#         idPaciente INTEGER NOT NULL,
               
#         FOREIGN KEY (idPaciente) REFERENCES pacientes(id)
#     )
# """)

# cursor.execute("""
#     CREATE TABLE Procedimentos(
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         nome VARCHAR(255) NOT NULL,
#         desc TEXT NOT NULL,
#         valorPlano DECIMAL(10,2) NOT NULL,
#         valorParticular DECIMAL(10,2) NOT NULL
#     )
# """)

# cursor.execute("""
#     CREATE TABLE Atendimentos(
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         data DATETIME NOT NULL,
#         tipo TEXT CHECK(tipo IN ('plano', 'particular')) NOT NULL,
#         numeroPlano VARCHAR(50),
#         valorTotal DECIMAL(10,2) NOT NULL,
#         idPaciente INTEGER NOT NULL,
#         idUsuario INTEGER NOT NULL,
               
#         FOREIGN KEY (idPaciente) REFERENCES pacientes(id),
#         FOREIGN KEY (idUsuario) REFERENCES usuarios(id),
        
#          CHECK (
#             (tipo = 'plano' AND numeroPlano IS NOT NULL) OR
#             (tipo = 'particular' AND numeroPlano IS NULL)
#         )
#     )
# """)

# cursor.execute("""
#     CREATE TABLE Atendimento_Procedimento(
#         idAtendimento INTEGER NOT NULL,
#         idProcedimento INTEGER NOT NULL,
#         PRIMARY KEY (idAtendimento, idProcedimento),
               
#         FOREIGN KEY (idAtendimento) REFERENCES atendimentos(id),
#         FOREIGN KEY (idProcedimento) REFERENCES procedimentos(id)
#     )
# """)

conn.commit()
cursor.close()
conn.close()