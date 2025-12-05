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
        if history_file is not None:
            self.history_file = os.path.abspath(history_file)
        else:
            self.history_file = os.path.abspath("./history_file.txt")

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

    @staticmethod
    def setHistoryFile(history_file, command=None):
        """Change le fichier d'historique et recharge l'historique de l'instance singleton."""
        if hasattr(HistoryManager, "_instance"):
            instance = HistoryManager._instance
            instance.history_file = os.path.abspath(history_file)
            # Recharger l'historique
            instance._history = []
            instance._next_index = 1
            if instance.history_file:
                try:
                    open(instance.history_file, "a", encoding="utf-8").close()
                except Exception:
                    instance.history_file = None
                if instance.history_file:
                    try:
                        with open(instance.history_file, "r", encoding="utf-8") as f:
                            for line in f:
                                line = line.rstrip("\n")
                                if line:
                                    instance._history.append((instance._next_index, line))
                                    instance._next_index += 1
                    except FileNotFoundError:
                        pass
            # Ajouter la commande au début si fournie
            if command:
                instance._history.insert(0, (1, command))
                # Ajuster les indices
                for i in range(1, len(instance._history)):
                    idx, cmd = instance._history[i]
                    instance._history[i] = (i + 1, cmd)
                instance._next_index = len(instance._history) + 1
                # Réécrire le fichier
                if instance.history_file:
                    try:
                        with open(instance.history_file, "w", encoding="utf-8") as f:
                            for idx, cmd in instance._history:
                                f.write(cmd.rstrip("\n") + "\n")
                    except Exception:
                        pass

    def getHistory(self, max_entries: Optional[int] = None) -> List[tuple[int, str]]:
        """Retourne une copie de la liste d'historique (de la plus ancienne à la plus récente)."""
        max_entries = max_entries if max_entries is None else int(max_entries)
        with self._lock:
            if max_entries is not None:
                return list(self._history[-max_entries:])
            return list(self._history)
