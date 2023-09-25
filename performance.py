import cProfile
from src.match import perform_matching


profiler = cProfile.Profile()
profiler.enable()
perform_matching(
    pattern_pathstr="tests/yamls/moonbounce_regex_matcher.yaml",
    assembly="tests/assembly/moonbounce_malware_truncated.s",
)
profiler.disable()
profiler.dump_stats("profiling_results.pstat")
