# Monte Carlo Pi Estimation

A Python project for estimating the mathematical constant $\pi$ using the **Monte Carlo method**, featuring statistical error analysis, performance benchmarking, and publication-ready visualizations.

---

## 📌 Overview

The Monte Carlo method estimates $\pi$ by simulating random uniform sampling across a square and observing the proportion of points that land inside an inscribed circle.

### Mathematical Principle

1. Consider a square of side length $2$ centered at the origin, with area $A_{\text{square}} = 2 \times 2 = 4$.
2. Inscribe a unit circle of radius $r = 1$ centered at $(0, 0)$, with area $A_{\text{circle}} = \pi r^2 = \pi$.
3. Uniformly sample points $(x, y)$ such that $x, y \in [-1, 1]$.
4. A point lies inside the circle if $x^2 + y^2 \le 1$.
5. The probability $P$ of a random point falling inside the circle is the ratio of their areas:
   $$\frac{A_{\text{circle}}}{A_{\text{square}}} = \frac{\pi}{4}$$
6. Therefore, $\pi$ can be approximated as:
   $$\pi \approx 4 \times \frac{N_{\text{inside}}}{N_{\text{total}}}$$

---

## 📁 Project Structure

```text
pi-monte-carlo/
├── experiments/
│   ├── benchmark.py       # Benchmark suite with timing & statistical metrics
│   └── visualize.py       # Visualization generator for convergence & plots
├── results/               # Output directory for CSV logs and plots
│   ├── benchmark_results.csv
│   ├── pi_convergence.png
│   ├── absolute_error.png
│   ├── standard_error.png
│   ├── execution_time.png
│   ├── throughput.png
│   └── sample_points.png
├── src/
│   ├── __init__.py
│   └── estimator.py       # Core Monte Carlo estimator & result dataclass
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **matplotlib** (for visualization scripts)

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd pi-monte-carlo
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate    # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install matplotlib
   ```

---

## 💻 Usage

### 1. Basic Estimation

Run the core estimator module directly to perform a sample estimation:

```bash
python -m src.estimator
```

Or import it in your own Python code:

```python
from src.estimator import MonteCarloPi

estimator = MonteCarloPi(seed=42)
result = estimator.estimate(number_of_points=1_000_000)

print(f"Estimated π: {result.pi_estimate}")
print(f"Absolute Error: {result.absolute_error:.6f}")
print(f"Relative Error: {result.relative_error_percent:.4f}%")
print(f"Theoretical SE: {result.standard_error:.6f}")
print(f"95% CI: {result.confidence_interval_95}")
```

### 2. Run Benchmarks

Run benchmarks across multiple sample sizes (e.g., $10^2$ to $10^6$ points) with multiple repetitions:

```bash
python experiments/benchmark.py --samples 100 1000 10000 100000 1000000 --repetitions 5
```

**Options:**
- `--samples`: List of sample sizes to test (default: `100 1000 10000 100000 1000000`).
- `-r, --repetitions`: Number of repetitions per sample size for statistical averaging (default: `5`).
- `-s, --seed`: Base random seed (default: `118`, set `< 0` for non-deterministic runs).
- `-o, --output`: CSV destination path (default: `./results/results.csv`).

### 3. Generate Visualizations

Generate analytical charts and a 2D plot of sampled points:

```bash
python experiments/visualize.py
```

This runs the benchmark and saves all charts directly to the `results/` folder:
- **`sample_points.png`**: Scatter plot showing points inside vs. outside the unit circle.
- **`pi_convergence.png`**: Convergence of $\hat{\pi}$ toward $\pi$ as $N$ increases.
- **`absolute_error.png`**: Mean absolute error vs. sample size on a log scale.
- **`standard_error.png`**: Theoretical standard error decay $\mathcal{O}(1/\sqrt{N})$.
- **`execution_time.png`**: Runtime scaling across sample sizes.
- **`throughput.png`**: Sampling rate in points per second.
- **`benchmark_results.csv`**: Full numeric summary table.

---

## 📊 Statistical Properties

- **Convergence Rate:** The standard error decays as $\mathcal{O}\left(\frac{1}{\sqrt{N}}\right)$, meaning reducing error by a factor of 10 requires 100× more samples.
- **Theoretical Standard Error:**
  $$\text{SE} = \sqrt{\frac{\pi (4 - \pi)}{N}}$$
- **Confidence Intervals (95%):**
  $$\hat{\pi} \pm 1.96 \times \text{SE}$$

