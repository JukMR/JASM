"Parse arguements module"
import argparse


def parse_args_from_console() -> argparse.Namespace:
    "Get and parse user arguments"

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pattern", required=True, help="Input pattern for parsing")
    parser.add_argument("--debug", default=False, action="store_true", help="Set debugging level")
    parser.add_argument("--dissasemble-program", default="objdump", help="Set the program to use as dissasembler")
    parser.add_argument("--info", default=True, action="store_true", help="Set info level")
    parser.add_argument(
        "--disable_logging_to_file", default=False, action="store_true", help="Disable logging to logfile"
    )
    parser.add_argument(
        "--disable_logging_to_terminal", default=False, action="store_true", help="Disable logging to terminal"
    )

    # Create a mutually exclusive group for the two arguments
    group = parser.add_mutually_exclusive_group(required=True)

    # Add the two arguments to the group
    group.add_argument("-b", "--binary", help="Input binary for parsing")
    group.add_argument("-s", "--assembly", help="Input assembly for parsing")

    parsed_args = parser.parse_args()

    return parsed_args
