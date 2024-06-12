# lentes_project/categoria_lente.py

from lentes_project.lente import Lente

class CategoriaLente:
    def __init__(self, nome):
        self.nome = nome
        self.lentes = {}

    def adicionar_lente(self, num, lente):
        self.lentes[num] = lente

    def mostrar_opcoes(self):
        print(f"Tipos de lentes disponíveis para {self.nome.replace('_', ' ')}:")
        for num, lente in self.lentes.items():
            print(f"{num}: {lente.nome}")

    def obter_preco(self, num_lente, esferico, cilindrico, adicao):
        if num_lente in self.lentes:
            lente = self.lentes[num_lente]
            return lente.obter_preco(esferico, cilindrico, adicao)
        else:
            return "Tipo de lente não encontrado."
