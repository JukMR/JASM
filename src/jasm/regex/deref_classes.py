from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class DerefObject:
    """Represents a deref object."""

    # k(a,b,c) -> [a+b*c+k]
    # main_reg = a
    # register_multiplier = b
    # constant_multiplier = c
    # constant_offset = k

    main_reg: str
    constant_offset: Optional[str | int]
    register_multiplier: Optional[str]
    constant_multiplier: Optional[str | int]

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

    def __init__(self, command_dict: Dict[str, Dict[str, str]]) -> None:
        self.deref_elems = command_dict["$deref"]

    def build(self) -> DerefObject:
        """Main build method"""
        try:
            main_reg = self.deref_elems["main_reg"]
        except ValueError as exc:
            raise ValueError(f"main_reg is required for deref object: {self.deref_elems}") from exc

        return DerefObject(
            main_reg=main_reg,
            constant_offset=self.deref_elems.get("constant_offset"),
            register_multiplier=self.deref_elems.get("register_multiplier"),
            constant_multiplier=self.deref_elems.get("constant_multiplier"),
        )
