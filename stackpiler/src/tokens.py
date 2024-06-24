from enum import Enum
from dataclasses import dataclass

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

    # control flow
    LBRACE = iota() # { -- func block. implicit
    RBRACE = iota() # }
    LPAREN = iota() # ( -- parameter
    RPAREN = iota() # )
    LBRACK = iota() # [ -- list
    RBRACK = iota() # ]

    # operators
    # unary operators
    POS = iota() # [+]a -- [a]
    NEG = iota() # [-]a -- [-a]

    # binary operators
    ADD = iota() # a b [+] = b + a
    SUB = iota() # a b [-] = b - a
    MUL = iota() # a b [*] = b * a
    DIV = iota() # a b [/ or //] = b / a
    MOD = iota() # a b [%] = b % a


    ### 1 1 ADD 2 MUL 4 MUL = 16
    ### (((1 1 ADD) 2 MUL) 4 MUL)

    ### expression
    ###

    NOT = iota() # z [!] = not Z
    AND = iota() # y z [&] = y and z
    OR = iota()  # y z [|] = y or z

    EQ = iota() # a b [=] = a == b
    NQ = iota() # a b [!=] = a != b
    GT = iota() # a b [>] = a > b
    GQ = iota() # a b [>=] = a >= b
    LT = iota() # a b [<] = a < b
    LQ = iota() # a b [<=] = a <= b

    # types
    INT = iota() # [0-9] # dynamically typed from numbers. can be explicitly casted.
    FLOAT = iota() # [0-9].[0-9]. implicit, but can be explicitly casted.

    VAR = iota() # var IDENTIFIER
    FUNC = iota() # func IDENTIFIER block end
    END = iota() # end of block declaration. used by: func, if/else, while/do

    IF = iota() # if (condition) block end
    ELSE = iota() # else block end

    WHILE = iota() # while (condition) block end
    DO = iota() # do block while (condition) end. implicit if while comes first.

    IDENTIFIER = iota() # [a-zA-Z] # variable or function name.
    COMMENT = iota() # //

    RETURN = iota() # return

    EOF = iota()

@dataclass(repr=False)
class Token:
    type: TokenType
    val: str | int | float | None

    def __str__(self):
        return f"Token({self.type}, {self.val})"
