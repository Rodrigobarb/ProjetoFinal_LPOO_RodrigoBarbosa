from dao.db_config import DatabaseConfig
from model.equipe import Equipe

class EquipeDAO:
    @staticmethod
    def inserir(equipe):
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "INSERT INTO tb_equipes (equ_nome, equ_data_criacao, equ_jogo_id) VALUES (%s, %s, %s) RETURNING equ_id"
        cursor.execute(sql, (equipe.nome, equipe.data_criacao, equipe.jogo_id))
        equipe.id = cursor.fetchone()[0]
        conexao.commit()
        cursor.close()
        conexao.close()
        return equipe

    @staticmethod
    def atualizar(equipe):
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "UPDATE tb_equipes SET equ_nome=%s, equ_data_criacao=%s, equ_jogo_id=%s WHERE equ_id=%s"
        cursor.execute(sql, (equipe.nome, equipe.data_criacao, equipe.jogo_id, equipe.id))
        conexao.commit()
        cursor.close()
        conexao.close()

    @staticmethod
    def excluir(id):
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "DELETE FROM tb_equipes WHERE equ_id=%s"
        cursor.execute(sql, (id,))
        conexao.commit()
        cursor.close()
        conexao.close()

    @staticmethod
    def buscar_por_id(id):
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "SELECT * FROM tb_equipes WHERE equ_id=%s"
        cursor.execute(sql, (id,))
        registro = cursor.fetchone()
        cursor.close()
        conexao.close()
        if registro:
            return Equipe(registro[0], registro[1], registro[2], registro[3])
        return None

    @staticmethod
    def listar_todos():
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "SELECT * FROM tb_equipes ORDER BY equ_nome"
        cursor.execute(sql)
        registros = cursor.fetchall()
        cursor.close()
        conexao.close()
        return [Equipe(r[0], r[1], r[2], r[3]) for r in registros]

    @staticmethod
    def filtrar_por_jogo(jogo_id):
        conexao = DatabaseConfig.get_connection()
        cursor = conexao.cursor()
        sql = "SELECT * FROM tb_equipes WHERE equ_jogo_id=%s ORDER BY equ_nome"
        cursor.execute(sql, (jogo_id,))
        registros = cursor.fetchall()
        cursor.close()
        conexao.close()
        return [Equipe(r[0], r[1], r[2], r[3]) for r in registros]
