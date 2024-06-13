# ui.py

import tkinter as tk
from tkinter import ttk, messagebox
from models import SistemaLentes
from business import CalculadoraPreco
from lentes_project.sistema_lentes import SistemaLentes
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import tempfile
import os
import subprocess
import webbrowser

class LentesApp:
    def __init__(self, root):
        self.sistema = SistemaLentes()
        self.root = root
        self.root.title("Calculadora de Lentes")
        self.root.geometry("1200x600")  # Ajustando o tamanho da janela
        self.root.configure(bg='#2F4F4F')  # Dark Green Background

        # Estilos
        self.style = ttk.Style()
        self.style.configure('TLabel', background='#2F4F4F', foreground='#FFD700', font=('Arial', 12))
        self.style.configure('TCombobox', fieldbackground='#2F4F4F', background='#2F4F4F', foreground='#000000', font=('Arial', 12))
        self.style.configure('Treeview', background='#2F4F4F', foreground='#FFD700', rowheight=25, fieldbackground='#2F4F4F')
        self.style.configure('Treeview.Heading', background='#2F4F4F', foreground='#FFD700', font=('Arial', 12, 'bold'))

        # Criação do Notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')

        # Frame da aba principal
        self.main_frame = tk.Frame(self.notebook, bg='#2F4F4F')
        self.notebook.add(self.main_frame, text="Calculadora de Lentes")

        # Frame da aba de detalhamento
        self.detail_frame = tk.Frame(self.notebook, bg='#2F4F4F')
        self.notebook.add(self.detail_frame, text="Detalhamento")

        # Adicionando widgets na aba principal
        self.create_main_tab_widgets()

        # Adicionando widgets na aba de detalhamento
        self.create_detail_tab_widgets()

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

    def create_detail_tab_widgets(self):
        # Moldura para a planilha
        self.detail_frame_inner = tk.LabelFrame(self.detail_frame, text="Planilha Financeira", bg='#2F4F4F', fg='#FFD700', font=('Arial', 14, 'bold'), padx=10, pady=10)
        self.detail_frame_inner.pack(expand=True, fill='both', padx=20, pady=20)

        # Configurar colunas da planilha
        self.tree = ttk.Treeview(self.detail_frame_inner, columns=("produto", "valor_lente", "custo", "margem", "renda_liquida"), show='headings')
        self.tree.heading("produto", text="Produto")
        self.tree.heading("valor_lente", text="Valor da Lente")
        self.tree.heading("custo", text="Custo")
        self.tree.heading("margem", text="Margem")
        self.tree.heading("renda_liquida", text="Renda Líquida")

        self.tree.column("produto", anchor='center', width=200)
        self.tree.column("valor_lente", anchor='center', width=150)
        self.tree.column("custo", anchor='center', width=100)
        self.tree.column("margem", anchor='center', width=100)
        self.tree.column("renda_liquida", anchor='center', width=200)

        self.tree.pack(expand=True, fill='both')

        # Add grid lines
        self.tree.tag_configure('evenrow', background='#3E3E3E')
        self.tree.tag_configure('oddrow', background='#2F4F4F')

        # Botão de imprimir
        self.imprimir_button = tk.Button(self.detail_frame, text="Imprimir", command=self.imprimir, bg='#006400', fg='#FFD700', font=('Arial', 12, 'bold'))
        self.imprimir_button.pack(pady=10)

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

            # Atualizar a planilha na aba de detalhamento
            self.update_detail_tab(od_tipo_lente, oe_tipo_lente, margem, self.armacao_var.get())
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def update_detail_tab(self, od_tipo_lente, oe_tipo_lente, margem, incluir_armacao):
        for item in self.tree.get_children():
            self.tree.delete(item)

        produtos = [
            ("Lente OD", od_tipo_lente.debito / 2, od_tipo_lente.debito, margem),
            ("Lente OE", oe_tipo_lente.debito / 2, oe_tipo_lente.debito, margem),
            ("Montagem", 30.00, 30.00, 0.4)  # Valor fixo para montagem e margem fixa de 40%
        ]

        if incluir_armacao == "Sim":
            produtos.append(("Armação", 100.00, 100.00, 0.4))  # Margem fixa de 40%

        for i, (produto, valor_lente, custo, margem) in enumerate(produtos):
            renda_liquida = custo * margem
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert('', 'end', values=(produto, f"R$ {valor_lente:.2f}", f"R$ {custo:.2f}", f"{margem * 100:.0f}%", f"R$ {renda_liquida:.2f}"), tags=(tag,))

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

        for item in self.tree.get_children():
            self.tree.delete(item)

    def range_float(self, start, end, step=0.25):
        values = []
        while start <= end:
            values.append(round(start, 2))
            start += step
        return values
    
    def imprimir(self):
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            c = canvas.Canvas(tmp_file.name, pagesize=A4)
            width, height = A4

            # Set the title and styles
            c.setFont("Helvetica-Bold", 16)
            c.drawString(100, height - 50, "Detalhamento Financeiro")

            c.setFont("Helvetica", 12)
            x_offset = 50
            y_offset = height - 100
            line_height = 20

            # Draw the table headers
            headers = ["Produto", "Valor da Lente", "Custo", "Margem", "Renda Líquida"]
            for i, header in enumerate(headers):
                c.drawString(x_offset + i*120, y_offset, header)

            # Draw the table content
            for i, row in enumerate(self.tree.get_children()):
                y_offset -= line_height
                item = self.tree.item(row)['values']
                for j, value in enumerate(item):
                    c.drawString(x_offset + j*120, y_offset, str(value))

            c.save()

        # Open the PDF with the default application
        webbrowser.open(tmp_file.name)
