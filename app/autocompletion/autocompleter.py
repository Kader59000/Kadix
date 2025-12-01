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
        matches = [cmd for cmd in self.commands if cmd.startswith(text)]
        if len(matches) > 1:
            if state == 0: 
                # Premier Tab : ring the bell et ne rien compléter
                print('\x07', flush=True)
                return None
            else:
                # Deuxième Tab : affiche uniquement la ligne des suggestions
                res = '  '.join(matches)
                print(res)
                return None
        if state < len(matches):
            return matches[state] + " "

    def start(self):
        # Configure readline pour utiliser la complétion sur Tab
        readline.set_completer(self.completer)
        readline.parse_and_bind("tab: complete")