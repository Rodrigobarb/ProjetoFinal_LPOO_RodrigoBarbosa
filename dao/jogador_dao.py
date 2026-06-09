from dao.db_config import DatabaseConfig
from model.jogador import Jogador

class JogadorDAO:
    @staticmethod
    def inserir(jogador):
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "INSERT INTO tb_jogadores (jgd_nome, jgd_cpf, jgd_nickname, jgd_equipe_id) VALUES (%s, %s, %s, %s) RETURNING jgd_id"
        cursor.execute(sql, (jogador.nome, jogador.cpf, jogador.nickname, jogador.equipe_id))
        jogador.id = cursor.fetchone()[0]
        conexao.commit()
        cursor.close()
        conexao.close()
        return jogador

    @staticmethod
    def atualizar(jogador):
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "UPDATE tb_jogadores SET jgd_nome=%s, jgd_cpf=%s, jgd_nickname=%s, jgd_equipe_id=%s WHERE jgd_id=%s"
        cursor.execute(sql, (jogador.nome, jogador.cpf, jogador.nickname, jogador.equipe_id, jogador.id))
        conexao.commit()
        cursor.close()
        conexao.close()

    @staticmethod
    def excluir(id):
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "DELETE FROM tb_jogadores WHERE jgd_id=%s"
        cursor.execute(sql, (id,))
        conexao.commit()
        cursor.close()
        conexao.close()

    @staticmethod
    def buscar_por_id(id):
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "SELECT * FROM tb_jogadores WHERE jgd_id=%s"
        cursor.execute(sql, (id,))
        registro = cursor.fetchone()
        cursor.close()
        conexao.close()
        if registro:
            return Jogador(registro[0], registro[1], registro[2], registro[3], registro[4])
        return None

    @staticmethod
    def listar_todos():
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "SELECT * FROM tb_jogadores ORDER BY jgd_nome"
        cursor.execute(sql)
        registros = cursor.fetchall()
        cursor.close()
        conexao.close()
        return [Jogador(r[0], r[1], r[2], r[3], r[4]) for r in registros]

    @staticmethod
    def filtrar_por_equipe(equipe_id):
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "SELECT * FROM tb_jogadores WHERE jgd_equipe_id=%s ORDER BY jgd_nome"
        cursor.execute(sql, (equipe_id,))
        registros = cursor.fetchall()
        cursor.close()
        conexao.close()
        return [Jogador(r[0], r[1], r[2], r[3], r[4]) for r in registros]
