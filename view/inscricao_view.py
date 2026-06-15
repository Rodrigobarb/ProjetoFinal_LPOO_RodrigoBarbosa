import tkinter as tk
from tkinter import ttk, messagebox
from model.inscricao import Inscricao
from model.status_torneio import StatusTorneio
from dao.inscricao_dao import InscricaoDAO
from dao.torneio_dao import TorneiDAO
from dao.equipe_dao import EquipeDAO

class InscricaoView:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Inscrições em Torneios")
        self.window.geometry("900x600")
        
        frame_form = tk.Frame(self.window)
        frame_form.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(frame_form, text="Torneio:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.combo_torneio = ttk.Combobox(frame_form, width=40, state="readonly")
        self.combo_torneio.grid(row=0, column=1, padx=5, pady=5)
        self.combo_torneio.bind("<<ComboboxSelected>>", self.atualizar_lista_inscricoes)
        self.carregar_torneios()
        
        tk.Label(frame_form, text="Equipe:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.combo_equipe = ttk.Combobox(frame_form, width=40, state="readonly")
        self.combo_equipe.grid(row=1, column=1, padx=5, pady=5)
        self.carregar_equipes()
        
        frame_buttons = tk.Frame(self.window)
        frame_buttons.pack(pady=10)
        
        tk.Button(frame_buttons, text="Inscrever Equipe", command=self.inscrever, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Cancelar Inscrição", command=self.cancelar, width=15).pack(side=tk.LEFT, padx=5)
        
        tk.Label(self.window, text="Equipes Inscritas:", font=("Arial", 12, "bold")).pack(pady=10)
        
        frame_tree = tk.Frame(self.window)
        frame_tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(frame_tree, columns=("ID", "Equipe", "Data Inscrição"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Equipe", text="Equipe")
        self.tree.heading("Data Inscrição", text="Data Inscrição")
        
        self.tree.column("ID", width=80)
        self.tree.column("Equipe", width=300)
        self.tree.column("Data Inscrição", width=200)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.torneios_dict = {}
        self.equipes_dict = {}

    def carregar_torneios(self):
        torneios = TorneiDAO.listar_todos()
        self.torneios_dict = {f"{t.nome} ({t.get_tipo()})": t for t in torneios}
        self.combo_torneio['values'] = list(self.torneios_dict.keys())

    def carregar_equipes(self):
        equipes = EquipeDAO.listar_todos()
        self.equipes_dict = {equipe.nome: equipe.id for equipe in equipes}
        self.combo_equipe['values'] = list(self.equipes_dict.keys())

    def inscrever(self):
        if not self.combo_torneio.get():
            messagebox.showwarning("Aviso", "Selecione um torneio")
            return
        if not self.combo_equipe.get():
            messagebox.showwarning("Aviso", "Selecione uma equipe")
            return
        
        torneio = self.torneios_dict[self.combo_torneio.get()]
        equipe_id = self.equipes_dict[self.combo_equipe.get()]
        
        # Validação: torneio deve estar ABERTO
        if torneio.status != StatusTorneio.ABERTO:
            messagebox.showerror("Erro", "Apenas torneios com status ABERTO aceitam inscrições!")
            return
        
        # Validação: equipe não pode estar já inscrita
        if InscricaoDAO.verificar_inscricao_existente(equipe_id, torneio.id):
            messagebox.showerror("Erro", "Esta equipe já está inscrita neste torneio!")
            return
        
        inscricao = Inscricao(equipe_id=equipe_id, torneio_id=torneio.id)
        InscricaoDAO.inserir(inscricao)
        messagebox.showinfo("Sucesso", "Equipe inscrita com sucesso!")
        self.atualizar_lista_inscricoes()

    def cancelar(self):
        if not self.tree.selection():
            messagebox.showwarning("Aviso", "Selecione uma inscrição")
            return
        
        item = self.tree.selection()[0]
        valores = self.tree.item(item, "values")
        inscricao_id = int(valores[0])
        
        if messagebox.askyesno("Confirmar", "Cancelar inscrição?"):
            InscricaoDAO.excluir(inscricao_id)
            messagebox.showinfo("Sucesso", "Inscrição cancelada!")
            self.atualizar_lista_inscricoes()

    def atualizar_lista_inscricoes(self, event=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not self.combo_torneio.get():
            return
        
        torneio = self.torneios_dict[self.combo_torneio.get()]
        inscricoes = InscricaoDAO.listar_por_torneio(torneio.id)
        
        for insc in inscricoes:
            equipe = EquipeDAO.buscar_por_id(insc.equipe_id)
            self.tree.insert("", tk.END, values=(insc.id, equipe.nome if equipe else "", insc.data_inscricao))
