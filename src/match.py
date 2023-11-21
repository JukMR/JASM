"""
Main match module
"""

from enum import Enum, auto
from typing import List

from src.consumer import CompleteConsumer, InstructionObserverConsumer, StreamConsumer
from src.global_definitions import InputFileType
from src.matched_observers import MatchedObserver
from src.regex.yaml2regex import Yaml2Regex
from src.stringify_asm.abstracts.abs_observer import IInstructionObserver, IMatchedObserver
from src.stringify_asm.abstracts.asm_parser import AsmParser
from src.stringify_asm.abstracts.disassembler import Disassembler
from src.stringify_asm.implementations.null_disassembler import NullDisassembler
from src.stringify_asm.implementations.objdump.composable_producer import ComposableProducer, IInstructionProducer
from src.stringify_asm.implementations.objdump.objdump_disassembler import ObjdumpDisassembler
from src.stringify_asm.implementations.objdump.objdump_parser import ObjdumpParser
from src.stringify_asm.implementations.observers import RemoveEmptyInstructions

DEFAULT_FLAGS = "-d"


def get_user_observer() -> List[IInstructionObserver]:
    """Retrieve a list of user defined observers."""
    return []


def get_instruction_observers() -> List[IInstructionObserver]:
    """Retrieve a list of instruction observers."""

    observers: List[IInstructionObserver] = [RemoveEmptyInstructions()]
    observers.extend(get_user_observer())

    return observers


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


class ConsumerType(Enum):
    """Enum for the consumer type."""

    complete = auto()
    stream = auto()


def create_consumer(
    regex_rule: str, iMatchedObserver: IMatchedObserver, consumer_type: ConsumerType
) -> InstructionObserverConsumer:
    """Decide which consumer to create"""

    match consumer_type:
        case ConsumerType.complete:
            return CompleteConsumer(regex_rule=regex_rule, matched_observer=iMatchedObserver)
        case ConsumerType.stream:
            return StreamConsumer(regex_rule=regex_rule, matched_observer=iMatchedObserver)


def perform_matching(pattern_pathstr: str, input_file: str, input_file_type: InputFileType) -> bool | str:
    """Main function to perform regex matching on assembly or binary."""

    regex_rule = get_regex_rule(pattern_pathstr=pattern_pathstr)

    return do_matching_and_get_result(
        regex_rule=regex_rule, input_file=input_file, input_file_type=input_file_type, return_bool_result=True
    )


def get_regex_rule(pattern_pathstr: str) -> str:
    """Retrieve the regex rule from the pattern file"""
    regex_rule = Yaml2Regex(pattern_pathstr).produce_regex()

    return regex_rule


def do_matching_and_get_result(
    regex_rule: str,
    input_file: str,
    input_file_type: InputFileType,
    return_bool_result: bool = True,
) -> bool | str:
    """Main function to perform regex matching on assembly or binary."""

    matched_observer = MatchedObserver()

    # TODO: enable user to choose between stream and complete
    consumer = create_consumer(
        regex_rule=regex_rule, iMatchedObserver=matched_observer, consumer_type=ConsumerType.complete
    )

    # Consumer call observers
    observer_list = get_instruction_observers()

    for obs in observer_list:
        consumer.add_observer(obs)

    # Create producer
    producer = create_producer(file_type=input_file_type)

    # Do the processing
    producer.process_file(file=input_file, iConsumer=consumer)

    if return_bool_result:
        return matched_observer.matched
    return matched_observer.stringified_instructions
