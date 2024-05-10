import cProfile
from jasm.global_definitions import InputFileType
from jasm.match.match import MasterOfPuppets


profiler = cProfile.Profile()
profiler.enable()
MasterOfPuppets().perform_matching(
    pattern_pathstr="tests/yamls/oren_rule_att_improved_rule.yaml",
    input_file="tests/binary/lenovo2.bin",
    input_file_type=InputFileType.binary,
)
profiler.disable()
profiler.dump_stats("lenovo_profiling_results.pstat")
