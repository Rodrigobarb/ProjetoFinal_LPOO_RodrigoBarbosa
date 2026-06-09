from abc import ABC, abstractmethod
from datetime import date
from model.status_torneio import StatusTorneio

class Torneio(ABC):
    def __init__(self, id=None, nome="", data_inicio=None, status=StatusTorneio.ABERTO, jogo_id=None):
        self._id = id
        self._nome = nome
        self._data_inicio = data_inicio if data_inicio else date.today()
        self._status = status if isinstance(status, StatusTorneio) else StatusTorneio[status]
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
    def data_inicio(self):
        return self._data_inicio

    @data_inicio.setter
    def data_inicio(self, value):
        self._data_inicio = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value if isinstance(value, StatusTorneio) else StatusTorneio[value]

    @property
    def jogo_id(self):
        return self._jogo_id

    @jogo_id.setter
    def jogo_id(self, value):
        self._jogo_id = value

    @abstractmethod
    def get_tipo(self):
        """Retorna o tipo do torneio"""
        pass

    def __str__(self):
        return f"{self.nome} ({self.get_tipo()})"


class TorneioPorEliminacao(Torneio):
    def get_tipo(self):
        return "ELIMINACAO"


class TorneioPorPontos(Torneio):
    def get_tipo(self):
        return "PONTOS"
