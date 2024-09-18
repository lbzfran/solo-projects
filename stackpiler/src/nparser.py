from tokens import TokenType


def run(src: str):

    file = open(src, "r")
    temp = file.read()
    file.close()

    program = " ".join(temp.split("\n")).split(" ")

    print(program)


if __name__ == "__main__":
    run("out.skt")
