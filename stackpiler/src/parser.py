from tokens import Token, TokenType
from lexer import Lexer

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer

        self.current_token = Token(TokenType.NONE, None)
        self.peek_token = Token(TokenType.NONE, None)

        self.symbols = {} # variables

        self.stack = []

        # initializes current and peek tokens.
        self.advance()
        self.advance()

    def advance(self):
        self.current_token = self.peek_token
        self.peek_token = self.lexer.get_token()

    def check_symbol(self, var):
        # bool
        if var in self.symbols.keys():
            return True
        return False

    def check_token(self, token_type: TokenType):
        # checks if current token is of a given token type.
        return self.current_token.type == token_type

    def check_peek(self, token_type: TokenType):
        return self.peek_token.type == token_type

    def match_token(self, token_type: TokenType):
        # if the current token is not a given type, error.
        if not self.check_token(token_type):
            raise ValueError(f"Expected token type: {token_type}, but got: {self.current_token.type}")
        self.advance()

    # expression parsing

    # 1

    def primary(self):
        # primary: INT | FLOAT | IDENTIFIER | NONE
        print('primary')
        value = None
        if self.check_token(TokenType.INT) or self.check_token(TokenType.FLOAT):
            value = self.current_token.val
        elif self.check_token(TokenType.IDENTIFIER):
            # variable cannot be defined within an expression.
            if not self.check_symbol(self.current_token.val):
                raise ValueError(f"Var referenced before assignment: {self.current_token.val}")
        self.advance()
        return value

    # -1
    def factor(self):
        # factor: [+] primary | [-] primary | [(] expression [)]
        # optional. handles only numbers.
        print('factor->',end='')

        if self.check_token(TokenType.LPAREN):
            self.advance()
            x = self.expression()
            self.match_token(TokenType.RPAREN)
            return x

        sign = 1
        if self.check_token(TokenType.POS):
            self.advance()
        elif self.check_token(TokenType.NEG):
            sign = -1
            self.advance()
        return sign * self.primary()

    def expression(self):
        print('expression->',end='')

        while not self.check_token(TokenType.END):
            if self.check_token(TokenType.INT) or self.check_token(TokenType.FLOAT) or \
                    self.check_token(TokenType.POS) or self.check_token(TokenType.NEG) or \
                    self.check_token(TokenType.LPAREN):
                        self.stack.append(self.factor())
            elif self.check_token(TokenType.IDENTIFIER):
                if self.check_symbol(self.current_token.val):
                    print('symbol')
                    self.stack.append(self.current_token.val)
                    self.advance()
                else:
                    raise ValueError(f"variable referenced before assignment: {self.current_token.val}")
            elif self.current_token.type in [TokenType.ADD, TokenType.SUB,
                                             TokenType.MUL, TokenType.DIV, TokenType.MOD,
                                             TokenType.EQ, TokenType.NQ, TokenType.GT,
                                             TokenType.GQ, TokenType.LT, TokenType.LQ,
                                             ]:
                self.statement(self.current_token.type)
            else:
                print(f"no handling found for {self.current_token} within expression.")
        self.match_token(TokenType.END)

        return self.stack.pop()


    def statement(self, token = None):
        match (token or self.current_token.type):
            case TokenType.POP:
                print("POP")
                self.advance()

                if len(self.stack) > 0:

                    last = self.stack.pop()

                    if last in self.symbols:
                        print(self.symbols[last])
                    else:
                        print(last)

            case TokenType.PUSH:
                print("PUSH")
                self.advance()

                if self.check_token(TokenType.POP):
                    # mechanic that pushes the latest element to the top of the stack.
                    self.stack.insert(0,self.stack.pop())
                    self.advance()
                    return

                self.stack.append(self.expression())

            case TokenType.DUP:
                print("DUP")
                self.advance()

                if len(self.stack) > 0:
                    self.stack.append(self.stack[-1])
                else:
                    raise ValueError("Not enough elements in stack.")

            case TokenType.SWAP:
                print("SWAP")
                self.advance()

                if len(self.stack) >= 2:
                    a = self.stack.pop()
                    b = self.stack.pop()

                    self.stack.append(a)
                    self.stack.append(b)
                else:
                    raise ValueError("Not enough elements in stack.")

            case TokenType.OVER:
                print("OVER")
                self.advance()

                if len(self.stack) >= 2:
                    self.stack.append(self.stack[-2])
                else:
                    raise ValueError("Not enough elements in stack.")

            case TokenType.ROT:
                print("ROT")
                self.advance()

                if len(self.stack) >= 3:
                    a = self.stack.pop()
                    b = self.stack.pop()
                    c = self.stack.pop()

                    self.stack.append(b)
                    self.stack.append(c)
                    self.stack.append(a)
                else:
                    raise ValueError("Not enough elements in stack.")

            case TokenType.ADD:
                print("ADD")
                self.advance()

                if len(self.stack) >= 2:
                    a = self.stack.pop()
                    b = self.stack.pop()

                    if self.check_symbol(a):
                        a = self.symbols[a]
                    if self.check_symbol(b):
                        b = self.symbols[b]

                    self.stack.append(a + b)
                elif len(self.stack) < 1:
                    raise ValueError("Not enough elements in stack.")

            case TokenType.SUB:
                print("SUB")
                self.advance()

                if len(self.stack) >= 2:
                    a = self.stack.pop()
                    b = self.stack.pop()

                    if self.check_symbol(a):
                        a = self.symbols[a]
                    if self.check_symbol(b):
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

                    if self.check_symbol(a):
                        a = self.symbols[a]
                    if self.check_symbol(b):
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

                    if self.check_symbol(a):
                        a = self.symbols[a]
                    if self.check_symbol(b):
                        b = self.symbols[b]

                    self.stack.append(a / b)
                elif len(self.stack) < 1:
                    raise ValueError("Not enough elements in stack.")

            case TokenType.MOD:
                print("MOD")
                self.advance()

                if len(self.stack) >= 2:
                    a = self.stack.pop()
                    b = self.stack.pop()

                    if self.check_symbol(a):
                        a = self.symbols[a]
                    if self.check_symbol(b):
                        b = self.symbols[b]

                    self.stack.append(a % b)
                elif len(self.stack) < 1:
                    raise ValueError("Not enough elements in stack.")


            case TokenType.VAR:
                # creates a variable that can be referenced and pushed to the stack.
                print("VAR")
                self.advance()

                name = self.current_token.val
                self.match_token(TokenType.IDENTIFIER)

                self.symbols[name] = self.expression()

            case TokenType.FUNC:
                print("FUNC")
                assert False, "Not implemented"

            case TokenType.EQ:
                print("EQ")
                self.advance()

                if len(self.stack) >= 2:
                    a = self.stack.pop()
                    b = self.stack.pop()

                    self.stack.append(a == b)
                elif len(self.stack) < 1:
                    raise ValueError("Not enough elements in stack.")

            case TokenType.NQ:
                print("NQ")
                self.advance()

                if len(self.stack) >= 2:
                    a = self.stack.pop()
                    b = self.stack.pop()

                    self.stack.append(a != b)
                elif len(self.stack) < 1:
                    raise ValueError("Not enough elements in stack.")

            case TokenType.GT:
                print("EQ")
                self.advance()

                if len(self.stack) >= 2:
                    a = self.stack.pop()
                    b = self.stack.pop()

                    self.stack.append(a > b)
                elif len(self.stack) < 1:
                    raise ValueError("Not enough elements in stack.")

            case TokenType.GQ:
                print("NQ")
                self.advance()

                if len(self.stack) >= 2:
                    a = self.stack.pop()
                    b = self.stack.pop()

                    self.stack.append(a >= b)
                elif len(self.stack) < 1:
                    raise ValueError("Not enough elements in stack.")

            case TokenType.LT:
                print("EQ")
                self.advance()

                if len(self.stack) >= 2:
                    a = self.stack.pop()
                    b = self.stack.pop()

                    self.stack.append(a < b)
                elif len(self.stack) < 1:
                    raise ValueError("Not enough elements in stack.")

            case TokenType.LQ:
                print("NQ")
                self.advance()

                if len(self.stack) >= 2:
                    a = self.stack.pop()
                    b = self.stack.pop()

                    self.stack.append(a <= b)
                elif len(self.stack) < 1:
                    raise ValueError("Not enough elements in stack.")

            case TokenType.IF:
                print("IF")
                self.advance()
                if self.boolean():
                    while not self.check_token(TokenType.END):
                        self.statement()
                else:
                    while not self.check_token(TokenType.END):
                        self.advance()
                self.advance()

            case TokenType.WHILE:
                print("WHILE")
                # first instance of looping.
                assert False, "Not implemented"

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
