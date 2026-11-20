import argparse
import csv
import math
import statistics
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


from src.estimator import MonteCarloPi


def benchmark(sample_sizes, repetitions=5, seed: int | None = 72):
    if repetitions <= 0:
        raise ValueError("Repetitions must be positive.")

    results = []

    for n in sample_sizes:
        if n <= 0:
            raise ValueError("Sample sizes must be positive.")

        estimates = []
        errors = []
        execution_times = []
        standard_errors = []

        for i in range(repetitions):
            estimator = MonteCarloPi(seed=None if seed is None else seed + i)

            start = time.perf_counter()
            result = estimator.estimate(n, return_points=False)
            elapsed = time.perf_counter() - start

            estimates.append(result.pi_estimate)
            errors.append(result.absolute_error)
            execution_times.append(elapsed)
            standard_errors.append(result.standard_error)

        mean_estimate = statistics.mean(estimates)
        mean_error = statistics.mean(errors)
        mean_time = statistics.mean(execution_times)

        theoretical_se = statistics.mean(standard_errors)
        relative_error = mean_error / math.pi * 100

        results.append(
            {
                "Points": n,
                "Estimated Pi": round(mean_estimate, 7),
                "Std Dev": (
                    round(statistics.stdev(estimates), 7) if repetitions > 1 else 0.0
                ),
                "Theoretical SE": round(theoretical_se, 7),
                "95% CI Half-Width": round(1.96 * theoretical_se, 7),
                "Mean Abs Error": round(mean_error, 7),
                "Relative Error (%)": round(relative_error, 5),
                "Execution Time (s)": round(mean_time, 6),
                "Time Std Dev (s)": (
                    round(statistics.stdev(execution_times), 6)
                    if repetitions > 1
                    else 0.0
                ),
                "Throughput (pts/s)": round(n / mean_time, 1) if mean_time > 0 else 0.0,
            }
        )

    return results


def print_results(results):
    if not results:
        print("No results to display.")
        return

    columns = [
        ("Points", "Points"),
        ("Estimated Pi", "Estimated Pi"),
        ("Std Dev", "Std Dev"),
        ("Theoretical SE", "Theoretical SE"),
        ("Mean Abs Error", "Mean Abs Error"),
        ("Relative Error (%)", "Relative Error (%)"),
        ("Execution Time (s)", "Execution Time (s)"),
    ]

    headers = [header for header, _ in columns]
    widths = [
        max(
            len(header),
            *(
                len(f"{row[key]:,}" if key == "Points" else str(row[key]))
                for row in results
            ),
        )
        for header, key in columns
    ]

    print(
        "\n" + " | ".join(header.ljust(width) for header, width in zip(headers, widths))
    )

    print("-" * (sum(widths) + 3 * (len(widths) - 1)))

    for row in results:
        values = [
            f"{row[key]:,}" if key == "Points" else str(row[key]) for _, key in columns
        ]

        print(" | ".join(value.rjust(width) for value, width in zip(values, widths)))


def save_csv(results, filename="results.csv"):
    path = Path(filename)

    if not path.is_absolute():
        path = PROJECT_ROOT / path

    path.parent.mkdir(parents=True, exist_ok=True)

    if not results:
        raise ValueError("No results to save.")

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    return path.resolve()


def main():
    parser = argparse.ArgumentParser(description="Monte Carlo Pi Benchmark")

    parser.add_argument(
        "--samples",
        nargs="+",
        type=int,
        default=[100, 1000, 10000, 100000, 1000000],
        help="Sample sizes",
    )

    parser.add_argument(
        "-r",
        "--repetitions",
        type=int,
        default=5,
        help="Number of runs per sample size",
    )

    parser.add_argument(
        "-s",
        "--seed",
        type=int,
        default=72,
        help="Random seed (negative for random seeds)",
    )

    parser.add_argument(
        "-o", "--output", default="./results/results.csv", help="CSV output filename"
    )

    args = parser.parse_args()

    seed = args.seed if args.seed >= 0 else None

    print(f"\nMonte Carlo Pi Benchmark " f"({args.repetitions} repetitions)\n")

    results = benchmark(
        sample_sizes=args.samples, repetitions=args.repetitions, seed=seed
    )

    print_results(results)

    path = save_csv(results, args.output)
    print(f"\nResults saved to: {path}")


if __name__ == "__main__":
    main()
