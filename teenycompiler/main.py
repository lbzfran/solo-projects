from lexer import *
from emit import *
from parse import *
import sys

def main():
    print("Teeny Compiler loaded.")

    if len(sys.argv) != 2:
        sys.exit("ERROR: Compiler needs source file as argument.")
    with open(sys.argv[1], 'r') as infile:
        source = infile.read()

    lexer = Lexer(source)
    emitter = Emitter("out.c")
    parser = Parser(lexer, emitter)

    parser.program()
    emitter.writeFile()
    print("Parsing completed.")

if __name__ == "__main__":
    main()
