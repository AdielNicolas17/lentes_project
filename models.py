# models.py

class Lente:
    def __init__(self, nome, debito, credito, esferico_range, cilindrico_range, adicao_range):
        self.nome = nome
        self.debito = debito
        self.credito = credito
        self.esferico_range = esferico_range
        self.cilindrico_range = cilindrico_range
        self.adicao_range = adicao_range

class CategoriaLentes:
    def __init__(self):
        self.lentes = {}

    def adicionar_lente(self, lente):
        self.lentes[lente.nome] = lente

class SistemaLentes:
    def __init__(self):
        self.categorias = {
            "visao_simples": CategoriaLentes(),
            "progressiva": CategoriaLentes()
        }
        self.inicializar_lentes()

    def inicializar_lentes(self):
        # Adicione a inicialização das lentes aqui
        pass
