from model.torneio import TorneioPorEliminacao, TorneioPorPontos
from model.status_torneio import StatusTorneio

class TorneiFactory:
    """
    Factory Method para criação de diferentes tipos de Torneio.
    
    Justificativa:
    - Encapsula a lógica de criação de objetos complexos (TorneioPorEliminacao vs TorneioPorPontos)
    - Permite adicionar novos tipos de torneio sem modificar código cliente
    - Centraliza regras de instanciação e validação
    """
    
    @staticmethod
    def criar_torneio(tipo, nome, data_inicio, jogo_id, status=StatusTorneio.ABERTO, id=None):
        """
        Cria instância de Torneio baseado no tipo especificado.
        
        Args:
            tipo (str): 'ELIMINACAO' ou 'PONTOS'
            nome (str): Nome do torneio
            data_inicio (date): Data de início
            jogo_id (int): ID do jogo
            status (StatusTorneio): Status inicial
            id (int): ID do torneio (para recuperação do banco)
        
        Returns:
            Torneio: Instância de TorneioPorEliminacao ou TorneioPorPontos
        """
        if tipo == "ELIMINACAO":
            torneio = TorneioPorEliminacao(id, nome, data_inicio, status, jogo_id)
        elif tipo == "PONTOS":
            torneio = TorneioPorPontos(id, nome, data_inicio, status, jogo_id)
        else:
            raise ValueError(f"Tipo de torneio inválido: {tipo}")
        
        return torneio
