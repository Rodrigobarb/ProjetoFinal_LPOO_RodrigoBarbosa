from dao.db_config import DatabaseConfig
from model.inscricao import Inscricao

class InscricaoDAO:
    @staticmethod
    def inserir(inscricao):
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "INSERT INTO tb_inscricoes (ins_equipe_id, ins_torneio_id, ins_data_inscricao) VALUES (%s, %s, %s) RETURNING ins_id"
        cursor.execute(sql, (inscricao.equipe_id, inscricao.torneio_id, inscricao.data_inscricao))
        inscricao.id = cursor.fetchone()[0]
        conexao.commit()
        cursor.close()
        conexao.close()
        return inscricao

    @staticmethod
    def excluir(id):
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "DELETE FROM tb_inscricoes WHERE ins_id=%s"
        cursor.execute(sql, (id,))
        conexao.commit()
        cursor.close()
        conexao.close()

    @staticmethod
    def listar_por_torneio(torneio_id):
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "SELECT * FROM tb_inscricoes WHERE ins_torneio_id=%s ORDER BY ins_data_inscricao"
        cursor.execute(sql, (torneio_id,))
        registros = cursor.fetchall()
        cursor.close()
        conexao.close()
        return [Inscricao(r[0], r[1], r[2], r[3]) for r in registros]

    @staticmethod
    def verificar_inscricao_existente(equipe_id, torneio_id):
        """Verifica se equipe já está inscrita no torneio"""
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "SELECT COUNT(*) FROM tb_inscricoes WHERE ins_equipe_id=%s AND ins_torneio_id=%s"
        cursor.execute(sql, (equipe_id, torneio_id))
        count = cursor.fetchone()[0]
        cursor.close()
        conexao.close()
        return count > 0

    @staticmethod
    def listar_equipes_inscritas(torneio_id):
        """Retorna lista de IDs das equipes inscritas no torneio"""
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "SELECT ins_equipe_id FROM tb_inscricoes WHERE ins_torneio_id=%s"
        cursor.execute(sql, (torneio_id,))
        registros = cursor.fetchall()
        cursor.close()
        conexao.close()
        return [r[0] for r in registros]
