"Parse arguements module"
import argparse


def parse_args_from_console() -> argparse.Namespace:
    "Get and parse user arguments"

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pattern", required=True, help="Input pattern for parsing")
    parser.add_argument("--debug", default=False, action="store_true", help="Set debugging level")
    parser.add_argument("--info", default=True, action="store_true", help="Set info level")
    parser.add_argument("--dissasemble-program", default="objdump", help="Set the program to use as dissasembler")
    parser.add_argument("--enable_logging_to_file", default=True, action="store_true", help="Enable logging to logfile")
    parser.add_argument(
        "--enable_logging_to_terminal", default=True, action="store_true", help="Enable logging to terminal"
    )
    parser.add_argument(
        "--all-matches", default=False, action="store_true", help="Return all matches instead of only first match"
    )
    parser.add_argument(
        "--return_addrs_and_instructions",
        default=False,
        action="store_true",
        help="Return instructions as long as addressess",
    )

    # Create a mutually exclusive group for the two arguments
    group = parser.add_mutually_exclusive_group(required=True)

    # Add the two arguments to the group
    group.add_argument("-b", "--binary", help="Input binary for parsing")
    group.add_argument("-s", "--assembly", help="Input assembly for parsing")

    # Return only a file_type argument

    parsed_args = parser.parse_args()

    return parsed_args
