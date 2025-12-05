from app.history_manager import HistoryManager
from typing import Optional

class HistoryNavigator:
    def __init__(self):
        self.history = HistoryManager.getInstance()
        self.current_index = None  # None means not navigating, at the end

    def get_previous(self) -> Optional[str]:
        """Retourne la commande précédente dans l'historique."""
        hist = self.history.getHistory()
        if not hist:
            return None
        if self.current_index is None:
            self.current_index = len(hist) - 1
        else:
            if self.current_index > 0:
                self.current_index -= 1
            else:
                return None  # déjà au début
        return hist[self.current_index][1]  # (index, command)

    def get_next(self) -> Optional[str]:
        """Retourne la commande suivante dans l'historique."""
        hist = self.history.getHistory()
        if not hist or self.current_index is None:
            return None
        if self.current_index < len(hist) - 1:
            self.current_index += 1
            return hist[self.current_index][1]
        else:
            self.current_index = None
            return ""  # revenir à une ligne vide

    def reset(self):
        """Remet la navigation à zéro."""
        self.current_index = None