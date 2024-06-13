# business.py

class CalculadoraPreco:
    @staticmethod
    def calcular_preco(lente_od, lente_oe, incluir_armacao, margem, incluir_consulta):
        preco_base = ((lente_od.debito + lente_oe.debito) / 2 + 40)
        preco_debito = preco_base * margem
        preco_credito = preco_base * margem
        
        if incluir_armacao == "Sim":
            preco_debito += 100.00
            preco_credito += 110.00

        if incluir_consulta == "Sim":
            preco_debito += 60.00
            preco_credito += 60.00

        return preco_debito, preco_credito