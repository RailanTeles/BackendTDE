from datetime import datetime

class Procedimento:
    def __init__(self, id: int, nome: str, desc: str, valorPlano: float, valorParticular: float):
        self.id = id
        self.nome = nome
        self.desc = desc
        self.valorPlano = valorPlano
        self.valorParticular = valorParticular

class Atendimento:
    def __init__(self, id: int, data: datetime, paciente_id: int, procedimentos: list, tipo: str, numero_plano: str, usuario_id: int, valor_total: float):
        self.id = id
        self.data = data
        self.paciente_id = paciente_id
        self.procedimentos = procedimentos  # lista de Procedimento
        self.tipo = tipo  # 'plano' ou 'particular'
        self.numero_plano = numero_plano
        self.usuario_id = usuario_id
        self.valor_total = valor_total
