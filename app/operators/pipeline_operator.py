import os
import sys
from app.operators.operator import Operator


class PipelineOperator(Operator):
    """Représente un opérateur de pipeline (`|`)."""

    def __init__(self, token, left_command, right_command):
        super().__init__(token, symbol_pattern=r"\|")
        self.left_command = left_command
        self.right_command = right_command

    def execute(self):
        """Lance les deux commandes en chaînant la sortie gauche dans l'entrée droite."""
        read_fd, write_fd = os.pipe()
        # Ouvrir explicitement l'écrivain et exécuter la commande gauche en écrivant dedans.
        writer = os.fdopen(write_fd, "w")
        reader = os.fdopen(read_fd, "r")
        self.left_command.execute(stdout=writer)
        # s'assurer que les buffers sont vidés
        writer.flush()
        writer.close()
        # Ouvrir le lecteur et exécuter la commande droite en lisant depuis ce lecteur.

        self.right_command.execute(stdin=reader)
        reader.close()
        return None

