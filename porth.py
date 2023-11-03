from lib.parser import Parser
from lib.scanner import Scanner
from lib.interpreter import Interpreter
from lib.compiler import Compiler

from sys import argv
from os.path import exists
from time import time

def main() -> None:
    filename: str = ""
    syntax_version: int = 2
    print_bytecode: bool = False
    raw_bytecode: bool = False
    show_stack: bool = False
    silence: bool = False
    pre_compiled: bool = False
    pre_compile_file: bool = False
    pci: bool = False
    _time: bool = False

    start = time()

    for arg in argv:

        if arg == "-time":
            _time = True

        if arg == "-pci":
            pci = True

        if arg in ["-pc", "-pre_compile"]:
            pre_compile_file = True

        if arg in "--show_stack":
            show_stack = True

        if arg in ["-b", "-bytecode"]:
            print_bytecode = True

        if arg in ["-rb", "-raw_bytecode"]:
            raw_bytecode = True

        if arg == "-Werror":
            ...

        if arg == "-silence":
            silence = True

        if arg[:7] == "-porth:":
            syntax_version = int(arg.split(":")[1])

        if arg[-6:] == ".porth" and exists(arg):
            filename = arg

        if arg[-7:] == ".iporth" and exists(arg):
            filename = arg
            pre_compiled = True

    if filename == "":
        print("No file provided.")
        exit(1)

    interpreter = Interpreter(filename)
    #compiler = Compiler()
    #compiler.compile()
    
    with open(filename, "r") as file:
        if pre_compiled:
            guh = list(eval(file.read()))
        elif syntax_version >= 2:
            guh = Scanner(file.read(), filename).scan_tokens()
        else:
            parser = Parser()
            guh = parser.clean_output([parser.parse_word_into_op(word[1]) for word in enumerate(file.read().split())])
        #compiler.compile(guh)
    if pre_compile_file:
        with open(f"{filename[:-6]}.iporth", "w") as file:
            file.write(f"{guh}")
        exit(0)

    if pci:
        skip_to_end = False
        end_tolerance = 0
        output = []
        for token in guh:
            if skip_to_end:
                if token["type"] == "IF_STATEMENT":
                    end_tolerance += 1
                if token["type"] == "END_STATEMENT":
                    if end_tolerance == 0:
                        skip_to_end = False
                    else:
                        end_tolerance -= 1
                continue
            if token["type"] == "OP_PRIVATE":
                skip_to_end = True
                continue
            else:
                output.append(token)
                continue
                
        with open(f"{filename[:-6]}.iporth", "w") as file:
            file.write(f"{output}")
        exit(0)

    if print_bytecode:
        [print(f"{item}") for item in guh]
    elif raw_bytecode:
        print(guh)
    else:
        interpreter.interpret(guh, show_stack, silence)

    if _time:
        print(f"Time Elapsed: {str(time() - start)[:6]} seconds")
