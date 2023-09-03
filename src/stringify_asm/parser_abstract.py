"Main abstract Dissasembler class"

from abc import ABC, abstractmethod

from src.global_definitions import PathStr


class Parser(ABC):
    "Main parser base abstract class"

    def __init__(self, assembly_pathstr: PathStr) -> None:
        self.assembly_pathstr = assembly_pathstr

    @abstractmethod
    def parse(self) -> str:
        "Method for parsing instruction from given assembly"
