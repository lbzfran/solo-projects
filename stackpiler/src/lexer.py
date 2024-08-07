from os import access, R_OK
from os.path import isfile
from tokens import Token, TokenType

class Lexer:
    def __init__(self, src: str):
        assert isfile(src) and access(src, R_OK), f"File {src} does not exist/is not readable."
        with open(src, 'r') as file:
            self.src = file.read() + '\n'
        self.pos = -1
        self.current_char = ''
        self.advance()

    @property
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

    def protected(self, char: str):
        if char in ['(', ')', '{', '}', '[', ']', ';', '"', "'"]:
            return True
        return False

    def word(self):
        # traverse src for a word bounded together.
        assert self.current_char.isalpha() or self.peek == '_', "Invalid word format."
        start_pos = self.pos
        while self.peek.isalpha() or self.peek.isdigit() or self.peek == '_':
            self.advance()
            if self.protected(self.peek):
                # protected symbols; cannot be part of a word.
                break
        self.advance()

        return self.src[start_pos: self.pos]

    def char(self):
        # traverse src for a character bounded together.
        assert self.current_char == "'", "Invalid char format."
        self.advance() # skip first '
        start_pos = self.pos
        if self.current_char in ['\\']:
            self.advance()
            if not self.current_char in ['n', 't', 'r', '0', "'", '"', '\\']:
                raise ValueError(f"Invalid escape character: {self.current_char}")
        self.advance()
        return self.src[start_pos: self.pos]

    def string(self):
        # traverse src for a string bounded together.
        assert self.current_char == '"', "Invalid string format."
        self.advance()
        start_pos = self.pos
        while self.current_char != '"':
            self.advance()
        self.advance()

        # removes quotes.
        return self.src[start_pos: self.pos-1]

    def number(self):
        # traverse src for a number bounded together.
        assert self.current_char.isdigit(), "Invalid number format."

        start_pos = self.pos
        if self.protected(self.peek):
            # protected symbols; cannot be part of a num.
            # essentially skips advancing if ';' is next so it can be tokenized on its own.
            return int(self.src[start_pos: self.pos+1])

        if self.peek == '.':

            self.advance()
            if not self.peek.isdigit():
                raise ValueError("Invalid number format: expected digit after '.'")

            while self.peek.isdigit():
                self.advance()
            return float(self.src[start_pos: self.pos+1])

        while self.peek.isdigit():

            self.advance()
            if self.protected(self.peek):
                # protected symbols; cannot be part of a num.
                return int(self.src[start_pos: self.pos])

            if self.peek == '.':

                self.advance()
                if not self.peek.isdigit():
                    raise ValueError("Invalid number format: expected digit after '.'")

                while self.peek.isdigit():
                    self.advance()
                return float(self.src[start_pos: self.pos+1])

        return int(self.src[start_pos: self.pos+1])

    def skip_whitespace(self):
        # skip all whitespace characters.
        while self.current_char in [' ', '\n', '\t']:
            self.advance()

    def skip_comment(self):
        # c-style commenting.
        if self.current_char == '/' and self.peek == '/':
            while self.current_char != '\n':
                self.advance()

    def get_token(self):

        token_type = TokenType.NONE
        ## tokenizer not working properly.
        while self.current_char != '\0':
            self.skip_whitespace()
            self.skip_comment()
            if self.current_char.isdigit():
                num = self.number()
                if isinstance(num, int):
                    token_type = TokenType.INT
                else:
                    token_type = TokenType.FLOAT

                self.advance()
                return Token(token_type, num)

            elif self.current_char.isalpha():
                # check if keyword or operator, assume identifier by default.
                word = self.word()
                token_type = TokenType.ID

                match (word.upper()):
                    case "RET":
                        token_type = TokenType.RETURN
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

                    case "ADD":
                        token_type = TokenType.ADD
                    case "SUB":
                        token_type = TokenType.SUB
                    case "MUL":
                        token_type = TokenType.MUL
                    case "DIV":
                        token_type = TokenType.DIV

                    case "NOT":
                        token_type = TokenType.NOT
                    case "AND":
                        token_type = TokenType.AND
                    case "OR":
                        token_type = TokenType.OR

                    case "BOOL":
                        token_type = TokenType.VAR
                    case "INT":
                        token_type = TokenType.VAR
                    case "FLOAT":
                        token_type = TokenType.VAR
                    case "STR":
                        token_type = TokenType.VAR

                    case "FUNC":
                        token_type = TokenType.FUNC
                    case "END":
                        token_type = TokenType.END

                    case "IF":
                        token_type = TokenType.IF
                    case "ELSE":
                        token_type = TokenType.ELSE
                    case "FI":
                        token_type = TokenType.FI
                    case "WHILE":
                        token_type = TokenType.WHILE
                    case "DO":
                        token_type = TokenType.DO

                    case _:
                        if word in ('true', 'false'):
                            token_type = TokenType.BOOL

                # if word did not match any keyword, return identifier.
                #self.advance()
                return Token(token_type, word)

            else:
                # symbol handling. check if symbol is valid.
                symbol = self.current_char
                if symbol in ['(', ')', '{', '}', '&', '|', '=', '!', '>', '<', ':', ';', "'" ,'"'] \
                        or symbol in ['+', '-', '*', '/']:
                    match (symbol):
                        case '(':
                            token_type = TokenType.LPAREN
                        case ')':
                            token_type = TokenType.RPAREN
                        case '{':
                            token_type = TokenType.LBRACE
                        case '}':
                            token_type = TokenType.RBRACE
                        case '[':
                            token_type = TokenType.LBRACK
                        case ']':
                            token_type = TokenType.RBRACK

                        case ':':
                            token_type = TokenType.ASSIGN
                        case ';':
                            token_type = TokenType.SEMI


                        case '&':
                            token_type = TokenType.AND
                        case '|':
                            token_type = TokenType.OR


                        case '=':
                            token_type = TokenType.EQ
                        case '!':
                            if self.peek == '=':
                                token_type = TokenType.NQ
                                self.advance()
                                symbol += '='
                            else:
                                token_type = TokenType.NOT
                        case '>':
                            if self.peek == '=':
                                token_type = TokenType.GQ
                                self.advance()
                                symbol += '='
                            else:
                                token_type = TokenType.GT
                        case '<':
                            if self.peek == '=':
                                token_type = TokenType.LQ
                                self.advance()
                                symbol += '='
                            else:
                                token_type = TokenType.LT

                        case '+':
                            if self.peek.isdigit():
                                token_type = TokenType.POS
                                #return Token(TokenType.NUMBER, self.number())
                            else:
                                token_type = TokenType.ADD
                        case '-':
                            if self.peek.isdigit():
                                token_type = TokenType.NEG
                                #return Token(TokenType.NUMBER, -1 * self.number())
                            else:
                                token_type = TokenType.SUB
                        case '*':
                            token_type = TokenType.MUL
                        case '/':
                            token_type = TokenType.DIV
                        case "'":
                            token_type = TokenType.CHAR
                            symbol = self.char()
                        case '"':
                            token_type = TokenType.STR
                            symbol = self.string()

                    self.advance()
                    return Token(token_type, symbol)


                elif symbol == '\\':
                    self.advance()
                    return Token(token_type, symbol)

                elif symbol in [' ', '\n', '\t'] or symbol == '/' and self.peek == '/':
                    continue

                elif symbol == '\0':
                    break

                else:
                    raise ValueError(f"Invalid character: {symbol}")




        return Token(TokenType.EOF, '')


if __name__ == '__main__':
    sun = Lexer("tomson.skt")

    while sun.current_char != '\0':
        print(sun.get_token())
