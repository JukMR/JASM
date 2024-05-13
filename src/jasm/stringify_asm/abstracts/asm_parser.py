from abc import ABC, abstractmethod

from src.jasm.match.abstracts.i_consumer import IConsumer


class AsmParser(ABC):
    @abstractmethod
    def parse(self, file: str, iConsumer: IConsumer) -> None:
        "Method for parsing instruction from given assembly"
