from tokens import Token, TokenType
from lexer import Lexer

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer

        self.current_token = Token(TokenType.NONE, None)
        self.peek_token = Token(TokenType.NONE, None)

        self.symbols = {} # variables
        self.functions = {}

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

    def check_token(self, token_type: TokenType, other_token: Token = None):
        # checks if current token is of a given token type.
        if other_token:
            return other_token.type == token_type
        return self.current_token.type == token_type

    def check_peek(self, token_type: TokenType):
        return self.peek_token.type == token_type

    def match_token(self, token_type: TokenType):
        # if the current token is not a given type, error.
        if not self.check_token(token_type):
            raise ValueError(f"Expected token type: {token_type}, but got: {self.current_token.type}")
        self.advance()

    def check_string(self, *args):
        # used to validate, mainly for algebraic expressions that cannot use strings.
        for k in args:
            if isinstance(k, str):
                return True
        return False

    # expression parsing

    # 1

    def primary(self, tokens = None, idx = None):
        # primary: INT | FLOAT | IDENTIFIER | NONE
        print('primary')
        value = None
        if not tokens:
            if self.check_token(TokenType.INT) or self.check_token(TokenType.FLOAT):
                value = self.current_token.val

            elif self.check_token(TokenType.IDENTIFIER):
                # variable cannot be defined within an expression.
                if not self.check_symbol(self.current_token.val):
                    raise ValueError(f"Var referenced before assignment: {self.current_token.val}")
                value = self.symbols[self.current_token.val]

            elif self.check_token(TokenType.STR) or self.check_token(TokenType.CHAR):
                value = self.current_token.val
            self.advance()



        else:
            # running on a local stack.
            print(f'primary on idx: {idx}')
            if self.check_token(TokenType.INT, tokens[idx]) or self.check_token(TokenType.FLOAT, tokens[idx]):
                value = tokens[idx].val

            elif self.check_token(TokenType.IDENTIFIER, tokens[idx]):
                # variable cannot be defined within an expression.
                print(tokens[idx].val)

                if not self.check_symbol(tokens[idx].val):
                    raise ValueError(f"Var referenced before assignment: {tokens[idx].val}")
                value = self.symbols[tokens[idx].val]

            elif self.check_token(TokenType.STR, tokens[idx]) or self.check_token(TokenType.CHAR, tokens[idx]):
                value = tokens[idx].val
            idx += 1
            return value, idx
        return value

    # -1
    def factor(self, tokens = None, idx = None):
        # factor: [+] primary | [-] primary | [(] expression [)]
        # optional. handles only numbers.
        print('factor->',end='')

        if not tokens:
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

            # string handling
            if self.check_token(TokenType.STR):
                return self.primary()
            return sign * self.primary()


        else:
            # running on a local stack.
            if self.check_token(TokenType.LPAREN, tokens[idx]):
                idx += 1
                _, idx = self.expression(tokens, idx)
                idx += 1

            sign = 1
            if self.check_token(TokenType.POS, tokens[idx]):
                idx += 1
            elif self.check_token(TokenType.NEG, tokens[idx]):
                sign = -1
                idx += 1

            # string handling
            if self.check_token(TokenType.STR, tokens[idx]):
                return self.primary(tokens, idx)
            x, idx = self.primary(tokens, idx)
            return sign * x, idx

    def expression(self, tokens = None, jdx = None):
        print('expression->',end='')

        if not tokens:
            if self.check_token(TokenType.STR):
                print('string')
                return self.factor()

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
                    raise ValueError(f"no handling found for {self.current_token} within expression.")
            self.match_token(TokenType.END)

        else:
            # running on a local stack.
            idx = jdx or 0
            while not self.check_token(TokenType.END, tokens[idx]):
                if self.check_token(TokenType.INT,tokens[idx]) or self.check_token(TokenType.FLOAT,tokens[idx]) or \
                        self.check_token(TokenType.POS, tokens[idx]) or self.check_token(TokenType.NEG, tokens[idx]) or \
                        self.check_token(TokenType.LPAREN):
                            x, idx = self.factor(tokens, idx)
                            self.stack.append(x)
                            print(x)
                            idx += 1
                elif self.check_token(TokenType.IDENTIFIER, tokens[idx]):
                    if self.check_symbol(tokens[idx].val):
                        print('symbol')
                        self.stack.append(tokens[idx].val)
                        idx += 1
                    else:
                        raise ValueError(f"variable referenced before assignment: {self.current_token.val}")
                elif tokens[idx].type in [TokenType.ADD, TokenType.SUB,
                                                 TokenType.MUL, TokenType.DIV, TokenType.MOD,
                                                 TokenType.EQ, TokenType.NQ, TokenType.GT,
                                                 TokenType.GQ, TokenType.LT, TokenType.LQ,
                                                 ]:
                    self.statement(tokens[idx].type)
                    idx += 1

                else:
                    raise ValueError(f"no handling found for {self.current_token} within expression.")

            if jdx:
                return self.stack.pop(), idx

        return self.stack.pop()

    def snippet(self, tokens):
        local_tokens = tokens.copy()
        x = self.expression(local_tokens)
        print(x)
        return x

    def statement(self, token = None):
        match (token or self.current_token.type):
            case TokenType.POP:
                print("POP")
                self.advance()

                if self.check_token(TokenType.STR) or self.check_token(TokenType.CHAR):
                    print(self.current_token.val)
                    self.advance()

                elif len(self.stack) > 0:
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
                    print(a,b,c)

                    # a b c | c a b | b c a

                    self.stack.append(b)
                    self.stack.append(a)
                    self.stack.append(c)
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

                    if self.check_string(a,b):
                        raise ValueError("string caught in algebraic expression: ", a, b)

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

                    if self.check_string(a,b):
                        raise ValueError("string caught in algebraic expression: ", a, b)

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

                    if self.check_string(a,b):
                        raise ValueError("string caught in algebraic expression: ", a, b)

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

                    if self.check_string(a,b):
                        raise ValueError("string caught in algebraic expression: ", a, b)

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

                    if self.check_string(a,b):
                        raise ValueError("string caught in algebraic expression: ", a, b)

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

                    if self.check_symbol(a):
                        a = self.symbols[a]
                    if self.check_symbol(b):
                        b = self.symbols[b]

                    self.stack.append(a == b)
                elif len(self.stack) < 1:
                    raise ValueError("Not enough elements in stack.")

            case TokenType.NQ:
                print("NQ")
                self.advance()

                if len(self.stack) >= 2:
                    a = self.stack.pop()
                    b = self.stack.pop()

                    if self.check_symbol(a):
                        a = self.symbols[a]
                    if self.check_symbol(b):
                        b = self.symbols[b]

                    self.stack.append(a != b)
                elif len(self.stack) < 1:
                    raise ValueError("Not enough elements in stack.")

            case TokenType.GT:
                print("EQ")
                self.advance()

                if len(self.stack) >= 2:
                    a = self.stack.pop()
                    b = self.stack.pop()

                    if self.check_symbol(a):
                        a = self.symbols[a]
                    if self.check_symbol(b):
                        b = self.symbols[b]

                    if self.check_string(a,b):
                        raise ValueError("string caught in invalid bool expression: ", a, b)

                    self.stack.append(a > b)
                elif len(self.stack) < 1:
                    raise ValueError("Not enough elements in stack.")

            case TokenType.GQ:
                print("NQ")
                self.advance()

                if len(self.stack) >= 2:
                    a = self.stack.pop()
                    b = self.stack.pop()

                    if self.check_symbol(a):
                        a = self.symbols[a]
                    if self.check_symbol(b):
                        b = self.symbols[b]

                    if self.check_string(a,b):
                        raise ValueError("string caught in invalid bool expression: ", a, b)

                    self.stack.append(a >= b)
                elif len(self.stack) < 1:
                    raise ValueError("Not enough elements in stack.")

            case TokenType.LT:
                print("EQ")
                self.advance()

                if len(self.stack) >= 2:
                    a = self.stack.pop()
                    b = self.stack.pop()

                    if self.check_symbol(a):
                        a = self.symbols[a]
                    if self.check_symbol(b):
                        b = self.symbols[b]

                    if self.check_string(a,b):
                        raise ValueError("string caught in invalid bool expression: ", a, b)

                    self.stack.append(a < b)
                elif len(self.stack) < 1:
                    raise ValueError("Not enough elements in stack.")

            case TokenType.LQ:
                print("NQ")
                self.advance()

                if len(self.stack) >= 2:
                    a = self.stack.pop()
                    b = self.stack.pop()

                    if self.check_symbol(a):
                        a = self.symbols[a]
                    if self.check_symbol(b):
                        b = self.symbols[b]

                    if self.check_string(a,b):
                        raise ValueError("string caught in invalid bool expression: ", a, b)

                    self.stack.append(a <= b)
                elif len(self.stack) < 1:
                    raise ValueError("Not enough elements in stack.")

            case TokenType.IF:
                print("IF")
                self.advance()
                if self.comparison():
                    while not self.check_token(TokenType.FI):
                        self.statement()
                else:
                    while not self.check_token(TokenType.FI) and not self.check_token(TokenType.ELSE):
                        self.advance()
                    if self.check_token(TokenType.ELSE):
                        self.advance()
                        while not self.check_token(TokenType.FI):
                            self.statement()
                self.advance()

            case TokenType.WHILE:
                print("WHILE")
                # first instance of looping.
                # TODO: some ideas; maybe save all tokens inside loop, and reparse them.

                self.advance()


                # loop through condition until it returns false.
                condition = []
                self.match_token(TokenType.LPAREN)
                while not self.check_token(TokenType.RPAREN):
                    condition.append(self.current_token)
                    self.advance()
                self.match_token(TokenType.RPAREN)

                print([x.val for x in condition])

                while self.snippet(condition):
                    print('while->',end='')

                    # for testing only
                    self.symbols['y'] += 1

               #if self.snippet(condition):
               #    statement_loop = []
               #    while not self.check_token(TokenType.END):
               #        statement_loop.append(self.current_token)
               #        self.advance()

               #    print(statement_loop)
               #    assert False, "Not implemented"
               #    while self.snippet(condition):
               #        for token in statement_loop:
               #            self.statement(token)

            case _:
                raise ValueError(f"Statement not recognized: {self.current_token}")



    def program(self, show_stack = False):
        # parse all statements in program.
        while not self.check_token(TokenType.EOF):
            self.statement()
            if show_stack:
                print(self.stack)


if __name__ == "__main__":
    lexer = Lexer("tomson.skt")
    parser = Parser(lexer)

    parser.program()
