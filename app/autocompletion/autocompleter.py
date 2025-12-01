import readline
from app.commands.command import BuiltinCommand

class AutoCompleter:
    """
    Classe pour gérer l'autocomplétion des commandes internes du shell.
    """
    def __init__(self):
        # Récupère la liste des commandes internes
        self.commands = list(BuiltinCommand.BUILTIN_COMMANDS.keys())

    def completer(self, text, state):
        # Filtre les commandes qui commencent par le texte saisi
        matches = [cmd for cmd in self.commands if cmd.startswith(text)]
        if state < len(matches):
            print(f"Completer match for state {state} and text '{text}': {matches[state]}")
            return matches[state]
        print(f"No match for state {state} and text '{text}'")
        return None

    def start(self):
        # Configure readline pour utiliser la complétion sur Tab
        readline.set_completer(self.completer)
        readline.parse_and_bind("tab: complete")