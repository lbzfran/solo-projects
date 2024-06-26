
# Goals
Create a turing complete, stack based programming language in c.

SPACE Separated. keywords and values are separated by space(s).


# Features
The program will be stored in a stack array, where execution will be done
for each element in the array.
Keywords:
PUSH: pushes an expression to the stack.
POP : sends the top value to the output.
ADD : takes the top two (last two) values, adds them, and pushes the result.
SUB : takes the top two values, subtracts them, and pushes the result.
MUL : takes the top two values, multiplies them, and pushes the result.

GRAMMAR:

program = {statement}
statement =
    | PUSH expression
    | IF comparison {statement} END
    | (POP | DUP | SWAP | OVER | ROT | EXCH)
    | (ADD | SUB | MUL | DIV | MOD)
comparison = expression expression (== | != | < | > | <= | >=)
expression = term term ( ADD | SUB | MUL | DIV | MOD )
factor = ( POS | NEG ) primary
primary = INT | FLOAT | IDENTIFIER
