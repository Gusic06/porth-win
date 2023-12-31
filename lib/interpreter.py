from os.path import abspath
from os import system

class Interpreter:

    def __init__(self, filename: str) -> None:
        self.filename: str = filename
        self.stack: list = []
        self.index: int = 0

        self.procs = []

        self.variable: dict = {}
        self.variables: list = []

        self.while_loop: bool = False
        self.failed_while: bool = False

        self.go_to_end: bool = False
        self.end_tolerance: int = 0
        self.repeat: int = 0
        self.file: str = ""

    def is_digit(self, item: str) -> bool:
        try:
            item = int(item) # a lazy hack
            return True
        except Exception:
            return False

    def interpret(self, instructions: list[dict], show_stack: bool = False, silence: bool = False) -> None:
        try:
            self.index = 0
            for index in range(len(instructions)):
                #print(index)
                instruction: dict = instructions[self.index]
                self.index += 1

                if self.go_to_end is True: # for a situation where nested end statements exist (such as nested if conditions)

                    if instruction["token"] == "ELSE_STATEMENT" and self.end_tolerance == 0:
                        self.go_to_end = False

                    if instruction["token"] != "END_STATEMENT":
                        if instruction["token"] == "IF_STATEMENT" or instruction["token"] == "DO_STATEMENT":
                            self.end_tolerance += 1
                        continue

                    else:
                        if self.end_tolerance == 0:
                            self.go_to_end = False
                            if self.while_loop:
                                self.while_loop = False
                                self.index = index
                        else:
                            self.end_tolerance -= 1
                        continue

                
                if instruction["token"] == "PROC":
                    self.procs.append(instruction)

                if instruction["token"] == "INPUT_STATEMENT":
                    self.stack.append(input())

                if instruction["token"] == "WHILE_STATEMENT":
                    self.jump = self.index + 1
                    self.while_loop = True
                    #print(self.repeat)

                if instruction["token"] == "DO_STATEMENT":
                    print(self.stack)
                    self.comparison = self.stack.pop()
                    print(self.stack)
                    if self.comparison == 1:
                        continue
                    else:
                        self.go_to_end = True
                        self.while_loop = False

                if instruction["token"] == "IF_STATEMENT":
                    self.comparison = self.stack.pop()

                    if self.comparison == 1:
                        continue
                    else:
                        if self.while_loop:
                            self.while_loop = False
                        self.go_to_end = True

                if instruction["token"] == "ELSE_STATEMENT":
                    self.go_to_end = True
                
                if instruction["token"] == "END_STATEMENT":
                    if self.while_loop:
                        if self.failed_while:
                            self.while_loop = False
                        else:
                            self.index = self.jump
                    ...
                    #if self.repeat != 0:
                    #    print("guh")

                if instruction["token"] == "OP_JOIN":
                    self.item1 = self.stack.pop()
                    self.item2 = self.stack.pop()
                    self.stack.append(f"{self.item1}{self.item2}")

                if instruction["token"] == "OP_EXIT":
                    self.exit_code = self.stack.pop()
                    exit(self.exit_code)

                if instruction["token"] == "OP_EXEC":
                    self.code = self.stack.pop()
                    exec(self.code)

                if instruction["token"] == "OP_ASSIGN":
                    self.var_name = self.stack.pop()
                    if instructions[index - 1]["type"] == "int" or instructions[index - 1]["type"] == "string":
                        print(f"{instruction['file']}:{instruction['pos'][0]}:{instruction['pos'][1]}: Cannot give variable name an integer/string value")
                        exit(1)
                    instructions[index]["type"] = "var"
                    self.item = self.stack.pop()
                    self.variables.append({"name" : self.var_name, "contents" : self.item})

                if instruction["token"] == "OP_DROP":
                    self.stack.pop()

                if instruction["token"] == "OP_DROPALL":
                    self.stack = []

                if instruction["token"] == "OP_SWAP":
                    self.item1 = self.stack.pop()
                    self.item2 = self.stack.pop()
                    self.stack.append(self.item1)
                    self.stack.append(self.item2)

                if instruction["token"] == "OP_DUP":
                    self.item = self.stack.pop()
                    self.stack.append(self.item)
                    self.stack.append(self.item)

                if instruction["token"] == "OP_PUSH":

                    if instruction["value"] == "__file__":
                        self.stack.append(abspath(self.filename))
                        continue

                    if instruction["value"] == "__main__":
                        if instruction["file"] == self.filename:
                            self.stack.append(1)
                        else:
                            self.stack.append(0)
                        continue

                    if instruction["value"] == "__system__":
                        system(self.stack.pop())
                        continue

                    if instruction["type"] == "identifier":
                        
                        self.is_proc = False
                        self.is_var = False
                        for proc in self.procs:
                            self.is_proc = False
                            if proc["value"]["name"] == instruction["value"]:
                                self.interpret(proc["value"]["contents"], show_stack, silence)
                                self.is_proc = True
                                continue

                        for variable in self.variables:
                            if variable["name"] == instruction["value"]:
                                self.stack.append(variable["contents"])
                                self.is_var = True
                                continue

                        if not self.is_proc and not self.is_var:
                            self.stack.append(instruction["value"])

                    elif instruction["type"] != "identifier":
                        self.stack.append(instruction["value"])

                if instruction["token"] == "OP_OUT":
                    output = self.stack.pop()
                    if silence is False:
                        if instructions[index - 1]["type"] == "var":
                            for variable in self.variables:
                                if variable["name"] == instructions[index - 1]["value"]:
                                    print(output, end="")
                                    break
                            else:
                                print(f"{instruction['file']}:{instruction['pos'][0]}:{instruction['pos'][1]}: Cannot print identifier that hasn't been assigned a value.")
                                exit(1)
                        else:
                            print(output, end="")

                if instruction["token"] == "OP_OUTLN":
                    output = self.stack.pop()
                    if silence is False:
                        if instructions[index - 1]["type"] == "var":
                            for variable in self.variables:
                                if variable["name"] == instructions[index - 1]["value"]:
                                    print(output)
                                    break
                            else:
                                print(f"{instruction['file']}:{instruction['pos'][0]}:{instruction['pos'][1]}: Cannot print identifier that hasn't been assigned a value.")
                                exit(1)
                        else:
                            print(output)
                   

                if instruction["token"] == "OP_DIV":
                    self.item1 = self.stack.pop()
                    self.item2 = self.stack.pop()
                    self.stack.append(round(self.item2 / self.item1))

                if instruction["token"] == "OP_MULTI":
                    self.item1 = self.stack.pop()
                    self.item2 = self.stack.pop()
                    self.stack.append(self.item1 * self.item2)

                if instruction["token"] == "OP_EQUALITY":
                    self.item1 = self.stack.pop()
                    self.item2 = self.stack.pop()
                    self.stack.append(int(self.item1 == self.item2))

                if instruction["token"] == "OP_INEQUALITY":
                    self.item1 = self.stack.pop()
                    self.item2 = self.stack.pop()
                    self.stack.append(int(self.item2 != self.item1))

                if instruction["token"] == "OP_GT":
                    if instructions[index - 2]["type"] == "string" or instructions[index - 1]["type"] == "string":
                        print(f"\n{instruction['file']}:{instruction['pos'][0]}:{instruction['pos'][1]}: Cannot use '>' operand on string type")
                        exit(1)
                    self.item1 = self.stack.pop()
                    self.item2 = self.stack.pop()
                    self.stack.append(int(self.item2 > self.item1))

                if instruction["token"] == "OP_LT":
                    if instructions[index - 2]["type"] == "string" or instructions[index - 1]["type"] == "string":
                        print(f"\n{instruction['file']}:{instruction['pos'][0]}:{instruction['pos'][1]}: Cannot use '<' operand on string type")
                        exit(1)
                    self.item1 = self.stack.pop()
                    self.item2 = self.stack.pop()
                    self.stack.append(int(self.item2 < self.item1))

                if instruction["token"] == "OP_LTEQUALITY":
                    if instructions[index - 2]["type"] == "string" or instructions[index - 1]["type"] == "string":
                        print(f"\n{instruction['file']}:{instruction['pos'][0]}:{instruction['pos'][1]}: Cannot use '<=' operand on string type")
                        exit(1)
                    self.item1 = self.stack.pop()
                    self.item2 = self.stack.pop()
                    self.stack.append(int(self.item2 <= self.item1))

                if instruction["token"] == "OP_GTEQUALITY":
                    if instructions[index - 2]["type"] == "string" or instructions[index - 1]["type"] == "string":
                        print(f"\n{instruction['file']}:{instruction['pos'][0]}:{instruction['pos'][1]}: Cannot use '>=' operand on string type")
                        exit(1)
                    self.item1 = self.stack.pop()
                    self.item2 = self.stack.pop()
                    self.stack.append(int(self.item2 >= self.item1))

                if instruction["token"] == "OP_PLUS":
                    if instructions[index - 2]["type"] == "string" or instructions[index - 1]["type"] == "string":
                        print(f"\n{instruction['file']}:{instruction['pos'][0]}:{instruction['pos'][1]}: Cannot use '+' operand on string type")
                        exit(1)
                    self.item1 = self.stack.pop()
                    self.item2 = self.stack.pop()
                    self.stack.append(self.item1 + self.item2)

                if instruction["token"] == "OP_PLUSEQUALS":
                    if instructions[index - 2]["type"] == "string" or instructions[index - 1]["type"] == "string":
                        print(f"\n{instruction['file']}:{instruction['pos'][0]}:{instruction['pos'][1]}: Cannot use '+' operand on string type")
                        exit(1)
                    if instructions[index - 2]["type"] == "identifier":
                        ...

                if instruction["token"] == "OP_MINUS":
                    if instructions[index - 2]["type"] == "string" or instructions[index - 1]["type"] == "string":
                        print(f"\n{instruction['file']}:{instruction['pos'][0]}:{instruction['pos'][1]}: Cannot use '-' operand on string type")
                        exit(1)
                    self.item1 = self.stack.pop()
                    self.item2 = self.stack.pop()
                    self.stack.append(self.item2 - self.item1)

                if instruction["token"] == "OP_NOT":
                    self.result = self.stack.pop()

                    if self.result == 1:
                        self.stack.append(0)
                    
                    if self.result == 0:
                        self.stack.append(1)

                if instruction["token"] == "OP_SLICE":
                    self.slice = self.stack.pop()
                    self.string = self.stack.pop()
                    self.return_value = str(eval(f"'{self.string}'{self.slice}"))
                    self.stack.append(self.return_value)

                if show_stack:
                    print(f"{index}{' ' * (4 - len(str(index)))}: {self.stack}")

            if len(self.stack) != 0:
                s: str = "s" if len(self.stack) > 1 or self.stack == 0 else ""
                were: str = "were" if len(self.stack) > 1 or self.stack == 0 else "was"
                #print(f"\n{self.filename}: [ {len(self.stack)} ] item{s} {were} left unused on the stack.")

        except Exception as Error:
            print("guh")
            print(f"\n{instruction['file']}:{instruction['pos'][0]}:{instruction['pos'][1]}: {Error=}")
            exit(1)
