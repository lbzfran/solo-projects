from os import access, R_OK
from os.path import isfile
from tokens import TokenType
from lexer import Lexer
from parser import Parser
import sys



if len(sys.argv) > 1:
    for filename in sys.argv[1:]:
        if not (isfile(filename) and access(filename, R_OK)):
            print(f"[-] file {filename} does not exist/is not readable."); continue
        Parser(Lexer(filename)).program()

elif __name__ == "__main__":

    print("[*] Stackpiler loaded successfully.\nload | run | token | exit")
    load_file = False
    fns = []
    while True:
        input_string = input("> ")

        input_string = input_string.split()

        if input_string[0] == "load":
            if not len(input_string) > 1: print("[-] load [filepath]"); continue
            if not (isfile(input_string[1]) and access(input_string[1], R_OK)):
                print(f"[-] file {input_string[1]} does not exist/is not readable."); continue
            if input_string[1] in fns: print("[-] file already loaded."); continue
            fns.append(input_string[1])
            print("[+]")
        elif input_string[0] == "run":
            if not len(input_string) > 1: print("[-] run [filename]"); continue
            if not fns or not input_string[1] in fns: print("[-] file to run not loaded."); continue
            Parser(Lexer(input_string[1])).program()
            print("[+]")
        elif input_string[0] == "token":
            if not len(input_string) > 1: print("[-] token [filename]"); continue
            if not fns or not input_string[1] in fns: print("[-] file to run not loaded."); continue
            lex = Lexer(input_string[1])
            while lex.current_char != '\0': print(lex.get_token())
            print("[+]")
        elif input_string[0] == "exit":
            break



