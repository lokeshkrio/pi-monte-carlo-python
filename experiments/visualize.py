import argparse
import csv
import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from experiments.benchmark import benchmark, print_results
from src.estimator import MonteCarloPi

RESULTS_DIR = PROJECT_ROOT / "results"


def save_graph(x, y, title, xlabel, ylabel, filename, reference=None):
    plt.figure(figsize=(9, 5))

    plt.plot(x, y, marker="o", label=ylabel)

    if reference is not None:
        plt.axhline(reference, color="red", linestyle="--", label="Actual Pi")
        plt.legend()

    plt.xscale("log")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(RESULTS_DIR / filename, dpi=300)
    plt.close()

    print(f"Saved: {filename}")


def plot_sample_points(number_of_points: int = 10000, seed: int | None = 42):
    estimator = MonteCarloPi(seed=seed)

    result = estimator.estimate(number_of_points, return_points=True)

    inside_x = []
    inside_y = []
    outside_x = []
    outside_y = []

    for x, y in result.points or ():
        if x * x + y * y <= 1:
            inside_x.append(x)
            inside_y.append(y)
        else:
            outside_x.append(x)
            outside_y.append(y)

    fig, ax = plt.subplots(figsize=(7, 7))

    # Plot sampled points
    ax.scatter(inside_x, inside_y, s=5, color="green", label="Inside circle", alpha=0.5)

    ax.scatter(
        outside_x, outside_y, s=5, color="red", label="Outside circle", alpha=0.5
    )

    # Draw unit circle
    circle = Circle(
        (0, 0), 1, fill=False, color="black", linewidth=2, label="Unit circle"
    )

    ax.add_patch(circle)

    # Sampling region
    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-1.05, 1.05)
    ax.set_aspect("equal")

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title(f"Monte Carlo Pi Simulation ({number_of_points:,} Points)")

    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(RESULTS_DIR / "sample_points.png", dpi=300)

    plt.close()

    print("Saved: sample_points.png")


def run_visualization(samples, repetitions=5, seed: int | None = 118, plot_points=10000):

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    print("\nRunning Monte Carlo benchmark...\n")

    results = benchmark(sample_sizes=samples, repetitions=repetitions, seed=seed)

    print_results(results)

    # Save benchmark results
    csv_path = RESULTS_DIR / "benchmark_results.csv"

    with open(csv_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"\nSaved: {csv_path.name}")

    # Extract metrics
    points = [r["Points"] for r in results]
    estimates = [r["Estimated Pi"] for r in results]
    errors = [r["Mean Abs Error"] for r in results]
    standard_errors = [r["Theoretical SE"] for r in results]
    times = [r["Execution Time (s)"] for r in results]
    throughput = [r["Throughput (pts/s)"] for r in results]

    # 1. Pi convergence
    save_graph(
        points,
        estimates,
        "Monte Carlo Pi Convergence",
        "Number of Random Points",
        "Estimated Pi",
        "pi_convergence.png",
        reference=math.pi,
    )

    # 2. Absolute error
    save_graph(
        points,
        errors,
        "Absolute Error vs Sample Size",
        "Number of Random Points",
        "Mean Absolute Error",
        "absolute_error.png",
    )

    # 3. Standard error
    save_graph(
        points,
        standard_errors,
        "Theoretical Standard Error",
        "Number of Random Points",
        "Standard Error",
        "standard_error.png",
    )

    # 4. Execution time
    save_graph(
        points,
        times,
        "Execution Time vs Sample Size",
        "Number of Random Points",
        "Execution Time (seconds)",
        "execution_time.png",
    )

    # 5. Throughput
    save_graph(
        points,
        throughput,
        "Simulation Throughput",
        "Number of Random Points",
        "Points per Second",
        "throughput.png",
    )

    # 6. Sample points and unit circle
    plot_sample_points(number_of_points=plot_points, seed=seed)

    print("\nAll visualizations generated successfully!")


def main():
    parser = argparse.ArgumentParser(description="Monte Carlo Pi Visualizations")

    parser.add_argument(
        "--samples", nargs="+", type=int, default=[100, 1000, 10000, 100000, 1000000]
    )

    parser.add_argument("-r", "--repetitions", type=int, default=5)

    parser.add_argument("-s", "--seed", type=int, default=118)

    parser.add_argument(
        "--plot-points",
        type=int,
        default=10000,
        help="Number of points to display in the unit-circle plot",
    )

    args = parser.parse_args()

    if any(n <= 0 for n in args.samples):
        parser.error("Sample sizes must be positive.")

    if args.repetitions <= 0 or args.plot_points <= 0:
        parser.error("Repetitions and plot points must be positive.")

    seed = args.seed if args.seed >= 0 else None

    run_visualization(
        samples=args.samples,
        repetitions=args.repetitions,
        seed=seed,
        plot_points=args.plot_points,
    )


if __name__ == "__main__":
    main()
