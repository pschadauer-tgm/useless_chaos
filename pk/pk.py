from typing import Any, Tuple, Callable
# str -> Tuple[str, Any] | None

class Parser:
    def parse(self, str) -> Tuple[str, Any] | None:
        pass
    def map(self, func : Callable):
        pass

class CharP(Parser):
    char : str
    f : Callable
    def __init__(self, char : str, f = None):
        self.char = char
        self.f = f
    def parse(self, str) -> Tuple[str, Any] | None:
        if len(str) == 0:
            return None
        if str[0] == self.char:
            if self.f == None:
                return (str[1:], self.char)
            else:
                return (str[1:], self.f(self.char))
        return None

class ExceptCharP(Parser):
    xchar : list[str]
    f : Callable
    def __init__(self, xchar : str, f = None):
        self.xchar = xchar
        self.f = f
    def parse(self, str) -> Tuple[str, Any] | None:
        if len(str) == 0:
            return None
        if str[0] not in self.xchar:
            if self.f == None:
                return (str[1:], str[0])
            else:
                return (str[1:], self.f(str[0]))
        return None

class SeqP(Parser):
    parser : list[Parser]
    f : Callable
    def __init__(self, *parser, f = None):
        self.parser = parser
        self.f = f
    def parse(self, str) -> Tuple[str, Any] | None:
        ret = []
        for p in self.parser:
            if (res := p.parse(str)) != None:
                str = res[0]
                ret.append(res[1])
            else:
                return None
        if self.f == None:
            return (str, ret)
        else:
            return (str, self.f(ret))

class MultiP(Parser):
    parser : Parser
    f : Callable
    def __init__(self, parser, f = None):
        self.parser = parser
        self.f = f
    def parse(self, str) -> Tuple[str, Any] | None:
        ret = []
        while (res := self.parser.parse(str)) != None:
            str = res[0]
            ret.append(res[1])
        if self.f == None:
            return (str, ret)
        else:
            if (res := self.f(ret)) == None:
                return None
            return (str, res)


class OneInP(Parser):
    parser : list[Parser]
    def __init__(self, *parser):
        self.parser = parser
    def parse(self, str) -> Tuple[str, Any] | None:
        for p in self.parser:
            if (res := p.parse(str)) != None:
                return res
        return None

class MaybeP(Parser):
    parser : Parser
    def __init__(self, parser):
        self.parser = parser
    def parse(self, str) -> Tuple[str, Any] | None:
        res = self.parser.parse(str)
        if res == None:
            return (str, None)
        return res

def StrP(str):
    parser = []
    for c in str:
        parser.append(CharP(c))
    return SeqP(*parser, f = (lambda x: "".join(x)))

DigitP = OneInP(
        CharP("0"),
        CharP("1"),
        CharP("2"),
        CharP("3"),
        CharP("4"),
        CharP("5"),
        CharP("6"),
        CharP("7"),
        CharP("8"),
        CharP("9"))

def arr_to_int(x):
    try:
        return int("".join(x))
    except:
        return None

IntP = MultiP(DigitP, f = arr_to_int)

NewLineP = OneInP(
        CharP("\n"),
        StrP("\r\n"))

EmptyP = MultiP(OneInP(
        CharP(" "),
        CharP("\t"),
        NewLineP))
