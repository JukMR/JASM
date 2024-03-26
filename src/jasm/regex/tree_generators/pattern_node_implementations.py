from itertools import permutations
from typing import List, Optional

from jasm.global_definitions import (
    IGNORE_INST_ADDR,
    OPTIONAL_COMMA,
    OPTIONAL_PERCENTAGE_CHAR,
    SKIP_TO_END_OF_PATTERN_NODE,
    RegisterCaptureSuffixs,
    TimeType,
)
from jasm.logging_config import logger
from jasm.regex.tree_generators.capture_group import (
    CaptureGroupIndexInstruction,
    CaptureGroupIndexOperand,
    CaptureGroupIndexRegister,
)
from jasm.regex.tree_generators.deref_classes import DerefObject, DerefObjectBuilder
from jasm.regex.tree_generators.pattern_node import PatternNode, PatternNode, get_pattern_node_name


class PatternNodeDerefProperty(PatternNode):

    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
            pattern_node_dict=pattern_node.pattern_node_dict,
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            root_node=pattern_node.root_node,
        )

    def get_regex(self) -> str:
        return self.process_deref_child()

    def process_deref_child(self) -> str:
        if self.children:
            assert isinstance(self.children, list)
            assert len(self.children) == 1

            child_regex = self.children[0].get_regex()
            return child_regex

        return str(self.name)


class PatternNodeDeref(PatternNode):

    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
            pattern_node_dict=pattern_node.pattern_node_dict,
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            root_node=pattern_node.root_node,
        )

    def get_regex(self) -> str:
        return self.process_deref()

    def process_deref(self) -> str:
        times_regex = TimeTypeBuilder().get_min_max_regex(times=self.times)

        deref_object: DerefObject = DerefObjectBuilder(self).build()
        deref_regex = deref_object.get_regex()

        if times_regex:
            return f"(?:{deref_regex},){times_regex}"
        return f"{deref_regex},"


# Get all the instruction


class PatternNodeTimes(PatternNode):
    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
            pattern_node_dict=pattern_node.pattern_node_dict,
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            root_node=pattern_node.root_node,
        )

    def get_regex(self) -> str:
        return ""


class PattterNodeCaptureGroupReferenceOperand(PatternNode):
    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
            pattern_node_dict=pattern_node.pattern_node_dict,
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            root_node=pattern_node.root_node,
        )

    def get_regex(self) -> str:
        return self.get_capture_group_reference_operand()

    @staticmethod
    def get_capture_group_reference_operand() -> str:
        return r"([^,|]+),"  # Get the operand value


class PatternNodeDerefPropertyCaptureGroupReference(PatternNode):
    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
            pattern_node_dict=pattern_node.pattern_node_dict,
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            root_node=pattern_node.root_node,
        )

    def get_regex(self) -> str:
        return self.get_capture_group_reference_deref()

    @staticmethod
    def get_capture_group_reference_deref() -> str:
        return r"([^,|]+)"  # Get the deref property value


class PatternNodeDerefPropertyCaptureGroupCall(PatternNode):
    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
            pattern_node_dict=pattern_node.pattern_node_dict,
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            root_node=pattern_node.root_node,
        )

    def get_regex(self) -> str:
        return self.get_capture_group_call_operand()

    # Capture group call
    def get_capture_group_call_operand(self) -> str:

        from jasm.regex.tree_generators.capture_group import CaptureGroupIndexOperand

        capture_group_instance = CaptureGroupIndexOperand(pattern_node=self)

        index = capture_group_instance.to_regex()

        return f"{index}"


class PatternNodeCaptureGroupReference(PatternNode):
    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
            pattern_node_dict=pattern_node.pattern_node_dict,
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            root_node=pattern_node.root_node,
        )

    def get_regex(self) -> str:
        return self.get_capture_group_reference()

    # Capture group reference
    @staticmethod
    def get_capture_group_reference() -> str:
        return rf"{IGNORE_INST_ADDR}([^|]+),\|"


