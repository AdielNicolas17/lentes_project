# main.py

import tkinter as tk
from tkinter import ttk, messagebox
from lentes_project.sistema_lentes import SistemaLentes

class LentesApp:
    def __init__(self, root):
        self.sistema = SistemaLentes()
        self.root = root
        self.root.title("Calculadora de Lentes")
        self.root.geometry("600x500")  # Aumentando o tamanho da janela
        self.root.configure(bg='#2F4F4F')  # Dark Green Background
        
        # Estilos
        self.style = ttk.Style()
        self.style.configure('TLabel', background='#2F4F4F', foreground='#FFD700', font=('Arial', 12))
        self.style.configure('TCombobox', font=('Arial', 12))
        
        # Frame principal
        self.frame = tk.Frame(root, bg='#2F4F4F')
        self.frame.pack(padx=20, pady=20, anchor='w')

        # Categorias
        self.categoria_label = ttk.Label(self.frame, text="Categoria de Lentes")
        self.categoria_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        
        self.categoria_var = tk.StringVar()
        self.categoria_menu = ttk.Combobox(self.frame, textvariable=self.categoria_var, state='readonly', width=40)
        self.categoria_menu['values'] = ["Visão Simples", "Progressiva"]
        self.categoria_menu.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.categoria_menu.bind('<<ComboboxSelected>>', self.update_tipos_lentes)

        # Tipos de Lentes
        self.tipo_lente_label = ttk.Label(self.frame, text="Tipo de Lente")
        self.tipo_lente_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        
        self.tipo_lente_var = tk.StringVar()
        self.tipo_lente_menu = ttk.Combobox(self.frame, textvariable=self.tipo_lente_var, state='readonly', width=40)
        self.tipo_lente_menu.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        self.tipo_lente_menu.bind('<<ComboboxSelected>>', self.update_opcoes_lentes)
        
        # Esférico
        self.esferico_label = ttk.Label(self.frame, text="Valor Esférico")
        self.esferico_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        
        self.esferico_var = tk.StringVar()
        self.esferico_menu = ttk.Combobox(self.frame, textvariable=self.esferico_var, state='readonly', width=40)
        self.esferico_menu.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        
        # Cilíndrico
        self.cilindrico_label = ttk.Label(self.frame, text="Valor Cilíndrico")
        self.cilindrico_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')
        
        self.cilindrico_var = tk.StringVar()
        self.cilindrico_menu = ttk.Combobox(self.frame, textvariable=self.cilindrico_var, state='readonly', width=40)
        self.cilindrico_menu.grid(row=3, column=1, padx=10, pady=10, sticky='w')
        
        # Adição
        self.adicao_label = ttk.Label(self.frame, text="Valor de Adição")
        self.adicao_label.grid(row=4, column=0, padx=10, pady=10, sticky='w')
        
        self.adicao_var = tk.StringVar()
        self.adicao_menu = ttk.Combobox(self.frame, textvariable=self.adicao_var, state='readonly', width=40)
        self.adicao_menu.grid(row=4, column=1, padx=10, pady=10, sticky='w')
        
        # Botões
        self.buttons_frame = tk.Frame(root, bg='#2F4F4F')
        self.buttons_frame.pack(pady=20)
        
        self.calcular_button = tk.Button(self.buttons_frame, text="Calcular", command=self.calcular_preco, bg='#006400', fg='#FFD700', font=('Arial', 12, 'bold'))
        self.calcular_button.grid(row=0, column=0, padx=57)
        
        self.refazer_button = tk.Button(self.buttons_frame, text="Refazer", command=self.resetar_opcoes, bg='#006400', fg='#FFD700', font=('Arial', 12, 'bold'))
        self.refazer_button.grid(row=0, column=1, padx=57)
        
        # Resultado
        self.resultado_label = ttk.Label(root, text="", font=("Arial", 14, "bold"))
        self.resultado_label.pack(pady=10)

    def update_tipos_lentes(self, event):
        categoria = self.categoria_var.get()
        if categoria == "Visão Simples":
            self.tipo_lente_menu['values'] = [lente.nome for lente in self.sistema.categorias["visao_simples"].lentes.values()]
            self.adicao_menu.config(state='disabled')
            self.cilindrico_menu.config(state='normal')
        else:
            self.tipo_lente_menu['values'] = [lente.nome for lente in self.sistema.categorias["progressiva"].lentes.values()]
            self.adicao_menu.config(state='normal')
            self.cilindrico_menu.config(state='disabled')
        self.tipo_lente_var.set('')
        self.update_opcoes_lentes(None)
        
    def update_opcoes_lentes(self, event):
        categoria = self.categoria_var.get()
        tipo_lente_nome = self.tipo_lente_var.get()
        
        if categoria == "Visão Simples":
            categoria_key = "visao_simples"
        else:
            categoria_key = "progressiva"
        
        tipo_lente = next((v for k, v in self.sistema.categorias[categoria_key].lentes.items() if v.nome == tipo_lente_nome), None)
        
        if tipo_lente:
            esferico_values = [str(v) for v in self.range_float(tipo_lente.esferico_range[0], tipo_lente.esferico_range[1])]
            self.esferico_menu['values'] = esferico_values
            self.esferico_var.set('')
            
            if categoria == "Visão Simples":
                cilindrico_values = [str(v) for v in self.range_float(tipo_lente.cilindrico_range[0], tipo_lente.cilindrico_range[1])]
                self.cilindrico_menu['values'] = cilindrico_values
                self.cilindrico_var.set('')
                self.cilindrico_menu.config(state='readonly')
            else:
                self.cilindrico_menu['values'] = []
                self.cilindrico_var.set('')
                self.cilindrico_menu.config(state='disabled')
                
            if categoria == "Progressiva":
                adicao_values = [str(v) for v in self.range_float(tipo_lente.adicao_range[0], tipo_lente.adicao_range[1])]
                self.adicao_menu['values'] = adicao_values
                self.adicao_var.set('')
                self.adicao_menu.config(state='readonly')
            else:
                self.adicao_menu['values'] = []
                self.adicao_var.set('')
                self.adicao_menu.config(state='disabled')

    def calcular_preco(self):
        categoria = self.categoria_var.get()
        tipo_lente_nome = self.tipo_lente_var.get()
        esferico = self.esferico_var.get()
        cilindrico = self.cilindrico_var.get()
        adicao = self.adicao_var.get()

        try:
            esferico = float(esferico)
            if categoria == "Visão Simples":
                cilindrico = float(cilindrico)
            if categoria == "Progressiva":
                adicao = float(adicao)
        except ValueError:
            messagebox.showerror("Erro de entrada", "Por favor, insira valores numéricos válidos para esférico, cilíndrico e adição.")
            return

        if categoria == "Visão Simples":
            categoria_key = "visao_simples"
            adicao = None
        else:
            categoria_key = "progressiva"
            cilindrico = None

        tipo_lente = next((k for k, v in self.sistema.categorias[categoria_key].lentes.items() if v.nome == tipo_lente_nome), None)

        if tipo_lente is not None:
            preco = self.sistema.categorias[categoria_key].obter_preco(tipo_lente, esferico, cilindrico, adicao)
            self.resultado_label.config(text=preco)
        else:
            messagebox.showerror("Erro", "Tipo de lente não encontrado.")
    
    def resetar_opcoes(self):
        self.categoria_var.set('')
        self.tipo_lente_var.set('')
        self.esferico_var.set('')
        self.cilindrico_var.set('')
        self.adicao_var.set('')
        self.resultado_label.config(text='')
        self.esferico_menu['values'] = []
        self.cilindrico_menu['values'] = []
        self.adicao_menu['values'] = []
        self.adicao_menu.config(state='readonly')
        self.cilindrico_menu.config(state='readonly')

    def range_float(self, start, end, step=0.25):
        values = []
        while start <= end:
            values.append(round(start, 2))
            start += step
        return values

if __name__ == "__main__":
    root = tk.Tk()
    app = LentesApp(root)
    root.mainloop()
