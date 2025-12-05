import os
import threading
from typing import List, Optional


class HistoryManager:
    """Gère l'historique des commandes du shell.

    L'historique est conservé en mémoire et persisté dans le fichier
    `./history_file.txt`. Si le fichier n'existe pas il sera créé.
    """

    @staticmethod
    def getInstance():
        """Retourne l'instance singleton de HistoryManager."""
        if not hasattr(HistoryManager, "_instance"):
            HistoryManager._instance = HistoryManager()
        return HistoryManager._instance

    def __init__(self, max_entries: Optional[int] = None):
        self._lock = threading.Lock()
        self._history: List[str] = []
        # fichier d'historique fixe (relatif au cwd)
        self.history_file = os.path.abspath("./history_file.txt")
        self.max_entries = max_entries

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
                            self._history.append(line)
            except FileNotFoundError:
                # fichier non existant -> démarrer vide (déjà essayé de créer)
                pass

    def logCommand(self, command: str) -> None:
        """Ajoute `command` à l'historique et l'écrit dans le fichier (si configuré).

        Le paramètre `command` est stocké tel quel (chaîne). Si `max_entries`
        est défini, on tronque l'historique pour conserver uniquement les
        dernières entrées.
        """
        if command is None:
            return
        cmd = str(command)
        with self._lock:
            self._history.append(cmd)
            if self.max_entries is not None and len(self._history) > self.max_entries:
                # conserver les dernières `max_entries`
                self._history = self._history[-self.max_entries :]

            if self.history_file:
                # ouvrir en append et écrire la ligne
                try:
                    with open(self.history_file, "a", encoding="utf-8") as f:
                        f.write(cmd.rstrip("\n") + "\n")
                except Exception:
                    # N'échoue pas si on ne peut pas écrire l'historique
                    pass

    def getHistory(self) -> List[str]:
        """Retourne une copie de la liste d'historique (de la plus ancienne à la plus récente)."""
        with self._lock:
            return list(self._history)
