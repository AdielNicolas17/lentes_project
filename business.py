# business.py

class CalculadoraPreco:
    @staticmethod
    def calcular_preco(lente_od, lente_oe, incluir_armacao):
        preco_debito = ((lente_od.debito + lente_oe.debito) / 2 + 40) * 4.5
        preco_credito = ((lente_od.credito + lente_oe.credito) / 2 + 40) * 5
        
        if incluir_armacao == "Sim":
            preco_debito += 100.00
            preco_credito += 110.00

        return preco_debito, preco_credito
