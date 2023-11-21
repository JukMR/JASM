from typing import List


def is_leaf(command) -> bool:
    name = get_name(command)
    return not name.startswith("$")


def get_name(command) -> str:
    return command.keys()[0]


def get_childs(command) -> List:
    return command.values()


def process_command(command):
    childs = get_childs(command)
    strings: List[str] = process_childs(childs)
    return process_based_on_command_type(command, strings)


def direct_processing(command) -> str:
    if is_leaf(command):
        return process_leaf(command)
    return process_based_on_command_type(command, strings)


def get_times(command) -> str:
    times = command.get("times", None)
    if not times:
        return "{1}"
    return times


def process_leaf(command) -> str:
    name = get_name(command)
    operands = get_operands(command)
    times = get_times()

    return form_regex(name, operands, times)
