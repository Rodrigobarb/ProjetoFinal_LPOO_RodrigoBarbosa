class Jogo:
    def __init__(self, id=None, nome="", genero="", plataforma="", max_jogadores_equipe=5):
        self._id = id
        self._nome = nome
        self._genero = genero
        self._plataforma = plataforma
        self._max_jogadores_equipe = max_jogadores_equipe

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
    def genero(self):
        return self._genero

    @genero.setter
    def genero(self, value):
        self._genero = value

    @property
    def plataforma(self):
        return self._plataforma

    @plataforma.setter
    def plataforma(self, value):
        self._plataforma = value

    @property
    def max_jogadores_equipe(self):
        return self._max_jogadores_equipe

    @max_jogadores_equipe.setter
    def max_jogadores_equipe(self, value):
        self._max_jogadores_equipe = value

    def __str__(self):
        return f"{self.nome} ({self.genero} - {self.plataforma})"
