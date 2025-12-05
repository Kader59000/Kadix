import os
import threading
from typing import List, Optional


class HistoryManager:
    """Gère l'historique des commandes du shell.

    L'historique est conservé en mémoire et persisté dans le fichier
    `./history_file.txt`. Si le fichier n'existe pas il sera créé.
    """
    history_file = os.path.abspath("./history_file.txt")  # Variable de classe

    @staticmethod
    def getInstance():
        """Retourne l'instance singleton de HistoryManager."""
        if not hasattr(HistoryManager, "_instance"):
            HistoryManager._instance = HistoryManager()
        return HistoryManager._instance

    def __init__(self):
        self.history: List[str] = []

    def getHistory(self, max_entries = None):
        """Retourne l'historique des commandes.

        Args:
            max_entries (Optional[int]): Nombre maximum d'entrées à retourner.
                Si None, retourne tout l'historique.

        Returns:
            List[Tuple[int, str]]: Liste des tuples (index, commande).
        """
        if max_entries is None:
            max_entries = len(self.history)
        for i in range(max(0, len(self.history) - max_entries), len(self.history)):
            yield (i + 1, self.history[i])
    
    def logCommand(self, command: str):
        """Ajoute une commande à l'historique et la persiste dans le fichier."""
        self.history.append(command)

    def appendHistoryFromFile(self, file_path: str):
        """Ajoute l'historique depuis un fichier existant."""
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                for line in f:
                    self.history.append(line.rstrip('\n'))

