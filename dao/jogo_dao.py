from dao.db_config import DatabaseConfig
from model.jogo import Jogo

class JogoDAO:
    @staticmethod
    def inserir(jogo):
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "INSERT INTO tb_jogos (jog_nome, jog_genero, jog_plataforma, jog_max_jogadores_equipe) VALUES (%s, %s, %s, %s) RETURNING jog_id"
        cursor.execute(sql, (jogo.nome, jogo.genero, jogo.plataforma, jogo.max_jogadores_equipe))
        jogo.id = cursor.fetchone()[0]
        conexao.commit()
        cursor.close()
        conexao.close()
        return jogo

    @staticmethod
    def atualizar(jogo):
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "UPDATE tb_jogos SET jog_nome=%s, jog_genero=%s, jog_plataforma=%s, jog_max_jogadores_equipe=%s WHERE jog_id=%s"
        cursor.execute(sql, (jogo.nome, jogo.genero, jogo.plataforma, jogo.max_jogadores_equipe, jogo.id))
        conexao.commit()
        cursor.close()
        conexao.close()

    @staticmethod
    def excluir(id):
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "DELETE FROM tb_jogos WHERE jog_id=%s"
        cursor.execute(sql, (id,))
        conexao.commit()
        cursor.close()
        conexao.close()

    @staticmethod
    def buscar_por_id(id):
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "SELECT * FROM tb_jogos WHERE jog_id=%s"
        cursor.execute(sql, (id,))
        registro = cursor.fetchone()
        cursor.close()
        conexao.close()
        if registro:
            return Jogo(registro[0], registro[1], registro[2], registro[3], registro[4])
        return None

    @staticmethod
    def listar_todos():
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "SELECT * FROM tb_jogos ORDER BY jog_nome"
        cursor.execute(sql)
        registros = cursor.fetchall()
        cursor.close()
        conexao.close()
        return [Jogo(r[0], r[1], r[2], r[3], r[4]) for r in registros]

    @staticmethod
    def filtrar(genero=None, plataforma=None):
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "SELECT * FROM tb_jogos WHERE 1=1"
        params = []
        if genero:
            sql += " AND jog_genero ILIKE %s"
            params.append(f"%{genero}%")
        if plataforma:
            sql += " AND jog_plataforma ILIKE %s"
            params.append(f"%{plataforma}%")
        sql += " ORDER BY jog_nome"
        cursor.execute(sql, params)
        registros = cursor.fetchall()
        cursor.close()
        conexao.close()
        return [Jogo(r[0], r[1], r[2], r[3], r[4]) for r in registros]
