"""
Main match module
"""

from enum import Enum, auto
from typing import List, Optional

from src.consumer import CompleteConsumer, InstructionObserverConsumer, StreamConsumer
from src.global_definitions import EnumDisasStyle, InputFileType
from src.matched_observers import MatchedObserver
from src.regex.yaml2regex import Yaml2Regex
from src.stringify_asm.abstracts.abs_observer import IInstructionObserver, IMatchedObserver
from src.stringify_asm.abstracts.asm_parser import AsmParser
from src.stringify_asm.abstracts.disassembler import Disassembler
from src.stringify_asm.implementations.composable_producer import ComposableProducer, IInstructionProducer
from src.stringify_asm.implementations.gnu_objdump.gnu_objdump_disassembler import GNUObjdumpDisassembler
from src.stringify_asm.implementations.gnu_objdump.gnu_objdump_parser import ObjdumpParser
from src.stringify_asm.implementations.gnu_objdump.gnu_objdump_parser_manual import ObjdumpParserManual
from src.stringify_asm.implementations.null_disassembler import NullDisassembler
from src.stringify_asm.implementations.observers import RemoveEmptyInstructions

DEFAULT_FLAGS = "-d"


class ConsumerType(Enum):
    """Enum for the consumer type."""

    complete = auto()
    stream = auto()


class ObserverBuilder:
    """Observers retriever."""

    @staticmethod
    def get_user_observer() -> List[IInstructionObserver]:
        """Retrieve a list of user defined observers."""
        return []

    def get_instruction_observers(self) -> List[IInstructionObserver]:
        """Retrieve a list of instruction observers."""

        observers: List[IInstructionObserver] = [RemoveEmptyInstructions()]
        observers.extend(self.get_user_observer())

        return observers


class ConsumerBuilder:
    """Builder for the consumer."""

    @staticmethod
    def build(
        regex_rule: str, iMatchedObserver: IMatchedObserver, consumer_type: ConsumerType
    ) -> InstructionObserverConsumer:
        """Decide which consumer to create"""

        match consumer_type:
            case ConsumerType.complete:
                return CompleteConsumer(regex_rule=regex_rule, matched_observer=iMatchedObserver)
            case ConsumerType.stream:
                return StreamConsumer(regex_rule=regex_rule, matched_observer=iMatchedObserver)


class ProducerBuilder:
    """Builder for the producer."""

    @staticmethod
    def build(file_type: InputFileType, assembly_style: Optional[EnumDisasStyle] = None) -> IInstructionProducer:
        """Create a producer based on the file type."""

        # Logic for choosing diferent type of parser should be here

        # parser: AsmParser = ObjdumpParser()
        parser: AsmParser = ObjdumpParserManual()
        disassembler: Disassembler

        # Logic for choosing diferent type of disassembler should be here
        match file_type:
            case InputFileType.binary:
                disassembler = GNUObjdumpDisassembler(enum_disas_style=assembly_style)
            case InputFileType.assembly:
                disassembler = NullDisassembler()

            case _:
                raise ValueError("Either assembly or binary must be provided")

        return ComposableProducer(disassembler=disassembler, parser=parser)


class MasterOfPuppets:
    """Main class which is responsible for the execution of the program."""

    def perform_matching(self, pattern_pathstr: str, input_file: str, input_file_type: InputFileType) -> bool | str:
        """Main function to perform regex matching on assembly or binary."""

        regex_rule = self._get_regex_rule(pattern_pathstr=pattern_pathstr)

        file_style = self.get_file_style(pattern_pathstr=pattern_pathstr)

        return self._do_matching_and_get_result(
            regex_rule=regex_rule,
            assembly_style=file_style,
            input_file=input_file,
            input_file_type=input_file_type,
            return_bool_result=True,
        )

    @staticmethod
    def _get_regex_rule(pattern_pathstr: str) -> str:
        """Retrieve the regex rule from the pattern file"""
        regex_rule = Yaml2Regex(pattern_pathstr).produce_regex()

        return regex_rule

    def get_file_style(self, pattern_pathstr: str) -> Optional[EnumDisasStyle]:
        """Retrieve the file style from the pattern file"""
        file_stype = Yaml2Regex(pattern_pathstr).get_assembly_style()

        return file_stype

    @staticmethod
    def _do_matching_and_get_result(
        regex_rule: str,
        assembly_style: Optional[EnumDisasStyle],
        input_file: str,
        input_file_type: InputFileType,
        return_bool_result: bool = True,
    ) -> bool | str:
        """Main function to perform regex matching on assembly or binary."""

        matched_observer = MatchedObserver()

        consumer = ConsumerBuilder().build(
            regex_rule=regex_rule, iMatchedObserver=matched_observer, consumer_type=ConsumerType.complete
        )

        # Consumer call observers
        observer_list = ObserverBuilder().get_instruction_observers()

        for obs in observer_list:
            consumer.add_observer(obs)

        # Create producer
        producer = ProducerBuilder().build(file_type=input_file_type, assembly_style=assembly_style)

        # Do the processing
        producer.process_file(file=input_file, iConsumer=consumer)

        if return_bool_result:
            return matched_observer.matched
        return matched_observer.stringified_instructions
