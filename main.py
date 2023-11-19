"Main entry module"
from argparse import Namespace
from parse_arguments import parse_args_from_console
from src.logging_config import configure_logger
from src.match import InputFileType, perform_matching
from src.measure_performance import measure_performance
from src.logging_config import configure_logger
from src.match import perform_matching, InputFileType
from src.tester import Tester

tester_stringify_inst: Tester


def start_configurations() -> Namespace:
    # Enable tester flag for test_parsing file

    # pylint: disable=global-statement
    global TESTER
    TESTER = True
    if TESTER:
        global tester_stringify_inst  # pylint: disable=global-statement
        tester_stringify_inst = Tester()

    # Parse user args
    args: Namespace = parse_args_from_console()

    # Configure logger
    configure_logger(
        debug=args.debug,
        info=args.info,
        enable_log_to_file=args.enable_logging_to_file,
        enable_log_to_terminal=args.enable_logging_to_terminal,
    )

    return args


@measure_performance(perf_title="Main function")
def main() -> None:
    "Main function"

    args = start_configurations()

    print("Starting execution... ")
    input_file_type = decide_assembly_or_binary(args=args)
    perform_matching(pattern_pathstr=args.pattern, input_file=args.input_file, input_file_type=input_file_type)


def decide_assembly_or_binary(args: Namespace) -> InputFileType:
    "Decide whether the input file is assembly or binary"
    if args.assembly:
        return InputFileType.assembly
    if args.binary:
        return InputFileType.binary

    raise ValueError("Either assembly or binary must be provided")


if __name__ == "__main__":
    main()
