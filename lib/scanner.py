from os import system
from os.path import exists

class Scanner:

    def __init__(self, source: str, filename: str) -> None:
        self.path = __file__.split("\lib\scanner.py")
        self.source = source
        self.filename = filename
        self.orginal_filename = filename
        self.line = 1
        self.line_index = 0
        self.start = 0
        self.current_index = 0
        self.output = []

        self.include: bool = False
        self.included_contents: list = []

    def at_end(self) -> bool:
        return self.current_index >= len(self.source)
      
    def advance(self) -> bool:
        self.return_value = self.source[self.current_index]
        self.current_index += 1
        return self.return_value

    def create_token(self, token_type: str, value: any, struct: str, pos: tuple[int, int]) -> None:
        self.output.append({"token" : token_type, "value" : value, "type" : struct, "pos" : pos, "file" : self.filename})
    
    def scan_token(self) -> None:
        self.character = self.advance()
        self.line_index += 1
        match self.character:

            case "(":
                self.create_token("OP_LPAREN", None, "operator", (self.line, self.line_index))

            case ")":
                self.create_token("OP_RPAREN", None, "operator", (self.line, self.line_index))

            case "{":
                self.create_token("OP_LBRACE", None, "operator", (self.line, self.line_index))
            
            case "}":
                self.create_token("OP_RBRACE", None, "operator", (self.line, self.line_index))

            case ",":
                self.create_token("OP_COMMA", None, "operator", (self.line, self.line_index))

            case ".":
                self.create_token("OP_DOT", None, "operator", (self.line, self.line_index))

            case "-":
                if self.match("="):
                    self.create_token("OP_MINUSEQUALS", None, "operator", (self.line, self.line_index))
                else:
                    self.create_token("OP_MINUS", None, "operator", (self.line, self.line_index))

            case "+":
                if self.match("="):
                    self.create_token("OP_PLUSEQUALS", None, "operator", (self.line, self.line_index))
                else:
                    self.create_token("OP_PLUS", None, "operator", (self.line, self.line_index))

            case "*":
                if self.match("="):
                    self.create_token("OP_MULTIEQUALS", None, "operator", (self.line, self.line_index))
                else:
                    self.create_token("OP_MULTI", None, "operator", (self.line, self.line_index))
            
            case "!":
                if self.match("=") is True:
                    self.create_token("OP_INEQUALITY", None, "operator", (self.line, self.line_index))
                else:
                    self.create_token("OP_NOT", None, "operator", (self.line, self.line_index))

            case "=":
                if self.match("=") is True:
                    self.create_token("OP_EQUALITY", None, "operator", (self.line, self.line_index))
                else:
                    self.create_token("OP_ASSIGN", None, "operator", (self.line, self.line_index))

            case "<":
                if self.match("=") is True:
                    self.create_token("OP_LTEQUALITY", None, "operator", (self.line, self.line_index))
                else:
                    self.create_token("OP_LT", None, "operator", (self.line, self.line_index))

            case ">":
                if self.match("=") is True:
                    self.create_token("OP_GTEQUALITY", None, "operator", (self.line, self.line_index))
                else:
                    self.create_token("OP_GT", None, "operator", (self.line, self.line_index))

            case "/":
                if self.match("="):
                    self.create_token("OP_DIVEQUALS", None, "operator", (self.line, self.line_index))
                elif self.match("/"):
                    while (self.peek() != "\n" and not self.at_end()):
                        self.advance()
                else:
                    self.create_token("OP_DIV", None, "operator", (self.line, self.line_index))

            case '"':
                self.string()

            case " ":
                pass

            case "\r":
                pass

            case "\t":
                pass

            case "\n":
                self.line += 1
                self.line_index = 0

            case _:
                if self.is_digit(self.character):
                    self.number()
                if self.is_alpha(self.character):
                    self.identifier()
                if not self.is_alpha(self.character) and not self.is_digit(self.character):
                    print(f"Unexpected item at:\n    line:  [ {self.line} ]\n    index: [ {self.line_index} ]")

        
    def number(self) -> None:
        while self.is_digit(self.peek()):
            self.advance()

        if self.peek() == "." and self.is_digit(self.peek_next()):
            self.advance()

            while self.is_digit(self.peek()):
                self.advance()

        self.create_token("OP_PUSH", int(self.source[self.start:self.current_index]), "int", (self.line, self.line_index))


    def identifier(self) -> None:
        while self.is_alphanumeric(self.peek()):
            self.advance()
        self.text = self.source[self.start:self.current_index]
        match self.text:

            case "if":
                self.create_token("IF_STATEMENT", None, "operator", (self.line, self.line_index))

            case "else":
                self.create_token("ELSE_STATEMENT", None, "operator", (self.line, self.line_index))

            case "end":
                self.create_token("END_STATEMENT", None, "operator", (self.line, self.line_index))

            case "while":
                self.create_token("WHILE_STATEMENT", None, "operator", (self.line, self.line_index))

            case "do":
                self.create_token("DO_STATEMENT", None, "operator", (self.line, self.line_index))

            case "__input__":
                self.create_token("INPUT_STATEMENT", None, "operator", (self.line, self.line_index))

            case "join":
                self.create_token("OP_JOIN", None, "operator", (self.line, self.line_index))

            case "exit":
                self.create_token("OP_EXIT", None, "operator", (self.line, self.line_index))

            case "drop":
                self.create_token("OP_DROP", None, "operator", (self.line, self.line_index))

            case "dropall":
                self.create_token("OP_DROPALL", None, "operator", (self.line, self.line_index))

            case "exec":
                self.create_token("OP_EXEC", None, "operator", (self.line, self.line_index))

            case "swap":
                self.create_token("OP_SWAP", None, "operator", (self.line, self.line_index))

            case "slice":
                self.create_token("OP_SLICE", None, "operator", (self.line, self.line_index))

            case "print":
                self.create_token("OP_OUT", None, "operator", (self.line, self.line_index))

            case "println":
                self.create_token("OP_OUTLN", None, "operator", (self.line, self.line_index))

            case "for":
                self.create_token("FOR_STATEMENT", None, "operator", (self.line, self.line_index))

            case "true":
                self.create_token("OP_PUSH", 1, "int", (self.line, self.line_index))

            case "false":
                self.create_token("OP_PUSH", 0, "int", (self.line, self.line_index))

            case "dup":
                self.create_token("OP_DUP", None, "operator", (self.line, self.line_index))

            case "include":
                self.include = True

            case "private":
                self.create_token("OP_PRIVATE", None, "operator", (self.line, self.line_index))

            case "proc":
                self.create_token("PROC_STATEMENT", None, "operator", (self.line, self.line_index)) # {"type" : "PROC", "value" : {"name" : "hello", "contents" : [<iporth-code>]}, "struct" : "proc", "pos" : (1, 1), "file" : "std.porth"}

            case "in":
                self.create_token("IN_STATEMENT", None, "operator", (self.line, self.line_index))

            case _:
                self.create_token("OP_PUSH", self.text, "identifier", (self.line, self.line_index))


    def is_alphanumeric(self, character) -> bool:
        return self.is_alpha(character) or self.is_digit(character)

    def is_alpha(self, character) -> bool:
        return (character >= "a" and character <= "z") or (character >= "A" and character <= "Z") or character == "_"

    def is_digit(self, character) -> bool:
        try:
            character = int(character)
            return True
        except Exception:
            return False

    def string(self) -> None:
        while self.peek() != '"' and not self.at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        
        if self.at_end():
            raise Exception(f"\nUnterminated string at:\n    line:  [ {self.line} ]\n    index: [ {self.line_index} ]")
        
        self.advance()

        try:
            self.return_value = self.source[self.start + 1 : self.current_index - 1]
            if self.include:

                if self.return_value == self.filename:
                    print(f"{self.filename}:{self.line}:{self.line_index}: Cannot include source file within itself.")
                    exit(1)

                if self.return_value[-6:] == ".porth":
                    if self.return_value in ["std.porth", "system.porth", "string.porth"]:
                        with open(f"{self.path[0]}\\std\\{self.return_value[:-6]}.iporth", "r") as file:
                            self.included_contents.extend(list(eval(file.read())))
                    elif not exists(f"{self.return_value[:-6]}.iporth"):
                        system(f"porth {self.return_value} -pci")
                        self.return_value = f"{self.return_value[:-6]}.iporth"
                        with open(self.return_value, "r") as file:
                            self.included_contents.extend(list(eval(file.read())))
                self.include = False
            else:
                self.create_token("OP_PUSH", self.return_value, "string", (self.line, self.line_index))
        except Exception:
            pass

    def peek_next(self) -> str:
        if self.current_index >= len(self.source):
            return "\0"
        else:
            return self.source[self.current_index + 1]

    def peek(self) -> str:
        if self.at_end():
            return "\0"
        else:
            return self.source[self.current_index]

    def match(self, expected: str) -> bool:
        if self.at_end() or self.source[self.current_index] != expected:
            return False
        else:
            self.current_index += 1
            return True

    def scan_tokens(self) -> None:
        while not self.at_end():
            self.start = self.current_index
            self.scan_token()
        self.included_contents.extend(self.output)
        self.output = []
        self.index = 0
        self.go_to_end = False
        self.completed_proc = False
        self.in_proc = False
        while len(self.included_contents) >= self.index + 1: # second pass for creating proc, probably gonna make the interpreter slower but oh well
            instruction = self.included_contents[self.index]
            if self.go_to_end:
                if instruction["token"] != "END_STATEMENT":
                    if instruction["token"] == "IF_STATEMENT":
                        self.end_tolerance += 1
                else:
                    if self.end_tolerance == 0:
                        self.go_to_end = False
                        self.completed_proc = True
                        continue
                    else:
                        self.end_tolerance -= 1
                self.proc_contents.append(instruction)

            elif instruction["token"] == "PROC_STATEMENT":
                self.end_tolerance: int = 0
                self.in_proc = True
                self.proc_name: str = self.included_contents[self.index + 1]["value"]
                self.proc_contents: list[dict] = []

                if self.included_contents[self.index + 2]["token"] == "IN_STATEMENT":
                    self.index += 2
                    self.go_to_end: bool = True
        
            elif self.completed_proc:
                self.proc = {"token" : "PROC", "value" : {"name" : self.proc_name, "contents" : self.proc_contents}, "type" : "identifier", "pos" : instruction["pos"], "file" : self.filename}
                self.output.append(self.proc)
                self.completed_proc = False
                self.in_proc = False

            else:
                self.output.append(instruction)
            
            self.index += 1

        return self.output