class PatternNodeCaptureGroupCall(PatternNode):
    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
            pattern_node_dict=pattern_node.pattern_node_dict,
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            root_node=pattern_node.root_node,
        )

    def get_regex(self) -> str:
        return self.get_capture_group_call_instruction()

    # Capture group call
    def get_capture_group_call_instruction(self) -> str:

        capture_group_instance = CaptureGroupIndexInstruction(pattern_node=self)

        index = capture_group_instance.to_regex()

        return f"{index}"


class PatternNodeCaptureGroupCallOperand(PatternNode):
    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
            pattern_node_dict=pattern_node.pattern_node_dict,
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            root_node=pattern_node.root_node,
        )

    def get_regex(self) -> str:
        return self.get_capture_group_call_operand()

    # Capture group call
    def get_capture_group_call_operand(self) -> str:

        from jasm.regex.tree_generators.capture_group import CaptureGroupIndexOperand

        capture_group_instance = CaptureGroupIndexOperand(pattern_node=self)

        index = capture_group_instance.to_regex()

        return f"{index}"


class PatternNodeMnemonic(PatternNode):

    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
            pattern_node_dict=pattern_node.pattern_node_dict,
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            root_node=pattern_node.root_node,
        )

    def get_regex(self) -> str:
        return self.process_leaf()

    def process_leaf(self) -> str:
        name = self.name
        children = self.children
        times = self.times

        # Leaf is operand
        if not children and isinstance(self, PatternNodeOperand):
            # Is an operand
            return str(self.sanitize_operand_name(name))
        # Is a mnemonic with no operands
        print(f"Found a mnemonic with no operands in yaml rule: {self.name}")

        assert isinstance(children, List) or (not children), "Children must be a list or None"
        # This line shouldn't be necessary but the linter complains children could be dict
        assert not isinstance(children, dict), "Children must be a list or None"
        return RegexWithOperandsCreator(name=name, operands=children, times=times).generate_regex()

    def sanitize_operand_name(self, name: str | int) -> str | int:
        def _is_hex_operand(name: str | int) -> bool:
            if isinstance(name, int):
                return False
            if name.endswith("h"):
                tmp = name.removesuffix("h")
                try:
                    int(tmp, base=16)
                    return True
                except ValueError:
                    return False
            return False

        if _is_hex_operand(name):

            def _process_hex_operand(hex_operand_elem: str) -> str:
                operand_elem = "0x" + hex_operand_elem.removesuffix("h")
                return operand_elem

            # Match hex operand
            assert isinstance(name, str), "Operand name must be a string"
            return _process_hex_operand(name)

        pattern_nod_name = get_pattern_node_name(name)
        return pattern_nod_name


class PatternNodeOperand(PatternNode):

    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
            pattern_node_dict=pattern_node.pattern_node_dict,
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            root_node=pattern_node.root_node,
        )

    def get_regex(self) -> str:
        return self.process_leaf()

    def process_leaf(self) -> str:
        name = self.name
        children = self.children
        times = self.times

        # Leaf is operand
        if not children and isinstance(self, PatternNodeOperand):
            # Is an operand
            return str(self.sanitize_operand_name(name))
        # Is a mnemonic with no operands
        print(f"Found a mnemonic with no operands in yaml rule: {self.name}")

        assert isinstance(children, List) or (not children), "Children must be a list or None"
        # This line shouldn't be necessary but the linter complains children could be dict
        assert not isinstance(children, dict), "Children must be a list or None"
        return RegexWithOperandsCreator(name=name, operands=children, times=times).generate_regex()

    def sanitize_operand_name(self, name: str | int) -> str | int:
        def _is_hex_operand(name: str | int) -> bool:
            if isinstance(name, int):
                return False
            if name.endswith("h"):
                tmp = name.removesuffix("h")
                try:
                    int(tmp, base=16)
                    return True
                except ValueError:
                    return False
            return False

        if _is_hex_operand(name):

            def _process_hex_operand(hex_operand_elem: str) -> str:
                operand_elem = "0x" + hex_operand_elem.removesuffix("h")
                return operand_elem

            # Match hex operand
            assert isinstance(name, str), "Operand name must be a string"
            return _process_hex_operand(name)

        pattern_nod_name = get_pattern_node_name(name)
        return pattern_nod_name


