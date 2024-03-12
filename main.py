"Main entry module"
from argparse import Namespace

from jasm.global_definitions import InputFileType, MatchConfig, MatchingSearchMode
from jasm.logging_config import configure_logger, logger
from jasm.match import MasterOfPuppets
from jasm.measure_performance import measure_performance
from parse_arguments import parse_args_from_console


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

    # Set assembly mode or binary mode
    match input_file_type:
        case InputFileType.assembly:
            input_file = args.assembly

        case InputFileType.binary:
            input_file = args.binary

        case _:
            raise ValueError("Invalid input file type")

    # Set first matching only or full matches
    if args.all_matches:
        matching_mode = MatchingSearchMode.all_finds
    else:
        matching_mode = MatchingSearchMode.first_find

    match_config = MatchConfig(
        pattern_pathstr=args.pattern,
        input_file=input_file,
        input_file_type=input_file_type,
        matching_mode=matching_mode,
        return_only_address=args.return_only_address,
        macros=args.macros,
    )

    MasterOfPuppets(match_config=match_config).perform_matching()


def decide_assembly_or_binary(args: Namespace) -> InputFileType:
    "Decide whether the input file is assembly or binary"
    if args.assembly:
        return InputFileType.assembly
    if args.binary:
        return InputFileType.binary

    raise ValueError("Either assembly or binary must be provided")


if __name__ == "__main__":
    main()
