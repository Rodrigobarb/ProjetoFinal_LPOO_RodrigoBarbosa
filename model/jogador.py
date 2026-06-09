import re

class Jogador:
    def __init__(self, id=None, nome="", cpf="", nickname="", equipe_id=None):
        self._id = id
        self._nome = nome
        self._cpf = cpf
        self._nickname = nickname
        self._equipe_id = equipe_id

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
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, value):
        self._cpf = value

    @property
    def nickname(self):
        return self._nickname

    @nickname.setter
    def nickname(self, value):
        self._nickname = value

    @property
    def equipe_id(self):
        return self._equipe_id

    @equipe_id.setter
    def equipe_id(self, value):
        self._equipe_id = value

    @staticmethod
    def validar_cpf(cpf):
        """Valida CPF com formato e dígitos verificadores"""
        cpf = re.sub(r'\D', '', cpf)
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False
        
        # Validação do primeiro dígito
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digito1 = (soma * 10 % 11) % 10
        if int(cpf[9]) != digito1:
            return False
        
        # Validação do segundo dígito
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digito2 = (soma * 10 % 11) % 10
        return int(cpf[10]) == digito2

    def __str__(self):
        return f"{self.nickname} ({self.nome})"
