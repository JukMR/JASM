from enum import Enum
from typing import Final, Optional

from jasm.global_definitions import OPTIONAL_PERCENTAGE_CHAR
from jasm.jasm_regex.tree_generators.pattern_node_abstract import PatternNode

OPTIONAL_HEX_CHAR: Final = "(?:0x)?"


class DerefChildNames(Enum):
    """Represents the child names of a deref object."""

    MAIN_REG = "main_reg"
    CONSTANT_OFFSET = "constant_offset"
    REGISTER_MULTIPLIER = "register_multiplier"
    CONSTANT_MULTIPLIER = "constant_multiplier"


class DerefObject:
    """Represents a deref object."""

    # k(a,b,c) -> [a+b*c+k]
    # main_reg = a
    # register_multiplier = b
    # constant_multiplier = c
    # constant_offset = k

    def __init__(
        self,
        main_reg: str,
        constant_offset: Optional[str | int],
        register_multiplier: Optional[str],
        constant_multiplier: Optional[str | int],
    ) -> None:

        self.main_reg = f"{OPTIONAL_PERCENTAGE_CHAR}{main_reg}"
        self.constant_offset = f"{OPTIONAL_HEX_CHAR}{constant_offset}" if constant_offset else None
        self.register_multiplier = f"{OPTIONAL_PERCENTAGE_CHAR}{register_multiplier}" if register_multiplier else None
        self.constant_multiplier = f"{OPTIONAL_HEX_CHAR}{constant_multiplier}" if constant_multiplier else None

    def get_regex(self) -> str:
        """Returns regex from the given deref object."""
        if self.constant_offset and self.register_multiplier and self.constant_multiplier:
            return self._get_regex_from_full_deref()
        return self._form_regex_with_some_elem_missing()

    def _form_regex_with_some_elem_missing(self) -> str:
        """Forms regex from the given deref object in case there is some element missing."""
        regex = ""

        # add main_reg
        regex += rf"\[{self.main_reg}"

        # check if register_multiplier exists and add it
        if self.register_multiplier and self.constant_multiplier:
            regex += rf"\+{self.register_multiplier}\*{self.constant_multiplier}"
        elif self.register_multiplier:
            regex += rf"\+{self.register_multiplier}"
        elif self.constant_multiplier:
            regex += rf"\+{self.constant_multiplier}"

        # check if constant_offset exists and add it
        if self.constant_offset:
            regex += rf"\+{self.constant_offset}"

        return regex + r"\]"  # add closing bracket

    def _get_regex_from_full_deref(self) -> str:
        deref_child_regex = (
            rf"\[{self.main_reg}\+{self.register_multiplier}\*{self.constant_multiplier}\+{self.constant_offset}\]"
        )
        return deref_child_regex


class DerefObjectBuilder:
    """Builds a deref object from the given command dict."""

    def __init__(self, parent: PatternNode) -> None:
        self.parent = parent

    def build(self) -> DerefObject:
        """Builds a deref object from the given command dict."""
        main_reg = self._child_getter(parent=self.parent, child_name=DerefChildNames.MAIN_REG)

        if not main_reg:
            raise ValueError("main_reg is required for deref object")

        constant_offset = self._child_getter(parent=self.parent, child_name=DerefChildNames.CONSTANT_OFFSET)
        register_multiplier = self._child_getter(parent=self.parent, child_name=DerefChildNames.REGISTER_MULTIPLIER)
        constant_multiplier = self._child_getter(parent=self.parent, child_name=DerefChildNames.CONSTANT_MULTIPLIER)

        # Get regex for each child
        main_reg_regex = main_reg.get_regex()
        constant_offset_regex = constant_offset.get_regex() if constant_offset else None
        register_multiplier_regex = register_multiplier.get_regex() if register_multiplier else None
        constant_multiplier_regex = constant_multiplier.get_regex() if constant_multiplier else None

        return DerefObject(
            main_reg=main_reg_regex,
            constant_offset=constant_offset_regex,
            register_multiplier=register_multiplier_regex,
            constant_multiplier=constant_multiplier_regex,
        )

    @staticmethod
    def _child_getter(parent: PatternNode, child_name: DerefChildNames) -> Optional[PatternNode]:
        """Get the child of the given parent."""
        if not parent.children:
            return None

        for child in parent.children:
            if child.name == child_name.value:
                return child
        return None
