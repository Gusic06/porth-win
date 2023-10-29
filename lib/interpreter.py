
class Interpreter:

    def __init__(self) -> None:
        self.stack: list = []
        self.index: int = 0

        self.go_to_end: bool = False
        self.end_tolerance: int = 0
        self.repeat = 0
        self.file = ""


    def interpret(self, instructions: list[dict], show_stack: bool = False) -> None:
        for instruction in instructions:

            if show_stack:
                print(f"{self.index} : {self.stack}")

            if self.go_to_end is True: # for a nested if loop

                if instruction["type"] == "ELSE_STATEMENT" and self.end_tolerance == 0:
                    self.go_to_end = False

                if instruction["type"] != "END_STATEMENT":
                    if instruction["type"] == "IF_STATEMENT":
                        self.end_tolerance += 1
                    continue

                else:
                    if self.end_tolerance == 0:
                        self.go_to_end = False
                    else:
                        self.end_tolerance -= 1
                    continue

            if instruction["type"] == "FOR_STATEMENT":
                self.jump = self.index + 1
                self.item1 = self.stack.pop()
                self.item2 = self.stack.pop()
                self.repeat = self.item1 - self.item2
                print(self.repeat)

            if instruction["type"] == "IF_STATEMENT":
                self.comparison = self.stack.pop()
                self.ignore_else = True
                if self.comparison == 1:
                    continue
                else:
                    self.go_to_end = True

            if instruction["type"] == "ELSE_STATEMENT":
                self.go_to_end = True
            
            if instruction["type"] == "END_STATEMENT":
                self.go_to_end = False
                #if self.repeat != 0:
                #    print("guh")

            if instruction["type"] == "OP_DROP":
                self.stack.pop()

            if instruction["type"] == "OP_DROPALL":
                self.stack = []

            if instruction["type"] == "OP_SWAP":
                self.item1 = self.stack.pop()
                self.item2 = self.stack.pop()
                self.stack.append(self.item2)
                self.stack.append(self.item1)

            if instruction["type"] == "OP_PUSH": 
                self.stack.append(instruction["value"])

            if instruction["type"] == "OP_OUT":  
                print(self.stack.pop())

            if instruction["type"] == "OP_DIV":
                self.item1 = self.stack.pop()
                self.item2 = self.stack.pop()
                self.stack.append(round(self.item2 / self.item1))

            if instruction["type"] == "OP_MULTI":
                self.item1 = self.stack.pop()
                self.item2 = self.stack.pop()
                self.stack.append(self.item1 * self.item2)

            if instruction["type"] == "OP_EQUALITY":
                self.item1 = self.stack.pop()
                self.item2 = self.stack.pop()
                self.stack.append(int(self.item1 == self.item2))

            if instruction["type"] == "OP_INEQUALITY":
                self.item1 = self.stack.pop()
                self.item2 = self.stack.pop()
                self.stack.append(int(self.item2 != self.item1))

            if instruction["type"] == "OP_GT":
                self.item1 = self.stack.pop()
                self.item2 = self.stack.pop()
                self.stack.append(int(self.item2 > self.item1))

            if instruction["type"] == "OP_INCLUDE":
                print(instructions[self.index + 1]["value"])
                self.file = instructions[self.index + 1]["value"]

            if instruction["type"] == "OP_LT":
                self.item1 = self.stack.pop()
                self.item2 = self.stack.pop()
                self.stack.append(int(self.item2 < self.item1))

            if instruction["type"] == "OP_LTEQUALITY":
                self.item1 = self.stack.pop()
                self.item2 = self.stack.pop()
                self.stack.append(int(self.item2 <= self.item1))

            if instruction["type"] == "OP_GTEQUALITY":
                self.item1 = self.stack.pop()
                self.item2 = self.stack.pop()
                self.stack.append(int(self.item2 >= self.item1))

            if instruction["type"] == "OP_ADD":
                self.item1 = self.stack.pop()
                self.item2 = self.stack.pop()
                self.stack.append(self.item1 + self.item2)

            if instruction["type"] == "OP_SUB":
                self.item1 = self.stack.pop()
                self.item2 = self.stack.pop()
                self.stack.append(self.item2 - self.item1)
            
            self.index += 1

        if len(self.stack) != 0:
            s: str = "s" if len(self.stack) > 1 or self.stack == 0 else ""
            were: str = "were" if len(self.stack) > 1 or self.stack == 0 else "was"

            print(f"Warning: [ {len(self.stack)} ] item{s} {were} left unused on the stack.")