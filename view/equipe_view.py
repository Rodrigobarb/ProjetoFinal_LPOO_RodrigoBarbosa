import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from model.equipe import Equipe
from dao.equipe_dao import EquipeDAO
from dao.jogo_dao import JogoDAO

class EquipeView:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Gerenciar Equipes")
        self.window.geometry("900x600")
        
        # Frame de formulário
        frame_form = tk.Frame(self.window)
        frame_form.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(frame_form, text="Nome:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_nome = tk.Entry(frame_form, width=30)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_form, text="Data Criação:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.entry_data = tk.Entry(frame_form, width=15)
        self.entry_data.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_data.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(frame_form, text="Jogo:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.combo_jogo = ttk.Combobox(frame_form, width=28, state="readonly")
        self.combo_jogo.grid(row=1, column=1, padx=5, pady=5)
        self.carregar_jogos()
        
        # Botões
        frame_buttons = tk.Frame(self.window)
        frame_buttons.pack(pady=10)
        
        tk.Button(frame_buttons, text="Inserir", command=self.inserir, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Atualizar", command=self.atualizar, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Excluir", command=self.excluir, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Limpar", command=self.limpar, width=10).pack(side=tk.LEFT, padx=5)
        
        # Filtros
        frame_filtro = tk.Frame(self.window)
        frame_filtro.pack(pady=10)
        
        tk.Label(frame_filtro, text="Filtrar por Jogo:").pack(side=tk.LEFT, padx=5)
        self.filtro_jogo = ttk.Combobox(frame_filtro, width=25, state="readonly")
        self.filtro_jogo.pack(side=tk.LEFT, padx=5)
        self.carregar_filtro_jogos()
        
        tk.Button(frame_filtro, text="Filtrar", command=self.filtrar).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_filtro, text="Listar Todos", command=self.listar).pack(side=tk.LEFT, padx=5)
        
        # Treeview
        frame_tree = tk.Frame(self.window)
        frame_tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(frame_tree, columns=("ID", "Nome", "Data Criação", "Jogo"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Data Criação", text="Data Criação")
        self.tree.heading("Jogo", text="Jogo")
        
        self.tree.column("ID", width=50)
        self.tree.column("Nome", width=250)
        self.tree.column("Data Criação", width=150)
        self.tree.column("Jogo", width=250)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self.selecionar)
        
        scrollbar = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.listar()
        self.equipe_selecionada = None
        self.jogos_dict = {}

    def carregar_jogos(self):
        jogos = JogoDAO.listar_todos()
        self.jogos_dict = {jogo.nome: jogo.id for jogo in jogos}
        self.combo_jogo['values'] = list(self.jogos_dict.keys())

    def carregar_filtro_jogos(self):
        jogos = JogoDAO.listar_todos()
        self.filtro_jogos_dict = {jogo.nome: jogo.id for jogo in jogos}
        self.filtro_jogo['values'] = list(self.filtro_jogos_dict.keys())

    def inserir(self):
        if not self.validar_campos():
            return
        equipe = Equipe(
            nome=self.entry_nome.get(),
            data_criacao=datetime.strptime(self.entry_data.get(), "%Y-%m-%d").date(),
            jogo_id=self.jogos_dict[self.combo_jogo.get()]
        )
        EquipeDAO.inserir(equipe)
        messagebox.showinfo("Sucesso", "Equipe inserida com sucesso!")
        self.limpar()
        self.listar()

    def atualizar(self):
        if not self.equipe_selecionada:
            messagebox.showwarning("Aviso", "Selecione uma equipe para atualizar")
            return
        if not self.validar_campos():
            return
        self.equipe_selecionada.nome = self.entry_nome.get()
        self.equipe_selecionada.data_criacao = datetime.strptime(self.entry_data.get(), "%Y-%m-%d").date()
        self.equipe_selecionada.jogo_id = self.jogos_dict[self.combo_jogo.get()]
        EquipeDAO.atualizar(self.equipe_selecionada)
        messagebox.showinfo("Sucesso", "Equipe atualizada com sucesso!")
        self.limpar()
        self.listar()

    def excluir(self):
        if not self.equipe_selecionada:
            messagebox.showwarning("Aviso", "Selecione uma equipe para excluir")
            return
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir esta equipe?"):
            EquipeDAO.excluir(self.equipe_selecionada.id)
            messagebox.showinfo("Sucesso", "Equipe excluída com sucesso!")
            self.limpar()
            self.listar()

    def listar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        equipes = EquipeDAO.listar_todos()
        for equipe in equipes:
            jogo = JogoDAO.buscar_por_id(equipe.jogo_id)
            self.tree.insert("", tk.END, values=(equipe.id, equipe.nome, equipe.data_criacao, jogo.nome if jogo else ""))

    def filtrar(self):
        if not self.filtro_jogo.get():
            messagebox.showwarning("Aviso", "Selecione um jogo para filtrar")
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        jogo_id = self.filtro_jogos_dict[self.filtro_jogo.get()]
        equipes = EquipeDAO.filtrar_por_jogo(jogo_id)
        for equipe in equipes:
            jogo = JogoDAO.buscar_por_id(equipe.jogo_id)
            self.tree.insert("", tk.END, values=(equipe.id, equipe.nome, equipe.data_criacao, jogo.nome if jogo else ""))

    def selecionar(self, event):
        item = self.tree.selection()[0]
        valores = self.tree.item(item, "values")
        self.equipe_selecionada = EquipeDAO.buscar_por_id(int(valores[0]))
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, self.equipe_selecionada.nome)
        self.entry_data.delete(0, tk.END)
        self.entry_data.insert(0, self.equipe_selecionada.data_criacao)
        jogo = JogoDAO.buscar_por_id(self.equipe_selecionada.jogo_id)
        self.combo_jogo.set(jogo.nome if jogo else "")

    def limpar(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_data.delete(0, tk.END)
        self.entry_data.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.combo_jogo.set("")
        self.equipe_selecionada = None

    def validar_campos(self):
        if not self.entry_nome.get():
            messagebox.showwarning("Aviso", "Nome é obrigatório")
            return False
        if not self.combo_jogo.get():
            messagebox.showwarning("Aviso", "Jogo é obrigatório")
            return False
        try:
            datetime.strptime(self.entry_data.get(), "%Y-%m-%d")
        except:
            messagebox.showwarning("Aviso", "Data inválida (formato: AAAA-MM-DD)")
            return False
        return True
