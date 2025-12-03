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
        writer = None
        reader = None
        try:
            # Ouvrir explicitement l'écrivain et exécuter la commande gauche en écrivant dedans.
            writer = os.fdopen(write_fd, "w")
            self.left_command.execute(stdout=writer)
            # fermer l'écrivain pour signaler EOF au lecteur
            #reset les sysout et sysin
            sys.stdout = sys.__stdout__
            sys.stdin = sys.__stdin__

            # Ouvrir le lecteur et exécuter la commande droite en lisant depuis ce lecteur.
            reader = os.fdopen(read_fd, "r") 
            self.right_command.execute(stdin=reader)
            writer.close()
            writer = None
            reader.close()
            reader = None
            #reset les sysout et sysin
            sys.stdout = sys.__stdout__
            sys.stdin = sys.__stdin__

        finally:
            # Ne pas masquer les erreurs : fermer proprement tout flux restant.
            if writer is not None:
                try:
                    writer.close()
                except Exception:
                    pass
            if reader is not None:
                try:
                    reader.close()
                except Exception:
                    pass
            # Tenter de fermer les FDs bruts si encore ouverts (ignorent les erreurs).
            for fd in (read_fd, write_fd):
                try:
                    os.close(fd)
                except OSError:
                    pass
        return None

