# lentes_project/lente.py

class Lente:
    def __init__(self, nome, esferico_range, cilindrico_range, adicao_range, debito, credito):
        self.nome = nome
        self.esferico_range = esferico_range
        self.cilindrico_range = cilindrico_range
        self.adicao_range = adicao_range
        self.debito = debito
        self.credito = credito

    def verificar_intervalo(self, valor, intervalo):
        if intervalo is None:
            return True
        return intervalo[0] <= valor <= intervalo[1]

    def obter_preco(self, esferico, cilindrico, adicao):
        if self.verificar_intervalo(esferico, self.esferico_range):
            if self.verificar_intervalo(cilindrico, self.cilindrico_range):
                if self.verificar_intervalo(adicao, self.adicao_range):
                    return f"Preço (Débito): R$ {self.debito}, Preço (Crédito): R$ {self.credito}"
                else:
                    return "Valor de adição fora do intervalo permitido."
            else:
                return "Valor de cilíndrico fora do intervalo permitido."
        else:
            return "Valor de esférico fora do intervalo permitido."
