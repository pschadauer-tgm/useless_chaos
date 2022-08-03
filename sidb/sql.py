from db import DB, Datatype
from enum import Enum

class And():
    def __init__(self, a, b):
        self.p_a = a
        self.p_b = b
    def eval(self, para):
        return self.p_a.eval(para) and self.p_b.eval(para)
    def __repr__(self):
        return f"(and {self.p_a} {self.p_b})"
class Or():
    def __init__(self, a, b):
        self.p_a = a
        self.p_b = b
    def eval(self, para):
        return self.p_a.eval(para) or self.p_b.eval(para)
    def __repr__(self):
        return f"(or {self.p_a} {self.p_b})"

class Bigger():
    def __init__(self, a, b):
        self.p_a = a
        self.p_b = b
    def eval(self, para):
        return self.p_a.eval(para) > self.p_b.eval(para)
    def __repr__(self):
        return f"(> {self.p_a} {self.p_b})"

class Smaller():
    def __init__(self, a, b):
        self.p_a = a
        self.p_b = b
    def eval(self, para):
        return self.p_a.eval(para) < self.p_b.eval(para)
    def __repr__(self):
        return f"(< {self.p_a} {self.p_b})"

class Eq():
    def __init__(self, a, b):
        self.p_a = a
        self.p_b = b
    def eval(self, para):
        return self.p_a.eval(para) == self.p_b.eval(para)
    def __repr__(self):
        return f"(== {self.p_a} {self.p_b})"

class Taker():
    def __init__(self, a):
        self.to_take = a
    def eval(self, para):
        return para[self.to_take]
    def __repr__(self):
        return f"(take {self.to_take})"

class Value():
    def __init__(self, a):
        self.value = a
    def eval(self, para):
        return self.value
    def __repr__(self):
        return f"({self.value})"

def combine(parent, p_arr):
    while (value := next(parent, None)) != None:
        yield tuple([p.eval(value) for p in p_arr]) 

def take(parent, to_take : list[int]):
    while (value := next(parent, None)) != None:
        to_ret = []
        for t in to_take:
            to_ret.append(value[t])
        yield tuple(to_ret)

def filter(parent, filt):
    while (value := next(parent, None)) != None:
        if filt.eval(value):
            yield value

def limit(parent, maximum):
    counter = 0
    while (value := next(parent, None)) != None:
        yield value
        counter += 1
        if counter == maximum:
            break

# bad insertion sort
def order(parent, to_order : int, asc = True):
    buf = []
    while (value := next(parent, None)) != None:
        i = 0
        for indx, x in enumerate(buf):
            if value[to_order] < x[to_order]:
                break
            i = indx + 1
        buf.insert(i, value)
    for x in buf:
        yield x

class TokenType(Enum):
    SELECT = "SELECT"
    FROM = "FROM"
    WHERE = "WHERE"
    CREATE = "CREATE"
    TABLE = "TABLE"
    LIMIT = "LIMIT"
    INSERT = "INSERT"
    INTO = "INTO"
    VALUES = "VALUES"
    ORDER = "ORDER"
    BY = "BY"
    DESC = "DESC"

    STAR = "*"
    COMMA = ","

    AND = "AND"
    OR = "OR"
    GREATER = ">"
    SMALLER = "<"
    EQ = "="

    NUMBER = "NUM"
    IDENTIFIER = "IDENT"
    
    STR_START = "'"
    L_PAREN = "("
    R_PAREN = ")"

    TRUE = "TRUE"
    FALSE = "FALSE"

    BOOL = "BOOLEAN"
    STRING = "STRING"
    INT = "INT"
    
    def important(self):
        return self in [TokenType.SELECT, TokenType.FROM, TokenType.WHERE, TokenType.LIMIT, TokenType.ORDER]
    def datatype(self):
        if self == TokenType.BOOL:
            return Datatype.BOOL
        if self == TokenType.STRING:
            return Datatype.STR
        if self == TokenType.INT:
            return Datatype.INT
        return None
    def infix(self):
        if self in [TokenType.GREATER, TokenType.SMALLER, TokenType.EQ]:
            return (3, 4)
        elif self in [TokenType.AND, TokenType.OR]:
            return (1, 2)
    def ast_constr(self, lhs, rhs):
        if self == TokenType.GREATER:
            return Bigger(lhs, rhs)
        if self == TokenType.SMALLER:
            return Smaller(lhs, rhs)
        if self == TokenType.AND:
            return And(lhs, rhs)
        if self == TokenType.OR:
            return Or(lhs, rhs)
        if self == TokenType.EQ:
            return Eq(lhs, rhs)
        return None

class Token():
    typ : TokenType
    def __init__(self, typ : TokenType, value = None):
        self.typ = typ
        self.value = value
    def __repr__(self):
        return str(self.typ) if self.value == None else str(self.typ) + " \"" + str(self.value) + "\""

def scan(inp : str) -> list[Token]:
    inp.replace(">", " > ")
    inp = inp.replace("<", " < ")
    inp = inp.replace("=", " = ")
    inp = inp.replace("'A", "' A")
    inp = inp.replace("'O", "' O")
    inp = inp.replace("(", " ( ")
    inp = inp.replace(")", " ) ")
    inp = inp.replace(",", " , ")
    inp = inp.replace("\t", " ")
    inp = inp.replace("\n", " ")
    tokens : list[Token] = []
    for word in inp.split(" "):
        if word in (" ", "  ", ""):
            continue
        try:
            tokens.append(Token(TokenType(word.upper())))
        except ValueError:
            try:
                tokens.append(Token(TokenType.NUMBER, int(word)))
            except ValueError:
                tokens.append(Token(TokenType.IDENTIFIER, word))
    return tokens

