from os import system

class Compiler:

    def __init__(self) -> None:
        self.main_asm: str = """bits 64
global main
extern printf
section .text
main:
"""
        self.addr_counter: int = 0
        self.vars = []

    def compile(self, instructions: list[dict]) -> None:
        for index in range(len(instructions)):
            instruction = instructions[index]

            if instruction["type"] == "OP_PUSH":
                if instruction["struct"] == "string":
                    self.vars.append(f"\naddr_{self.addr_counter}:\n    db \"{instruction['value']}\", 10, 0\n")

            if instruction["type"] == "OP_OUT":
                self.main_asm += "    lea rcx, [rax]\n    sub rsp, 8+16\n    call printf\n    add rsp, 8+16\n"

        self.main_asm += "    ret\n"

        print(self.main_asm)

        for var in self.vars:
            self.main_asm += var

        with open("output.asm", "w") as file:
            file.write(self.main_asm)

        system("nasm -fwin64 output.asm")
        system("gcc output.obj")
        system(".\\a.exe")