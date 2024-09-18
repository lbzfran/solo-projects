import sys

from lexer import Lexer
from tokens import Token, TokenType


def request_values(token):
    # validates an instruction token,
    # and returns the number of values it needs.
    # returns -1 if invalid.
    if token.type == TokenType.PUSH:
        return 1
    if token.type == TokenType.VAR:
        # <VAR> id assign expr
        return 3
    if token.type == TokenType.ADD:
        return 0
    if token.type == TokenType.SUB:
        return 0
    if token.type == TokenType.MUL:
        return 0
    if token.type == TokenType.DIV:
        return 0
    if token.type == TokenType.POP:
        return 0
    return -1


variables = 0
var_table = {}


def compile(token_list: list):
    # optimizes per statement, ending with a semicolon.

    emit = []
    instruction = token_list.pop(0)

    reqs = request_values(instruction)

    if reqs < 0:
        raise ValueError(f"invalid instruction: {instruction}")

    emit.append(f"{instruction.type.value:02X}")

    # VAR ID ASSIGN expr

    while reqs > 0:
        if token_list[0].type == TokenType.ID:

            # ID
            # if exists:
            #  return value
            # else:
            #  validate instruction as "VAR"
            #  if true, add to var_table
            #  else raise exception

            id = token_list.pop(0).val
            reqs -= 1

            if id not in var_table.keys():  # if does not exist
                if instruction.type == TokenType.VAR:
                    token_list.pop(0)  # remove ASSIGN
                    reqs -= 1

                    var_table[id] = f"{token_list.pop(0).val:02X}"
                    reqs -= 1

                else:
                    raise ValueError(f"invalid instruction: {instruction}")
            emit.append(f"{var_table[id]}")

        else:  # assume constant
            emit.append(f"{token_list.pop(0).val:02X}")
            reqs -= 1

    return emit


def emitter(token: Token):
    # converts a token into bytecode.
    # given example: PUSH 1
    global constants

    if token.type == TokenType.PUSH:
        constants = 1
        return f"{token.type.value:02X}"
    if token.type == TokenType.ASSIGN and constants > 0:
        return ""
    elif token.type == TokenType.ID:
        global variables
        global var_table

        if token.val not in var_table.keys():
            var_table[token.val] = f"{variables:02X}"
            variables += 1
        return f"{token.type.value:02X} {var_table[token.val]}"

    elif constants > 0:
        constants -= 1
        return f"{token.val:02X}"

    return f"{token.type.value:02X}"


if __name__ == "__main__":

    sun = Lexer("tomson.skt")

    hexcodes: list[str] = []
    statement = []
    while sun.current_char != "\0":
        if sun.current_char != ";":
            statement.append(sun.get_token())
        else:
            # clear semi
            sun.get_token()

            x = compile(statement)

            for i in x:
                hexcodes.append(i)

    filename = "out.skt"
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    file = open(filename, "w")
    count = 0
    for i in hexcodes:
        if count > 40:
            file.write("\n")
            count = 0
        file.write(f"{i} ")
        count += 1
    file.write("\n")
    file.close()
