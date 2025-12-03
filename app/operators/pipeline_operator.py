import os
import sys
import subprocess
import io
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
        # Ouvrir explicitement l'écrivain et exécuter la commande gauche en écrivant dedans.
        writer = os.fdopen(write_fd, "w")
        try:
            self.left_command.execute(stdout=writer)
        finally:
            # fermer le writer pour signaler EOF au lecteur
            try:
                writer.close()
            except Exception:
                pass

        # Lire tout le contenu écrit dans le pipe pour vérifier puis transmettre
        reader = os.fdopen(read_fd, "r")
        try:
            data = reader.read()
        finally:
            # on ferme le reader localement — on transmettra les données explicitement
            try:
                reader.close()
            except Exception:
                pass

        # Vérification : la commande gauche a-t-elle écrit quelque chose ?
        if not data:
            print("[pipeline] Aucune donnée écrite dans le pipe par la commande de gauche.")

        # Transmettre les données à la commande de droite
        if hasattr(self.right_command, 'spawn') and callable(getattr(self.right_command, 'spawn')):
            # commande externe — spawn un process et envoyer les données via stdin
            proc = self.right_command.spawn(stdin=subprocess.PIPE)
            if proc.stdin is not None:
                # proc.stdin est en mode binaire ; encoder la chaîne
                try:
                    proc.stdin.write(data.encode())
                except Exception:
                    # si l'écriture échoue, laisser l'exception remonter
                    proc.stdin.close()
                    proc.wait()
                    raise
                proc.stdin.close()
            proc.wait()
        else:
            # builtin : lui fournir un StringIO en stdin
            strio = io.StringIO(data)
            try:
                self.right_command.execute(stdin=strio)
            finally:
                try:
                    strio.close()
                except Exception:
                    pass
        return None

