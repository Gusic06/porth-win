from os import system
from os.path import exists

class Scanner:

    def __init__(self, source: str, filename: str) -> None:
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

    def at_end(self):
        return self.current_index >= len(self.source)
      
    def advance(self):
        self.return_value = self.source[self.current_index]
        self.current_index += 1
        return self.return_value

    def create_token(self, token_type: str, value: any, struct: str, pos: tuple[int, int]) -> None:
        self.output.append({"type" : token_type, "value" : value, "struct" : struct, "pos" : pos, "file" : self.filename})
    
    def scan_token(self):
        self.character = self.advance()
        self.line_index += 1
        match self.character:

            case "(":
                self.create_token("OP_LPAREN", None, "identifier", (self.line, self.line_index))

            case ")":
                self.create_token("OP_RPAREN", None, "identifier", (self.line, self.line_index))

            case "{":
                self.create_token("OP_LBRACE", None, "identifier", (self.line, self.line_index))
            
            case "}":
                self.create_token("OP_RBRACE", None, "identifier", (self.line, self.line_index))

            case ",":
                self.create_token("OP_COMMA", None, "identifier", (self.line, self.line_index))

            case ".":
                self.create_token("OP_DOT", None, "identifier", (self.line, self.line_index))

            case "-":
                if self.match("="):
                    self.create_token("OP_MINUSEQUALS", None, "identifier", (self.line, self.line_index))
                else:
                    self.create_token("OP_MINUS", None, "identifier", (self.line, self.line_index))

            case "+":
                if self.match("="):
                    self.create_token("OP_PLUSEQUALS", None, "identifier", (self.line, self.line_index))
                else:
                    self.create_token("OP_PLUS", None, "identifier", (self.line, self.line_index))

            case "*":
                if self.match("="):
                    self.create_token("OP_MULTIEQUALS", None, "identifier", (self.line, self.line_index))
                else:
                    self.create_token("OP_MULTI", None, "identifier", (self.line, self.line_index))
            
            case "!":
                if self.match("=") is True:
                    self.create_token("OP_INEQUALITY", None, "identifier", (self.line, self.line_index))
                else:
                    self.create_token("OP_NOT", None, "identifier", (self.line, self.line_index))

            case "=":
                if self.match("=") is True:
                    self.create_token("OP_EQUALITY", None, "identifier", (self.line, self.line_index))
                else:
                    self.create_token("OP_ASSIGN", None, "identifier", (self.line, self.line_index))

            case "<":
                if self.match("=") is True:
                    self.create_token("OP_LTEQUALITY", None, "identifier", (self.line, self.line_index))
                else:
                    self.create_token("OP_LT", None, "identifier", (self.line, self.line_index))

            case ">":
                if self.match("=") is True:
                    self.create_token("OP_GTEQUALITY", None, "identifier", (self.line, self.line_index))
                else:
                    self.create_token("OP_GT", None, "identifier", (self.line, self.line_index))

            case "/":
                if self.match("="):
                    self.create_token("OP_DIVEQUALS", None, "identifier", (self.line, self.line_index))
                elif self.match("/"):
                    while (self.peek() != "\n" and not self.at_end()):
                        self.advance()
                else:
                    self.create_token("OP_DIV", None, "identifier", (self.line, self.line_index))

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

        
    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        if self.peek() == "." and self.is_digit(self.peek_next()):
            self.advance()

            while self.is_digit(self.peek()):
                self.advance()

        self.create_token("OP_PUSH", int(self.source[self.start:self.current_index]), "int", (self.line, self.line_index))


    def identifier(self):
        while self.is_alphanumeric(self.peek()):
            self.advance()
        self.text = self.source[self.start:self.current_index]
        match self.text:

            case "if":
                self.create_token("IF_STATEMENT", None, "identifier", (self.line, self.line_index))

            case "else":
                self.create_token("ELSE_STATEMENT", None, "identifier", (self.line, self.line_index))

            case "end":
                self.create_token("END_STATEMENT", None, "identifier", (self.line, self.line_index))

            case "while":
                self.create_token("WHILE_STATEMENT", None, "identifier", (self.line, self.line_index))

            case "do":
                self.create_token("DO_STATEMENT", None, "identifier", (self.line, self.line_index))

            case "__input__":
                self.create_token("INPUT_STATEMENT", None, "identifier", (self.line, self.line_index))

            case "join":
                self.create_token("OP_JOIN", None, "identifier", (self.line, self.line_index))

            case "exit":
                self.create_token("OP_EXIT", None, "identifier", (self.line, self.line_index))

            case "drop":
                self.create_token("OP_DROP", None, "identifier", (self.line, self.line_index))

            case "dropall":
                self.create_token("OP_DROPALL", None, "identifier", (self.line, self.line_index))

            case "exec":
                self.create_token("OP_EXEC", None, "identifier", (self.line, self.line_index))

            case "swap":
                self.create_token("OP_SWAP", None, "identifier", (self.line, self.line_index))

            case "slice":
                self.create_token("OP_SLICE", None, "identifier", (self.line, self.line_index))

            case "print":
                self.create_token("OP_OUT", None, "identifier", (self.line, self.line_index))

            case "println":
                self.create_token("OP_OUTLN", None, "identifier", (self.line, self.line_index))

            case "for":
                self.create_token("FOR_STATEMENT", None, "identifier", (self.line, self.line_index))

            case "true":
                self.create_token("OP_PUSH", 1, "int", (self.line, self.line_index))

            case "false":
                self.create_token("OP_PUSH", 0, "int", (self.line, self.line_index))

            case "dup":
                self.create_token("OP_DUP", None, "identifier", (self.line, self.line_index))

            case "include":
                self.include = True

            case "private":
                self.create_token("OP_PRIVATE", None, "identifier", (self.line, self.line_index))

            case "proc":
                self.create_token("PROC_STATEMENT", None, "identifier", (self.line, self.line_index)) # {"type" : "PROC", "value" : {"name" : "hello", "contents" : [<iporth-code>]}, "struct" : "proc", "pos" : (1, 1), "file" : "std.porth"}

            case "in":
                self.create_token("IN_STATEMENT", None, "identifier", (self.line, self.line_index))

            case _:
                self.create_token("OP_PUSH", self.text, "identifier", (self.line, self.line_index))


    def is_alphanumeric(self, character):
        return self.is_alpha(character) or self.is_digit(character)

    def is_alpha(self, character):
        return (character >= "a" and character <= "z") or (character >= "A" and character <= "Z") or character == "_"

    def is_digit(self, character):
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
                    if not exists(f"{self.return_value[:-6]}.iporth"):
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
        while len(self.included_contents) >= self.index + 1: # second pass for creating proc, probably gonna make the interpreter slower but oh well
            instruction = self.included_contents[self.index]
            if self.go_to_end:
                self.proc_contents.append(instruction)
                if instruction["type"] != "END_STATEMENT":
                    if instruction["type"] == "IF_STATEMENT":
                        self.end_tolerance += 1

                else:
                    if self.end_tolerance == 0:
                        self.go_to_end = False
                        self.completed_proc = True
                    else:
                        self.end_tolerance -= 1
                    continue

            if instruction["type"] == "PROC_STATEMENT":
                self.end_tolerance: int = 0
                self.proc_name: str = self.included_contents[self.index + 1]["value"]
                self.proc_contents: list[dict] = []

                if self.included_contents[self.index + 2]["type"] == "IN_STATEMENT":
                    self.index += 3
                    self.go_to_end: bool = True
        
            if self.completed_proc:
                self.proc = {"type" : "PROC", "value" : {"name" : self.proc_name, "contents" : self.proc_contents}, "struct" : "identifier", "pos" : instruction["pos"], "file" : self.filename}
                self.output.append(self.proc)
                self.completed_proc = False
            else:
                self.output.append(instruction)
            
            self.index += 1


        return self.output