class PatternNodeBranch(PatternNode):
    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
            pattern_node_dict=pattern_node.pattern_node_dict,
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            root_node=pattern_node.root_node,
        )

    def get_regex(self) -> str:
        return self.process_branch()

    def process_branch(self) -> str:
        child_regexes = self.process_children()
        times_regex: Optional[str] = TimeTypeBuilder().get_min_max_regex(times=self.times)
        return BranchProcessor().process_pattern_node(parent=self, child_regexes=child_regexes, times_regex=times_regex)

    def process_children(self) -> List[str]:
        if self.children:
            return [child.get_regex() for child in self.children]
        raise ValueError("Children list is empty")


class PatternNodeRoot(PatternNode):
    # This is the case of the root node $and
    # In here we will be save the state of the capture group references

    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
            pattern_node_dict=pattern_node.pattern_node_dict,
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            root_node=pattern_node.root_node,
        )

    def get_regex(self) -> str:
        return self.process_branch()

    def process_branch(self) -> str:
        child_regexes = self.process_children()
        times_regex: Optional[str] = TimeTypeBuilder().get_min_max_regex(times=self.times)
        return BranchProcessor().process_pattern_node(parent=self, child_regexes=child_regexes, times_regex=times_regex)

    def process_children(self) -> List[str]:
        if self.children:
            return [child.get_regex() for child in self.children]
        raise ValueError("Children list is empty")


class BranchProcessor:
    def process_pattern_node(
        self,
        parent: PatternNode,
        child_regexes: List[str],
        times_regex: Optional[str],
    ) -> str:
        """
        Process a pattern_node based on its name and child regexes.

        :param pattern_node_name: The name of the pattern_node.
        :param child_regexes: List of regexes from child pattern_nodes.
        :param times_regex: The regex string for repeating the match.
        :return: The processed pattern_node regex.
        """
        match parent.name:
            # Match case where pattern_node.name is and or pattern

            case "$and":
                return self.process_and(child_regexes, times_regex=times_regex)
            case "$or":
                return self.process_or(child_regexes, times_regex=times_regex)
            case "$not":
                return self.process_not(child_regexes, times_regex=times_regex)
            # case "$perm":
            #     return self.process_perm(child_regexes, times_regex=times_regex)
            case "$and_any_order":
                return self.process_and_any_order(child_regexes, times_regex=times_regex)
            case _:
                raise ValueError("Unknown pattern_node type")

    @staticmethod
    def process_and(child_regexes: List[str], times_regex: Optional[str]) -> str:
        if times_regex:
            return f"(?:{''.join(child_regexes) + SKIP_TO_END_OF_PATTERN_NODE}){times_regex}"
        return f"(?:{''.join(child_regexes)})"

    def process_or(self, child_regexes: List[str], times_regex: Optional[str]) -> str:
        if times_regex:
            return f"(?:{self.join_or_instructions(child_regexes)}){times_regex}"
        return f"(?:{self.join_or_instructions(child_regexes)})"

    @staticmethod
    def process_not(child_regexes: List[str], times_regex: Optional[str]) -> str:
        if times_regex:
            return f"(?:(?!{''.join(child_regexes)}){SKIP_TO_END_OF_PATTERN_NODE}){times_regex}"
        return f"(?:(?!{''.join(child_regexes)}){SKIP_TO_END_OF_PATTERN_NODE})"

    # @staticmethod
    # def process_perm(child_regexes: List[str], times_regex: Optional[str]) -> str:
    #     # TODO: implement this
    #     return ""

    def process_and_any_order(self, child_regexes: List[str], times_regex: Optional[str]) -> str:
        full_all_against_all_regex: List[List[str]] = self.generate_any_order_permutation(child_regexes)

        regex_list: List[str] = []
        for list_regex in full_all_against_all_regex:
            regex_list.append(self.process_and(child_regexes=list_regex, times_regex=None))

        return self.process_or(regex_list, times_regex)

    @staticmethod
    def generate_any_order_permutation(child_regexes: List[str]) -> List[List[str]]:
        # Generate all the permutation of this list
        return [list(permutation) for permutation in permutations(child_regexes)]

    @staticmethod
    def join_or_instructions(inst_list: List[str]) -> str:
        "Join instructions from list using operand to generate regex"

        assert inst_list, "There are no instructions to join"

        regex_instructions = [f"(?:{elem})" for elem in inst_list]

        joined_by_bar_instructions = "|".join(regex_instructions)

        return joined_by_bar_instructions


