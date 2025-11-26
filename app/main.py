import sys
import os
import subprocess
should_exit = False

def main():
    while True:
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
    builtin_command = builtin_command_getter(command)
    if builtin_command:
        builtin_command(args)
        return
    installed_command = find_installed_command(command)
    if installed_command:
        process = subprocess.Popen([command] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        print (stdout, end="")
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
    args = [] # list of (arg, was_quoted)
    current_arg = ''
    in_quotes = False
    do_concatenation = False
    for i in range(len(args_str)):
        current_char = args_str[i]
        if current_char == "'" and not in_quotes:
            if i > 0 and args_str[i-1] == "'":
                do_concatenation = True
            in_quotes = True
        elif current_char == "'" and in_quotes:
            in_quotes = False
            if current_arg != "'":
                if do_concatenation:
                    args.append(args.pop() + current_arg)
                    do_concatenation = False
                else:
                    args.append(current_arg)
            else:
                if i < len(args_str)-1 and args_str[i+1] != " ":
                    do_concatenation = True
            current_arg = ''
        elif current_char == " " and not in_quotes:
            if current_arg:
                if do_concatenation:
                    args.append(args.pop() + current_arg)
                    do_concatenation = False
                else:
                    args.append(current_arg)
                current_arg = ''
        else:
            current_arg += current_char
    if do_concatenation:
        args.append(args.pop() + current_arg)
    else:
        args.append(current_arg)
    return args

        


if __name__ == "__main__":
    main()
