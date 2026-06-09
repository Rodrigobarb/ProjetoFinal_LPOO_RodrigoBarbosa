from dao.db_config import DatabaseConfig
from model.partida import Partida

class PartidaDAO:
    @staticmethod
    def inserir(partida):
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "INSERT INTO tb_partidas (par_torneio_id, par_fase, par_equipe1_id, par_equipe2_id, par_vencedor_id) VALUES (%s, %s, %s, %s, %s) RETURNING par_id"
        cursor.execute(sql, (partida.torneio_id, partida.fase, partida.equipe1_id, partida.equipe2_id, partida.vencedor_id))
        partida.id = cursor.fetchone()[0]
        conexao.commit()
        cursor.close()
        conexao.close()
        return partida

    @staticmethod
    def atualizar(partida):
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "UPDATE tb_partidas SET par_torneio_id=%s, par_fase=%s, par_equipe1_id=%s, par_equipe2_id=%s, par_vencedor_id=%s WHERE par_id=%s"
        cursor.execute(sql, (partida.torneio_id, partida.fase, partida.equipe1_id, partida.equipe2_id, partida.vencedor_id, partida.id))
        conexao.commit()
        cursor.close()
        conexao.close()

    @staticmethod
    def excluir(id):
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "DELETE FROM tb_partidas WHERE par_id=%s"
        cursor.execute(sql, (id,))
        conexao.commit()
        cursor.close()
        conexao.close()

    @staticmethod
    def listar_por_torneio(torneio_id):
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "SELECT * FROM tb_partidas WHERE par_torneio_id=%s ORDER BY par_fase, par_id"
        cursor.execute(sql, (torneio_id,))
        registros = cursor.fetchall()
        cursor.close()
        conexao.close()
        return [Partida(r[0], r[1], r[2], r[3], r[4], r[5]) for r in registros]

    @staticmethod
    def excluir_por_torneio(torneio_id):
        """Remove todas as partidas de um torneio"""
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "DELETE FROM tb_partidas WHERE par_torneio_id=%s"
        cursor.execute(sql, (torneio_id,))
        conexao.commit()
        cursor.close()
        conexao.close()
