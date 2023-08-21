'Regex common functions module'

from src.global_definitions import IncludeExcludeListType

def list_without_last_character(string: str) -> str:
    'Return copy of string without last character'

    return string[:-1]

def join_instructions(inst_list: IncludeExcludeListType, ignore_pattern: str) -> str:
    'Join instructions from list using ignore_pattern to generate regex'

    if inst_list is None or len(inst_list) == 0:
        raise ValueError("There are no instructions to join")

    joined_instructions = [f"{elem}{ignore_pattern}" for elem in inst_list]
    return '|'.join(joined_instructions)
