import sys
import os
import subprocess
import shlex
should_exit = False

def main():
    while True:
        reset_redirection()
        sys.stdout.write("$ ")
        user_input = input()
        splitted_input = handle_input(user_input)
        command_input = splitted_input[0]
        args = splitted_input[1:]
        if (command_exists(command_input)):
            execute_command(command_input, args)
        else:
            print(f"{command_input}: command not found")

        if should_exit:
            break
    pass

def echo_command(args):
    for i in range (len(args) - 1):
        print(args[i] + " ", end="")
    if (len(args) > 0):
        print(args[-1], end="")
    print("", end="\n")

def type_command(args):
    if len(args) != 1:
        print("type: invalid number of arguments", end="\n")
        return
    if (args[0] in BUILTIN_COMMANDS):
        print(f"{args[0]} is a shell builtin", end="\n")
    elif is_installed_command(args[0]):
        print(f"{args[0]} is {find_installed_command(args[0])}", end="\n")
    else:
        print(f"{args[0]}: not found", end="\n")

def exit_command(args):
    global should_exit
    should_exit = True

def pwd_command(args):
    print(os.getcwd())

def cd_command(args):
    if len(args) != 1:
        print("cd: invalid number of arguments")
        return
    try:
        os.chdir(os.path.expanduser(args[0]))
    except FileNotFoundError:
        print(f"cd: no such file or directory: {args[0]}", end="\n")

BUILTIN_COMMANDS = {
    "echo": echo_command,
    "type": type_command,
    "exit": exit_command,
    "pwd": pwd_command,
    "cd": cd_command
}

def command_exists(command):
    return command in BUILTIN_COMMANDS or is_installed_command(command)

def builtin_command_getter(command):
    return BUILTIN_COMMANDS.get(command, None)

def execute_command(command, args):
    check_redirection(args)
    builtin_command = builtin_command_getter(command)
    if builtin_command:
        builtin_command(args)
        return
    installed_command = find_installed_command(command)
    if installed_command:
        process = subprocess.Popen([command] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        print('process return code:', process.returncode)
        if process.returncode != 0:
            print(stderr, end="", file=sys.stderr)
        else:
            print(stdout, end="")
        return

def find_installed_command(command):
    path = os.environ.get("PATH")
    path_separator = os.pathsep 
    directories = path.split(path_separator)
    for directory in directories:
        possible_path = os.path.join(directory, command)
        if os.path.isfile(possible_path) and os.access(possible_path, os.X_OK):
            return possible_path
    return None

def is_installed_command(command):
    return find_installed_command(command) is not None

def handle_input(args_str):
    inp = shlex.split(args_str)
    return inp

def redirect(file_descriptor, output_file):
    if file_descriptor != "1" and file_descriptor != "2":
        print(f"Redirection of file descriptor {file_descriptor} is not supported.")
        return False
    if not output_file:
        print("No output file specified for redirection.")
        return False
    if file_descriptor == "1":
        sys.stdout = open(output_file, "w")
    elif file_descriptor == "2":
        sys.stderr = open(output_file, "w")
    return True

def reset_redirection():
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

def check_redirection(args):
    for i in range(len(args)):
        if '>' in args[i]:
            parts = args[i].split('>')
            if (len(parts) != 2):
                print("Invalid redirection syntax.")
                return False
            file_descriptor = parts[0]
            if (file_descriptor == ''):
                file_descriptor = "1"
            if i == len(args) - 1:
                print("No output file specified for redirection.")
                return False
            output_file = args[i + 1]
            redirect(file_descriptor, output_file)
            # Modifie args en place pour retirer la redirection
            del args[i:]
            return True
    return False

if __name__ == "__main__":
    main()
