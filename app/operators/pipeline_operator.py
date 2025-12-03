import subprocess
import os
from app.commands.command import InstalledCommand
from app.operators.operator import Operator
class PipelineOperator(Operator):
    """Représente un opérateur de pipeline (`|`)."""

    def __init__(self, token, left_command, right_command):
        super().__init__(token, symbol_pattern=r"\|")
        self.left_command = left_command
        self.right_command = right_command

    def execute(self):
        """Lance les deux commandes en chaînant la sortie gauche dans l'entrée droite."""
        if not isinstance(self.left_command, InstalledCommand) or not isinstance(self.right_command, InstalledCommand):
            raise NotImplementedError("Les pipelines supportent uniquement les commandes installées pour l'instant.")
        left_proc = self.left_command.spawn(stdout=subprocess.PIPE)
        right_proc = self.right_command.spawn(stdin=left_proc.stdout)
        left_proc.stdout.close()
        right_proc.wait()
        left_proc.wait()
        return None

    def execute(self):
        """Lance les deux commandes en chaînant la sortie gauche dans l'entrée droite."""
        r, w = os.pipe()
        self.left_command.execute(stdout=os.fdopen(w))
        os.close(w)
        self.right_command.execute(stdin=os.fdopen(r))
        os.close(r)
        return None

