# ui.py

import tkinter as tk
from tkinter import ttk, messagebox
from models import SistemaLentes
from business import CalculadoraPreco
from lentes_project.sistema_lentes import SistemaLentes

class LentesApp:
    def __init__(self, root):
        self.sistema = SistemaLentes()
        self.root = root
        self.root.title("Calculadora de Lentes")
        self.root.geometry("1000x640")  # Ajustando o tamanho da janela
        self.root.configure(bg='#2F4F4F')  # Dark Green Background

        # Estilos
        self.style = ttk.Style()
        self.style.configure('TLabel', background='#2F4F4F', foreground='#FFD700', font=('Arial', 12))
        self.style.configure('TCombobox', fieldbackground='#2F4F4F', background='#2F4F4F', foreground='#000000', font=('Arial', 12))

        # Criação do Notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')

        # Frame da aba principal
        self.main_frame = tk.Frame(self.notebook, bg='#2F4F4F')
        self.notebook.add(self.main_frame, text="Calculadora de Lentes")

        # Frame da nova aba
        self.new_tab_frame = tk.Frame(self.notebook, bg='#2F4F4F')
        self.notebook.add(self.new_tab_frame, text="Nova Aba")

        # Adicionando widgets na aba principal
        self.create_main_tab_widgets()

        # Adicionando widgets na nova aba
        self.create_new_tab_widgets()

    def create_main_tab_widgets(self):
        # Molduras na aba principal
        self.od_frame = tk.LabelFrame(self.main_frame, text="OD", bg='#2F4F4F', fg='#FFD700', font=('Arial', 14, 'bold'), padx=20, pady=20)
        self.od_frame.place(x=50, y=20, width=400, height=300)

        self.oe_frame = tk.LabelFrame(self.main_frame, text="OE", bg='#2F4F4F', fg='#FFD700', font=('Arial', 14, 'bold'), padx=20, pady=20)
        self.oe_frame.place(x=550, y=20, width=400, height=300)

        self.set_frame = tk.LabelFrame(self.main_frame, text="SET", bg='#2F4F4F', fg='#FFD700', font=('Arial', 14, 'bold'), padx=20, pady=20)
        self.set_frame.place(x=50, y=330, width=400, height=200)

        self.create_widgets(self.od_frame, 'od')
        self.create_widgets(self.oe_frame, 'oe')
        self.create_set_widgets(self.set_frame)

        # Resultado
        self.resultado_debito_label = ttk.Label(self.main_frame, text="", font=("Arial", 14, "bold"))
        self.resultado_debito_label.place(x=550, y=350)

        self.resultado_credito_label = ttk.Label(self.main_frame, text="", font=("Arial", 14, "bold"))
        self.resultado_credito_label.place(x=550, y=380)

        # Botões
        self.calcular_button = tk.Button(self.main_frame, text="Calcular", command=self.calcular_preco, bg='#006400', fg='#FFD700', font=('Arial', 12, 'bold'))
        self.calcular_button.place(x=790, y=550)

        self.refazer_button = tk.Button(self.main_frame, text="Refazer", command=self.resetar_opcoes, bg='#006400', fg='#FFD700', font=('Arial', 12, 'bold'))
        self.refazer_button.place(x=890, y=550)  # margem de 5 mm da borda direita

    def create_new_tab_widgets(self):
        # Adicione os widgets específicos para a nova aba aqui
        new_tab_label = ttk.Label(self.new_tab_frame, text="Bem-vindo à Nova Aba!", font=("Arial", 16), background='#2F4F4F', foreground='#FFD700')
        new_tab_label.pack(pady=20)

    def create_widgets(self, frame, prefix):
        # Categorias
        categoria_label = ttk.Label(frame, text="Categoria de Lentes")
        categoria_label.grid(row=0, column=0, padx=(10, 0), pady=10, sticky='w')
        
        categoria_var = tk.StringVar()
        categoria_menu = ttk.Combobox(frame, textvariable=categoria_var, state='readonly', width=30)
        categoria_menu.grid(row=0, column=1, padx=(3, 10), pady=10, sticky='w')
        categoria_menu['values'] = ["Visão Simples", "Progressiva"]
        categoria_menu.bind('<<ComboboxSelected>>', lambda event: self.update_tipos_lentes(event, prefix))

        setattr(self, f"{prefix}_categoria_var", categoria_var)
        setattr(self, f"{prefix}_categoria_menu", categoria_menu)

        # Tipos de Lentes
        tipo_lente_label = ttk.Label(frame, text="Tipo de Lente")
        tipo_lente_label.grid(row=1, column=0, padx=(10, 0), pady=10, sticky='w')
        
        tipo_lente_var = tk.StringVar()
        tipo_lente_menu = ttk.Combobox(frame, textvariable=tipo_lente_var, state='readonly', width=30)
        tipo_lente_menu.grid(row=1, column=1, padx=(3, 10), pady=10, sticky='w')
        tipo_lente_menu.bind('<<ComboboxSelected>>', lambda event: self.update_opcoes_lentes(event, prefix))

        setattr(self, f"{prefix}_tipo_lente_var", tipo_lente_var)
        setattr(self, f"{prefix}_tipo_lente_menu", tipo_lente_menu)

        # Esférico
        esferico_label = ttk.Label(frame, text="Valor Esférico")
        esferico_label.grid(row=2, column=0, padx=(10, 0), pady=10, sticky='w')
        
        esferico_var = tk.StringVar()
        esferico_menu = ttk.Combobox(frame, textvariable=esferico_var, state='readonly', width=30)
        esferico_menu.grid(row=2, column=1, padx=(3, 10), pady=10, sticky='w')

        setattr(self, f"{prefix}_esferico_var", esferico_var)
        setattr(self, f"{prefix}_esferico_menu", esferico_menu)

        # Cilíndrico
        cilindrico_label = ttk.Label(frame, text="Valor Cilíndrico")
        cilindrico_label.grid(row=3, column=0, padx=(10, 0), pady=10, sticky='w')
        
        cilindrico_var = tk.StringVar()
        cilindrico_menu = ttk.Combobox(frame, textvariable=cilindrico_var, state='readonly', width=30)
        cilindrico_menu.grid(row=3, column=1, padx=(3, 10), pady=10, sticky='w')

        setattr(self, f"{prefix}_cilindrico_var", cilindrico_var)
        setattr(self, f"{prefix}_cilindrico_menu", cilindrico_menu)

        # Adição
        adicao_label = ttk.Label(frame, text="Valor de Adição")
        adicao_label.grid(row=4, column=0, padx=(10, 0), pady=10, sticky='w')
        
        adicao_var = tk.StringVar()
        adicao_menu = ttk.Combobox(frame, textvariable=adicao_var, state='readonly', width=30)
        adicao_menu.grid(row=4, column=1, padx=(3, 10), pady=10, sticky='w')

        setattr(self, f"{prefix}_adicao_var", adicao_var)
        setattr(self, f"{prefix}_adicao_menu", adicao_menu)

    def create_set_widgets(self, frame):
        # Incluir Armação
        armacao_label = ttk.Label(frame, text="Incluir Armação")
        armacao_label.grid(row=0, column=0, padx=(10, 0), pady=10, sticky='w')
        self.armacao_var = tk.StringVar(value="Não")
        armacao_sim = tk.Radiobutton(frame, text="Sim", variable=self.armacao_var, value="Sim", bg='#2F4F4F', fg='#FFD700', font=('Arial', 12))
        armacao_nao = tk.Radiobutton(frame, text="Não", variable=self.armacao_var, value="Não", bg='#2F4F4F', fg='#FFD700', font=('Arial', 12))
        armacao_sim.grid(row=0, column=1, padx=(3, 10), pady=10, sticky='w')
        armacao_nao.grid(row=0, column=2, padx=(3, 10), pady=10, sticky='w')

        # Margem
        margem_label = ttk.Label(frame, text="Margem")
        margem_label.grid(row=1, column=0, padx=(10, 0), pady=10, sticky='w')
        self.margem_var = tk.StringVar()
        margem_menu = ttk.Combobox(frame, textvariable=self.margem_var, state='readonly', width=10)  # Ajuste de largura
        margem_menu['values'] = ["250%", "300%", "350%", "400%"]
        margem_menu.grid(row=1, column=1, padx=(3, 10), pady=10, sticky='w')

        # Consulta
        consulta_label = ttk.Label(frame, text="Incluir Consulta")
        consulta_label.grid(row=2, column=0, padx=(10, 0), pady=10, sticky='w')
        self.consulta_var = tk.StringVar(value="Não")
        consulta_sim = tk.Radiobutton(frame, text="Sim", variable=self.consulta_var, value="Sim", bg='#2F4F4F', fg='#FFD700', font=('Arial', 12))
        consulta_nao = tk.Radiobutton(frame, text="Não", variable=self.consulta_var, value="Não", bg='#2F4F4F', fg='#FFD700', font=('Arial', 12))
        consulta_sim.grid(row=2, column=1, padx=(3, 10), pady=10, sticky='w')
        consulta_nao.grid(row=2, column=2, padx=(3, 10), pady=10, sticky='w')

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

            margem = float(self.margem_var.get().strip('%')) / 100
            preco_debito, preco_credito = CalculadoraPreco.calcular_preco(od_tipo_lente, oe_tipo_lente, self.armacao_var.get(), margem, self.consulta_var.get())

            self.resultado_debito_label.config(text=f"A VISTA: R$ {preco_debito:.2f}")
            self.resultado_credito_label.config(text=f"CREDITO: R$ {preco_credito:.2f}")
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
        self.margem_var.set('')
        self.consulta_var.set('Não')
        self.resultado_debito_label.config(text='')
        self.resultado_credito_label.config(text='')

    def range_float(self, start, end, step=0.25):
        values = []
        while start <= end:
            values.append(round(start, 2))
            start += step
        return values
