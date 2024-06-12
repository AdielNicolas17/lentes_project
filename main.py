# main.py

import tkinter as tk
from tkinter import ttk, messagebox
from lentes_project.sistema_lentes import SistemaLentes

class LentesApp:
    def __init__(self, root):
        self.sistema = SistemaLentes()
        self.root = root
        self.root.title("Calculadora de Lentes")
        self.root.geometry("1000x600")  # Ajustando o tamanho da janela
        self.root.configure(bg='#2F4F4F')  # Dark Green Background

        # Estilos
        self.style = ttk.Style()
        self.style.configure('TLabel', background='#2F4F4F', foreground='#FFD700', font=('Arial', 12))
        self.style.configure('TCombobox', font=('Arial', 12))

        # Molduras
        self.od_frame = tk.LabelFrame(root, text="OD", bg='#2F4F4F', fg='#FFD700', font=('Arial', 14, 'bold'), padx=20, pady=20)
        self.od_frame.place(x=50, y=20, width=400, height=300)

        self.oe_frame = tk.LabelFrame(root, text="OE", bg='#2F4F4F', fg='#FFD700', font=('Arial', 14, 'bold'), padx=20, pady=20)
        self.oe_frame.place(x=550, y=20, width=400, height=300)

        self.create_widgets(self.od_frame, 'od')
        self.create_widgets(self.oe_frame, 'oe')

        # Incluir Armação
        self.armacao_label = ttk.Label(root, text="Incluir Armação")
        self.armacao_label.place(x=420, y=350)
        self.armacao_var = tk.StringVar(value="Não")
        self.armacao_sim = tk.Radiobutton(root, text="Sim", variable=self.armacao_var, value="Sim", bg='#2F4F4F', fg='#FFD700', font=('Arial', 12))
        self.armacao_nao = tk.Radiobutton(root, text="Não", variable=self.armacao_var, value="Não", bg='#2F4F4F', fg='#FFD700', font=('Arial', 12))
        self.armacao_sim.place(x=550, y=350)
        self.armacao_nao.place(x=610, y=350)
        
        # Resultado
        self.resultado_label = ttk.Label(root, text="", font=("Arial", 14, "bold"))
        self.resultado_label.place(x=420, y=380)

        # Botões
        self.calcular_button = tk.Button(root, text="Calcular", command=self.calcular_preco, bg='#006400', fg='#FFD700', font=('Arial', 12, 'bold'))
        self.calcular_button.place(x=420, y=420)

        self.refazer_button = tk.Button(root, text="Refazer", command=self.resetar_opcoes, bg='#006400', fg='#FFD700', font=('Arial', 12, 'bold'))
        self.refazer_button.place(x=530, y=420)

    def create_widgets(self, frame, prefix):
        # Categorias
        categoria_label = ttk.Label(frame, text="Categoria de Lentes")
        categoria_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        
        categoria_var = tk.StringVar()
        categoria_menu = ttk.Combobox(frame, textvariable=categoria_var, state='readonly', width=30)
        categoria_menu['values'] = ["Visão Simples", "Progressiva"]
        categoria_menu.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        categoria_menu.bind('<<ComboboxSelected>>', lambda event: self.update_tipos_lentes(event, prefix))

        setattr(self, f"{prefix}_categoria_var", categoria_var)
        setattr(self, f"{prefix}_categoria_menu", categoria_menu)

        # Tipos de Lentes
        tipo_lente_label = ttk.Label(frame, text="Tipo de Lente")
        tipo_lente_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        
        tipo_lente_var = tk.StringVar()
        tipo_lente_menu = ttk.Combobox(frame, textvariable=tipo_lente_var, state='readonly', width=30)
        tipo_lente_menu.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        tipo_lente_menu.bind('<<ComboboxSelected>>', lambda event: self.update_opcoes_lentes(event, prefix))

        setattr(self, f"{prefix}_tipo_lente_var", tipo_lente_var)
        setattr(self, f"{prefix}_tipo_lente_menu", tipo_lente_menu)

        # Esférico
        esferico_label = ttk.Label(frame, text="Valor Esférico")
        esferico_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        
        esferico_var = tk.StringVar()
        esferico_menu = ttk.Combobox(frame, textvariable=esferico_var, state='readonly', width=30)
        esferico_menu.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        setattr(self, f"{prefix}_esferico_var", esferico_var)
        setattr(self, f"{prefix}_esferico_menu", esferico_menu)

        # Cilíndrico
        cilindrico_label = ttk.Label(frame, text="Valor Cilíndrico")
        cilindrico_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')
        
        cilindrico_var = tk.StringVar()
        cilindrico_menu = ttk.Combobox(frame, textvariable=cilindrico_var, state='readonly', width=30)
        cilindrico_menu.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        setattr(self, f"{prefix}_cilindrico_var", cilindrico_var)
        setattr(self, f"{prefix}_cilindrico_menu", cilindrico_menu)

        # Adição
        adicao_label = ttk.Label(frame, text="Valor de Adição")
        adicao_label.grid(row=4, column=0, padx=10, pady=10, sticky='w')
        
        adicao_var = tk.StringVar()
        adicao_menu = ttk.Combobox(frame, textvariable=adicao_var, state='readonly', width=30)
        adicao_menu.grid(row=4, column=1, padx=10, pady=10, sticky='w')

        setattr(self, f"{prefix}_adicao_var", adicao_var)
        setattr(self, f"{prefix}_adicao_menu", adicao_menu)

    def update_tipos_lentes(self, event, prefix):
        categoria = getattr(self, f"{prefix}_categoria_var").get()
        tipo_lente_menu = getattr(self, f"{prefix}_tipo_lente_menu")

        if categoria == "Visão Simples":
            tipo_lente_menu['values'] = [lente.nome for lente in self.sistema.categorias["visao_simples"].lentes.values()]
            getattr(self, f"{prefix}_adicao_menu").config(state='disabled')
            getattr(self, f"{prefix}_cilindrico_menu").config(state='normal')
        else:
            tipo_lente_menu['values'] = [lente.nome for lente in self.sistema.categorias["progressiva"].lentes.values()]
            getattr(self, f"{prefix}_adicao_menu").config(state='normal')
            getattr(self, f"{prefix}_cilindrico_menu").config(state='disabled')
        getattr(self, f"{prefix}_tipo_lente_var").set('')
        self.update_opcoes_lentes(None, prefix)
        
    def update_opcoes_lentes(self, event, prefix):
        categoria = getattr(self, f"{prefix}_categoria_var").get()
        tipo_lente_nome = getattr(self, f"{prefix}_tipo_lente_var").get()
        
        if categoria == "Visão Simples":
            categoria_key = "visao_simples"
        else:
            categoria_key = "progressiva"
        
        tipo_lente = next((v for k, v in self.sistema.categorias[categoria_key].lentes.items() if v.nome == tipo_lente_nome), None)
        
        if tipo_lente:
            esferico_values = [str(v) for v in self.range_float(tipo_lente.esferico_range[0], tipo_lente.esferico_range[1])]
            getattr(self, f"{prefix}_esferico_menu")['values'] = esferico_values
            getattr(self, f"{prefix}_esferico_var").set('')
            
            if categoria == "Visão Simples":
                cilindrico_values = [str(v) for v in self.range_float(tipo_lente.cilindrico_range[0], tipo_lente.cilindrico_range[1])]
                getattr(self, f"{prefix}_cilindrico_menu")['values'] = cilindrico_values
                getattr(self, f"{prefix}_cilindrico_var").set('')
                getattr(self, f"{prefix}_cilindrico_menu").config(state='readonly')
            else:
                getattr(self, f"{prefix}_cilindrico_menu")['values'] = []
                getattr(self, f"{prefix}_cilindrico_var").set('')
                getattr(self, f"{prefix}_cilindrico_menu").config(state='disabled')
                
            if categoria == "Progressiva":
                adicao_values = [str(v) for v in self.range_float(tipo_lente.adicao_range[0], tipo_lente.adicao_range[1])]
                getattr(self, f"{prefix}_adicao_menu")['values'] = adicao_values
                getattr(self, f"{prefix}_adicao_var").set('')
                getattr(self, f"{prefix}_adicao_menu").config(state='readonly')
            else:
                getattr(self, f"{prefix}_adicao_menu")['values'] = []
                getattr(self, f"{prefix}_adicao_var").set('')
                getattr(self, f"{prefix}_adicao_menu").config(state='disabled')

    def calcular_preco(self):
        try:
            od_tipo_lente_nome = self.od_tipo_lente_var.get()
            oe_tipo_lente_nome = self.oe_tipo_lente_var.get()
            
            od_tipo_lente = next((v for k, v in self.sistema.categorias["visao_simples"].lentes.items() if v.nome == od_tipo_lente_nome), None) or \
                            next((v for k, v in self.sistema.categorias["progressiva"].lentes.items() if v.nome == od_tipo_lente_nome), None)
            
            oe_tipo_lente = next((v for k, v in self.sistema.categorias["visao_simples"].lentes.items() if v.nome == oe_tipo_lente_nome), None) or \
                            next((v for k, v in self.sistema.categorias["progressiva"].lentes.items() if v.nome == oe_tipo_lente_nome), None)
            
            if not od_tipo_lente or not oe_tipo_lente:
                raise ValueError("Tipo de lente não encontrado.")

            preco_debito = ((od_tipo_lente.debito + oe_tipo_lente.debito) / 2 + 40) * 4.5
            preco_credito = ((od_tipo_lente.credito + oe_tipo_lente.credito) / 2 + 40) * 5
            
            if self.armacao_var.get() == "Sim":
                preco_debito += 100.00
                preco_credito += 110.00

            preco_text = f"Preço (Débito): R$ {preco_debito:.2f}, Preço (Crédito): R$ {preco_credito:.2f}"
            self.resultado_label.config(text=preco_text)
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def resetar_opcoes(self):
        for prefix in ["od", "oe"]:
            getattr(self, f"{prefix}_categoria_var").set('')
            getattr(self, f"{prefix}_tipo_lente_var").set('')
            getattr(self, f"{prefix}_esferico_var").set('')
            getattr(self, f"{prefix}_cilindrico_var").set('')
            getattr(self, f"{prefix}_adicao_var").set('')
            getattr(self, f"{prefix}_esferico_menu")['values'] = []
            getattr(self, f"{prefix}_cilindrico_menu")['values'] = []
            getattr(self, f"{prefix}_adicao_menu")['values'] = []
            getattr(self, f"{prefix}_adicao_menu").config(state='readonly')
            getattr(self, f"{prefix}_cilindrico_menu").config(state='readonly')
        
        self.armacao_var.set('Não')
        self.resultado_label.config(text='')

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
