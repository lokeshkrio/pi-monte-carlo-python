from dataclasses import dataclass
import math
import random


@dataclass(frozen=True)
class EstimationResult:
    pi_estimate: float
    points: list[tuple[float, float]] | None = None
    inside_circle: int = 0
    total_points: int = 0

    def __post_init__(self):
        if self.total_points <= 0:
            raise ValueError("Total points must be positive.")

        if not 0 <= self.inside_circle <= self.total_points:
            raise ValueError("Invalid number of points inside the circle.")

    @property
    def absolute_error(self) -> float:
        return abs(self.pi_estimate - math.pi)

    @property
    def relative_error(self) -> float:
        return self.absolute_error / math.pi

    @property
    def relative_error_percent(self) -> float:
        return self.relative_error * 100.0

    @property
    def standard_error(self) -> float:
        return math.sqrt(math.pi * (4.0 - math.pi) / self.total_points)

    @property
    def confidence_interval_95(self) -> tuple[float, float]:
        margin = 1.96 * self.standard_error
        return (self.pi_estimate - margin, self.pi_estimate + margin)


class MonteCarloPi:

    def __init__(self, seed=None):
        self.rng = random.Random(seed)

    def sample_points(self, number_of_points: int) -> list[tuple[float, float]]:
        if number_of_points <= 0:
            raise ValueError("Number of points must be positive.")

        uniform = self.rng.uniform
        return [
            (uniform(-1.0, 1.0), uniform(-1.0, 1.0)) for _ in range(number_of_points)
        ]

    def estimate(
        self, number_of_points: int, return_points: bool = False
    ) -> EstimationResult:
        if number_of_points <= 0:
            raise ValueError("Number of points must be positive.")

        inside_circle = 0
        if return_points:
            points = self.sample_points(number_of_points)
            for x, y in points:
                if x * x + y * y <= 1.0:
                    inside_circle += 1
        else:
            points = None
            for _ in range(number_of_points):
                x, y = self.rng.uniform(-1.0, 1.0), self.rng.uniform(-1.0, 1.0)
                if x * x + y * y <= 1.0:
                    inside_circle += 1

        pi_estimate = 4.0 * inside_circle / number_of_points

        return EstimationResult(
            pi_estimate=pi_estimate,
            points=points,
            inside_circle=inside_circle,
            total_points=number_of_points,
        )


if __name__ == "__main__":
    # Example usage
    estimator = MonteCarloPi(seed=42)
    result = estimator.estimate(10000000, return_points=False)
    print(f"Estimated π: {result.pi_estimate}")
    print(f"Absolute Error: {result.absolute_error}")
    print(f"Relative Error: {result.relative_error_percent:.4f}%")
    print(f"Standard Error: {result.standard_error}")
    print(f"95% Confidence Interval: {result.confidence_interval_95}")
