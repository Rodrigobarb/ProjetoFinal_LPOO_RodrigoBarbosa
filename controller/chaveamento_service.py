import math
from model.partida import Partida
from dao.partida_dao import PartidaDAO

class ChaveamentoService:
    """
    Serviço para geração de chaveamento de torneios por eliminação simples.
    """
    
    @staticmethod
    def gerar_chaveamento_eliminacao(torneio_id, equipes_ids):
        """
        Gera chaveamento por eliminação simples.
        
        Args:
            torneio_id: ID do torneio
            equipes_ids: Lista de IDs das equipes inscritas
        
        Returns:
            Lista de partidas criadas
        """
        if len(equipes_ids) < 2:
            raise ValueError("É necessário pelo menos 2 equipes para gerar chaveamento")
        
        # Limpar partidas anteriores
        PartidaDAO.excluir_por_torneio(torneio_id)
        
        # Determinar fase inicial baseado no número de equipes
        num_equipes = len(equipes_ids)
        fase = ChaveamentoService._determinar_fase(num_equipes)
        
        # Criar partidas da primeira fase
        partidas = []
        for i in range(0, len(equipes_ids), 2):
            if i + 1 < len(equipes_ids):
                partida = Partida(
                    torneio_id=torneio_id,
                    fase=fase,
                    equipe1_id=equipes_ids[i],
                    equipe2_id=equipes_ids[i + 1]
                )
                partidas.append(PartidaDAO.inserir(partida))
        
        return partidas
    
    @staticmethod
    def _determinar_fase(num_equipes):
        """Determina a fase inicial baseado no número de equipes"""
        if num_equipes <= 2:
            return "FINAL"
        elif num_equipes <= 4:
            return "SEMIFINAL"
        elif num_equipes <= 8:
            return "QUARTAS"
        elif num_equipes <= 16:
            return "OITAVAS"
        else:
            return f"FASE_{math.ceil(math.log2(num_equipes))}"
