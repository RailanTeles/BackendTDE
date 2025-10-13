from datetime import datetime

class Responsavel:
    def __init__(self, id: int, cpf:str, nome: str, email: str, telefone: str, dataNascimento: str, idPaciente: int):
        self.id = id
        self.cpf = cpf
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.dataNascimento = self.passarParaData(dataNascimento)
        self.idPaciente = idPaciente

    def passarParaData(self, dataNascimento: str):
        """
        Transforma data em string para o bd aceitar.
        """
        return datetime.strptime(dataNascimento, '%Y-%m-%d').date().strftime('%Y-%m-%d')
    
    def verificarMaiorIdade(self):
        """
        Verifica se a pessoa é de maior. Se sim, retorna true. Se não, false.
        """
        hoje = datetime.now()
        verificarDataNascimento = datetime.strptime(self.dataNascimento, '%Y-%m-%d')
        aniversarioMaiorIdade = verificarDataNascimento.replace(year=verificarDataNascimento.year + 18)

        return hoje > aniversarioMaiorIdade