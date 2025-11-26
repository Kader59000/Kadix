import sys


def main():
    while True:
        sys.stdout.write("$ ")
        user_input = input()
        splitted_input = user_input.split(" ")
        command_input = splitted_input[0]
        args = splitted_input[1:]
        if (command_input == "exit"):
            break
        command = command_getter(command_input)
        if (command != None):
            command(args)
            continue
        else:
            print(f"{command_input}: command not found")
    pass

def echo_command(args):
    for i in range (len(args) - 1):
        print(args[i] + " ", end="")
    print(args[-1], end="")
    print("", end="\n")

def command_getter(command):
    if (command == "echo"):
        return echo_command
    return None


if __name__ == "__main__":
    main()
