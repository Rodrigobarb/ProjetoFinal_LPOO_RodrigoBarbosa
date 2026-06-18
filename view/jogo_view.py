import tkinter as tk
from tkinter import ttk, messagebox
from model.jogo import Jogo
from dao.jogo_dao import JogoDAO

class JogoView:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Gerenciar Jogos")
        self.window.geometry("900x600")
        
        # Frame de formulário
        frame_form = tk.Frame(self.window)
        frame_form.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(frame_form, text="Nome:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_nome = tk.Entry(frame_form, width=30)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_form, text="Gênero:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.entry_genero = tk.Entry(frame_form, width=20)
        self.entry_genero.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(frame_form, text="Plataforma:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_plataforma = tk.Entry(frame_form, width=20)
        self.entry_plataforma.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame_form, text="Max Jogadores/Equipe:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.entry_max_jogadores = tk.Entry(frame_form, width=10)
        self.entry_max_jogadores.grid(row=1, column=3, padx=5, pady=5)
        
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
        
        tk.Label(frame_filtro, text="Filtrar por Gênero:").pack(side=tk.LEFT, padx=5)
        self.filtro_genero = tk.Entry(frame_filtro, width=15)
        self.filtro_genero.pack(side=tk.LEFT, padx=5)
        
        tk.Label(frame_filtro, text="Plataforma:").pack(side=tk.LEFT, padx=5)
        self.filtro_plataforma = tk.Entry(frame_filtro, width=15)
        self.filtro_plataforma.pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_filtro, text="Filtrar", command=self.filtrar).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_filtro, text="Listar Todos", command=self.listar).pack(side=tk.LEFT, padx=5)
        
        # Treeview
        frame_tree = tk.Frame(self.window)
        frame_tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(frame_tree, columns=("ID", "Nome", "Gênero", "Plataforma", "Max Jogadores"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Gênero", text="Gênero")
        self.tree.heading("Plataforma", text="Plataforma")
        self.tree.heading("Max Jogadores", text="Max Jogadores/Equipe")
        
        self.tree.column("ID", width=50)
        self.tree.column("Nome", width=250)
        self.tree.column("Gênero", width=150)
        self.tree.column("Plataforma", width=150)
        self.tree.column("Max Jogadores", width=150)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self.selecionar)
        
        scrollbar = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.listar()
        self.jogo_selecionado = None

    def inserir(self):
        if not self.validar_campos():
            return
        try:
            jogo = Jogo(
                nome=self.entry_nome.get(),
                genero=self.entry_genero.get(),
                plataforma=self.entry_plataforma.get(),
                max_jogadores_equipe=int(self.entry_max_jogadores.get())
            )
            JogoDAO.inserir(jogo)
            messagebox.showinfo("Sucesso", "Jogo inserido com sucesso!")
            self.limpar()
            self.listar()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inserir jogo: {str(e)}")

    def atualizar(self):
        if not self.jogo_selecionado:
            messagebox.showwarning("Aviso", "Selecione um jogo para atualizar")
            return
        if not self.validar_campos():
            return
        self.jogo_selecionado.nome = self.entry_nome.get()
        self.jogo_selecionado.genero = self.entry_genero.get()
        self.jogo_selecionado.plataforma = self.entry_plataforma.get()
        self.jogo_selecionado.max_jogadores_equipe = int(self.entry_max_jogadores.get())
        JogoDAO.atualizar(self.jogo_selecionado)
        messagebox.showinfo("Sucesso", "Jogo atualizado com sucesso!")
        self.limpar()
        self.listar()

    def excluir(self):
        if not self.jogo_selecionado:
            messagebox.showwarning("Aviso", "Selecione um jogo para excluir")
            return
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este jogo?"):
            try:
                JogoDAO.excluir(self.jogo_selecionado.id)
                messagebox.showinfo("Sucesso", "Jogo excluído com sucesso!")
                self.limpar()
                self.listar()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir jogo: {str(e)}")

    def listar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        jogos = JogoDAO.listar_todos()
        for jogo in jogos:
            self.tree.insert("", tk.END, values=(jogo.id, jogo.nome, jogo.genero, jogo.plataforma, jogo.max_jogadores_equipe))

    def filtrar(self):
        genero = self.filtro_genero.get().strip() if self.filtro_genero.get() else None
        plataforma = self.filtro_plataforma.get().strip() if self.filtro_plataforma.get() else None
        if not genero and not plataforma:
            messagebox.showwarning("Aviso", "Preencha pelo menos um filtro (Gênero ou Plataforma)")
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        jogos = JogoDAO.filtrar(genero, plataforma)
        for jogo in jogos:
            self.tree.insert("", tk.END, values=(jogo.id, jogo.nome, jogo.genero, jogo.plataforma, jogo.max_jogadores_equipe))

    def selecionar(self, event):
        if not self.tree.selection():
            return
        item = self.tree.selection()[0]
        valores = self.tree.item(item, "values")
        self.jogo_selecionado = JogoDAO.buscar_por_id(int(valores[0]))
        if not self.jogo_selecionado:
            return
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, self.jogo_selecionado.nome)
        self.entry_genero.delete(0, tk.END)
        self.entry_genero.insert(0, self.jogo_selecionado.genero)
        self.entry_plataforma.delete(0, tk.END)
        self.entry_plataforma.insert(0, self.jogo_selecionado.plataforma)
        self.entry_max_jogadores.delete(0, tk.END)
        self.entry_max_jogadores.insert(0, self.jogo_selecionado.max_jogadores_equipe)

    def limpar(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_genero.delete(0, tk.END)
        self.entry_plataforma.delete(0, tk.END)
        self.entry_max_jogadores.delete(0, tk.END)
        self.jogo_selecionado = None

    def validar_campos(self):
        if not self.entry_nome.get():
            messagebox.showwarning("Aviso", "Nome é obrigatório")
            return False
        if not self.entry_genero.get():
            messagebox.showwarning("Aviso", "Gênero é obrigatório")
            return False
        if not self.entry_plataforma.get():
            messagebox.showwarning("Aviso", "Plataforma é obrigatória")
            return False
        try:
            max_jog = int(self.entry_max_jogadores.get())
            if max_jog <= 0:
                raise ValueError
        except:
            messagebox.showwarning("Aviso", "Max Jogadores deve ser um número positivo")
            return False
        return True
