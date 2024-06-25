from tokens import Token, TokenType
from lexer import Lexer

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer

        self.current_token = Token(TokenType.NONE, None)
        self.peek_token = Token(TokenType.NONE, None)

        self.symbols = {} # variables

        self.stack = []
        self.op = []

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
        """
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

    # -1 -2 MUL.

    def term(self):
        # term: factor (factor [MUL | DIV | MOD])
        print('term->',end='')
        a = self.factor() # 1 -2 mul

        if self.check_token(TokenType.POS) or self.check_token(TokenType.NEG) or self.check_token(TokenType.LPAREN) or \
            self.check_peek(TokenType.MUL) or self.check_peek(TokenType.DIV) or self.check_peek(TokenType.MOD):
            # guaranteed factor if sign/lparen is present.
            # also guaranteed if next token is a valid operator (mul/div/mod).
            b = self.factor()

        while self.check_peek(TokenType.MUL) or \
                self.check_peek(TokenType.DIV) or self.check_peek(TokenType.MOD):

            b = self.factor()
            print(f'in term: {a}*{b}')
            if self.check_token(TokenType.MUL):
                a *= b
            elif self.check_token(TokenType.DIV):
                a /= b
            elif self.check_token(TokenType.MOD):
                a %= b
            else:
                print(self.peek_token)

            self.advance()
        return a

    # (-1 -2 MUL) 3 ADD

    def old_expression(self):
        # expression: term (term [ADD | SUB])
        print('expression->',end='')
        a = self.term()
        while self.check_peek(TokenType.ADD) or self.check_peek(TokenType.SUB):
            b = self.term()

            print(f'in expr: {a}+{b}')
            if self.check_token(TokenType.ADD):
                a += b
            elif self.check_token(TokenType.SUB):
                a -= b

            self.advance()
        return a
    def comparison(self) -> bool:
        # 5 < 6
        a = self.expression()
        if self.check_peek(TokenType.EQ) or self.check_peek(TokenType.NQ) or \
                self.check_peek(TokenType.GT) or self.check_peek(TokenType.GQ) or \
                self.check_peek(TokenType.LT) or self.check_peek(TokenType.LQ):
            b = self.expression()

            match (self.current_token.type):
                case TokenType.EQ:
                    a = a == b
                case TokenType.NQ:
                    a = a != b
                case TokenType.GT:
                    a = a > b
                case TokenType.GQ:
                    a = a >= b
                case TokenType.LT:
                    a = a < b
                case TokenType.LQ:
                    a = a <= b
            self.advance()
        else:
            raise ValueError(f"Expected comparison operator, but got: {self.peek_token.val}")

        while self.check_peek(TokenType.EQ) or self.check_peek(TokenType.NQ) or \
                self.check_peek(TokenType.GT) or self.check_peek(TokenType.GQ) or \
                self.check_peek(TokenType.LT) or self.check_peek(TokenType.LQ):
            b = self.expression()

            match (self.current_token.type):
                case TokenType.EQ:
                    a = a == b
                case TokenType.NQ:
                    a = a != b
                case TokenType.GT:
                    a = a > b
                case TokenType.GQ:
                    a = a >= b
                case TokenType.LT:
                    a = a < b
                case TokenType.LQ:
                    a = a <= b
            self.advance()

        if self.check_token(TokenType.NOT):
            self.advance()
            return not a
        return a

    # ((-1 -2 MUL) 3 ADD) > (5 6 ADD)

    def boolean(self) -> bool:
        # comparison (AND | OR) comparison
        a = self.comparison()

        # x y and z or a and b

        while self.check_peek(TokenType.AND) or self.check_peek(TokenType.OR):
            b = self.comparison()

            match (self.current_token.type):
                case TokenType.AND:
                    a = a and b
                case TokenType.OR:
                    a = a or b
            self.advance()
        return a
        """

    def expression(self):
        print('expression->',end='')

        while not self.check_token(TokenType.END):
            if self.check_token(TokenType.INT) or self.check_token(TokenType.FLOAT) or \
                    self.check_token(TokenType.POS) or self.check_token(TokenType.NEG):
                        self.stack.append(self.factor())
            elif self.check_token(TokenType.IDENTIFIER):
                if self.check_symbol(self.current_token.val):
                    self.stack.append(self.current_token.val)
                else:
                    raise ValueError(f"Var referenced before assignment: {self.current_token.val}")
            elif self.check_token(TokenType.ADD) or self.check_token(TokenType.SUB) or \
                    self.check_token(TokenType.MUL) or self.check_token(TokenType.DIV) or \
                    self.check_token(TokenType.MOD):
                match (self.current_token.type):
                    case TokenType.ADD:
                        #self.op.append(TokenType.ADD)
                        self.statement(TokenType.ADD)
                    case TokenType.SUB:
                        #self.op.append(TokenType.SUB)
                        self.statement(TokenType.SUB)
                    case TokenType.MUL:
                        #self.op.append(TokenType.MUL)
                        self.statement(TokenType.MUL)
                    case TokenType.DIV:
                        #self.op.append(TokenType.DIV)
                        self.statement(TokenType.DIV)
                    case TokenType.MOD:
                        #self.op.append(TokenType.MOD)
                        self.statement(TokenType.MOD)
        self.match_token(TokenType.END)


    def statement(self, token = None):
        match (token or self.current_token.type):
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
                """
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
                """
            case TokenType.PUSH:
                print("PUSH")
                self.advance()

                if self.check_token(TokenType.POP):
                    # mechanic that pushes the latest element to the top of the stack.
                    self.stack.insert(0,self.stack.pop())
                    self.advance()
                    return

                self.expression()

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
                # creates a variable, but does not push it to the stack.
                self.advance()

                name = self.current_token.val
                self.match_token(TokenType.IDENTIFIER)

                num = 1
                if self.check_token(TokenType.NEG):
                    num = -1
                    self.advance()
                elif self.check_token(TokenType.POS):
                    self.advance()

                if self.check_token(TokenType.FLOAT) or self.check_token(TokenType.INT):
                    self.symbols[name] = num * self.current_token.val
                    self.advance()
                else:
                    raise ValueError(f"Expected number, but got: {self.current_token.val}")

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
