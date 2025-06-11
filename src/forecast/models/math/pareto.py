import math
from typing import Optional


class Pareto:
    def __init__(self, p90: float, p99: float):

        if p90 <= 0 or p99 <= p90:
            raise ValueError("Percentiles must be positive and p99 must be > p90")

        self.p90 = p90
        self.p99 = p99
        q90 = 0.90
        q99 = 0.99

        # Solve for alpha using two quantiles and the Pareto inverse CDF formula:
        # x = xmin / (1 - p)^(1/alpha)
        # log(p99/p90) = (1/alpha) * log((1 - q90)/(1 - q99))

        log_ratio_x = math.log(p99 / p90)
        log_ratio_q = math.log((1 - q90) / (1 - q99))

        self.alpha = log_ratio_q / log_ratio_x

        # Backsolve for xmin using one of the quantiles
        self.xmin = p90 * (1 - q90) ** (1 / self.alpha)

    def pdf(self, x: float) -> float:
        if x < self.xmin:
            return 0.0
        return self.alpha * self.xmin**self.alpha / x ** (self.alpha + 1)

    def cdf(self, x: float) -> float:
        if x < self.xmin:
            return 0.0
        return 1 - (self.xmin / x) ** self.alpha

    def ppf(self, p: float) -> float:
        if not (0 < p < 1):
            raise ValueError("p must be between 0 and 1")
        return self.xmin / (1 - p) ** (1 / self.alpha)

    def mean(self) -> float:
        if self.alpha <= 1:
            return float("inf")
        return self.alpha * self.xmin / (self.alpha - 1)

    def var(self) -> float:
        if self.alpha <= 2:
            return float("inf")
        return (self.xmin**2 * self.alpha) / ((self.alpha - 1) ** 2 * (self.alpha - 2))

    def pdf_to_probability(self, x: float, epsilon: Optional[float] = None) -> float:
        """
        Converts the PDF at x to a probability by integrating over [x-epsilon, x+epsilon].
        If epsilon is not provided, use 1% of xmin as a default scale.
        """
        eps = epsilon if epsilon is not None else 0.01 * self.xmin
        a = max(self.xmin, x - eps)
        b = x + eps
        return self.cdf(b) - self.cdf(a)
