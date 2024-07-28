from enum import Enum
from dataclasses import dataclass

from tokens import iota

class ErrorCode(Enum):
    UNEXPECTED_TOKEN = iota(True)
    ID_NOT_FOUND = iota()

@dataclass
class Error(Exception):
    code: ErrorCode
    message: str

    def __str__(self):
        return f"{self.code.name}: {self.message}"


if __name__ == "__main__":
    e = Error(ErrorCode.UNEXPECTED_TOKEN, "Unexpected token")
    print(e)
