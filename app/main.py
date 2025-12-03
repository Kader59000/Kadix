import shlex
from app.commands.command import Command, CommandNotFoundException, BuiltinCommand, PathCommandLocator, InstalledCommand
from app.operators.pipeline_operator import PipelineOperator
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
        if not splitted_input:
            continue
        # Gestion des pipelines multiples (séparateur '|')
        if "|" in splitted_input:
            # découpe en segments de tokens entre les '|'
            segments = []
            cur = []
            for tok in splitted_input:
                if tok == "|":
                    if not cur:
                        break
                    segments.append(cur)
                    cur = []
                else:
                    cur.append(tok)
            if cur:
                segments.append(cur)

            # validation minimale
            if len(segments) < 2 or any(len(s) == 0 for s in segments):
                print("Invalid pipeline syntax.")
                continue

            try:
                # construire les Command instances
                cmds = [Command.getCommand(s[0], s[1:]) for s in segments]
            except CommandNotFoundException as e:
                print(e)
                continue

            # Exécuter le pipeline multi-commandes
            def run_pipeline(commands):
                n = len(commands)
                if n == 0:
                    return None
                if n == 1:
                    return commands[0].execute()

                pipes = [os.pipe() for _ in range(n - 1)]
                procs = []
                try:
                    for i, cmd in enumerate(commands):
                        in_fd = pipes[i - 1][0] if i > 0 else None
                        out_fd = pipes[i][1] if i < n - 1 else None

                        if isinstance(cmd, InstalledCommand):
                            proc = cmd.spawn(stdin=in_fd, stdout=out_fd)
                            procs.append(proc)
                        else:
                            fin = os.fdopen(in_fd, "r") if in_fd is not None else None
                            fout = os.fdopen(out_fd, "w") if out_fd is not None else None
                            try:
                                cmd.execute(stdin=fin, stdout=fout)
                            finally:
                                if fout is not None:
                                    try:
                                        fout.flush()
                                    except Exception:
                                        pass
                                    fout.close()
                                if fin is not None:
                                    fin.close()

                    # fermer les FD parentaux
                    for r, w in pipes:
                        try:
                            os.close(r)
                        except OSError:
                            pass
                        try:
                            os.close(w)
                        except OSError:
                            pass

                    # attendre les processus externes
                    for p in procs:
                        try:
                            p.wait()
                        except Exception:
                            pass
                finally:
                    for r, w in pipes:
                        for fd in (r, w):
                            try:
                                os.close(fd)
                            except Exception:
                                pass
                return None

            run_pipeline(cmds)
            continue
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
