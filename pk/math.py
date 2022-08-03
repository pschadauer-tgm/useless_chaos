from pk import *

PUSH_INSTR = 0x0.to_bytes(4, 'little')
ADD_INSTR = 0x1.to_bytes(4, 'little')
MUL_INSTR = 0x2.to_bytes(4, 'little')
NO_CONTENT = bytes(4)

class Add:
    def __init__(self, l, r):
        self.l = l
        self.r = r
    def __repr__(self):
        return f"(+ {self.l} {self.r})"
    def bytecode(self):
        return self.l.bytecode() + self.r.bytecode() + (ADD_INSTR + NO_CONTENT)
    def calc(self):
        return self.l.calc() + self.r.calc()

class Mul:
    def __init__(self, l, r):
        self.l = l
        self.r = r
    def __repr__(self):
        return f"(* {self.l} {self.r})"
    def bytecode(self):
        return self.l.bytecode() + self.r.bytecode() + (MUL_INSTR + NO_CONTENT)
    def calc(self):
        return self.l.calc() * self.r.calc()

class Num:
    def __init__(self, v):
        self.v = v
    def __repr__(self):
        return str(self.v)
    def bytecode(self):
        return PUSH_INSTR + self.v.to_bytes(4, 'little')
    def calc(self):
        return self.v

numP = SeqP(IntP, f=(lambda x: Num(x[0])))

subP = OneInP()
subP.parser = [
        SeqP(
            numP,
            StrP("*"),
            subP,
            f=(lambda x: Mul(x[0], x[2]))
            ),
        numP
    ]

mathP = OneInP()
mathP.parser = [
        SeqP(
            subP,
            StrP("+"),
            mathP,
            f=(lambda x: Add(x[0], x[2]))
            ),
        subP
    ]

def main():
    inp = input("Enter math expression: ")
    err, p = mathP.parse(inp)
    with open("bytecode", "wb") as file:
        file.write(p.bytecode())

if __name__ == "__main__":
    main()
