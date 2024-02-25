import json
from pathlib import Path


def test_benchmark_degradation():

    baseline_json = ".benchmarks/Linux-CPython-3.11-64bit/0012_baselines.json"

    # This is the file that we want to check for performance degradation
    current_json = get_last_benchmark_file()
    current_json = ".benchmarks/Linux-CPython-3.11-64bit/0013_new_file.json"
    assert check_performance_degradation(baseline_json, current_json)


def check_performance_degradation(baseline_file: str, current_file: str, threshold: float = 22.0) -> bool:
    with open(baseline_file, "r", encoding="utf-8") as bf, open(current_file, "r", encoding="utf-8") as cf:
        baseline_data = json.load(bf)
        current_data = json.load(cf)

    for baseline, current in zip(baseline_data["benchmarks"], current_data["benchmarks"]):
        baseline_mean = baseline["stats"]["mean"]
        current_mean = current["stats"]["mean"]
        degradation = ((current_mean - baseline_mean) / baseline_mean) * 100

        if degradation > threshold:
            print(
                f"Test {baseline['name']} has degraded by {degradation:.2f}% which is above the threshold of {threshold}%. Failing..."
            )
            return False  # Indicates failure due to exceeding the threshold
    return True  # Indicates all tests passed the threshold check


def get_last_benchmark_file() -> str:
    # This function should return the path to the last benchmark fil
    benchmark_directory = Path(".benchmarks")

    for folder in benchmark_directory.iterdir():
        if folder.is_dir():
            # Sort the files in reverse order to get the lastest file
            for file in sorted(list(folder.iterdir()), reverse=True):
                if file.is_file() and file.suffix == ".json" and not "baseline" in file.name:
                    print("Using benchmark file to compare against baseline:", file)
                    return str(file)

    raise FileNotFoundError("No benchmark file found")
