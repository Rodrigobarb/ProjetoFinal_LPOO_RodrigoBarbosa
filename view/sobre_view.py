import tkinter as tk
from tkinter import ttk

class SobreView:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Sobre o Sistema")
        self.window.geometry("700x500")
        
        frame = tk.Frame(self.window, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text="Arena Games", font=("Arial", 24, "bold")).pack(pady=10)
        tk.Label(frame, text="Sistema de Gerenciamento de Torneios E-Sports", 
                font=("Arial", 12)).pack(pady=5)
        
        separator = ttk.Separator(frame, orient='horizontal')
        separator.pack(fill='x', pady=15)
        
        info_text = """
        📋 DESCRIÇÃO DO SISTEMA
        
        Sistema completo para gerenciamento de torneios de e-sports, permitindo:
        
        • Cadastro de jogos (MOBA, FPS, Esporte, etc.)
        • Gerenciamento de equipes e jogadores
        • Criação de torneios (Eliminação Simples ou Por Pontos)
        • Inscrição de equipes em torneios
        • Geração automática de chaveamento
        • Registro de resultados de partidas
        
        
        🎯 PADRÕES DE PROJETO UTILIZADOS
        
        • Factory Method: Criação de diferentes tipos de torneio
        • DAO: Abstração de persistência em PostgreSQL
        • MVC: Separação Model, View, Controller
        • Enum: Controle de status de torneios
        
        
        👨‍💻 AUTOR
        
        Desenvolvido para a disciplina LPOO 2026-1
        IFSul - Ciência da Computação
        Professora: Vanessa Lago Machado
        
        
        🛠️ TECNOLOGIAS
        
        Python 3.10+ | PostgreSQL | Tkinter | psycopg2
        """
        
        text_widget = tk.Text(frame, wrap=tk.WORD, font=("Arial", 10), 
                             bg="#f0f0f0", relief=tk.FLAT, padx=10, pady=10)
        text_widget.insert("1.0", info_text)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tk.Button(frame, text="Fechar", command=self.window.destroy, width=15).pack(pady=10)
