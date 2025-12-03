import shlex
from app.commands.command import Command, CommandNotFoundException, BuiltinCommand, PathCommandLocator
from app.operators.redirection_operator import RedirectionOperator, AppendOperator
from app.autocompletion.manual_autocompleter import ManualAutoCompleter

should_exit = False

def main():
    candidates = list(BuiltinCommand.BUILTIN_COMMANDS.keys())
    candidates += [cmd.split("/")[-1] for cmd in PathCommandLocator.list_all_commands()]
    completer = ManualAutoCompleter(candidates)
    while True:
        user_input = completer.read_line()
        splitted_input = handle_input(user_input)
        # Recherche d'un opérateur de redirection ou d'append
        op_indices = [i for i, token in enumerate(splitted_input) if token in ['>', '1>', '2>', '>>', '1>>', '2>>']]
        if op_indices:
            i = op_indices[0]
            operator_token = splitted_input[i]
            command = splitted_input[0]
            args = splitted_input[1:i]
            output_file = splitted_input[i+1] if i+1 < len(splitted_input) else None
            if output_file:
                cmd = Command.getCommand(command, args)
                if operator_token in ['>>', '1>>', '2>>']:
                    operator = AppendOperator(operator_token, command=cmd, target_file=output_file)
                else:
                    operator = RedirectionOperator(operator_token, command=cmd, target_file=output_file)
                operator.execute()
            else:
                print("No output file specified for redirection.")
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
