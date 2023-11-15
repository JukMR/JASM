from abc import ABC, abstractmethod
from typing import List
from src.consumer import IConsumer


class AsmParser(ABC):
    @abstractmethod
    def parse(self, file: str, iConsumer: IConsumer) -> None:
        "Method for parsing instruction from given assembly"