class TimeTypeBuilder:
    @staticmethod
    def get_min_max_regex(times: TimeType) -> Optional[str]:

        if times.min_times == 1 and times.max_times == 1:
            return None
        if times.min_times == times.max_times:
            return f"{{{times.min_times}}}"
        return f"{{{times.min_times},{times.max_times}}}"


class RegexWithOperandsCreator:
    def __init__(self, name: str | int, operands: Optional[List[PatternNode]], times: Optional[TimeType]) -> None:
        self.name = name
        self.operands = operands
        self.times = times

    def generate_regex(self) -> str:
        operands_regex: Optional[str] = self.get_operand_regex()
        times_regex: Optional[str] = self.get_min_max_regex()

        if times_regex:
            return self._form_regex_with_time(operands_regex=operands_regex, times_regex=times_regex)
        return self._form_regex_without_time(operands_regex=operands_regex)

    def get_operand_regex(self) -> Optional[str]:
        if not self.operands:
            return None

        return "".join(operand.get_regex() for operand in self.operands)

    def get_min_max_regex(self) -> Optional[str]:
        if not self.times:
            return None
        return TimeTypeBuilder().get_min_max_regex(times=self.times)

    def _form_regex_with_time(self, operands_regex: Optional[str], times_regex: str) -> str:
        # Add prefix and suffix to name to allow matching only substring
        pattern_nod_name = get_pattern_node_name(self.name)

        if operands_regex:
            return f"(?:{IGNORE_INST_ADDR}(?:{pattern_nod_name}{operands_regex}{SKIP_TO_END_OF_PATTERN_NODE})){times_regex}"
        return f"(?:{IGNORE_INST_ADDR}(?:{pattern_nod_name}{SKIP_TO_END_OF_PATTERN_NODE})){times_regex}"

    def _form_regex_without_time(self, operands_regex: Optional[str]) -> str:
        pattern_nod_name = get_pattern_node_name(self.name)

        if operands_regex:
            return f"{IGNORE_INST_ADDR}(?:{pattern_nod_name}{operands_regex}{SKIP_TO_END_OF_PATTERN_NODE})"
        return f"{IGNORE_INST_ADDR}(?:{pattern_nod_name}{SKIP_TO_END_OF_PATTERN_NODE})"


class PatternNodeNode(PatternNode):
    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
            pattern_node_dict=pattern_node.pattern_node_dict,
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            root_node=pattern_node.root_node,
        )

    def get_regex(self) -> str:
        return self.process_branch()

    def process_branch(self) -> str:
        child_regexes = self.process_children()
        times_regex: Optional[str] = TimeTypeBuilder().get_min_max_regex(times=self.times)
        return BranchProcessor().process_pattern_node(parent=self, child_regexes=child_regexes, times_regex=times_regex)

    def process_children(self) -> List[str]:
        if self.children:
            return [child.get_regex() for child in self.children]
        raise ValueError("Children list is empty")


class PatternNodeCaptureGroupReferenceRegister(PatternNode):
    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
            pattern_node_dict=pattern_node.pattern_node_dict,
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            root_node=pattern_node.root_node,
        )

    def get_regex(self) -> str:
        return self.get_capture_group_reference_register()

    @staticmethod
    def get_capture_group_reference_register() -> str:
        return f"{OPTIONAL_PERCENTAGE_CHAR}[re]?(.)[xhli],"


