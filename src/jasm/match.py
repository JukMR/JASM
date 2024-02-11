"""
Main match module
"""

from enum import Enum, auto
from typing import List, Optional

from jasm.consumer import CompleteConsumer, InstructionObserverConsumer, StreamConsumer
from jasm.global_definitions import (
    DisassStyle,
    InputFileType,
    MatchingReturnMode,
    ValidAddrRange,
    MatchingSearchMode,
)
from jasm.matched_observers import MatchedObserver
from jasm.regex.yaml2regex import Yaml2Regex
from jasm.stringify_asm.abstracts.abs_observer import IInstructionObserver, IMatchedObserver, Instruction
from jasm.stringify_asm.abstracts.asm_parser import AsmParser
from jasm.stringify_asm.abstracts.disassembler import Disassembler
from jasm.stringify_asm.implementations.composable_producer import ComposableProducer, IInstructionProducer
from jasm.stringify_asm.implementations.gnu_objdump.gnu_objdump_disassembler import GNUObjdumpDisassembler
from jasm.stringify_asm.implementations.gnu_objdump.gnu_objdump_parser_manual import ObjdumpParserManual
from jasm.stringify_asm.implementations.null_disassembler import NullDisassembler
from jasm.stringify_asm.implementations.observers import RemoveEmptyInstructions


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
        regex_rule: str,
        iMatchedObserver: IMatchedObserver,
        consumer_type: ConsumerType,
        matching_mode: MatchingSearchMode,
    ) -> InstructionObserverConsumer:
        """Decide which consumer to create"""

        match consumer_type:
            case ConsumerType.complete:
                return CompleteConsumer(
                    regex_rule=regex_rule, matched_observer=iMatchedObserver, matching_mode=matching_mode
                )
            case ConsumerType.stream:
                return StreamConsumer(regex_rule=regex_rule, matched_observer=iMatchedObserver)


class ProducerBuilder:
    """Builder for the producer."""

    @staticmethod
    def build(
        file_type: InputFileType, assembly_style: Optional[DisassStyle] = DisassStyle.att
    ) -> IInstructionProducer:
        """Create a producer based on the file type."""

        # Logic for choosing diferent type of parser should be here

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

    def perform_matching(
        self,
        pattern_pathstr: str,
        input_file: str,
        input_file_type: InputFileType,
        matching_mode: MatchingSearchMode = MatchingSearchMode.first_find,
        return_mode: MatchingReturnMode = MatchingReturnMode.bool,
    ) -> bool | str | List[str]:
        """Main function to perform regex matching on assembly or binary."""

        yaml2_regex_instance = Yaml2Regex(pattern_pathstr)

        regex_rule = self._get_regex_rule(yaml_2_regex_instance=yaml2_regex_instance)

        disass_style = self.get_disass_style(yaml_2_regex_instance=yaml2_regex_instance)

        valid_addr_range = self.get_file_valid_addr_range(yaml_2_regex_instance=yaml2_regex_instance)

        return self._do_matching_and_get_result(
            regex_rule=regex_rule,
            assembly_style=disass_style,
            input_file=input_file,
            input_file_type=input_file_type,
            valid_addr_range=valid_addr_range,
            matching_mode=matching_mode,
            return_mode=return_mode,
        )

    @staticmethod
    def _get_regex_rule(yaml_2_regex_instance: Yaml2Regex) -> str:
        """Retrieve the regex rule from the pattern file"""
        regex_rule = yaml_2_regex_instance.produce_regex()

        return regex_rule

    @staticmethod
    def get_disass_style(yaml_2_regex_instance: Yaml2Regex) -> Optional[DisassStyle]:
        """Retrieve the file style from the pattern file"""
        file_stype = yaml_2_regex_instance.get_assembly_style()

        return file_stype

    @staticmethod
    def get_file_valid_addr_range(yaml_2_regex_instance: Yaml2Regex) -> Optional[ValidAddrRange]:
        """Retrieve the file style from the pattern file"""
        file_valid_addr_range = yaml_2_regex_instance.get_valid_addr_range()

        return file_valid_addr_range

    @staticmethod
    def _do_matching_and_get_result(
        regex_rule: str,
        assembly_style: Optional[DisassStyle],
        input_file: str,
        input_file_type: InputFileType,
        matching_mode: MatchingSearchMode = MatchingSearchMode.first_find,
        valid_addr_range: Optional[ValidAddrRange] = None,
        return_mode: MatchingReturnMode = MatchingReturnMode.bool,
    ) -> bool | str | List[str]:
        """Main function to perform regex matching on assembly or binary."""

        matched_observer = MatchedObserver()

        consumer = ConsumerBuilder().build(
            regex_rule=regex_rule,
            iMatchedObserver=matched_observer,
            consumer_type=ConsumerType.complete,
            matching_mode=matching_mode,
        )

        # Consumer call observers
        observer_list = ObserverBuilder().get_instruction_observers()

        if valid_addr_range:
            valid_addr_observer = get_valid_addr_observer(valid_addr_range)
            observer_list.append(valid_addr_observer)

        for obs in observer_list:
            consumer.add_observer(obs)

        # Create producer
        producer = ProducerBuilder().build(file_type=input_file_type, assembly_style=assembly_style)

        # Do the processing
        producer.process_file(file=input_file, iConsumer=consumer)

        match return_mode:
            case MatchingReturnMode.bool:
                return matched_observer.matched
            case MatchingReturnMode.matched_addrs_list:
                # This mode implies that if the list is not empty, then the match was successful
                return matched_observer.addr_list
            case MatchingReturnMode.all_instructions_string:
                return matched_observer.stringified_instructions

        raise ValueError("Invalid return mode")


def get_valid_addr_observer(valid_addr_range: ValidAddrRange) -> IInstructionObserver:
    """Get the valid address observer"""
    return ValidAddrObserver(valid_addr_range)


class ValidAddrObserver(IInstructionObserver):
    """Valid address observer"""

    def __init__(self, valid_addr_range: ValidAddrRange) -> None:
        self.addr_range = valid_addr_range

    def observe_instruction(self, inst: Instruction) -> Optional[Instruction]:
        """Main observer method"""

        inst_addr_jump = inst.operands[0] if inst.operands else None
        if inst_addr_jump and self.addr_range.is_in_range(inst.addr):
            if inst.mnemonic in ["call", "jmp", "jne", "je", "jg", "jge", "jl", "jle", "jz", "jnz"]:
                return Instruction(addr=inst.addr, mnemonic=inst.mnemonic, operands=["valid_addr"])
        return inst
