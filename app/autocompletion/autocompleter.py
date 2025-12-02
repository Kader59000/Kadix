import  readline
from app.commands.command import BuiltinCommand, PathCommandLocator
import sys
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
        last_processed_input = ""

    def completer_v1(self, text, state):
        matches = [cmd for cmd in self.commands if cmd.startswith(text)]
        if len(matches) > 1:
            if state == 0: 
                # Premier Tab : ring the bell et ne rien compléter
                print('\x07', end='', flush=True)
                return '\x07'
            else:
                # Deuxième Tab : affiche uniquement la ligne des suggestions
                buf = readline.get_line_buffer()
                print('$ '  + buf)
                readline.clear_history()
                res = '  '.join(matches)
                print(res)
                print('$ '  + buf)
                return res
        if state < len(matches):
            return matches[state] + " "
        
    def completer(self, text, state):
        matches = [cmd for cmd in self.commands if cmd.startswith(text)]
        if not matches:
            # Aucun match, ring the bell
            if state == 0:
                print('\x07', end='', flush=True)
            return None
        if len(matches) == 1:
            # Un seul match, complète entièrement
            return matches[0][len(text):] + " "
        # Plusieurs matches, complète le LCP des suffixes
        suffixes = [cmd[len(text):] for cmd in matches]
        lcp = AutoCompleter.longest_common_prefix(suffixes)
        if not lcp:
            # Plusieurs matches mais pas d'avancée possible, ring the bell
            if state == 0:
                print('\x07', end='', flush=True)
            return None
        print('$ ' + text + lcp)
        return '$ ' + text + lcp

    
    @staticmethod
    def longest_common_prefix(strs):
        if not strs or len(strs) == 0: 
            return "" 
        reference = strs[0]
        longest_prefix = ''
        for i in range(len(reference)):
            char = reference[i]
            all_contain_prefix = True
            for chaine in strs:
                if len(chaine) <= i or chaine[i] != char:
                    all_contain_prefix = False
                    break
            if all_contain_prefix:
                longest_prefix += char
            else:
                break
        return longest_prefix



    def start(self):
        # Configure readline pour utiliser la complétion sur Tab
        readline.set_completer(self.completer)
        readline.parse_and_bind("tab: complete")