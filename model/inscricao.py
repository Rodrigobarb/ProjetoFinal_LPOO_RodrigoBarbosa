from datetime import datetime

class Inscricao:
    def __init__(self, id=None, equipe_id=None, torneio_id=None, data_inscricao=None):
        self._id = id
        self._equipe_id = equipe_id
        self._torneio_id = torneio_id
        self._data_inscricao = data_inscricao if data_inscricao else datetime.now()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def equipe_id(self):
        return self._equipe_id

    @equipe_id.setter
    def equipe_id(self, value):
        self._equipe_id = value

    @property
    def torneio_id(self):
        return self._torneio_id

    @torneio_id.setter
    def torneio_id(self, value):
        self._torneio_id = value

    @property
    def data_inscricao(self):
        return self._data_inscricao

    @data_inscricao.setter
    def data_inscricao(self, value):
        self._data_inscricao = value
