"Main entry module"
from parse_arguments import parse_args_from_console

from src.measure_performance import measure_performance
from src.logging_config import configure_logger
from src.match import perform_matching, InputFileType


@measure_performance(perf_title="Main function")
def main() -> None:
    "Main function"
    args = parse_args_from_console()

    configure_logger(
        debug=args.debug,
        info=args.info,
        enable_log_to_file=args.enable_logging_to_file,
        enable_log_to_terminal=args.enable_logging_to_terminal,
    )

    print("Starting execution... ")
    # TODO: determine this from the args
    input_file_type = InputFileType.assembly

    perform_matching(pattern_pathstr=args.pattern, input_file=args.input_file, input_file_type=input_file_type)


if __name__ == "__main__":
    main()
