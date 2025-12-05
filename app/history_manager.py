import os
import threading
from typing import List, Optional


class HistoryManager:
    """Gère l'historique des commandes du shell.

    L'historique est conservé en mémoire et persisté dans le fichier
    `./history_file.txt`. Si le fichier n'existe pas il sera créé.
    """
    # Variable de classe : prendre `HISTFILE` si défini, sinon fallback local
    _env_hist = os.environ.get("HISTFILE")
    history_file = os.path.abspath(_env_hist) if _env_hist else os.path.abspath("./history_file.txt")

    @staticmethod
    def getInstance():
        """Retourne l'instance singleton de HistoryManager."""
        if not hasattr(HistoryManager, "_instance"):
            HistoryManager._instance = HistoryManager()
        return HistoryManager._instance

    def __init__(self):
        self.history: List[str] = []
        # index (nombre d'entrées) déjà écrites par les appels à appendHistoryToFile
        self._last_appended_index = 0
        # Charger l'historique depuis le fichier par défaut (si présent)
        try:
            hist_file = getattr(self, 'history_file', None) or HistoryManager.history_file
            if hist_file and os.path.exists(hist_file):
                with open(hist_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.rstrip('\n')
                        if line:
                            self.history.append(line)
                # Considérer que ces lignes existent déjà dans le fichier
                self._last_appended_index = len(self.history)
        except Exception:
            # Ne pas échouer si lecture impossible
            pass

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
        hist = []
        for i in range(max(0, len(self.history) - max_entries), len(self.history)):
            hist.append((i + 1, self.history[i]))
        return hist
    
    def logCommand(self, command: str):
        """Ajoute une commande à l'historique et la persiste dans le fichier."""
        self.history.append(command)

    def appendHistoryFromFile(self, file_path: str):
        """Ajoute l'historique depuis un fichier existant."""
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                for line in f:
                    self.history.append(line.rstrip('\n'))
            # Considérer que le fichier contient déjà ces entrées
            self._last_appended_index = len(self.history)

    def saveHistoryToFile(self, file_path: Optional[str] = None):
        """Sauvegarde l'historique dans un fichier.

        Args:
            file_path (Optional[str]): Chemin du fichier. Si None, utilise
                `self.history_file`.
        """
        if file_path is None:
            file_path = self.history_file
        parent = os.path.dirname(os.path.abspath(file_path))
        if parent and not os.path.exists(parent):
            os.makedirs(parent, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            for command in self.history:
                f.write(command.rstrip('\n') + '\n')
        # après écriture complète, marquer tout comme déjà appendé
        self._last_appended_index = len(self.history)

    def appendHistoryToFile(self, file_path: Optional[str] = None):
        """Ajoute l'historique courant à un fichier existant.

        Args:
            file_path (Optional[str]): Chemin du fichier. Si None, utilise
                `self.history_file`.
        """
        if file_path is None:
            file_path = self.history_file
        abs_path = os.path.abspath(file_path)
        parent = os.path.dirname(abs_path)
        if parent and not os.path.exists(parent):
            os.makedirs(parent, exist_ok=True)
        # n'écrire que les entrées qui n'ont pas encore été appendées
        to_write = self.history[self._last_appended_index:]
        if not to_write:
            return
        with open(abs_path, 'a', encoding='utf-8') as f:
            for command in to_write:
                f.write(command.rstrip('\n') + '\n')
        self._last_appended_index = len(self.history)

