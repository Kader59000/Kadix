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
    sys.exit(0)

def pwd_command(args):
    print(os.getcwd())

def history_command(args):
    if args and args[0] == '-r':
        if len(args) < 2:
            print("history -r: missing file operand")
            return
        file_path = os.path.expanduser(args[1])
        try:
            hist_mgr = HistoryManager.getInstance(file_path)
            for index, command in hist_mgr.getHistory():
                print(f"    {index}  {command}")
        except FileNotFoundError:
            print(f"history -r: {file_path}: No such file or directory")
        except Exception as e:
            print(f"history -r: error reading {file_path}: {e}")
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
