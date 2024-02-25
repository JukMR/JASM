"""
Main match module
"""

from enum import Enum, auto
from typing import List, Optional

from jasm.consumer import CompleteConsumer, InstructionObserverConsumer
from jasm.global_definitions import (
    DisassStyle,
    InputFileType,
    MatchConfig,
    MatchingReturnMode,
    MatchingSearchMode,
    ValidAddrRange,
    Instruction,
)
from jasm.matched_observers import MatchedObserver
from jasm.regex.yaml2regex import Yaml2Regex
from jasm.stringify_asm.abstracts.abs_observer import IInstructionObserver, IMatchedObserver
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
        return_only_address: bool,
    ) -> InstructionObserverConsumer:
        """Decide which consumer to create"""

        match consumer_type:
            case ConsumerType.complete:
                return CompleteConsumer(
                    regex_rule=regex_rule,
                    matched_observer=iMatchedObserver,
                    matching_mode=matching_mode,
                    return_only_address=return_only_address,
                )
            # TODO: implement this consumer
            # case ConsumerType.stream:
            #     return StreamConsumer(regex_rule=regex_rule, matched_observer=iMatchedObserver)

            case _:
                raise ValueError("Invalid consumer type")


class ProducerBuilder:
    """Builder for the producer."""

    @staticmethod
    def build(file_type: InputFileType, assembly_style: DisassStyle = DisassStyle.att) -> IInstructionProducer:
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

    def __init__(self, match_config: MatchConfig) -> None:
        self.match_config = match_config

        yaml_2_regex_instance = Yaml2Regex(self.match_config.pattern_pathstr, macros_from_args=match_config.macros)

        self.regex_rule = yaml_2_regex_instance.produce_regex()
        self.disass_style = yaml_2_regex_instance.get_assembly_style()
        self.valid_addr_range = yaml_2_regex_instance.get_valid_addr_range()

    def perform_matching(self) -> bool | str | List[str]:
        """Main function to perform regex matching on assembly or binary."""

        return self._do_matching_and_get_result(
            regex_rule=self.regex_rule,
            assembly_style=self.disass_style,
            valid_addr_range=self.valid_addr_range,
        )

    def _do_matching_and_get_result(
        self,
        regex_rule: str,
        assembly_style: DisassStyle,
        valid_addr_range: Optional[ValidAddrRange],
    ) -> bool | str | List[str]:
        """Main function to perform regex matching on assembly or binary."""

        matched_observer = MatchedObserver()

        consumer = ConsumerBuilder().build(
            regex_rule=regex_rule,
            iMatchedObserver=matched_observer,
            consumer_type=ConsumerType.complete,
            matching_mode=self.match_config.matching_mode,
            return_only_address=self.match_config.return_only_address,
        )

        # Consumer call observers
        observer_list = ObserverBuilder().get_instruction_observers()

        if valid_addr_range:
            valid_addr_observer = ValidAddrObserver(valid_addr_range)
            observer_list.append(valid_addr_observer)

        for obs in observer_list:
            consumer.add_observer(obs)

        # Create producer
        producer = ProducerBuilder().build(file_type=self.match_config.input_file_type, assembly_style=assembly_style)

        # Do the processing
        producer.process_file(file=self.match_config.input_file, iConsumer=consumer)

        match self.match_config.return_mode:
            case MatchingReturnMode.bool:
                return matched_observer.matched

            case MatchingReturnMode.matched_addrs_list:
                # This mode implies that if the list is not empty, then the match was successful
                return matched_observer.addr_list

            case MatchingReturnMode.all_instructions_string:
                return matched_observer.stringified_instructions

        raise ValueError("Invalid return mode")


class ValidAddrObserver(IInstructionObserver):
    """Valid address observer"""

    def __init__(self, valid_addr_range: ValidAddrRange) -> None:
        self.addr_range = valid_addr_range

    def observe_instruction(self, inst: Instruction) -> Optional[Instruction]:
        """Main observer method"""

        jump_mnemonics = ["call", "callq", "jmp", "jne", "je", "jg", "jge", "jl", "jle", "jz", "jnz"]
        inst_addr_jump = inst.operands[0] if inst.operands else None

        if inst_addr_jump is None:
            return inst

        # The instruction is a jmp or call
        if inst.mnemonic in jump_mnemonics:

            # Check if inst_addr is derefering a register
            # Not supporting this yet
            if "*" in inst_addr_jump:
                return inst

            if self.addr_range.is_in_range(inst_addr_jump):
                return Instruction(addr=inst.addr, mnemonic=inst.mnemonic, operands=["valid_addr"])
        return inst
