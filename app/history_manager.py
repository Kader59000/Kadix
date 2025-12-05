import os
import threading
from typing import List, Optional


class HistoryManager:
    """Gère l'historique des commandes du shell.

    L'historique est conservé en mémoire et persisté dans le fichier
    `./history_file.txt`. Si le fichier n'existe pas il sera créé.
    """

    @staticmethod
    def getInstance(history_file=None):
        """Retourne l'instance singleton de HistoryManager pour le fichier par défaut,
        ou une nouvelle instance pour un fichier spécifique."""
        if history_file is not None:
            return HistoryManager(history_file)
        if not hasattr(HistoryManager, "_instance"):
            HistoryManager._instance = HistoryManager()
        return HistoryManager._instance

    def __init__(self, history_file=None):
        self._lock = threading.Lock()
        self._history: List[tuple[int, str]] = []
        self._next_index = 1
        # fichier d'historique
        if history_file is None:
            self.history_file = os.path.abspath("./history_file.txt")
        else:
            self.history_file = os.path.abspath(history_file)

        # s'assurer que le fichier existe (création si besoin)
        try:
            open(self.history_file, "a", encoding="utf-8").close()
        except Exception:
            # si création impossible, on continue quand même avec l'historique en mémoire
            self.history_file = None

        # Charger l'historique existant si le fichier est présent
        if self.history_file:
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.rstrip("\n")
                        if line:
                            self._history.append((self._next_index, line))
                            self._next_index += 1
            except FileNotFoundError:
                # fichier non existant -> démarrer vide (déjà essayé de créer)
                pass

    def logCommand(self, command: str) -> None:
        """Ajoute `command` à l'historique et l'écrit dans le fichier (si configuré).

        Le paramètre `command` est stocké tel quel (chaîne).
        """
        if command is None:
            return
        cmd = str(command)
        with self._lock:
            self._history.append((self._next_index, cmd))
            self._next_index += 1

            if self.history_file:
                # ouvrir en append et écrire la ligne
                try:
                    with open(self.history_file, "a", encoding="utf-8") as f:
                        f.write(cmd.rstrip("\n") + "\n")
                except Exception:
                    # N'échoue pas si on ne peut pas écrire l'historique
                    pass

    def setHistoryFile(self, history_file):
        """Change le fichier d'historique et recharge l'historique."""
        self.history_file = os.path.abspath(history_file)
        # Recharger l'historique
        self._history = []
        self._next_index = 1
        if self.history_file:
            try:
                open(self.history_file, "a", encoding="utf-8").close()
            except Exception:
                self.history_file = None
            if self.history_file:
                try:
                    with open(self.history_file, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.rstrip("\n")
                            if line:
                                self._history.append((self._next_index, line))
                                self._next_index += 1
                except FileNotFoundError:
                    pass
