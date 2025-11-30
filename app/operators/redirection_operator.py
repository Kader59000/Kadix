import sys
from .operator import Operator

class RedirectionOperator(Operator):
    """
    Classe pour gérer la redirection shell (>, 1>, 2>). Hérite de Operator.
    Le constructeur prend en paramètre la commande et le fichier cible.
    """
    def __init__(self, token, command, target_file):
        super().__init__(token, symbol_pattern=r">|1>|2>")
        self.command = command
        self.file_descriptor = token[:-1] if token != ">" else "1"
        self.target_file = target_file

    def execute(self):
        """Exécute la commande en redirigeant la sortie standard vers le fichier cible."""
        with open(self.target_file, "w") as f:
            if self.file_descriptor == "1":
                sys.stdout = f
            elif self.file_descriptor == "2":
                sys.stderr = f
            self.command.execute()
        # Restaure les flux standard
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

class AppendOperator(Operator):
    """
    Classe pour gérer la redirection en mode append (>>, 1>>). Hérite de Operator.
    Le constructeur prend en paramètre la commande et le fichier cible.
    """
    def __init__(self, token, command, target_file):
        super().__init__(token, symbol_pattern=r">>|1>>")
        self.command = command
        self.file_descriptor = token[:-2] if token != ">>" else "1"
        self.target_file = target_file

    def execute(self):
        """Exécute la commande en redirigeant la sortie standard vers le fichier cible en mode append."""
        with open(self.target_file, "a") as f:
            if self.file_descriptor == "1":
                sys.stdout = f
            elif self.file_descriptor == "2":
                sys.stderr = f
            self.command.execute()
        # Restaure les flux standard
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__