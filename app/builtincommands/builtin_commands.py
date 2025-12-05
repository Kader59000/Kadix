import os
from app.history_manager import HistoryManager
def echo_command(args):
    print(' '.join(args))

def type_command(args):
    if len(args) != 1:
        print("type: invalid number of arguments")
        return
    from app.commands.command import BuiltinCommand, InstalledCommand
    name = args[0]
    if name in BuiltinCommand.BUILTIN_COMMANDS:
        print(f"{name} is a shell builtin")
    elif InstalledCommand.find_installed_command(name):
        print(f"{name} is {InstalledCommand.find_installed_command(name)}")
    else:
        print(f"{name}: not found")

def exit_command(args):
    import sys
    history = HistoryManager.getInstance()
    history.saveHistoryToFile(os.environ.get("HISTFILE"))
    sys.exit(0)

def pwd_command(args):
    print(os.getcwd())

def history_command(args):
    if args and args[0] == '-r':
        if len(args) < 2:
            print("history -r: missing file operand")
            return
        file_path = os.path.expanduser(args[1])
        history = HistoryManager.getInstance()
        history.appendHistoryFromFile(file_path)
        return
    if args and args[0] == '-w':
        if len(args) < 2:
            print("history -w: missing file operand")
            return
        file_path = os.path.expanduser(args[1])
        history = HistoryManager.getInstance()
        try:
            history.saveHistoryToFile(file_path)
        except Exception as e:
            print(f"history -w: error writing {file_path}: {e}")
        return
    if args and args[0] == '-a':
        if len(args) < 2:
            print("history -a: missing file operand")
            return
        file_path = os.path.expanduser(args[1])
        history = HistoryManager.getInstance()
        try:
            history.appendHistoryToFile(file_path)
        except Exception as e:
            print(f"history -a: error appending {file_path}: {e}")
        return
    else:
        max_entries = None
        if args:
            try:
                max_entries = int(args[0])
            except ValueError:
                print("history: invalid number of entries")
                return
        history = HistoryManager.getInstance()
        for index, command in history.getHistory(max_entries):
            print(f"    {index}  {command}")

def cd_command(args):
    if len(args) != 1:
        print("cd: invalid number of arguments")
        return
    try:
        os.chdir(os.path.expanduser(args[0]))
    except FileNotFoundError:
        print(f"cd: no such file or directory: {args[0]}")
