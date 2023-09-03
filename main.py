"Main entry module"
from parse_arguments import parse_args_from_console

from src.measure_performance import measure_performance
from src.logging_config import configure_logger
from match import match


@measure_performance(perf_title="Main function")
def main() -> None:
    "Main function"
    args = parse_args_from_console()

    configure_logger(
        debug=args.debug,
        info=args.info,
        disable_log_to_file=args.disable_logging_to_file,
        disable_log_to_terminal=args.disable_logging_to_terminal,
    )

    print("Starting execution... ")
    match(
        pattern_pathstr=args.pattern,
        assembly=args.assembly,
        binary=args.binary,
        dissasemble_program=args.dissasemble_program,
    )


if __name__ == "__main__":
    main()
