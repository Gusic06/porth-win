from lib.parser import Parser
from lib.interpreter import Interpreter

from sys import argv
from os.path import exists

def main():
    filename: str = ""
    syntax_version: int = 1
    print_bytecode: bool = False
    show_stack: bool = False

    for arg in argv:

        if arg in "--show_stack":
            show_stack = True

        if arg in ["-b", "--bytecode"]:
            print_bytecode = True

        if arg == "-Werror":
            ...

        if arg[:7] == "-porth:":
            syntax_version = int(arg.split(":")[1])

        if arg[-6:] == ".porth" and exists(arg):
            filename = arg

    parser = Parser()
    interpreter = Interpreter()
    
    with open(filename, "r") as file:
        guh = parser.clean_output([parser.parse_word_into_op(word[1]) for word in enumerate(file.read().split())])

    #print(guh)

    if print_bytecode:
        [print(item) for item in guh]
    else:
        interpreter.interpret(guh, show_stack)