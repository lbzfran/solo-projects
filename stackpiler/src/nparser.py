from tokens import Token, TokenType
#from lexer import Lexer


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

        self.current_token = Token(TokenType.NONE, None)
        self.peek_token = Token(TokenType.NONE, None)

        self.variables = {}

        self.stack = []

        self.advance(); self.advance()

    def advance(self):
        self.current_token = self.peek_token
        self.peek_token = self.lexer.get_token()

    def check_token(self, token_type, other_token: Token = Token(TokenType.NONE, None)):
        if other_token.type != TokenType.NONE:
            return token_type == other_token.type
        return token_type == self.current_token.type

    def check_peek(self, token_type):
        return token_type == self.peek_token.type

    def validate_var(self, var, expr):
        # checks variable type matches expression.
        if var.upper() in ('INT', 'FLOAT') and isinstance(expr, (int, float)):
            return True
        elif var.upper() in ('STRING') and isinstance(expr, str):
            return True
        elif var.upper() in ('BOOL'):
            return True
        return False

    def check_symbol(self, value):
        # checks if name exists in var table
        if value in self.variables.keys():
            return True
        return False

    def match_token(self, token_type):
        # forces next token to be of a certain type, or exception
        assert self.check_token(token_type), f"Expected {token_type}, got {self.current_token.type}"
        self.advance()

    def factor(self):
        #print('factor')

        if self.check_token(TokenType.STR):
            word = self.current_token.val
            self.advance()
            return word

        elif self.check_token(TokenType.BOOL):
            bool_val = 0
            if self.current_token.val == 'true':
                bool_val = 1
            self.advance()
            return bool_val

        elif self.check_token(TokenType.LPAREN):
            self.advance()
            expr = self.expression()
            self.match_token(TokenType.RPAREN)
            return expr

        elif self.check_token(TokenType.POS):
            self.advance()
            return self.factor()
        elif self.check_token(TokenType.NEG):
            self.advance()
            return -self.factor()

        elif self.check_token(TokenType.INT) or self.check_token(TokenType.FLOAT):
            return self.current_token.val
        elif self.check_token(TokenType.ID):
            if self.check_symbol(self.current_token.val):
                return self.variables[self.current_token.val]
            else:
                raise ValueError(f"variable referenced before assignment: {self.current_token.val}")

    def expression(self):
        #print('expression->',end='')

        if self.check_token(TokenType.STR) or self.check_token(TokenType.BOOL):
            #print('string')
            return self.factor()

        elif self.check_token(TokenType.INT) or self.check_token(TokenType.FLOAT) or \
                self.check_token(TokenType.POS) or self.check_token(TokenType.NEG) or \
                self.check_token(TokenType.LPAREN):
            self.stack.append(self.factor())
        elif self.check_token(TokenType.ID):
            if self.check_symbol(self.current_token.val):
                #print('symbol')
                self.stack.append(self.variables[self.current_token.val][1])
            else:
                raise ValueError(f"variable referenced before assignment: {self.current_token.val}")
        elif self.current_token.type in [TokenType.ADD, TokenType.SUB,
                                         TokenType.MUL, TokenType.DIV, TokenType.MOD,
                                         TokenType.EQ, TokenType.NQ, TokenType.GT,
                                         TokenType.GQ, TokenType.LT, TokenType.LQ,
                                         ]:
            self.statement()

        else:
            raise ValueError(f"no handling found for {self.current_token} within expression.")
        self.advance()
        return self.stack.pop()


    def statement(self):
        # statement : compound | assignment | stack | empty

        node = ('mt',)
        if self.check_token(TokenType.LBRACK):
            # [statement_list]
            self.match_token(TokenType.LBRACK)
            stlist = self.statement_list()
            node = ('cmp', stlist)
            self.match_token(TokenType.RBRACK)
        elif self.check_token(TokenType.VAR):
            # VAR ID ASSIGN expr
            var = self.current_token.val
            self.advance()
            name = self.current_token.val
            self.match_token(TokenType.ID)
            self.match_token(TokenType.ASSIGN)
            expr = self.expression()
            if self.validate_var(var, expr):
                self.variables[name] = (var, expr)
            else:
                raise Exception(f'error creating variable with given values:\nname: {name} var: {var} expr: {expr}')
            node = ('var', var, name, expr)
        else:
            # stack operations:
            # always returns ('stack', val)
            match self.current_token.type:
                case TokenType.PUSH:
                    #print('PUSH')
                    self.advance()
                    expr = self.expression()
                    self.stack.append(expr)
                    node = ('push', expr)
                case TokenType.POP:
                    #print('POP')
                    self.advance()

                    assert len(self.stack) >= 1, "Not enough elements in stack to pop"
                    a = self.stack.pop()
                    if a in self.variables.keys():
                        a = self.variables[a]
                    #print(a)
                    node = ('a')
                case TokenType.DUP:
                    #print('DUP')
                    self.advance()

                    assert len(self.stack) >= 1, "Not enough elements in stack to duplicate"
                    a = self.stack[-1]
                    self.stack.append(a)
                    node = ('dup')
                case TokenType.SWAP:
                    #print('SWAP')
                    self.advance()

                    assert len(self.stack) >= 2, "Not enough elements in stack to swap"
                    a, b = self.stack.pop(), self.stack.pop()
                    self.stack.append(a)
                    self.stack.append(b)
                    node = ('swap')
                case TokenType.OVER:
                    #print('OVER')
                    self.advance()

                    assert len(self.stack) >= 2, "Not enough elements in stack to over"
                    a = self.stack[-2]
                    self.stack.append(a)
                    node = ('over')
                case TokenType.ROT:
                    #print('ROT')
                    self.advance()

                    assert len(self.stack) >= 3, "Not enough elements in stack to rotate"
                    a, b, c = self.stack.pop(), self.stack.pop(), self.stack.pop()

                    self.stack.append(b)
                    self.stack.append(a)
                    self.stack.append(c)
                    node = ('rot')

                case TokenType.ADD:
                    #print('ADD')
                    self.advance()

                    assert len(self.stack) >= 2, "Not enough elements in stack to add"
                    a, b = self.stack.pop(), self.stack.pop()
                    if a in self.variables.keys():
                        a = self.variables[a]
                    if b in self.variables.keys():
                        b = self.variables[b]
                    self.stack.append(b + a)
                    node = ('add')

                case TokenType.SUB:
                    #print('SUB')
                    self.advance()

                    assert len(self.stack) >= 2, "Not enough elements in stack to subtract"
                    a, b = self.stack.pop(), self.stack.pop()
                    if a in self.variables.keys():
                        a = self.variables[a]
                    if b in self.variables.keys():
                        b = self.variables[b]
                    self.stack.append(b - a)
                    node = ('sub')

                case TokenType.MUL:
                    #print('MUL')
                    self.advance()

                    assert len(self.stack) >= 2, "Not enough elements in stack to multiply"
                    a, b = self.stack.pop(), self.stack.pop()
                    if a in self.variables.keys():
                        a = self.variables[a]
                    if b in self.variables.keys():
                        b = self.variables[b]
                    self.stack.append(b * a)
                    node = ('mul')

                case TokenType.DIV:
                    #print('DIV')
                    self.advance()

                    assert len(self.stack) >= 2, "Not enough elements in stack to divide"
                    a, b = self.stack.pop(), self.stack.pop()
                    if a in self.variables.keys():
                        a = self.variables[a]
                    if b in self.variables.keys():
                        b = self.variables[b]
                    self.stack.append(b / a)
                    node = ('div')

                case TokenType.MOD:
                    #print('MOD')
                    self.advance()

                    assert len(self.stack) >= 2, "Not enough elements in stack to modulo"
                    a, b = self.stack.pop(), self.stack.pop()
                    if a in self.variables.keys():
                        a = self.variables[a]
                    if b in self.variables.keys():
                        b = self.variables[b]
                    self.stack.append(b % a)
                    node = ('mod')

                case TokenType.EQ:

                    self.advance()

                    assert len(self.stack) >= 2, "Not enough elements in stack to compare"
                    a, b = self.stack.pop(), self.stack.pop()
                    if a in self.variables.keys():
                        a = self.variables[a]
                    if b in self.variables.keys():
                        b = self.variables[b]

                    self.stack.append(1 if a == b else 0)
                    node = ('eq')

                case TokenType.NQ:

                    self.advance()

                    assert len(self.stack) >= 2, "Not enough elements in stack to compare"
                    a, b = self.stack.pop(), self.stack.pop()
                    if a in self.variables.keys():
                        a = self.variables[a]
                    if b in self.variables.keys():
                        b = self.variables[b]

                    self.stack.append(1 if a != b else 0)
                    node = ('nq')

                case TokenType.GT:

                    self.advance()

                    assert len(self.stack) >= 2, "Not enough elements in stack to compare"
                    a, b = self.stack.pop(), self.stack.pop()
                    if a in self.variables.keys():
                        a = self.variables[a]
                    if b in self.variables.keys():
                        b = self.variables[b]

                    self.stack.append(1 if a > b else 0)
                    node = ('gt')
                case TokenType.GQ:

                    self.advance()

                    assert len(self.stack) >= 2, "Not enough elements in stack to compare"
                    a, b = self.stack.pop(), self.stack.pop()
                    if a in self.variables.keys():
                        a = self.variables[a]
                    if b in self.variables.keys():
                        b = self.variables[b]

                    self.stack.append(1 if a >= b else 0)
                    node = ('gq')

                case TokenType.LT:

                    self.advance()

                    assert len(self.stack) >= 2, "Not enough elements in stack to compare"
                    a, b = self.stack.pop(), self.stack.pop()
                    if a in self.variables.keys():
                        a = self.variables[a]
                    if b in self.variables.keys():
                        b = self.variables[b]

                    self.stack.append(1 if a < b else 0)
                    node = ('lt')
                case TokenType.LQ:

                    self.advance()

                    assert len(self.stack) >= 2, "Not enough elements in stack to compare"
                    a, b = self.stack.pop(), self.stack.pop()
                    if a in self.variables.keys():
                        a = self.variables[a]
                    if b in self.variables.keys():
                        b = self.variables[b]

                    self.stack.append(1 if a <= b else 0)
                    node = ('lq')

                case TokenType.AND:

                    self.advance()

                    assert len(self.stack) >= 2, "Not enough elements in stack to compare"
                    a, b = self.stack.pop(), self.stack.pop()
                    if a in self.variables.keys():
                        a = self.variables[a]
                    if b in self.variables.keys():
                        b = self.variables[b]

                    self.stack.append(1 if a + b == 2 else 0)
                    node = ('and')

                case TokenType.OR:

                    self.advance()

                    assert len(self.stack) >= 2, "Not enough elements in stack to compare"
                    a, b = self.stack.pop(), self.stack.pop()
                    if a in self.variables.keys():
                        a = self.variables[a]
                    if b in self.variables.keys():
                        b = self.variables[b]

                    self.stack.append(1 if a + b > 0 else 0)
                    node = ('or')

                case TokenType.NOT:

                    self.advance()

                    assert len(self.stack) >= 1, "Not enough elements in stack to invert"
                    a = self.stack.pop()
                    if a in self.variables.keys():
                        a = self.variables[a]

                    self.stack.append(1 if a == 0 else 0)
                    node = ('not')


                case _:
                    print(self.current_token)

        return node


    def statement_list(self):

        stlist = [self.statement()]

        while self.current_token.type == TokenType.SEMI:
            self.match_token(TokenType.SEMI)

            if self.check_token(TokenType.RBRACK) or self.check_token(TokenType.EOF):
                break
            nt = self.statement()
            if nt[0] == 'mt':
                break
            stlist.append(nt)
            #print(self.stack)
        return stlist


    def program(self):
        # program : {compound_statement}

        node = self.statement_list()
        print(self.stack)
        # ..
        return node


if __name__ == '__main__':
    from lexer import Lexer
    lexer = Lexer('tomson.skt')
    parser = Parser(lexer)
    print(parser.program())
