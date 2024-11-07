from abc import ABC, abstractmethod
from jasm.consumer import IConsumer


class AsmParser(ABC):
    @abstractmethod
    def parse(self, file: str, iConsumer: IConsumer) -> None:
        "Method for parsing instruction from given assembly"
