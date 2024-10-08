# Goals

Create a turing complete, stack based programming language in python.

SPACE Separated. keywords and values are separated by space(s).

The next goal is to create a bytecode compilation that can be
interpreted by the machine.

# Notes

june 2024
Despite the effectiveness of the current parser, it lacks the ability to handle
loops and functions. As it stands, I will have to rewrite the parser to be able
to handle those cases effectively.

sept 2024
I've figured out an implementation that uses bytecode parsing instead, so I
will have to reformat the parser to read bytecode instead.

I will also require a bytecode emitter to be able to compile successfully.

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

program = {compound_statement}

compound_statement = statement_list

statement_list =
| statement
| statement SEMI statement_list

statement =
| expression
| compound_statement
| assignment_statement
| stack_statement
| empty

assignment_statement = variable ASSIGN expression

empty =

stack_statement =
| POP
| DUP
| SWAP
| OVER
| ROT
| EXCH

statement =
| PUSH expression
| IF comparison {statement} END
| (ADD | SUB | MUL | DIV | MOD)
comparison = expression expression (== | != | < | > | <= | >=)
expression =
| factor factor ( ADD | SUB | MUL | DIV | MOD )
| factor factor ( EQ | NE | LT | GT | LE | GE )
factor =
| LPAREN expression RPAREN
| variable
| POS factor
| NEG factor
| INT
| FLOAT
| BOOL
| STR

variable = ID
