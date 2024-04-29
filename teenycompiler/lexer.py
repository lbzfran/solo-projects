"""
lexer.py
given a string of code, it will iterate character by character to: * decide where each token starts/stops * what type of token it is.
If lexer fails, it will report an error for an invalid token.

"""
from token import *
import sys
class Lexer:
    def __init__(self, source):
        # lexer tracks current position of input string, and character at that position.

        self.source = source
        self.curChar = ''
        self.curPos = -1
        self.nextChar()

    # process next character
    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = '\0' # EOF
        else:
            self.curChar = self.source[self.curPos]

    # return lookahead character (without moving current position)
    def peek(self):
        if self.curPos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curPos+1]

    # invalid token found, print err and exit.
    def abort(self,msg):
        sys.exit("Lexing error. " + msg)

    # skip whitespace except newlines, which will indicate end of statement
    def skipWhitespace(self):
        while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
            self.nextChar()

    # skip comments in code
    def skipComment(self):
        if self.curChar == '#':
            while self.curChar != '\n':
                self.nextChar()

    # return next token
    def getToken(self):
        self.skipWhitespace()
        self.skipComment()
        token = None
        # check first character of token
        if self.curChar == '+':
            token = Token(self.curChar, TokenType.PLUS)	# Plus token.
        elif self.curChar == '-':
            token = Token(self.curChar, TokenType.MINUS)	# Minus token.
        elif self.curChar == '*':
            token = Token(self.curChar, TokenType.ASTERISK)	# Asterisk token.
        elif self.curChar == '/':
            token = Token(self.curChar, TokenType.SLASH)	# Slash token.
        elif self.curChar == '\n':
            token = Token(self.curChar, TokenType.NEWLINE)	# Newline token.
        elif self.curChar == '\0':
            token = Token('', TokenType.EOF)	# EOF token.
        elif self.curChar == '=':
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.EQEQ)
            else:
                token = Token(self.curChar, TokenType.EQ)
        elif self.curChar == '>':
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.GTEQ)
            else:
                token = Token(self.curChar, TokenType.GT)
        elif self.curChar == '<':
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.LTEQ)
            else:
                token = Token(self.curChar, TokenType.LT)
        elif self.curChar == '!':
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.NOTEQ)
            else:
                self.abort("Expected !=, got !" + self.peek())
        elif self.curChar == '\"':
            #get char between quotes
            self.nextChar()
            startPos = self.curPos
            
            while self.curChar != '\"':
                # does not allow special characters in string. no escape char, newlines, tabs, or %.
                if self.curChar == '\r' or self.curChar =='\n' or self.curChar == '\t' or self.curChar =='\\' or self.curChar == '%':
                    self.abort("Illegal character in string.")
                self.nextChar()

            tokText = self.source[startPos : self.curPos]
            token = Token(tokText, TokenType.STRING)
        elif self.curChar.isdigit():

            startPos = self.curPos
            while self.peek().isdigit():
                self.nextChar()
            if self.peek() == '.':
                self.nextChar()

                if not self.peek().isdigit():
                    #ERROR
                    self.abort("Illegal character in number.")
                while self.peek().isdigit():
                    self.nextChar()

            tokText = self.source[startPos : self.curPos + 1]
            token = Token(tokText, TokenType.NUMBER)

        elif self.curChar.isalpha():

            startPos = self.curPos
            while self.peek().isalnum():
                self.nextChar()

            tokText = self.source[startPos : self.curPos + 1]
            keyword = Token.checkIfKeyword(tokText)
            if keyword == None:
                token = Token(tokText, TokenType.IDENT)
            else:
                token = Token(tokText, keyword)
        else:
            # Unknown token!
            self.abort("Unknown token: " + self.curChar)
        
        self.nextChar()
        return token

    
if __name__ == "__main__":
    source = "IF+-123 foo*THEN/"
    lexer = Lexer(source)

    token = lexer.getToken()
    while token.kind != TokenType.EOF:
        print(token.kind)
        token = lexer.getToken()