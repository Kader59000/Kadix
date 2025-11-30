import sys
import shlex
from commands.command import Command, CommandNotFoundException
from operators.redirection_operator import RedirectionOperator

should_exit = False

def main():
    while True:
        sys.stdout.write("$ ")
        user_input = input()
        splitted_input = handle_input(user_input)
        # Vérifie la présence d'un opérateur de redirection
        if any(op in splitted_input for op in ['>', '1>', '2>']):
            # Recherche l'opérateur et ses paramètres
            for i, token in enumerate(splitted_input):
                if token in ['>', '1>', '2>']:
                    command = splitted_input[0]
                    args = splitted_input[1:i]
                    output_file = splitted_input[i+1] if i+1 < len(splitted_input) else None
                    if output_file:
                        operator = RedirectionOperator(command=[command]+args, target_file=output_file)
                        operator.execute()
                    else:
                        print("No output file specified for redirection.")
                    break
        else:
            command_input = splitted_input[0]
            args = splitted_input[1:]
            try:
                cmd = Command.getCommand(command_input, args)
                result = cmd.execute()
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
