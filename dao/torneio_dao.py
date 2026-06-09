from dao.db_config import DatabaseConfig
from model.torneio_factory import TorneiFactory
from model.status_torneio import StatusTorneio

class TorneiDAO:
    @staticmethod
    def inserir(torneio):
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "INSERT INTO tb_torneios (tor_nome, tor_data_inicio, tor_status, tor_tipo, tor_jogo_id) VALUES (%s, %s, %s, %s, %s) RETURNING tor_id"
        cursor.execute(sql, (torneio.nome, torneio.data_inicio, torneio.status.value, torneio.get_tipo(), torneio.jogo_id))
        torneio.id = cursor.fetchone()[0]
        conexao.commit()
        cursor.close()
        conexao.close()
        return torneio

    @staticmethod
    def atualizar(torneio):
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "UPDATE tb_torneios SET tor_nome=%s, tor_data_inicio=%s, tor_status=%s, tor_tipo=%s, tor_jogo_id=%s WHERE tor_id=%s"
        cursor.execute(sql, (torneio.nome, torneio.data_inicio, torneio.status.value, torneio.get_tipo(), torneio.jogo_id, torneio.id))
        conexao.commit()
        cursor.close()
        conexao.close()

    @staticmethod
    def excluir(id):
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "DELETE FROM tb_torneios WHERE tor_id=%s"
        cursor.execute(sql, (id,))
        conexao.commit()
        cursor.close()
        conexao.close()

    @staticmethod
    def buscar_por_id(id):
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "SELECT * FROM tb_torneios WHERE tor_id=%s"
        cursor.execute(sql, (id,))
        registro = cursor.fetchone()
        cursor.close()
        conexao.close()
        if registro:
            return TorneiFactory.criar_torneio(registro[4], registro[1], registro[2], registro[5], StatusTorneio[registro[3]], registro[0])
        return None

    @staticmethod
    def listar_todos():
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "SELECT * FROM tb_torneios ORDER BY tor_data_inicio DESC"
        cursor.execute(sql)
        registros = cursor.fetchall()
        cursor.close()
        conexao.close()
        return [TorneiFactory.criar_torneio(r[4], r[1], r[2], r[5], StatusTorneio[r[3]], r[0]) for r in registros]

    @staticmethod
    def filtrar_por_status(status):
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "SELECT * FROM tb_torneios WHERE tor_status=%s ORDER BY tor_data_inicio DESC"
        cursor.execute(sql, (status.value,))
        registros = cursor.fetchall()
        cursor.close()
        conexao.close()
        return [TorneiFactory.criar_torneio(r[4], r[1], r[2], r[5], StatusTorneio[r[3]], r[0]) for r in registros]