def section(tokens : list[Token]):
    current = None
    to_ret = {}
    for token in tokens:
        if token.typ.important():
            current = token.typ
            to_ret[current] = []
        else:
            to_ret[current].append(token)
    return to_ret

def plan(tokens : list[Token], db : DB):
    # create table
    if tokens[0].typ == TokenType.CREATE and tokens[1].typ == TokenType.TABLE:
        name = tokens[2].value
        if name == None:
            raise Exception("Invalid CRATE TABLE command.")
        types = []
        if tokens[3].typ != TokenType.L_PAREN:
            raise Exception("Expected \"(\" got something else.")
        last_token = tokens[3]
        for token in tokens[4:]:
            if (dt := token.typ.datatype()) != None:
                if last_token.typ != TokenType.IDENTIFIER:
                        raise Exception(f"Expected Token name. Got {last_token.typ}.")
                types.append((last_token.value, dt))
            last_token = token
        if len(types) == 0:
            raise Exception("Got no datatypes")
        db.add_table(name, types)
        return
    # insert into
    if tokens[0].typ == TokenType.INSERT and tokens[1].typ == TokenType.INTO:
        table = tokens[2].value
        if table not in db._schemas:
            raise Exception("Table does not exist.")
        if tokens[3].typ != TokenType.VALUES:
            raise Exception("Expected keyword VALUES.")
        to_insert = []
        for token in tokens[5:-1]:
            if token.typ != TokenType.COMMA:
                if token.typ == TokenType.TRUE:
                    to_insert.append(True)
                elif token.typ == TokenType.FALSE:
                    to_insert.append(False)
                else:
                    to_insert.append(token.value)
        db.insert(table, to_insert)
        return
    # plans a query
    if tokens[0].typ != TokenType.SELECT:
        raise Exception("Invalid Query")
    tokens = section(tokens)
    if TokenType.FROM not in tokens:
        raise Exception("No FROM Token found.")
    if (table := tokens[TokenType.FROM][0].value) not in db._schemas:
        raise Exception(f"This table does not exist.")
    query = db.seq_reader(table)
    if TokenType.WHERE in tokens:
        query = filter(query, parse(Lexer(tokens[TokenType.WHERE]), db._schemas[table][0]))
    if TokenType.ORDER in tokens:
        if tokens[TokenType.ORDER][0].typ != TokenType.BY:
            raise Exception("Expected BY keyword")
        to_order = db._schemas[table][0].index(tokens[TokenType.ORDER][1].value)
        query = order(query, to_order)
        # TODO: desc asc
    if TokenType.LIMIT in tokens:
        if (token := tokens[TokenType.LIMIT][0]).typ == TokenType.NUMBER:
            query = limit(query, token.value)
    if tokens[TokenType.SELECT][0].typ != TokenType.STAR:
        paras = []
        current = []
        for token in tokens[TokenType.SELECT]:
            if token.typ == TokenType.COMMA:
                paras.append(current)
                current = []
            else:
                current.append(token)
        paras.append(current)
        query = combine(query, [parse(Lexer(p), db._schemas[table][0]) for p in paras])
    return query

class Lexer():
    def __init__(self, tokens):
        self.tokens = tokens
    def next(self):
        token = self.tokens[0]
        self.tokens = self.tokens[1:]
        return token
    def peek(self):
        if len(self.tokens) == 0:
            return None
        return self.tokens[0]

def parse(tokens : Lexer, mapper : list[int], min_bp = 0):
    lhs = None
    if (lhs := tokens.next()).typ not in [TokenType.IDENTIFIER, TokenType.NUMBER, TokenType.TRUE, TokenType.FALSE]:
        raise Exception("Dafuq")
    if lhs.typ == TokenType.IDENTIFIER:
        try:
            lhs = Taker(mapper.index(lhs.value))
        except:
            lhs = Value(lhs.value)
    else:
        lhs = Value(lhs.value)
    while True:
        if tokens.peek() == None:
            break
        if (infix := (op := tokens.peek().typ).infix()) == None:
            raise Exception("Expected operator")
        if infix[0] < min_bp:
            break
        tokens.next()
        rhs = parse(tokens, mapper, infix[1])
        lhs = op.ast_constr(lhs, rhs)
    return lhs


def repl(filename : str):
    db = DB(filename)
    while True:
        inp = " "
        while inp[-1] != ";":
            inp += "\n" + input("sidb > ")
        if ".tables;" in inp:
            print(".... ", " | ".join(db._schemas.keys()))
            continue
        if ".desc" in inp:
            inp = inp.replace(";", " ;");
            table = inp.split(" ")[-2];
            print(".... ", " | ".join([str(x[0]) + " (" + str(x[1].name) + ")" for  x in zip(db._schemas[table][0], db._schemas[table][1])]))
            continue
        if ".q;" in inp:
            break
        out = plan(scan(inp[:-1]), db)
        if out != None:
            for x in out:
                out = ".... "
                for column in x:
                    out += "|" + str(column).rjust(12)
                print(out + "|")

if __name__ == "__main__":
    repl("hello.sidb")
