import tkinter as tk
from tkinter import ttk
from view.jogo_view import JogoView
from view.equipe_view import EquipeView
from view.jogador_view import JogadorView
from view.torneio_view import TorneiView
from view.inscricao_view import InscricaoView
from view.chaveamento_view import ChaveamentoView
from view.sobre_view import SobreView

ROXO_BG   = "#EEEDFE"
ROXO_FG   = "#534AB7"
TEAL_BG   = "#E1F5EE"
TEAL_FG   = "#0F6E56"
AZUL_BG   = "#E6F1FB"
AZUL_FG   = "#185FA5"
AMBAR_BG  = "#FAEEDA"
AMBAR_FG  = "#854F0B"
CORAL_BG  = "#FAECE7"
CORAL_FG  = "#993C1D"
VERDE_BG  = "#EAF3DE"
VERDE_FG  = "#3B6D11"

BG        = "#FFFFFF"
BG_SEC    = "#F5F5F3"
TEXT      = "#1A1A1A"
TEXT_SEC  = "#6B6B68"
BORDER    = "#E0E0DB"
FONT      = "Segoe UI"


class _CardButton(tk.Frame):
    """Botão no estilo card com ícone colorido, título e descrição."""

    def __init__(self, parent, icon: str, icon_bg: str, icon_fg: str,
                 label: str, desc: str, command=None):
        super().__init__(parent, bg=BG, cursor="hand2",
                         highlightthickness=1, highlightbackground=BORDER)
        self.command = command
        self._normal_bg = BG
        self._hover_bg  = BG_SEC

        # Ícone
        icon_frame = tk.Frame(self, bg=icon_bg, width=36, height=36)
        icon_frame.pack_propagate(False)
        icon_frame.pack(anchor="w", padx=14, pady=(14, 6))
        tk.Label(icon_frame, text=icon, bg=icon_bg, fg=icon_fg,
                 font=(FONT, 16)).place(relx=0.5, rely=0.5, anchor="center")

        # Texto
        tk.Label(self, text=label, bg=BG, fg=TEXT,
                 font=(FONT, 11, "bold"), anchor="w").pack(fill="x", padx=14)
        tk.Label(self, text=desc, bg=BG, fg=TEXT_SEC,
                 font=(FONT, 9), anchor="w", wraplength=155,
                 justify="left").pack(fill="x", padx=14, pady=(2, 14))

        # Eventos
        for w in self.winfo_children():
            w.bind("<Button-1>", self._on_click)
            w.bind("<Enter>",    self._on_enter)
            w.bind("<Leave>",    self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>",    self._on_enter)
        self.bind("<Leave>",    self._on_leave)

    def _on_click(self, _=None):
        if self.command:
            self.command()

    def _on_enter(self, _=None):
        self._set_bg(self._hover_bg)

    def _on_leave(self, _=None):
        self._set_bg(self._normal_bg)

    def _set_bg(self, color: str):
        self.configure(bg=color)
        for w in self.winfo_children():
            try:
                w.configure(bg=color)
            except tk.TclError:
                pass


class MainView:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Arena Games — Sistema de Gerenciamento de Torneios")
        self.root.geometry("820x560")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)

        self._criar_header()
        self._criar_separador()
        self._criar_grid()
        self._criar_statusbar()

    # ------------------------------------------------------------------ #
    #  Seções da tela                                                      #
    # ------------------------------------------------------------------ #

    def _criar_header(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=20, pady=(18, 10))

        icon_box = tk.Frame(header, bg=BG_SEC, width=40, height=40,
                            highlightthickness=1, highlightbackground=BORDER)
        icon_box.pack_propagate(False)
        icon_box.pack(side="left")
        tk.Label(icon_box, text="🏆", bg=BG_SEC,
                 font=(FONT, 18)).place(relx=0.5, rely=0.5, anchor="center")

        text_frame = tk.Frame(header, bg=BG)
        text_frame.pack(side="left", padx=12)
        tk.Label(text_frame, text="Arena Games", bg=BG, fg=TEXT,
                 font=(FONT, 14, "bold")).pack(anchor="w")
        tk.Label(text_frame, text="Sistema de gerenciamento de torneios",
                 bg=BG, fg=TEXT_SEC, font=(FONT, 10)).pack(anchor="w")

        # Botão Sobre no canto direito
        btn_sobre = tk.Label(header, text="Sobre", bg=BG, fg=TEXT_SEC,
                             font=(FONT, 10), cursor="hand2")
        btn_sobre.pack(side="right", padx=4)
        btn_sobre.bind("<Button-1>", lambda _: self.abrir_sobre())

    def _criar_separador(self):
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x")

    def _criar_grid(self):
        container = tk.Frame(self.root, bg=BG)
        container.pack(fill="both", expand=True, padx=20, pady=16)

        # ---- Seção: Cadastros ----
        self._label_secao(container, "Cadastros")

        linha1 = tk.Frame(container, bg=BG)
        linha1.pack(fill="x", pady=(6, 14))

        cards_cadastro = [
            ("🎮", ROXO_BG, ROXO_FG, "Jogos",
             "Cadastrar e editar jogos disponíveis", self.abrir_jogos),
            ("👥", TEAL_BG, TEAL_FG, "Equipes",
             "Gerenciar times e suas informações", self.abrir_equipes),
            ("👤", AZUL_BG, AZUL_FG, "Jogadores",
             "Cadastro e perfil de jogadores", self.abrir_jogadores),
        ]
        self._adicionar_cards(linha1, cards_cadastro)

        # ---- Seção: Torneios ----
        self._label_secao(container, "Torneios")

        linha2 = tk.Frame(container, bg=BG)
        linha2.pack(fill="x", pady=(6, 14))

        cards_torneio = [
            ("🏆", AMBAR_BG, AMBAR_FG, "Torneios",
             "Criar e gerenciar torneios", self.abrir_torneios),
            ("📋", CORAL_BG, CORAL_FG, "Inscrições",
             "Inscrever equipes em torneios", self.abrir_inscricoes),
            ("⎇",  VERDE_BG, VERDE_FG, "Chaveamento",
             "Visualizar e gerenciar brackets", self.abrir_chaveamento),
        ]
        self._adicionar_cards(linha2, cards_torneio)

    def _label_secao(self, parent, texto: str):
        tk.Label(parent, text=texto.upper(), bg=BG, fg=TEXT_SEC,
                 font=(FONT, 8, "bold")).pack(anchor="w")

    def _adicionar_cards(self, parent, definicoes: list):
        for icon, ibg, ifg, label, desc, cmd in definicoes:
            card = _CardButton(parent, icon=icon, icon_bg=ibg, icon_fg=ifg,
                               label=label, desc=desc, command=cmd)
            card.pack(side="left", fill="both", expand=True,
                      padx=(0, 10), ipady=4)

    def _criar_statusbar(self):
        bar = tk.Frame(self.root, bg=BG_SEC,
                       highlightthickness=1, highlightbackground=BORDER)
        bar.pack(fill="x", side="bottom")

        stats = [
            ("Torneios ativos", "—"),
            ("Equipes cadastradas", "—"),
            ("Jogadores", "—"),
        ]
        for i, (label, valor) in enumerate(stats):
            cell = tk.Frame(bar, bg=BG_SEC)
            cell.pack(side="left", padx=20, pady=10)
            tk.Label(cell, text=label, bg=BG_SEC, fg=TEXT_SEC,
                     font=(FONT, 9)).pack(anchor="w")
            tk.Label(cell, text=valor, bg=BG_SEC, fg=TEXT,
                     font=(FONT, 14, "bold")).pack(anchor="w")
            if i < len(stats) - 1:
                tk.Frame(bar, bg=BORDER, width=1).pack(
                    side="left", fill="y", pady=8)

    # ------------------------------------------------------------------ #
    #  Ações de abertura de views                                          #
    # ------------------------------------------------------------------ #

    def abrir_jogos(self):        JogoView(self.root)
    def abrir_equipes(self):      EquipeView(self.root)
    def abrir_jogadores(self):    JogadorView(self.root)
    def abrir_torneios(self):     TorneiView(self.root)
    def abrir_inscricoes(self):   InscricaoView(self.root)
    def abrir_chaveamento(self):  ChaveamentoView(self.root)
    def abrir_sobre(self):        SobreView(self.root)

    def run(self):
        self.root.mainloop()