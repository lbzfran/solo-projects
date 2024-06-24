from tokens import Token, TokenType
from lexer import Lexer

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer

        self.current_token = Token(TokenType.NONE, None)
        self.peek_token = Token(TokenType.NONE, None)

        self.symbols = {}

        self.stack = []

        # initializes current and peek tokens.
        self.advance()
        self.advance()

    def advance(self):
        self.current_token = self.peek_token
        self.peek_token = self.lexer.get_token()

    def check_token(self, token_type: TokenType):
        # checks if current token is of a given token type.
        return self.current_token.type == token_type

    def check_peek(self, token_type: TokenType):
        return self.peek_token.type == token_type

    def match(self, token_type: TokenType):
        # if the current token is not a given type, error.
        if not self.check_token(token_type):
            raise ValueError(f"Expected token type: {token_type}, but got: {self.current_token.type}")
        self.advance()

    # expression parsing

    def comparison(self):

        self.expression()
        if self.check_peek(TokenType.EQ) or self.check_peek(TokenType.NQ) or \
                self.check_peek(TokenType.GT) or self.check_peek(TokenType.GQ) or \
                self.check_peek(TokenType.LT) or self.check_peek(TokenType.LQ):
            self.expression()
            self.advance()
        else:
            raise ValueError(f"Expected comparison operator, but got: {self.peek_token.val}")

        while self.check_peek(TokenType.EQ) or self.check_peek(TokenType.NQ) or \
                self.check_peek(TokenType.GT) or self.check_peek(TokenType.GQ) or \
                self.check_peek(TokenType.LT) or self.check_peek(TokenType.LQ):
            self.expression()
            self.advance()

    def expression(self):
        # expression: term term (ADD | SUB)
        print('expression')
        self.term()
        while self.check_peek(TokenType.ADD) or self.check_peek(TokenType.SUB):
            self.term()
            self.advance()

    def term(self):
        # term: factor factor (MUL | DIV | MOD)
        print('term')
        self.unary()
        while self.check_peek(TokenType.MUL) or \
                self.check_peek(TokenType.DIV) or self.check_peek(TokenType.MOD):
            self.unary()
            self.advance()

    def unary(self):
        # unary: [+] primary | [-] primary
        # optional
        print('unary')
        if self.check_token(TokenType.PLUS) or self.check_token(TokenType.NEG):
            self.advance()
        self.primary()

    def primary(self):
        # primary: INT | FLOAT | IDENTIFIER
        print('primary')
        if self.check_token(TokenType.INT) or \
                self.check_token(TokenType.FLOAT):
            self.advance()
        elif self.check_token(TokenType.IDENTIFIER):
            if self.current_token.val not in self.symbols.keys():
                raise ValueError(f"Var referenced before assignment: {self.current_token.val}")
            self.advance()
        else:
            raise ValueError(f"Expected number or variable, but got: {self.current_token.val}")


    def is_symbol(self, var):
        # bool
        if var in self.symbols.keys():
            return True
        return False

    def statement(self):
        match (self.current_token.type):
            case TokenType.POP:
                print("POP")
                self.advance()

                if len(self.stack) > 0:

                    last = self.stack.pop()

                    if last in self.symbols:
                        print(self.symbols[last])
                        del self.symbols[last]
                    else:
                        print(last)

            case TokenType.PUSH:
                print("PUSH")
                self.advance()

                name = ''
                if self.check_token(TokenType.IDENTIFIER):
                    name = self.current_token.val
                    self.advance()

                num = 1
                if self.check_token(TokenType.NEG):
                    num = -1
                    self.advance()
                elif self.check_token(TokenType.PLUS):
                    self.advance()

                if self.check_token(TokenType.INT) or self.check_token(TokenType.FLOAT):
                    if name:
                        self.symbols[name] = num * self.current_token.val
                        self.stack.append(name)
                    else:
                        self.stack.append(num * self.current_token.val)
                    self.advance()
                else:
                    raise ValueError(f"Expected number, but got: {self.current_token.val}")

            case TokenType.ADD:
                print("ADD")
                self.advance()

                if len(self.stack) >= 2:
                    a = self.stack.pop()
                    b = self.stack.pop()

                    if self.is_symbol(a):
                        a = self.symbols[a]
                    if self.is_symbol(b):
                        b = self.symbols[b]

                    self.stack.append(a + b)
                elif len(self.stack) < 1:
                    raise ValueError("Not enough elements in stack.")

            case TokenType.SUB:
                self.advance()

                if len(self.stack) >= 2:
                    a = self.stack.pop()
                    b = self.stack.pop()

                    if self.is_symbol(a):
                        a = self.symbols[a]
                    if self.is_symbol(b):
                        b = self.symbols[b]

                    self.stack.append(a - b)
                elif len(self.stack) < 1:
                    raise ValueError("Not enough elements in stack.")

            case TokenType.MUL:
                print("MUL")
                self.advance()

                if len(self.stack) >= 2:
                    a = self.stack.pop()
                    b = self.stack.pop()

                    if self.is_symbol(a):
                        a = self.symbols[a]
                    if self.is_symbol(b):
                        b = self.symbols[b]

                    self.stack.append(a * b)
                elif len(self.stack) < 1:
                    raise ValueError("Not enough elements in stack.")

            case TokenType.DIV:
                print("DIV")
                self.advance()

                if len(self.stack) >= 2:
                    a = self.stack.pop()
                    b = self.stack.pop()

                    if self.is_symbol(a):
                        a = self.symbols[a]
                    if self.is_symbol(b):
                        b = self.symbols[b]

                    self.stack.append(a / b)
                elif len(self.stack) < 1:
                    raise ValueError("Not enough elements in stack.")

            case TokenType.VAR:
                # creates a variable, but does not push it to the stack.
                self.advance()

                name = self.current_token.val
                self.match(TokenType.IDENTIFIER)

                num = 1
                if self.check_token(TokenType.NEG):
                    num = -1
                    self.advance()
                elif self.check_token(TokenType.PLUS):
                    self.advance()

                if self.check_token(TokenType.FLOAT) or self.check_token(TokenType.INT):
                    self.symbols[name] = num * self.current_token.val
                    self.advance()
                else:
                    raise ValueError(f"Expected number, but got: {self.current_token.val}")

            case _:
                raise ValueError(f"Statement not recognized: {self.current_token}")



    def program(self):

        # parse all statements in program.
        while not self.check_token(TokenType.EOF):
            self.statement()
            print(self.stack)


if __name__ == "__main__":
    lexer = Lexer("tomson.skt")
    parser = Parser(lexer)

    parser.program()
