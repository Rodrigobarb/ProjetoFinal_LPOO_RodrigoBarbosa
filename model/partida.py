class Partida:
    def __init__(self, id=None, torneio_id=None, fase="", equipe1_id=None, equipe2_id=None, vencedor_id=None):
        self._id = id
        self._torneio_id = torneio_id
        self._fase = fase
        self._equipe1_id = equipe1_id
        self._equipe2_id = equipe2_id
        self._vencedor_id = vencedor_id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def torneio_id(self):
        return self._torneio_id

    @torneio_id.setter
    def torneio_id(self, value):
        self._torneio_id = value

    @property
    def fase(self):
        return self._fase

    @fase.setter
    def fase(self, value):
        self._fase = value

    @property
    def equipe1_id(self):
        return self._equipe1_id

    @equipe1_id.setter
    def equipe1_id(self, value):
        self._equipe1_id = value

    @property
    def equipe2_id(self):
        return self._equipe2_id

    @equipe2_id.setter
    def equipe2_id(self, value):
        self._equipe2_id = value

    @property
    def vencedor_id(self):
        return self._vencedor_id

    @vencedor_id.setter
    def vencedor_id(self, value):
        self._vencedor_id = value

    def __str__(self):
        return f"{self.fase}: Equipe {self.equipe1_id} vs Equipe {self.equipe2_id}"
