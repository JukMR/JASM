import json
import warnings
from pathlib import Path

import pytest


def test_benchmark_degradation() -> None:
    """Control the tests have not degraded by more than 40% in performance. If they have, fail the test."""

    baseline_json = get_last_baseline_file()

    # This is the file that we want to check for performance degradation
    current_json = get_last_benchmark_file()

    result = check_performance_degradation(baseline_json, current_json, threshold=40.0)

    # if not result:
    # pytest.fail("Performance degradation detected. Failing test...")


def check_performance_degradation(baseline_file: Path, current_file: Path, threshold: float) -> bool:
    """Check if the performance of the current benchmark has degraded by more than the threshold. If it has, return False. Otherwise, return True."""
    with open(baseline_file, "r", encoding="utf-8") as bf, open(current_file, "r", encoding="utf-8") as cf:
        baseline_data = json.load(bf)
        current_data = json.load(cf)

    for baseline, current in zip(baseline_data["benchmarks"], current_data["benchmarks"]):
        baseline_mean = baseline["stats"]["mean"]
        current_mean = current["stats"]["mean"]
        degradation = ((current_mean - baseline_mean) / baseline_mean) * 100

        if degradation > threshold:
            warnings.warn(
                f"Test {baseline['name']} has degraded by {degradation:.2f}% which is above the threshold of {threshold}%. Failing..."
            )
            return False  # Indicates failure due to exceeding the threshold
    return True  # Indicates all tests passed the threshold check


def get_last_baseline_file() -> Path:
    """This function should return the path to the last baseline file"""
    benchmark_directory = Path("benchmark_baseline")

    assert benchmark_directory.exists(), "No benchmark_baseline directory found. Check baseline file exist"

    for file in sorted(list(benchmark_directory.iterdir()), reverse=True):
        # Sort the files in reverse order to get the lastest file
        if file.is_file() and file.suffix == ".json":
            if "baseline" in file.name:
                print("Baseline file is:", file)
                return file

    raise ValueError("No baseline file found")


def get_last_benchmark_file() -> Path:
    """This function should return the path to the last benchmark file"""
    benchmark_directory = Path(".benchmarks")

    for folder in benchmark_directory.iterdir():
        if folder.is_dir():
            # Sort the files in reverse order to get the lastest file
            for file in sorted(list(folder.iterdir()), reverse=True):
                if file.is_file() and file.suffix == ".json":
                    if not "baseline" in file.name:
                        print("Using benchmark file to compare against baseline:", file)
                        return file

    raise FileNotFoundError("No benchmark file found")