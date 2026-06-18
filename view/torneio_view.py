import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from model.torneio_factory import TorneiFactory
from model.status_torneio import StatusTorneio
from dao.torneio_dao import TorneiDAO
from dao.jogo_dao import JogoDAO

class TorneiView:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Gerenciar Torneios")
        self.window.geometry("1000x600")
        
        frame_form = tk.Frame(self.window)
        frame_form.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(frame_form, text="Nome:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_nome = tk.Entry(frame_form, width=30)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_form, text="Data Início:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.entry_data = tk.Entry(frame_form, width=15)
        self.entry_data.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_data.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(frame_form, text="Tipo:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.combo_tipo = ttk.Combobox(frame_form, width=28, state="readonly", values=["ELIMINACAO", "PONTOS"])
        self.combo_tipo.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame_form, text="Status:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.combo_status = ttk.Combobox(frame_form, width=13, state="readonly", 
                                         values=["ABERTO", "EM_ANDAMENTO", "FINALIZADO"])
        self.combo_status.set("ABERTO")
        self.combo_status.grid(row=1, column=3, padx=5, pady=5)
        
        tk.Label(frame_form, text="Jogo:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.combo_jogo = ttk.Combobox(frame_form, width=28, state="readonly")
        self.combo_jogo.grid(row=2, column=1, padx=5, pady=5)
        self.carregar_jogos()
        
        frame_buttons = tk.Frame(self.window)
        frame_buttons.pack(pady=10)
        
        tk.Button(frame_buttons, text="Inserir", command=self.inserir, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Atualizar", command=self.atualizar, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Excluir", command=self.excluir, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Limpar", command=self.limpar, width=10).pack(side=tk.LEFT, padx=5)
        
        frame_filtro = tk.Frame(self.window)
        frame_filtro.pack(pady=10)
        
        tk.Label(frame_filtro, text="Filtrar por Status:").pack(side=tk.LEFT, padx=5)
        self.filtro_status = ttk.Combobox(frame_filtro, width=15, state="readonly", 
                                          values=["ABERTO", "EM_ANDAMENTO", "FINALIZADO"])
        self.filtro_status.pack(side=tk.LEFT, padx=5)
        
        tk.Label(frame_filtro, text="Tipo:").pack(side=tk.LEFT, padx=5)
        self.filtro_tipo = ttk.Combobox(frame_filtro, width=15, state="readonly", 
                                         values=["ELIMINACAO", "PONTOS"])
        self.filtro_tipo.pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_filtro, text="Filtrar", command=self.filtrar).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_filtro, text="Listar Todos", command=self.listar).pack(side=tk.LEFT, padx=5)
        
        frame_tree = tk.Frame(self.window)
        frame_tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(frame_tree, columns=("ID", "Nome", "Data", "Tipo", "Status", "Jogo"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Data", text="Data Início")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Jogo", text="Jogo")
        
        self.tree.column("ID", width=50)
        self.tree.column("Nome", width=250)
        self.tree.column("Data", width=100)
        self.tree.column("Tipo", width=100)
        self.tree.column("Status", width=120)
        self.tree.column("Jogo", width=200)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self.selecionar)
        
        scrollbar = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.torneio_selecionado = None
        self.listar()

    def carregar_jogos(self):
        jogos = JogoDAO.listar_todos()
        self.jogos_dict = {jogo.nome: jogo.id for jogo in jogos}
        self.combo_jogo['values'] = list(self.jogos_dict.keys())

    def inserir(self):
        if not self.validar_campos():
            return
        try:
            torneio = TorneiFactory.criar_torneio(
                tipo=self.combo_tipo.get(),
                nome=self.entry_nome.get(),
                data_inicio=datetime.strptime(self.entry_data.get(), "%Y-%m-%d").date(),
                jogo_id=self.jogos_dict[self.combo_jogo.get()],
                status=StatusTorneio[self.combo_status.get()]
            )
            TorneiDAO.inserir(torneio)
            messagebox.showinfo("Sucesso", f"Torneio {torneio.get_tipo()} criado via Factory!")
            self.limpar()
            self.listar()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inserir torneio: {str(e)}")

    def atualizar(self):
        if not self.torneio_selecionado:
            messagebox.showwarning("Aviso", "Selecione um torneio")
            return
        if not self.validar_campos():
            return
        try:
            # Se o tipo mudou, recriar o torneio via Factory para manter o polimorfismo
            tipo_novo = self.combo_tipo.get()
            if tipo_novo != self.torneio_selecionado.get_tipo():
                torneio = TorneiFactory.criar_torneio(
                    tipo=tipo_novo,
                    nome=self.entry_nome.get(),
                    data_inicio=datetime.strptime(self.entry_data.get(), "%Y-%m-%d").date(),
                    jogo_id=self.jogos_dict[self.combo_jogo.get()],
                    status=StatusTorneio[self.combo_status.get()],
                    id=self.torneio_selecionado.id
                )
            else:
                torneio = self.torneio_selecionado
                torneio.nome = self.entry_nome.get()
                torneio.data_inicio = datetime.strptime(self.entry_data.get(), "%Y-%m-%d").date()
                torneio.status = StatusTorneio[self.combo_status.get()]
                torneio.jogo_id = self.jogos_dict[self.combo_jogo.get()]
            TorneiDAO.atualizar(torneio)
            messagebox.showinfo("Sucesso", "Torneio atualizado!")
            self.limpar()
            self.listar()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar torneio: {str(e)}")

    def excluir(self):
        if not self.torneio_selecionado:
            messagebox.showwarning("Aviso", "Selecione um torneio")
            return
        if messagebox.askyesno("Confirmar", "Excluir torneio?"):
            try:
                TorneiDAO.excluir(self.torneio_selecionado.id)
                messagebox.showinfo("Sucesso", "Torneio excluído!")
                self.limpar()
                self.listar()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir torneio: {str(e)}")

    def listar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Limpar combos de filtro ao listar todos
        self.filtro_status.set("")
        self.filtro_tipo.set("")
        torneios = TorneiDAO.listar_todos()
        for t in torneios:
            jogo = JogoDAO.buscar_por_id(t.jogo_id)
            self.tree.insert("", tk.END, values=(t.id, t.nome, t.data_inicio, t.get_tipo(), t.status.value, jogo.nome if jogo else ""))

    def filtrar(self):
        filtro_status = self.filtro_status.get()
        filtro_tipo = self.filtro_tipo.get()
        
        if not filtro_status and not filtro_tipo:
            messagebox.showwarning("Aviso", "Selecione pelo menos um filtro (Status ou Tipo)")
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Buscar todos e filtrar localmente para suportar combinação de filtros
        torneios = TorneiDAO.listar_todos()
        
        if filtro_status:
            status = StatusTorneio[filtro_status]
            torneios = [t for t in torneios if t.status == status]
        
        if filtro_tipo:
            torneios = [t for t in torneios if t.get_tipo() == filtro_tipo]
        
        for t in torneios:
            jogo = JogoDAO.buscar_por_id(t.jogo_id)
            self.tree.insert("", tk.END, values=(t.id, t.nome, t.data_inicio, t.get_tipo(), t.status.value, jogo.nome if jogo else ""))

    def selecionar(self, event):
        if not self.tree.selection():
            return
        item = self.tree.selection()[0]
        valores = self.tree.item(item, "values")
        self.torneio_selecionado = TorneiDAO.buscar_por_id(int(valores[0]))
        if not self.torneio_selecionado:
            return
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, self.torneio_selecionado.nome)
        self.entry_data.delete(0, tk.END)
        self.entry_data.insert(0, self.torneio_selecionado.data_inicio)
        self.combo_tipo.set(self.torneio_selecionado.get_tipo())
        self.combo_status.set(self.torneio_selecionado.status.value)
        jogo = JogoDAO.buscar_por_id(self.torneio_selecionado.jogo_id)
        self.combo_jogo.set(jogo.nome if jogo else "")

    def limpar(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_data.delete(0, tk.END)
        self.entry_data.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.combo_tipo.set("")
        self.combo_status.set("ABERTO")
        self.combo_jogo.set("")
        self.torneio_selecionado = None

    def validar_campos(self):
        if not self.entry_nome.get():
            messagebox.showwarning("Aviso", "Nome obrigatório")
            return False
        if not self.combo_tipo.get():
            messagebox.showwarning("Aviso", "Tipo obrigatório")
            return False
        if not self.combo_jogo.get():
            messagebox.showwarning("Aviso", "Jogo obrigatório")
            return False
        try:
            datetime.strptime(self.entry_data.get(), "%Y-%m-%d")
        except:
            messagebox.showwarning("Aviso", "Data inválida (AAAA-MM-DD)")
            return False
        return True
