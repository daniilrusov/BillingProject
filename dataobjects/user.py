from dataclasses import dataclass

@dataclass
class User:
    username: str
    balance: int
    tasks: list
