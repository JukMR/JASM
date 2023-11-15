"""
Main match module
"""

from enum import Enum, auto
import re
from typing import Any, List, Optional, Sequence

from src.consumer import CompleteConsumer, InstructionObserverConsumer, StreamConsumer
from src.logging_config import logger
from src.measure_performance import measure_performance
from src.regex.yaml2regex import Yaml2Regex
from src.stringify_asm.abstracts.abs_observer import IConsumer, IInstructionObserver, IMatchedObserver, Instruction
from src.stringify_asm.abstracts.asm_parser import AsmParser
from src.stringify_asm.abstracts.disassembler import Disassembler
from src.stringify_asm.implementations.null_disassembler import NullDisassembler
from src.stringify_asm.implementations.objdump.ComposableProducer import ComposableProducer, IInstructionProducer
from src.stringify_asm.implementations.objdump.objdump_disassembler import ObjdumpDisassembler
from src.stringify_asm.implementations.objdump.objdump_parser import ObjdumpParser
from src.stringify_asm.implementations.observers import RemoveEmptyInstructions

TMP_ASSEMBLY_PATH = "tmp_dissasembly.s"
DEFAULT_FLAGS = "-d"


@measure_performance(perf_title="Run regex")
def execute_regex_on_assembly(regex_rule: str, assembly_string: str) -> List[Any]:
    """Execute the regex pattern on the provided assembly string."""
    return re.findall(pattern=regex_rule, string=assembly_string)


def get_instruction_observers() -> List[IInstructionObserver]:
    """Retrieve a list of instruction observers."""

    # TODO: add the observers from the user
    # user_observers = get_user_observer()

    return [RemoveEmptyInstructions()]


class InputFileType(Enum):
    binary = auto()
    assembly = auto()


def create_producer(file_type: InputFileType) -> IInstructionProducer:
    """Decide"""

    disassembler: Disassembler
    parser: AsmParser = ObjdumpParser()

    match file_type:
        case InputFileType.binary:
            disassembler = ObjdumpDisassembler(flags=DEFAULT_FLAGS)
        case InputFileType.assembly:
            disassembler = NullDisassembler()

        case _:
            raise ValueError("Either assembly or binary must be provided")

    return ComposableProducer(disassembler=disassembler, parser=parser)


class MatchedObserver(IMatchedObserver):
    def __init__(self) -> None:
        self._matched = False

    @property
    def matched(self) -> bool:
        return self._matched

    """Observer that logs the matched address"""

    # @override
    def regex_matched(self, addr: str) -> None:
        self._matched = True
        logger.info("Matched address: %s", addr)

    # @override
    def finalize(self) -> None:
        if not self._matched:
            logger.info("RESULT: Pattern not found\n")


def create_consumer(regex_rule: str, iMatchedObserver: IMatchedObserver) -> InstructionObserverConsumer:
    """Decide"""

    # TODO: implement the decision from the user for which consumer to use
    return CompleteConsumer(regex_rule=regex_rule, matched_observer=iMatchedObserver)


def perform_matching(
    pattern_pathstr: str,
    input_file: str,
    input_file_type: InputFileType,
) -> bool:
    """Main function to perform regex matching on assembly or binary."""

    # Produce directive regex rule
    regex_rule = Yaml2Regex(pattern_pathstr=pattern_pathstr).produce_regex()

    matched_observer = MatchedObserver()
    # TODO: enable user to choose between stream and complete
    consumer = create_consumer(regex_rule=regex_rule, iMatchedObserver=matched_observer)

    # Consumer call observers
    observer_list = get_instruction_observers()

    for obs in observer_list:
        consumer.add_observer(instruction_observer=obs)

    # Create producer
    producer = create_producer(file_type=input_file_type)

    # Do the processing
    producer.process_file(file=input_file, iConsumer=consumer)

    return matched_observer.matched
