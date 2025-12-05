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
    max_entries = None
    if len(args) != 0:
        max_entries = args[0]
    history = HistoryManager.getInstance()
    for index, command in enumerate(history.getHistory(max_entries), start=1):
        print(f"    {index}  {command}")

def cd_command(args):
    if len(args) != 1:
        print("cd: invalid number of arguments")
        return
    try:
        os.chdir(os.path.expanduser(args[0]))
    except FileNotFoundError:
        print(f"cd: no such file or directory: {args[0]}")
