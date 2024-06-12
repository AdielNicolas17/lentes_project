# lentes_project/sistema_lentes.py

from lentes_project.categoria_lente import CategoriaLente
from lentes_project.lente import Lente

class SistemaLentes:
    def __init__(self):
        self.categorias = {
            "visao_simples": CategoriaLente("Visão Simples"),
            "progressiva": CategoriaLente("Progressiva")
        }
        self.preencher_dados()

    def preencher_dados(self):
        # Visão Simples
        self.categorias["visao_simples"].adicionar_lente(1, Lente("VS RESINA AR (AR)", (-6.00, 6.00), (-2.00, 0), None, 14.99, 16.66))
        self.categorias["visao_simples"].adicionar_lente(2, Lente("VS RESINA AR ESTENDIDO (AR)", (-4.00, 3.00), (-4.00, -2.25), None, 40.00, 44.44))
        self.categorias["visao_simples"].adicionar_lente(3, Lente("VS RESINA BLUE (BC)", (-6.00, 4.00), (-2.00, 0), None, 40.00, 44.44))
        self.categorias["visao_simples"].adicionar_lente(4, Lente("VS RESINA BLUE ESTENDIDO(BC)", (-4.00, 4.00), (-4.00, -2.25), None, 71.91, 79.90))
        self.categorias["visao_simples"].adicionar_lente(5, Lente("VS RESINA FOTO AR (FR)", (-6.00, 6.00), (-2.00, 0), None, 40.00, 44.44))
        self.categorias["visao_simples"].adicionar_lente(6, Lente("VS RESINA FOTO AR ESTENDIDO (FR)", (-4.00, 4.00), (-4.00, -2.25), None, 65.01, 72.23))
        self.categorias["visao_simples"].adicionar_lente(7, Lente("VS RESINA FOTO AR SUPER ESTENDIDO (FR)", (-4.00, 4.00), (-6.00, -4.25), None, 99.90, 111.00))
        self.categorias["visao_simples"].adicionar_lente(8, Lente("VS RESINA FOTO BLUE (FB)", (-4.00, 3.00), (-2.00, 0), None, 119.00, 132.22))
        self.categorias["visao_simples"].adicionar_lente(9, Lente("VS RESINA FOTO BLUE ESTENDIDO (FB)", (-4.00, 4.00), (-4.00, -2.25), None, 139.90, 155.44))
        self.categorias["visao_simples"].adicionar_lente(10, Lente("VS POLY AR (PR)", (-6.00, 4.00), (-2.00, 0), None, 27.00, 30.00))
        self.categorias["visao_simples"].adicionar_lente(11, Lente("VS POLY AR ESTENDIDO (PR)", (-4.00, 2.00), (-4.00, -2.25), None, 62.91, 69.90))
        self.categorias["visao_simples"].adicionar_lente(12, Lente("VS POLY BLUE (PB)", (-6.00, 4.00), (-2.00, 0), None, 80.10, 89.00))
        self.categorias["visao_simples"].adicionar_lente(13, Lente("VS POLY BLUE ESTENDIDO (PB)", (-4.00, 4.00), (-4.00, -2.25), None, 129.89, 144.32))
        self.categorias["visao_simples"].adicionar_lente(14, Lente("VS POLY BLUE SUPER ESTENDIDO (PB)", (-4.00, 2.00), (-6.00, -4.25), None, 144.90, 161.00))
        self.categorias["visao_simples"].adicionar_lente(15, Lente("VS POLY FOTO AR (PF)", (-4.00, 3.00), (-2.00, 0), None, 148.41, 164.90))
        self.categorias["visao_simples"].adicionar_lente(16, Lente("VS POLY FOTO AR ESTENDIDO (PF)", (-4.00, 4.00), (-4.00, -2.25), None, 179.91, 199.90))
        self.categorias["visao_simples"].adicionar_lente(17, Lente("VS POLY FOTO BLUE (PFB)", (-3.00, 2.00), (-2.00, 0), None, 189.90, 211.00))
        self.categorias["visao_simples"].adicionar_lente(18, Lente("VS POLY FOTO BLUE ESTENDIDO (PFB)", (-2.00, 2.00), (-3.00, -2.25), None, 199.89, 222.10))
        self.categorias["visao_simples"].adicionar_lente(19, Lente("VS 1.67 AR", (-10.00, -3.00), (-2.00, 0), None, 149.94, 166.60))
        self.categorias["visao_simples"].adicionar_lente(20, Lente("VS 1.67 AR ESTENDIDO", (-10.00, -3.00), (-3.00, -2.25), None, 189.90, 211.00))

        # Progressiva
        self.categorias["progressiva"].adicionar_lente(21, Lente("MULTIFOCAL INC AC (MF INC AC)", (0.00, 2.00), None, (1.00, 3.00), 26.00, 28.89))
        self.categorias["progressiva"].adicionar_lente(22, Lente("MULTIFOCAL AR AC (MF AR AC)", (0.00, 2.00), None, (1.00, 3.00), 45.00, 50.00))
        self.categorias["progressiva"].adicionar_lente(23, Lente("MULTIFOCAL BC AC (MF BC AC)", (0.00, 2.00), None, (1.00, 3.00), 80.91, 89.90))
        self.categorias["progressiva"].adicionar_lente(24, Lente("MULTIFOCAL FOTO AR AC (MF FOTO AR AC) *", (0.00, 3.00), None, (1.00, 3.00), 70.00, 77.78))
        self.categorias["progressiva"].adicionar_lente(25, Lente("MULTIFOCAL FOTO BLUE (MF FOTO BC AC) *", (0.00, 2.00), None, (1.00, 3.00), 149.94, 166.60))

    def mostrar_categorias(self):
        print("Categorias de lentes disponíveis:")
        print("1: Visão Simples")
        print("2: Progressiva")

    def solicitar_entrada(self, prompt, tipo=float, validacao=None):
        while True:
            try:
                valor = tipo(input(prompt))
                if validacao and not validacao(valor):
                    raise ValueError
                return valor
            except ValueError:
                print("Entrada inválida. Tente novamente.")

    def executar(self):
        self.mostrar_categorias()
        categoria_escolha = self.solicitar_entrada("Informe o número correspondente à categoria de lente: ", int, lambda x: x in [1, 2])
        categoria = "visao_simples" if categoria_escolha == 1 else "progressiva"
        
        self.categorias[categoria].mostrar_opcoes()

        tipo_lente = self.solicitar_entrada("Informe o número correspondente ao tipo de lente: ", int, lambda x: x in self.categorias[categoria].lentes)
        esferico = self.solicitar_entrada("Informe o valor do esférico: ")
        cilindrico = self.solicitar_entrada("Informe o valor do cilíndrico: ")
        adicao = self.solicitar_entrada("Informe o valor da adição: ")

        preco = self.categorias[categoria].obter_preco(tipo_lente, esferico, cilindrico, adicao)
        print(preco)
