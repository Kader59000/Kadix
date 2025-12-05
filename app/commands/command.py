from abc import ABC, abstractmethod
import subprocess
import sys
from app.history_manager import HistoryManager
class CommandNotFoundException(Exception):
    pass

class Command(ABC):
    """
    Classe abstraite pour une commande shell.
    """
    @abstractmethod
    def execute(self):
        pass

    @staticmethod
    def getCommand(command, args):
        # Import des commandes internes
        if command in BuiltinCommand.BUILTIN_COMMANDS:
            return BuiltinCommand(command, args)
        # Recherche de la commande installée
        path = PathCommandLocator.find_command_path(command)
        if path:
            return InstalledCommand(command, path, args)
        raise CommandNotFoundException(f"{command}: command not found")


class InstalledCommand(Command):
    """
    Commande installée sur le système.
    """
    def __init__(self, name, path, args):
        self.name = name
        self.path = path
        self.args = args
 
    def execute(self, stdin=None, stdout=None, stderr=None, wait=True):
        """Lance la commande puis attend sa fin."""
        process = self.spawn(stdin=stdin, stdout=stdout, stderr=stderr)
        if wait:
            process.wait()
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        HistoryManager.getInstance().logCommand(f"{self.name}")
        return process

    def spawn(self, stdin=None, stdout=None, stderr=None):
        """Démarre la commande sans attendre et retourne le processus."""
        std_in = stdin if stdin is not None else sys.stdin
        std_out = stdout if stdout is not None else sys.stdout
        std_err = stderr if stderr is not None else sys.stderr
        program_name = self.name  # juste le nom, pas le chemin complet
        return subprocess.Popen([program_name] + list(self.args), executable=self.path, stdin=std_in, stdout=std_out, stderr=std_err)
    
    @staticmethod
    def is_installed_command(self):
        return PathCommandLocator.find_command_path(self.name) is not None

    @staticmethod
    def find_installed_command(command):
        """
        Recherche le chemin d'une commande installée en utilisant PathCommandLocator.
        """
        return PathCommandLocator.find_command_path(command)


class PathCommandLocator:
    """
    Classe utilitaire pour rechercher et lister les commandes disponibles dans le PATH.
    """
    @staticmethod
    def find_command_path(command):
        import os
        path = os.environ.get("PATH")
        path_separator = os.pathsep
        directories = path.split(path_separator)
        for directory in directories:
            possible_path = os.path.join(directory, command)
            if os.path.isfile(possible_path) and os.access(possible_path, os.X_OK):
                return possible_path
        return None

    @staticmethod
    def list_all_commands():
        import os
        path = os.environ.get("PATH")
        path_separator = os.pathsep
        directories = path.split(path_separator)
        commands = set()
        for directory in directories:
            if os.path.isdir(directory):
                for filename in os.listdir(directory):
                    file_path = os.path.join(directory, filename)
                    if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
                        commands.add(file_path)
        return sorted(commands)


class BuiltinCommand(Command):
    """
    Commande interne au shell.
    """
    from app.builtincommands.builtin_commands import echo_command, type_command, exit_command, pwd_command, cd_command, history_command
    BUILTIN_COMMANDS = {
                "echo": echo_command,
                "type": type_command,
                "exit": exit_command,
                "pwd": pwd_command,
                "cd": cd_command,
                "history": history_command,
            }

    def __init__(self, name, args):
        self.name = name
        self.args = args
    def execute(self, stdin=None, stdout=None, stderr=None, wait=True):
        if stdin is not None:
            sys.stdin = stdin
        if stdout is not None:
            sys.stdout = stdout
        if stderr is not None:
            sys.stderr = stderr
        if self.name in BuiltinCommand.BUILTIN_COMMANDS:
            command_result =  BuiltinCommand.BUILTIN_COMMANDS[self.name](self.args)
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            HistoryManager.getInstance().logCommand(f"{self.name}")   
            return command_result
        raise CommandNotFoundException(f"{self.name}: builtin command not found")