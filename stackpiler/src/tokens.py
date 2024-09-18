from dataclasses import dataclass
from enum import Enum


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
    PUSH = iota()  # a -- a ; implicit if var is defined, or constant is given.
    POP = iota()  # a --
    DUP = iota()  # a -- a a
    SWAP = iota()  # a b -- b a
    OVER = iota()  # a b -- a b a
    ROT = iota()  # a b c -- b c a

    # control flow
    LBRACE = iota()  # { -- func block. implicit
    RBRACE = iota()  # }
    LPAREN = iota()  # ( -- parameter
    RPAREN = iota()  # )
    LBRACK = iota()  # [ -- list
    RBRACK = iota()  # ]
    # SQUOTE = iota() # ' -- single quotes
    # DQUOTE = iota() # " -- double quotes

    # operators
    # unary operators
    POS = iota()  # [+]a -- [a]
    NEG = iota()  # [-]a -- [-a]

    # binary operators
    ADD = iota()  # a b [+] = b + a
    SUB = iota()  # a b [-] = b - a
    MUL = iota()  # a b [*] = b * a
    DIV = iota()  # a b [/ or //] = b / a
    MOD = iota()  # a b [%] = b % a

    ### 1 1 ADD 2 MUL 4 MUL = 16
    ### (((1 1 ADD) 2 MUL) 4 MUL)

    ### expression
    ###

    NOT = iota()  # [!]z = not z

    AND = iota()  # y z [&] = y and z
    OR = iota()  # y z [|] = y or z

    EQ = iota()  # a b [=] = a == b
    NQ = iota()  # a b [!=] = a != b
    GT = iota()  # a b [>] = a > b
    GQ = iota()  # a b [>=] = a >= b
    LT = iota()  # a b [<] = a < b
    LQ = iota()  # a b [<=] = a <= b

    # types
    BOOL = iota()  # [true, false] # derived from comparisons.
    INT = iota()  # [0-9] # dynamically typed from numbers. can be explicitly casted.
    FLOAT = iota()  # [0-9].[0-9]. implicit, but can be explicitly casted.
    ARR = iota()  # []. dynamic array.
    CHAR = iota()
    STR = iota()  # "[a-zA-Z0-9 ]" # explicit cast with ""

    VAR = iota()  # var COLON IDENTIFIER
    FUNC = iota()  # func IDENTIFIER block end
    END = iota()  # end of block declaration. used by: func, if/else, while/do

    ASSIGN = iota()  # : # variable assignment operator
    SEMI = iota()  # ; # statement separator

    IF = iota()  # if (condition) (compound_state) else (compound_state) fi
    ELSE = iota()  # else (compound_state) end
    FI = iota()  # end of if block.

    WHILE = iota()  # while (condition) (statement) end
    DO = iota()  # do block while (condition) end. implicit if while comes first.

    ID = iota()  # [a-zA-Z] # variable or function name.
    COMMENT = iota()  # //

    RETURN = iota()  # return

    EOF = iota()


@dataclass(repr=False)
class Token:
    type: TokenType
    val: str | int | float | None

    def __str__(self):
        return f"Token({self.type}, {self.val})"
