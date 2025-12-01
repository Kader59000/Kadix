import readline
from app.commands.command import BuiltinCommand, PathCommandLocator

class AutoCompleter:
    """
    Classe pour gérer l'autocomplétion des commandes internes et installées du shell.
    """
    def __init__(self):
        # Récupère la liste des commandes internes
        self.builtin_commands = list(BuiltinCommand.BUILTIN_COMMANDS.keys())
        # Récupère la liste des commandes installées (noms uniquement)
        self.installed_commands = [cmd.split("/")[-1] for cmd in PathCommandLocator.list_all_commands()]
        self.commands = sorted(set(self.builtin_commands + self.installed_commands))

    def completer(self, text, state):
        # Filtre les commandes qui commencent par le texte saisi
        matches = [cmd for cmd in self.commands if cmd.startswith(text)]
        if state < len(matches):
            return matches[state] + " "  # Ajoute un espace après la commande complétée
        return None

    def start(self):
        # Configure readline pour utiliser la complétion sur Tab
        readline.set_completer(self.completer)
        readline.parse_and_bind("tab: complete")