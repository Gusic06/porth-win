
class Parser:

    def __init__(self) -> None:
        ...

    def isdigit(self, text: str) -> bool:
        return text in "0123456789" and text not in "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"

    def parse_word_into_op(self, word: str) -> dict:
        self.op: dict = {}
        
        if word == "==": self.op.update({"type" : "OP_EQUALITY", "value" : None})
        elif word == "!=": self.op.update({"type" : "OP_INEQUALITY", "value" : None})
        elif word == "<=": self.op.update({"type" : "OP_LTEQUALITY", "value" : None})
        elif word == ">=": self.op.update({"type" : "OP_GTEQUALITY", "value" : None})
        elif word == "<": self.op.update({"type" : "OP_LT", "value" : None})
        elif word == ">": self.op.update({"type" : "OP_GT", "value" : None})
        elif word == "+": self.op.update({"type" : "OP_ADD", "value" : None})
        elif word == "-": self.op.update({"type" : "OP_SUB", "value" : None})
        elif word == "*": self.op.update({"type" : "OP_MULTI", "value" : None})
        elif word == "/": self.op.update({"type" : "OP_DIV", "value" : None})
        elif word == "print": self.op.update({"type" : "OP_OUT", "value" : None})
        elif word == "drop": self.op.update({"type" : "OP_DROP", "value" : None})
        elif word == "dropall": self.op.update({"type" : "OP_DROPALL", "value" : None})
        elif word == "include": self.op.update({"type" : "OP_INCLUDE", "value" : None})
        elif word == "swap": self.op.update({"type" : "OP_SWAP", "value" : None})
        elif word == "for": self.op.update({"type" : "FOR_STATEMENT", "value": None})
        elif word == "if": self.op.update({"type" : "IF_STATEMENT", "value" : None})
        elif word == "else": self.op.update({"type" : "ELSE_STATEMENT", "value" : None})
        elif word == "do": self.op.update({"type" : "DO_STATEMENT", "value" : None})
        elif word == "end": self.op.update({"type" : "END_STATEMENT", "value" : None})
        else:
            try:
                self.op.update({"type" : "OP_PUSH", "value" : int(word)})
            except Exception:
                pass
        if self.op == {}:
            self.op = {"type" : None, "value" : None}
        return self.op

    def clean_output(self, output: list[dict]) -> list[dict] | list:
        self.output_buffer: list[dict] = []
        for item in output:
            if item == None:
                continue
            else:
                self.output_buffer.append(item)
        return self.output_buffer