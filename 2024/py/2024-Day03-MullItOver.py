from typing import Generator, List, Tuple

class Token:
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__class__.__name__

class MulToken(Token):
    pass

class MiscToken(Token):
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return self.__class__.__name__ + f"({self.value})"

class NumberToken(Token):
    def __init__(self, value: int):
        self.value = value

    def __str__(self):
        return self.__class__.__name__ + f"({self.value})"

class CommaToken(Token):
    pass

class OpenToken(Token):
    pass

class CloseToken(Token):
    pass

class DoToken(Token):
    pass

class DontToken(Token):
    pass

class EOFToken(Token):
    pass


def tokenizer(filename: str):
    token = ""
    digit = ""
    def flush():
        yield from flush_token()
        yield from flush_digit()
    def flush_token():
        nonlocal token
        if token != "":
            if len(token)>=3 and token[-3:]=="mul":
                if (len(token)>3):
                    yield MiscToken(token[:-3])
                yield MulToken()
            elif len(token)>=5 and token[-5:]=="don't":
                if (len(token)>5):
                    yield MiscToken(token[:-5])
                yield DontToken()
            elif len(token)>=2 and token[-2:]=="do":
                if (len(token)>2):
                    yield MiscToken(token[:-2])
                yield DoToken()
            else:
                yield MiscToken(token)
            token = ""
    def flush_digit():
        nonlocal digit
        if digit != "":
            yield NumberToken(int(digit))
            digit = ""

    with open(filename) as f:
        while c := f.read(1):
            if c.isdigit():
                flush_token()
                digit += c
                continue
            elif c=="(":
                yield from flush()
                yield OpenToken()
            elif c==")":
                yield from flush()
                yield CloseToken()
            elif c==",":
                yield from flush()
                yield CommaToken()

            else:
                yield from flush_digit()
                token += c
    flush()
    yield EOFToken()

mulseq = [MulToken, OpenToken, NumberToken, CommaToken, NumberToken, CloseToken]
doseq = [DoToken, OpenToken, CloseToken]
dontseq = [DontToken, OpenToken, CloseToken]

found: List[Token | None] = [None, None , None, None, None, None]
idx = 0
result = 0
for token in tokenizer("2024-Day03.txt"):
    if isinstance(token, mulseq[idx]):
        found[idx] = token
        idx += 1
        if idx == len(mulseq):
            result += found[2].value * found[4].value
            idx = 0
    else:
        idx = 0

class MultiExpr:
    def __init__(self):
        self.result = 0
        self.track = True
        self.exprs = [
            (mulseq, self.multiply),
            (doseq, self.enable_tracking),
            (dontseq, self.disable_tracking)
        ]
        self.expridx = 0
        self.cmdidx = 0
        self.seq = list()

    def process(self, token: Token):
        if isinstance(token, self.exprs[self.expridx][0][self.cmdidx]):
            self.seq.append(token)
            self.cmdidx += 1
            if self.cmdidx == len(self.exprs[self.expridx][0]):
                self.exprs[self.expridx][1](self.seq)
                self.cmdidx = 0
                self.expridx = 0
                self.seq = []
        else:
            for i in range(len(self.exprs)):
                if isinstance(token, self.exprs[i][0][0]):
                    self.expridx = i
                    self.cmdidx = 1
                    self.seq = [token]
                    return
            self.expridx = 0
            self.cmdidx = 0
            self.seq = []

    
    def multiply(self, tokens: List[Token]):
        if self.track:
            self.result += tokens[2].value * tokens[4].value

    def enable_tracking(self, tokens: List[Token]):
        self.track = True

    def disable_tracking(self, tokens: List[Token]):
        self.track = False

print("Part 1:", result)
# Part 1: 174103751

p = MultiExpr()
for token in tokenizer("2024-Day03.txt"):
    p.process(token)
print("Part 2:", p.result)
# Part 2: 100411201

    
