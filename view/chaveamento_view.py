import tkinter as tk
from tkinter import ttk, messagebox
from dao.torneio_dao import TorneiDAO
from dao.equipe_dao import EquipeDAO
from dao.partida_dao import PartidaDAO
from dao.inscricao_dao import InscricaoDAO
from controller.chaveamento_service import ChaveamentoService

class ChaveamentoView:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Chaveamento de Torneios")
        self.window.geometry("1000x600")
        
        frame_top = tk.Frame(self.window)
        frame_top.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(frame_top, text="Torneio:").pack(side=tk.LEFT, padx=5)
        self.combo_torneio = ttk.Combobox(frame_top, width=40, state="readonly")
        self.combo_torneio.pack(side=tk.LEFT, padx=5)
        self.combo_torneio.bind("<<ComboboxSelected>>", self.carregar_partidas)
        self.carregar_torneios()
        
        tk.Button(frame_top, text="Gerar Chaveamento", command=self.gerar_chaveamento, width=18).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_top, text="Atualizar", command=self.carregar_partidas, width=12).pack(side=tk.LEFT, padx=5)
        
        frame_tree = tk.Frame(self.window)
        frame_tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(frame_tree, columns=("ID", "Fase", "Equipe 1", "Equipe 2", "Vencedor"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Fase", text="Fase")
        self.tree.heading("Equipe 1", text="Equipe 1")
        self.tree.heading("Equipe 2", text="Equipe 2")
        self.tree.heading("Vencedor", text="Vencedor")
        
        self.tree.column("ID", width=50)
        self.tree.column("Fase", width=120)
        self.tree.column("Equipe 1", width=250)
        self.tree.column("Equipe 2", width=250)
        self.tree.column("Vencedor", width=250)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        frame_vencedor = tk.Frame(self.window)
        frame_vencedor.pack(pady=10)
        
        tk.Label(frame_vencedor, text="Registrar Vencedor:").pack(side=tk.LEFT, padx=5)
        self.combo_vencedor = ttk.Combobox(frame_vencedor, width=30, state="readonly")
        self.combo_vencedor.pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_vencedor, text="Salvar Vencedor", command=self.salvar_vencedor, width=15).pack(side=tk.LEFT, padx=5)
        
        self.tree.bind("<<TreeviewSelect>>", self.selecionar_partida)
        
        self.torneios_dict = {}
        self.partida_selecionada = None

    def carregar_torneios(self):
        torneios = TorneiDAO.listar_todos()
        self.torneios_dict = {f"{t.nome} ({t.get_tipo()})": t for t in torneios}
        self.combo_torneio['values'] = list(self.torneios_dict.keys())

    def gerar_chaveamento(self):
        if not self.combo_torneio.get():
            messagebox.showwarning("Aviso", "Selecione um torneio")
            return
        
        torneio = self.torneios_dict[self.combo_torneio.get()]
        
        if torneio.get_tipo() != "ELIMINACAO":
            messagebox.showinfo("Info", "Chaveamento automático disponível apenas para torneios por ELIMINACAO")
            return
        
        equipes_ids = InscricaoDAO.listar_equipes_inscritas(torneio.id)
        
        if len(equipes_ids) < 2:
            messagebox.showerror("Erro", "É necessário pelo menos 2 equipes inscritas")
            return
        
        try:
            ChaveamentoService.gerar_chaveamento_eliminacao(torneio.id, equipes_ids)
            messagebox.showinfo("Sucesso", "Chaveamento gerado com sucesso!")
            self.carregar_partidas()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar chaveamento: {str(e)}")

    def carregar_partidas(self, event=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not self.combo_torneio.get():
            return
        
        torneio = self.torneios_dict[self.combo_torneio.get()]
        partidas = PartidaDAO.listar_por_torneio(torneio.id)
        
        for p in partidas:
            eq1 = EquipeDAO.buscar_por_id(p.equipe1_id)
            eq2 = EquipeDAO.buscar_por_id(p.equipe2_id)
            venc = EquipeDAO.buscar_por_id(p.vencedor_id) if p.vencedor_id else None
            
            self.tree.insert("", tk.END, values=(
                p.id, 
                p.fase, 
                eq1.nome if eq1 else "", 
                eq2.nome if eq2 else "", 
                venc.nome if venc else "Pendente"
            ))

    def selecionar_partida(self, event):
        if not self.tree.selection():
            return
        
        item = self.tree.selection()[0]
        valores = self.tree.item(item, "values")
        partida_id = int(valores[0])
        
        partidas = PartidaDAO.listar_por_torneio(self.torneios_dict[self.combo_torneio.get()].id)
        self.partida_selecionada = next((p for p in partidas if p.id == partida_id), None)
        
        if self.partida_selecionada:
            eq1 = EquipeDAO.buscar_por_id(self.partida_selecionada.equipe1_id)
            eq2 = EquipeDAO.buscar_por_id(self.partida_selecionada.equipe2_id)
            self.combo_vencedor['values'] = [eq1.nome, eq2.nome]

    def salvar_vencedor(self):
        if not self.partida_selecionada:
            messagebox.showwarning("Aviso", "Selecione uma partida")
            return
        
        if not self.combo_vencedor.get():
            messagebox.showwarning("Aviso", "Selecione o vencedor")
            return
        
        eq1 = EquipeDAO.buscar_por_id(self.partida_selecionada.equipe1_id)
        eq2 = EquipeDAO.buscar_por_id(self.partida_selecionada.equipe2_id)
        
        vencedor_nome = self.combo_vencedor.get()
        vencedor_id = eq1.id if eq1.nome == vencedor_nome else eq2.id
        
        self.partida_selecionada.vencedor_id = vencedor_id
        PartidaDAO.atualizar(self.partida_selecionada)
        
        messagebox.showinfo("Sucesso", "Vencedor registrado!")
        self.combo_vencedor.set("")
        self.carregar_partidas()