class PatternNodeCaptureGroupRegisterReferenceGenreg(PatternNode):
    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
            pattern_node_dict=pattern_node.pattern_node_dict,
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            root_node=pattern_node.root_node,
        )

    def get_regex(self) -> str:
        return self.get_capture_group_reference_register_genreg()

    def get_capture_group_reference_register_genreg(self) -> str:
        # The comma is optional just for when this is under a deref
        # On deref the comma should not be present
        # TODO: find a way to implement this cleaner

        # return f"{OPTIONAL_PERCENTAGE_CHAR}[re]?(.)[xhl],"
        return f"{OPTIONAL_PERCENTAGE_CHAR}[re]?(.)[xhl]{OPTIONAL_COMMA}"


class PatternNodeCaptureGroupRegisterReferenceIndreg(PatternNode):
    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
            pattern_node_dict=pattern_node.pattern_node_dict,
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            root_node=pattern_node.root_node,
        )

    def get_regex(self) -> str:
        return self.get_capture_group_reference_register_indreg()

    def get_capture_group_reference_register_indreg(self) -> str:
        # The comma is optional just for when this is under a deref
        # On deref the comma should not be present
        # TODO: find a way to implement this cleaner

        # return f"{OPTIONAL_PERCENTAGE_CHAR}[re]?([sd])il?,"
        return f"{OPTIONAL_PERCENTAGE_CHAR}[re]?([sd])il?{OPTIONAL_COMMA}"


class PatternNodeCaptureGroupRegisterReferenceStackreg(PatternNode):
    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
            pattern_node_dict=pattern_node.pattern_node_dict,
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            root_node=pattern_node.root_node,
        )

    def get_regex(self) -> str:
        return self.get_capture_group_reference_register_stackreg()

    def get_capture_group_reference_register_stackreg(self) -> str:
        # The comma is optional just for when this is under a deref
        # On deref the comma should not be present
        # TODO: find a way to implement this cleaner

        # return f"{OPTIONAL_PERCENTAGE_CHAR}[re]?(sp)l?,"
        return f"{OPTIONAL_PERCENTAGE_CHAR}[re]?(sp)l?{OPTIONAL_COMMA}"


class PatternNodeCaptureGroupRegisterReferenceBasereg(PatternNode):
    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
            pattern_node_dict=pattern_node.pattern_node_dict,
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            root_node=pattern_node.root_node,
        )

    def get_regex(self) -> str:
        return self.get_capture_group_reference_register_basereg()

    def get_capture_group_reference_register_basereg(self) -> str:
        # The comma is optional just for when this is under a deref
        # On deref the comma should not be present
        # TODO: find a way to implement this cleaner

        # return f"{OPTIONAL_PERCENTAGE_CHAR}[re]?(bp)l?,"
        return f"{OPTIONAL_PERCENTAGE_CHAR}[re]?(bp)l?{OPTIONAL_COMMA}"


