import tkinter as tk
from tkinter import ttk, messagebox
from model.jogador import Jogador
from dao.jogador_dao import JogadorDAO
from dao.equipe_dao import EquipeDAO

class JogadorView:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Gerenciar Jogadores")
        self.window.geometry("1000x600")
        
        frame_form = tk.Frame(self.window)
        frame_form.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(frame_form, text="Nome:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_nome = tk.Entry(frame_form, width=30)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_form, text="CPF:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.entry_cpf = tk.Entry(frame_form, width=20)
        self.entry_cpf.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(frame_form, text="Nickname:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_nickname = tk.Entry(frame_form, width=20)
        self.entry_nickname.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame_form, text="Equipe:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.combo_equipe = ttk.Combobox(frame_form, width=28, state="readonly")
        self.combo_equipe.grid(row=1, column=3, padx=5, pady=5)
        self.carregar_equipes()
        
        frame_buttons = tk.Frame(self.window)
        frame_buttons.pack(pady=10)
        
        tk.Button(frame_buttons, text="Inserir", command=self.inserir, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Atualizar", command=self.atualizar, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Excluir", command=self.excluir, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Limpar", command=self.limpar, width=10).pack(side=tk.LEFT, padx=5)
        
        frame_filtro = tk.Frame(self.window)
        frame_filtro.pack(pady=10)
        
        tk.Label(frame_filtro, text="Filtrar por Equipe:").pack(side=tk.LEFT, padx=5)
        self.filtro_equipe = ttk.Combobox(frame_filtro, width=25, state="readonly")
        self.filtro_equipe.pack(side=tk.LEFT, padx=5)
        self.carregar_filtro_equipes()
        
        tk.Button(frame_filtro, text="Filtrar", command=self.filtrar).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_filtro, text="Listar Todos", command=self.listar).pack(side=tk.LEFT, padx=5)
        
        frame_tree = tk.Frame(self.window)
        frame_tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(frame_tree, columns=("ID", "Nome", "CPF", "Nickname", "Equipe"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("CPF", text="CPF")
        self.tree.heading("Nickname", text="Nickname")
        self.tree.heading("Equipe", text="Equipe")
        
        self.tree.column("ID", width=50)
        self.tree.column("Nome", width=200)
        self.tree.column("CPF", width=150)
        self.tree.column("Nickname", width=150)
        self.tree.column("Equipe", width=200)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self.selecionar)
        
        scrollbar = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.listar()
        self.jogador_selecionado = None
        self.equipes_dict = {}

    def carregar_equipes(self):
        equipes = EquipeDAO.listar_todos()
        self.equipes_dict = {equipe.nome: equipe.id for equipe in equipes}
        self.combo_equipe['values'] = list(self.equipes_dict.keys())

    def carregar_filtro_equipes(self):
        equipes = EquipeDAO.listar_todos()
        self.filtro_equipes_dict = {equipe.nome: equipe.id for equipe in equipes}
        self.filtro_equipe['values'] = list(self.filtro_equipes_dict.keys())

    def inserir(self):
        if not self.validar_campos():
            return
        jogador = Jogador(nome=self.entry_nome.get(), cpf=self.entry_cpf.get(), 
                         nickname=self.entry_nickname.get(), equipe_id=self.equipes_dict[self.combo_equipe.get()])
        try:
            JogadorDAO.inserir(jogador)
            messagebox.showinfo("Sucesso", "Jogador inserido com sucesso!")
            self.limpar()
            self.listar()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inserir: {str(e)}")

    def atualizar(self):
        if not self.jogador_selecionado:
            messagebox.showwarning("Aviso", "Selecione um jogador")
            return
        if not self.validar_campos():
            return
        self.jogador_selecionado.nome = self.entry_nome.get()
        self.jogador_selecionado.cpf = self.entry_cpf.get()
        self.jogador_selecionado.nickname = self.entry_nickname.get()
        self.jogador_selecionado.equipe_id = self.equipes_dict[self.combo_equipe.get()]
        try:
            JogadorDAO.atualizar(self.jogador_selecionado)
            messagebox.showinfo("Sucesso", "Jogador atualizado!")
            self.limpar()
            self.listar()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {str(e)}")

    def excluir(self):
        if not self.jogador_selecionado:
            messagebox.showwarning("Aviso", "Selecione um jogador")
            return
        if messagebox.askyesno("Confirmar", "Excluir jogador?"):
            JogadorDAO.excluir(self.jogador_selecionado.id)
            messagebox.showinfo("Sucesso", "Jogador excluído!")
            self.limpar()
            self.listar()

    def listar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        jogadores = JogadorDAO.listar_todos()
        for j in jogadores:
            equipe = EquipeDAO.buscar_por_id(j.equipe_id)
            self.tree.insert("", tk.END, values=(j.id, j.nome, j.cpf, j.nickname, equipe.nome if equipe else ""))

    def filtrar(self):
        if not self.filtro_equipe.get():
            messagebox.showwarning("Aviso", "Selecione uma equipe")
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        equipe_id = self.filtro_equipes_dict[self.filtro_equipe.get()]
        jogadores = JogadorDAO.filtrar_por_equipe(equipe_id)
        for j in jogadores:
            equipe = EquipeDAO.buscar_por_id(j.equipe_id)
            self.tree.insert("", tk.END, values=(j.id, j.nome, j.cpf, j.nickname, equipe.nome if equipe else ""))

    def selecionar(self, event):
        item = self.tree.selection()[0]
        valores = self.tree.item(item, "values")
        self.jogador_selecionado = JogadorDAO.buscar_por_id(int(valores[0]))
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, self.jogador_selecionado.nome)
        self.entry_cpf.delete(0, tk.END)
        self.entry_cpf.insert(0, self.jogador_selecionado.cpf)
        self.entry_nickname.delete(0, tk.END)
        self.entry_nickname.insert(0, self.jogador_selecionado.nickname)
        equipe = EquipeDAO.buscar_por_id(self.jogador_selecionado.equipe_id)
        self.combo_equipe.set(equipe.nome if equipe else "")

    def limpar(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_cpf.delete(0, tk.END)
        self.entry_nickname.delete(0, tk.END)
        self.combo_equipe.set("")
        self.jogador_selecionado = None

    def validar_campos(self):
        if not self.entry_nome.get():
            messagebox.showwarning("Aviso", "Nome obrigatório")
            return False
        if not self.entry_cpf.get():
            messagebox.showwarning("Aviso", "CPF obrigatório")
            return False
        if not Jogador.validar_cpf(self.entry_cpf.get()):
            messagebox.showwarning("Aviso", "CPF inválido")
            return False
        if not self.entry_nickname.get():
            messagebox.showwarning("Aviso", "Nickname obrigatório")
            return False
        if not self.combo_equipe.get():
            messagebox.showwarning("Aviso", "Equipe obrigatória")
            return False
        return True
