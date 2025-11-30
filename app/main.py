import sys
import shlex
from commands.command import Command, CommandNotFoundException
should_exit = False

def main():
    while True:
        sys.stdout.write("$ ")
        user_input = input()
        splitted_input = handle_input(user_input)
        command_input = splitted_input[0]
        args = splitted_input[1:]
        try:
            cmd = Command.getCommand(command_input)
            result = cmd.execute(args)
        except CommandNotFoundException as e:
            print(f"{command_input}: command not found")
        except SystemExit:
            break
        if should_exit:
            break
    pass

def handle_input(args_str):
    return shlex.split(args_str)


if __name__ == "__main__":
    main()
