"Main entry module"
from argparse import Namespace

from parse_arguments import parse_args_from_console
from src.jasm.global_definitions import InputFileType
from src.jasm.logging_config import configure_logger
from src.jasm.match import MasterOfPuppets
from src.jasm.measure_performance import measure_performance


def start_configurations() -> Namespace:
    "Main function to parse user args and start logger"

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
    MasterOfPuppets().perform_matching(
        pattern_pathstr=args.pattern, input_file=args.input_file, input_file_type=input_file_type
    )


def decide_assembly_or_binary(args: Namespace) -> InputFileType:
    "Decide whether the input file is assembly or binary"
    if args.assembly:
        return InputFileType.assembly
    if args.binary:
        return InputFileType.binary

    raise ValueError("Either assembly or binary must be provided")


if __name__ == "__main__":
    main()
