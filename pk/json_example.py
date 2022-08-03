from pk import *
from typing import Callable

json_string = SeqP(
        CharP('"'),
        MultiP(ExceptCharP(['"'])),
        CharP('"'),
        f = (lambda x: "".join(x[1])))

json_open = CharP("{")
json_close = CharP("}")

arr_open = CharP("[")
arr_close = CharP("]")

def css(parser : Parser, f : Callable) -> Parser:
    return SeqP(
        MaybeP(
            MultiP(
                SeqP(
                    EmptyP,
                    parser,
                    EmptyP,
                    CharP(","),
                    f = (lambda x: x[1])
                )
            )
        ),
        EmptyP,
        MaybeP(parser),
        f = f
    )

# Parser is ok, but it lacks null
json_parser = OneInP()

json_attribute = SeqP(
    json_string,
    EmptyP,
    CharP(":"),
    EmptyP,
    json_parser,
    f = (lambda x: (x[0], x[4]))
)

json_parser.parser = [
    # Object
    SeqP(
        json_open,
        css(json_attribute, (lambda x: {key:value for key, value in
                (x[0] or []) + ([x[2]] if x[2] != None else [])})),
        json_close,
        f = (lambda x: x[1])
    ),
    # Array
    SeqP(
        arr_open,
        css(json_parser, (lambda x: (x[0] or []) + [x[2] or []])),
        arr_close,
        f = (lambda x: x[1])
    ),
    # String
    json_string,
    # Integer
    IntP
]

def parse(str) -> Any:
    return json_parser.parse(str)[1]

# gOoD UnIt tEsTs
assert parse('12') == 12
assert parse('["Hello, World", 12, [2, 3]]') == ["Hello, World", 12, [2, 3]]
assert parse('{"a" : [420, 69], "b" : {"a" : 187}}') == {"a" : [420, 69], "b" : {"a" : 187}}
