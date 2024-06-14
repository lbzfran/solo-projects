
from enum import Enum

class TokenType(Enum):
    # 0: EOF
    NONE = 0
    # 1-16 KEYWORDS (MUST BE IN CAPS)
    PUSH = 1
    POP = 2
    ADD = 3
    SUB = 4
    MUL = 5
    DIV = 6
    # 10-19
    NUMBER = 17
    START_IDENTIFIER = 18
    END_IDENTIFIER = 19

    # 99 EOF
    EOF = 99

# not currently important, but will need when i transform from oop to procedural.
def iota(reset=False):
    global iota_counter
    if reset:
        iota_counter = 0
    result = iota_counter
    iota_counter += 1
    return result

class Token:
    def __init__(self, token_type: TokenType, value: str | int | None):
        self.token_type = token_type
        self.value = value

    def __str__(self):
        return f"{self.token_type.name}: {self.value}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.token_type == other.token.type

class Lexer:
    def __init__(self, text: str):
        self.text = open(text, 'r').read().split()
        self.pos = 0
        self.current_token = None
        self.current_word = self.text[self.pos]

    def get(self):
        # find the current token.
        return self.current_token

    def peek(self):
        # check the next character in text.
        if self.pos + 1 < len(self.text):
            return self.text[self.pos + 1]
        return

    def advance(self):
        # move to the next character in text.
        self.pos += 1
        if self.pos < len(self.text):
            self.current_word = self.text[self.pos]
        else:
            self.current_word = None

    def get_token(self):
        while self.current_word is not None:
            if self.current_word.endswith(":"):
                return Token(TokenType.START_IDENTIFIER, self.current_word[:-1])
            elif self.current_word == ";":
                return Token(TokenType.END_IDENTIFIER, ";")
            elif self.current_word == "PUSH":
                return Token(TokenType.PUSH, self.current_word)
            elif self.current_word == "POP":
                return Token(TokenType.POP, self.current_word)
            elif self.current_word == "ADD":
                return Token(TokenType.ADD, self.current_word)
            elif self.current_word == "SUB":
                return Token(TokenType.SUB, self.current_word)
            elif self.current_word == "MUL":
                return Token(TokenType.MUL, self.current_word)
            elif self.current_word == "DIV":
                return Token(TokenType.DIV, self.current_word)
            elif self.current_word.isdigit():
                return Token(TokenType.NUMBER, int(self.current_word))
            raise Exception("Invalid word.")

        return Token(TokenType.EOF, None)


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = Token(TokenType.NONE, None)
        self.peek_token = Token(TokenType.NONE, None)

        self.stack = []

        # initializes current and peek tokens.
        self.advance()
        self.advance()

    def advance(self):
        self.current_token = self.peek_token
        self.peek_token = self.lexer.get_token()

        self.lexer.advance()

    def check_token(self, token_type: TokenType):
        # checks if current token is of a given token type.
        return self.current_token.token_type == token_type

    def statement(self):

        if self.check_token(TokenType.START_IDENTIFIER):
            self.advance()

        elif self.check_token(TokenType.END_IDENTIFIER):
            self.advance()

        elif self.check_token(TokenType.PUSH):
            print("PUSHING ", end="")
            self.advance()

            if self.check_token(TokenType.NUMBER):
                # push number to stack.
                print(f"{self.current_token.value}")
                self.stack.append(self.current_token.value)
                self.advance()
            else:
                raise Exception("Expected NUM after PUSH.")

        elif self.check_token(TokenType.POP):
            self.advance()

            if len(self.stack) == 0:
                raise Exception("Stack is empty.")

            print("POPPING", self.stack.pop())

        elif self.check_token(TokenType.ADD):
            self.advance()

            if len(self.stack) == 1:
                # if only one element in stack, op equivalent to adding to 0.
                pass
            elif len(self.stack) == 0:
                raise Exception("Not enough elements in stack.")

            elem1 = self.stack.pop()
            elem2 = self.stack.pop()
            self.stack.append(elem1 + elem2)

            print(f"ADDING {elem1} and {elem2}")

        else:
            print(f"Statement not recognized: {self.current_token.value}")
            self.advance()





    def program(self):
        while not self.check_token(TokenType.EOF):
            self.statement()

if __name__ == '__main__':
    sun = Parser(Lexer("tomson.skt"))

    sun.program()
