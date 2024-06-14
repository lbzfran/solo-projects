from lexer import Lexer, Token, TokenType
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

    def check_peek(self, token_type: TokenType):
        return self.peek_token.token_type == token_type

    def statement(self):

        if self.check_token(TokenType.IDENTIFIER):
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

        elif self.check_token(TokenType.DUP):
            self.advance()

            if len(self.stack) == 0:
                raise Exception("Stack is empty.")

            self.stack.append(self.stack[-1])

        elif self.check_token(TokenType.SWAP):
            self.advance()

            if len(self.stack) < 2:
                raise Exception("Not enough elements in stack.")

            fst = self.stack.pop()
            snd = self.stack.pop()
            self.stack.append(fst)
            self.stack.append(snd)


        elif self.check_token(TokenType.ADD):
            self.advance()

            if len(self.stack) == 1:
                # equivalent: x + 0 = x
                pass
            elif len(self.stack) == 0:
                raise Exception("Not enough elements in stack.")

            elem1 = self.stack.pop()
            elem2 = self.stack.pop()
            self.stack.append(elem1 + elem2)

            print(f"ADDING {elem1} and {elem2}")

        elif self.check_token(TokenType.SUB):
            self.advance()

            if len(self.stack) == 1:
                # equivalent: x - 0 = x
                pass
            elif len(self.stack) == 0:
                raise Exception("Not enough elements in stack.")

            elem1 = self.stack.pop()
            elem2 = self.stack.pop()
            self.stack.append(elem1 - elem2)

            print(f"SUBTRACTING {elem1} and {elem2}")

        elif self.check_token(TokenType.MUL):
            self.advance()

            if len(self.stack) == 1:
                # equivalent: x * 1 = x
                pass
            elif len(self.stack) == 0:
                raise Exception("Not enough elements in stack.")

            elem1 = self.stack.pop()
            elem2 = self.stack.pop()
            self.stack.append(elem1 * elem2)

            print(f"MULTIPLYING {elem1} and {elem2}")

        elif self.check_token(TokenType.DIV):
            self.advance()

            if len(self.stack) == 1:
                # equivalent: x / 1 = x
                pass
            elif len(self.stack) == 0:
                raise Exception("Not enough elements in stack.")

            elem1 = self.stack.pop()
            elem2 = self.stack.pop()
            self.stack.append(elem1 // elem2)

            print(f"DIVIDING {elem1} and {elem2}")

        elif self.check_token(TokenType.MOD):
            self.advance()

            if len(self.stack) == 1:
                # equivalent: x % 1 = x
                pass
            elif len(self.stack) == 0:
                raise Exception("Not enough elements in stack.")

            elem1 = self.stack.pop()
            elem2 = self.stack.pop()
            self.stack.append(elem1 % elem2)

            print(f"MOD {elem1} and {elem2}")

        else:
            print(f"Statement not recognized: {self.current_token.value}")
            self.advance()


    def program(self):
        while not self.check_token(TokenType.EOF):
            self.statement()
