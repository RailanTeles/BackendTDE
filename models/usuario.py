from enum import Enum

class TipoUsuario(Enum):
    ADMIN = "admin"
    DEFAULT = "default"

class Usuario:
    def __init__(self, id: int, email: str, nome: str, tipo: TipoUsuario, senha: str):
        self.id = id
        self.email = email
        self.nome = nome
        self.tipo = tipo
        self.senha = senha