from datetime import date

class Equipe:
    def __init__(self, id=None, nome="", data_criacao=None, jogo_id=None):
        self._id = id
        self._nome = nome
        self._data_criacao = data_criacao if data_criacao else date.today()
        self._jogo_id = jogo_id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, value):
        self._nome = value

    @property
    def data_criacao(self):
        return self._data_criacao

    @data_criacao.setter
    def data_criacao(self, value):
        self._data_criacao = value

    @property
    def jogo_id(self):
        return self._jogo_id

    @jogo_id.setter
    def jogo_id(self, value):
        self._jogo_id = value

    def __str__(self):
        return self.nome
