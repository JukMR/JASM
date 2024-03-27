from jasm.global_definitions import OPTIONAL_COMMA, OPTIONAL_PERCENTAGE_CHAR, RegisterCaptureSuffixs
from jasm.regex.tree_generators.capture_group_index import CaptureGroupIndexRegister
from jasm.regex.tree_generators.pattern_node_abstract import PatternNode


class PatternNodeCaptureGroupRegisterReferenceGenreg(PatternNode):
    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
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
