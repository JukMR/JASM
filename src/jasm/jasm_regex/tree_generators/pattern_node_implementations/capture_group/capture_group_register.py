from jasm.global_definitions import OPTIONAL_COMMA, OPTIONAL_PERCENTAGE_CHAR, RegisterCaptureSuffixs
from jasm.jasm_regex.tree_generators.capture_group_index import CaptureGroupIndexRegisterCall
from jasm.jasm_regex.tree_generators.pattern_node_abstract import PatternNode, PatternNodeData


class PatternNodeCaptureGroupSpecialRegisterReference(PatternNode):  # type: ignore

    def __init__(self, pattern_node_data: PatternNodeData, regex_slice: str) -> None:
        super().__init__(pattern_node_data)
        self.regex_slice = regex_slice

    def get_regex(self) -> str:
        return f"{OPTIONAL_PERCENTAGE_CHAR}[re]?{self.regex_slice}{OPTIONAL_COMMA}"


class PatternNodeCaptureGroupRegisterCall(PatternNode):  # type: ignore

    def get_regex(self) -> str:
        return self.get_capture_group_register_call()

    def get_capture_group_register_call(self) -> str:

        index = CaptureGroupIndexRegisterCall(pattern_node=self).to_regex()

        matching_rule: str = self.process_register_capture_group_name_based_on_register_type(
            index=index
        )

        # return OPTIONAL_PERCENTAGE_CHAR + matching_rule + ","
        # The comma is optional just for when this is under a deref
        # On deref the comma should not be present
        # TODO: find a way to implement this cleaner

        return OPTIONAL_PERCENTAGE_CHAR + matching_rule + OPTIONAL_COMMA  # type: ignore

    def process_register_capture_group_name_based_on_register_type(self, index: str) -> str:
        """Process the register capture group name based on the register special type."""

        pattern_name = self.name
        if not isinstance(pattern_name, str):
            raise TypeError("Operand name must be a string")

        if pattern_name.startswith("&genreg"):
            return self.process_register_capture_group_name_genreg(
                pattern_name=pattern_name, index=index
            )

        if pattern_name.startswith("&indreg"):
            return self.process_register_capture_group_name_indreg(
                pattern_name=pattern_name, index=index
            )

        if pattern_name.startswith("&stackreg"):
            return self.process_register_capture_group_name_framereg(
                pattern_name=pattern_name, index=index
            )

        if pattern_name.startswith("&basereg"):
            return self.process_register_capture_group_name_framereg(
                pattern_name=pattern_name, index=index
            )

        if pattern_name.startswith("&framereg"):
            return self.process_register_capture_group_name_framereg(
                pattern_name=pattern_name, index=index
            )

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
    def process_register_capture_group_name_framereg(pattern_name: str, index: str) -> str:
        """Process the register capture group name in case of framereg.
        These are:
            RBP, EBP
            RSP, ESP
            BP,  SP
            BPL, SPL
        """
        if pattern_name.endswith(RegisterCaptureSuffixs.SUFFIX_64.value):
            # Capturing an RBP or RSP
            return "r" + index

        if pattern_name.endswith(RegisterCaptureSuffixs.SUFFIX_32.value):
            # Capturing an EBP or ESP
            return "e" + index

        if pattern_name.endswith(RegisterCaptureSuffixs.SUFFIX_16.value):
            # Capturing a BP or SP
            return index

        if pattern_name.endswith(RegisterCaptureSuffixs.SUFFIX_8L.value):
            # Capturing a BPL or SPL
            return index + "l"

        raise NotImplementedError("Register capture group name not implemented")
