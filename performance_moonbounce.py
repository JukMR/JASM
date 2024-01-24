import cProfile
from src.jasm.global_definitions import InputFileType
from src.jasm.match import MasterOfPuppets


profiler = cProfile.Profile()
profiler.enable()
MasterOfPuppets().perform_matching(
    pattern_pathstr="tests/yamls/moonbounce_regex_matcher.yaml",
    input_file="tests/binary/moonbounce.bin",
    input_file_type=InputFileType.binary,
)
profiler.disable()
profiler.dump_stats("moonbounce_profiling_results.pstat")
