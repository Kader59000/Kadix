import re
from abc import ABC, abstractmethod

class Operator(ABC):
    """
    Classe abstraite pour les opérateurs du shell.
    """
    def __init__(self, token, symbol_pattern):
        self.symbol_pattern = symbol_pattern
        self.token = token
        if not self.match(token):
            raise ValueError(f"Le token '{token}' ne correspond pas au pattern '{symbol_pattern}'")

    def match(self, token):
        """Retourne True si le token correspond au pattern regex de l'opérateur."""
        return re.match(self.symbol_pattern, token) is not None

    @abstractmethod
    def execute(self):
        """Méthode abstraite à implémenter dans les sous-classes."""
        pass