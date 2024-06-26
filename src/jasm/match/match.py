"""
Main match module
"""

from typing import List, Optional

from jasm.global_definitions import (
    ConsumerType,
    DisassStyle,
    Instruction,
    MatchConfig,
    MatchingReturnMode,
    ValidAddrRange,
)
from jasm.match.implementations.consumer_builder import ConsumerBuilder
from jasm.match.implementations.matched_observers import MatchedObserver
from jasm.regex.yaml2regex import Yaml2Regex
from jasm.stringify_asm.abstracts.i_instruction_observer import IInstructionObserver
from jasm.stringify_asm.implementations.observers import RemoveEmptyInstructions
from jasm.stringify_asm.implementations.producer_builder import ProducerBuilder


class MasterOfPuppets:
    """Main class which is responsible for the execution of the program."""

    def __init__(self, match_config: MatchConfig) -> None:
        self.match_config = match_config

        yaml_2_regex_instance = Yaml2Regex(self.match_config.pattern_pathstr, macros_from_terminal=match_config.macros)

        self.regex_rule = yaml_2_regex_instance.produce_regex()
        self.disass_style = yaml_2_regex_instance.get_assembly_style()
        self.valid_addr_range = yaml_2_regex_instance.get_valid_addr_range()

    def perform_matching(self) -> bool | str | List[str]:
        """Main function to perform regex matching on assembly or binary."""

        return self._do_matching_and_get_result(
            regex_rule=self.regex_rule,
            assembly_style=self.disass_style,
        )

    def _do_matching_and_get_result(
        self,
        regex_rule: str,
        assembly_style: DisassStyle,
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
        observer_list = self.prepare_observers()

        for obs in observer_list:
            consumer.add_observer(obs)

        # Create producer
        producer = ProducerBuilder().build(file_type=self.match_config.input_file_type, assembly_style=assembly_style)

        # Do the processing
        producer.process_file(file=self.match_config.input_file, iConsumer=consumer)

        match self.match_config.return_mode:
            case MatchingReturnMode.bool:
                return_matched: bool = matched_observer.matched
                return return_matched

            case MatchingReturnMode.matched_addrs_list:
                # This mode implies that if the list is not empty, then the match was successful
                return_addr_list: list[str] = matched_observer.addr_list
                return return_addr_list

            case MatchingReturnMode.all_instructions_string:
                return_all_instructions_string: str = matched_observer.stringified_instructions
                return return_all_instructions_string

        raise ValueError("Invalid return mode")

    def prepare_observers(self) -> List[IInstructionObserver]:
        """Prepare the observers for the matching."""

        observer_list = ObserverBuilder().get_instruction_observers()

        if self.valid_addr_range:
            valid_addr_observer = ValidAddrObserver(self.valid_addr_range)
            observer_list.append(valid_addr_observer)

        return observer_list


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


class ValidAddrObserver(IInstructionObserver):  # type: ignore
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
