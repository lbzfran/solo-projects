from dataclasses import dataclass
from enum import Enum
from os import access, R_OK
from os.path import isfile

# not currently important, but will need when i transform from oop to procedural.
def iota(reset=False):
    global iota_counter
    if reset:
        iota_counter = 0
    result = iota_counter
    iota_counter += 1
    return result


class TokenType(Enum):
    NONE = iota(True)

    # stack manipulation
    PUSH = iota() # a -- a ; implicit if var is defined, or constant is given.
    POP = iota()  # a --
    DUP = iota()  # a -- a a
    SWAP = iota() # a b -- b a
    OVER = iota() # a b -- a b a
    ROT = iota()  # a b c -- b c a
    EXCH = iota() # a b -- b a

    # braces
    LBRACE = iota() # {
    RBRACE = iota() # }
    LPAREN = iota() # (
    RPAREN = iota() # )
    LBRACK = iota() # [
    RBRACK = iota() # ]

    # operators
    # unary operators
    NEG = iota() # [-]a -- [-a]

    # binary operators
    ADD = iota() # a b [+] = b + a
    SUB = iota() # a b [-] = b - a
    MUL = iota() # a b [*] = b * a
    DIV = iota() # a b [/ or //] = b / a
    MOD = iota() # a b [%] = b % a

    NOT = iota() # z [!] = not Z
    AND = iota() # y z [&] = y and z
    OR = iota()  # y z [|] = y or z

    # types
    INT = iota() # [0-9] # dynamically typed from numbers.
    FLOAT = iota() # [0-9].[0-9]
    IDENTIFIER = iota() # [a-zA-Z] # variable or function name.
    COMMENT = iota() # //

    RETURN = iota() # return

    EOF = iota()

@dataclass(repr=False)
class Token:
    type: TokenType
    val: str

    def __str__(self):
        return f"Token({self.type}, {self.val})"

# TODO: fix lexer so it can read char by char, and complete the tokenization process.
# (read keywords like PUSH, POP, etc. properly)
class Lexer:
    def __init__(self, src: str):
        assert isfile(src) and access(src, R_OK), f"File {src} does not exist/is not readable."
        with open(src, 'r') as file:
            self.src = file.read() + '\n'
        self.pos = -1
        self.current_char = ''
        self.advance()

    def peek(self):
        # check the next character in src.
        if self.pos + 1 < len(self.src):
            return self.src[self.pos + 1]
        else:
            return '\0'

    def advance(self):
        # move to the next character in src.
        self.pos += 1
        if self.pos < len(self.src):
            self.current_char = self.src[self.pos]
        else:
            self.current_char = '\0'

    def word(self):
        # traverse src for a word bounded together.
        assert self.current_char.isalpha(), "Invalid word format."
        start_pos = self.pos
        while self.peek().isalpha():
            self.advance()
        self.advance()

        return self.src[start_pos: self.pos]

    def number(self):
        # traverse src for a number bounded together.
        assert self.current_char.isdigit(), "Invalid number format."
        start_pos = self.pos
        while self.peek().isdigit():
            self.advance()
            if self.peek() == '.':
                self.advance()
                if not self.peek().isdigit():
                    raise ValueError("Invalid number format.")
                while self.peek().isdigit():
                    self.advance()
                return float(self.src[start_pos: self.pos + 1])

        self.advance()
        return int(self.src[start_pos: self.pos + 1])

    def skip_whitespace(self):
        # skip all whitespace characters.
        while self.current_char in [' ', '\n', '\t']:
            self.advance()

    def skip_comment(self):
        # c-style commenting.
        if self.current_char == '/' and self.peek() == '/':
            while self.current_char != '\n':
                self.advance()

    def get_token(self):

        ## tokenizer not working properly.
        while self.current_char != '\0':
            self.skip_whitespace()
            self.skip_comment()
            if self.current_char.isdigit():
                num = self.number()
                if isinstance(num, int):
                    return Token(TokenType.INT, num)
                return Token(TokenType.FLOAT, num)


                return Token(TokenType.NUMBER, self.number())
            elif self.current_char.isalpha():
                # check if keyword or operator, assume identifier by default.
                word = self.word()
                token_type = TokenType.IDENTIFIER

                match (word.upper()):
                    case "PUSH":
                        token_type = TokenType.PUSH
                    case "POP":
                        token_type = TokenType.POP
                    case "DUP":
                        token_type = TokenType.DUP
                    case "SWAP":
                        token_type = TokenType.SWAP
                    case "OVER":
                        token_type = TokenType.OVER
                    case "ROT":
                        token_type = TokenType.ROT
                    case "EXCH":
                        token_type = TokenType.EXCH
                    case "ADD":
                        token_type = TokenType.ADD
                    case "SUB":
                        token_type = TokenType.SUB
                    case "MUL":
                        token_type = TokenType.MUL
                    case "DIV":
                        token_type = TokenType.DIV

                # if word did not match any keyword, return identifier.
                return Token(token_type, word)

            else:
                # symbol handling. check if symbol is valid.
                if self.current_char in ['(', ')', '{', '}', '&', '|']:
                    match (self.current_char):
                        case '(':
                            return Token(TokenType.LPAREN, self.current_char)
                        case ')':
                            return Token(TokenType.RPAREN, self.current_char)
                        case '{':
                            return Token(TokenType.LBRACE, self.current_char)
                        case '}':
                            return Token(TokenType.RBRACE, self.current_char)
                        case '[':
                            return Token(TokenType.LBRACK, self.current_char)
                        case ']':
                            return Token(TokenType.RBRACK, self.current_char)
                        case '&':
                            return Token(TokenType.AND, self.current_char)
                        case '|':
                            return Token(TokenType.OR, self.current_char)
                elif self.current_char == '-' and self.peek().isdigit():
                    self.advance()
                    return Token(TokenType.NEG, "-")
                    #return Token(TokenType.NUMBER, -1 * self.number())

        return Token(TokenType.EOF, '')


if __name__ == '__main__':
    sun = Lexer("tomson.skt")

    while sun.current_char != '\0':
        print(sun.get_token())
