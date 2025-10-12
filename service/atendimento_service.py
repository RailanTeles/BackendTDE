from dao.atendimento_dao import AtendimentoDao

class AtendimentoService:
    def __init__(self):
        self.atendimentoDao = AtendimentoDao()

    def obterAtendimento(self, atendimento_id: int):
        atendimento = self.atendimentoDao.obterAtendimentoPorId(atendimento_id)
        if not atendimento:
            return {"msg": "Atendimento não encontrado"}, 404
        return atendimento, 200

    def obterAtendimentos(self, usuario_id: int, usuario_tipo: str):
        atendimentos = self.atendimentoDao.listarAtendimentos()
        if usuario_tipo == 'admin':
            return atendimentos, 200
        return [a for a in atendimentos if a['idUsuario'] == usuario_id], 200

    def criarAtendimento(self, data, paciente_id, procedimentos, tipo, numero_plano, usuario_id):
        if not procedimentos or len(procedimentos) == 0:
            return {"msg": "O atendimento deve possuir pelo menos um procedimento."}, 400
        if tipo == 'plano' and not numero_plano:
            return {"msg": "Número do plano de saúde é obrigatório para atendimentos do tipo plano."}, 400
        if tipo == 'particular' and numero_plano:
            return {"msg": "Número do plano de saúde não deve ser informado para atendimentos particulares."}, 400
        valor_total = 0
        for proc in procedimentos:
            if tipo == 'plano':
                valor_total += proc['valorPlano']
            else:
                valor_total += proc['valorParticular']
        atendimento_id = self.atendimentoDao.criarAtendimentoDB(data, paciente_id, procedimentos, tipo, numero_plano, usuario_id, valor_total)
        return {"msg": "Atendimento criado com sucesso", "id": atendimento_id}, 201

    def atualizarAtendimento(self, atendimento_id, data, paciente_id, procedimentos, tipo, numero_plano, usuario_id, usuario_tipo):
        atendimento = self.atendimentoDao.obterAtendimentoPorId(atendimento_id)
        if not atendimento:
            return {"msg": "Atendimento não encontrado."}, 404
        if usuario_tipo != 'admin' and atendimento['idUsuario'] != usuario_id:
            return {"msg": "Você não tem permissão para editar este atendimento."}, 403
        if not procedimentos or len(procedimentos) == 0:
            return {"msg": "O atendimento deve possuir pelo menos um procedimento."}, 400
        if tipo == 'plano' and not numero_plano:
            return {"msg": "Número do plano de saúde é obrigatório para atendimentos do tipo plano."}, 400
        if tipo == 'particular' and numero_plano:
            return {"msg": "Número do plano de saúde não deve ser informado para atendimentos particulares."}, 400
        valor_total = 0
        for proc in procedimentos:
            if tipo == 'plano':
                valor_total += proc['valorPlano']
            else:
                valor_total += proc['valorParticular']
        self.atendimentoDao.atualizarAtendimentoDB(atendimento_id, data, paciente_id, procedimentos, tipo, numero_plano, usuario_id, valor_total)
        return {"msg": "Atendimento atualizado com sucesso"}, 200

    def removerAtendimento(self, atendimento_id, usuario_id, usuario_tipo):
        atendimento = self.atendimentoDao.obterAtendimentoPorId(atendimento_id)
        if not atendimento:
            return {"msg": "Atendimento não encontrado."}, 404
        if usuario_tipo != 'admin' and atendimento['idUsuario'] != usuario_id:
            return {"msg": "Você não tem permissão para remover este atendimento."}, 403
        self.atendimentoDao.removerAtendimentoDB(atendimento_id)
        return {"msg": "Atendimento removido com sucesso"}, 200