class PatternNodeCaptureGroupRegisterCall(PatternNode):
    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
            pattern_node_dict=pattern_node.pattern_node_dict,
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            root_node=pattern_node.root_node,
        )

    def get_regex(self) -> str:
        return self.get_capture_group_register_call()

    def get_capture_group_register_call(self) -> str:

        capture_group_instance = CaptureGroupIndexRegister(pattern_node=self)
        index = capture_group_instance.to_regex()

        matching_rule = self.process_register_capture_group_name_based_on_register_type(index=index)

        # return OPTIONAL_PERCENTAGE_CHAR + matching_rule + ","
        # The comma is optional just for when this is under a deref
        # On deref the comma should not be present
        # TODO: find a way to implement this cleaner

        return OPTIONAL_PERCENTAGE_CHAR + matching_rule + OPTIONAL_COMMA

    def process_register_capture_group_name_based_on_register_type(self, index: str) -> str:
        """Process the register capture group name based on the register special type."""

        pattern_name = self.name
        assert isinstance(pattern_name, str), "Name must be a string"

        if pattern_name.startswith("&genreg"):
            return self.process_register_capture_group_name_genreg(pattern_name=pattern_name, index=index)

        if pattern_name.startswith("&indreg"):
            return self.process_register_capture_group_name_indreg(pattern_name=pattern_name, index=index)

        if pattern_name.startswith("&stackreg"):
            return self.process_register_capture_group_name_stackreg(pattern_name=pattern_name, index=index)

        if pattern_name.startswith("&basereg"):
            return self.process_register_capture_group_name_basereg(pattern_name=pattern_name, index=index)

        raise NotImplementedError(f"Register capture group name {pattern_name} not implemented")

    @staticmethod
    def process_register_capture_group_name_genreg(pattern_name: str, index: str) -> str:
        """Process the register capture group name in case of genreg.

        These are:
            RAX, EAX, AX, AH, AL,
            RBX, EBX, BX, BH, BL,
            RCX, ECX, CX, CH, CL,
            RDX, EDX, DX, DH, DL,

        """

        if pattern_name.endswith(RegisterCaptureSuffixs.SUFFIX_64.value):
            # Capturing an RAX, RBX, RCX, RDX
            return "r" + index + "x"

        if pattern_name.endswith(RegisterCaptureSuffixs.SUFFIX_32.value):
            # Capturing an EAX, EBX, ECX, EDX
            return "e" + index + "x"

        if pattern_name.endswith(RegisterCaptureSuffixs.SUFFIX_16.value):
            # Capturing an AX, BX, CX, DX
            return index + "x"

        if pattern_name.endswith(RegisterCaptureSuffixs.SUFFIX_8H.value):
            # Capturing an AH, BH, CH, DH
            return index + "h"

        if pattern_name.endswith(RegisterCaptureSuffixs.SUFFIX_8L.value):
            # Capturing an AL, BL, CL, DL
            return index + "l"

        raise NotImplementedError("Register capture group name not implemented")

    @staticmethod
    def process_register_capture_group_name_indreg(pattern_name: str, index: str) -> str:
        """Process the register capture group name in case of indreg_d and indreg_s.

        These are:
            RDI, EDI, DI, DIL
            RSI, ESI, SI, SIL

        """

        if pattern_name.endswith(RegisterCaptureSuffixs.SUFFIX_64.value):
            # Capturing an RDI or RSI
            return "r" + index + "i"

        if pattern_name.endswith(RegisterCaptureSuffixs.SUFFIX_32.value):
            # Capturing an EDI or ESI
            return "e" + index + "i"

        if pattern_name.endswith(RegisterCaptureSuffixs.SUFFIX_16.value):
            # Capturing an DI or SI
            return index + "i"

        if pattern_name.endswith(RegisterCaptureSuffixs.SUFFIX_8L.value):
            # Capturing an DIL or SIL
            return index + "il"

        raise NotImplementedError("Register capture group name not implemented")

    @staticmethod
    def process_register_capture_group_name_stackreg(pattern_name: str, index: str) -> str:
        """Process the register capture group name in case of stackreg.
        These are:
            RSP, ESP, SP, SPL

        """
        if pattern_name.endswith(RegisterCaptureSuffixs.SUFFIX_64.value):
            # Capturing an RSP
            return "r" + index

        if pattern_name.endswith(RegisterCaptureSuffixs.SUFFIX_32.value):
            # Capturing an ESP
            return "e" + index

        if pattern_name.endswith(RegisterCaptureSuffixs.SUFFIX_16.value):
            # Capturing an SP
            return index

        if pattern_name.endswith(RegisterCaptureSuffixs.SUFFIX_8L.value):
            # Capturing an SPL
            return index + "l"

        raise NotImplementedError("Register capture group name not implemented")

    @staticmethod
    def process_register_capture_group_name_basereg(pattern_name: str, index: str) -> str:
        """Process the register capture group name in case of basereg.
        These are:
            RBP, EBP, BP, BPL
        """
        if pattern_name.endswith(RegisterCaptureSuffixs.SUFFIX_64.value):
            # Capturing an RBP
            return "r" + index

        if pattern_name.endswith(RegisterCaptureSuffixs.SUFFIX_32.value):
            # Capturing an EBP
            return "e" + index

        if pattern_name.endswith(RegisterCaptureSuffixs.SUFFIX_16.value):
            # Capturing an BP
            return index

        if pattern_name.endswith(RegisterCaptureSuffixs.SUFFIX_8L.value):
            # Capturing an BPL
            return index + "l"

        raise NotImplementedError("Register capture group name not implemented")
