import math
from typing import Optional

class Pareto:
    def __init__(self, xmin: float, xmax: float, percentile: float):
        if not (0 < percentile < 1):
            raise ValueError("Percentile must be between 0 and 1")
        if xmin <= 0 or xmax <= xmin:
            raise ValueError("xmin must be > 0 and xmax must be > xmin")

        self.xmin = xmin
        self.xmax = xmax
        self.percentile = percentile

        # Derive alpha from the CDF inversion
        self.alpha = math.log(1 - percentile) / math.log(xmin / xmax)

    def pdf(self, x: float) -> float:
        if x < self.xmin:
            return 0.0
        return self.alpha * self.xmin**self.alpha / x**(self.alpha + 1)

    def cdf(self, x: float) -> float:
        if x < self.xmin:
            return 0.0
        return 1 - (self.xmin / x)**self.alpha

    def ppf(self, p: float) -> float:
        if not (0 < p < 1):
            raise ValueError("p must be between 0 and 1")
        return self.xmin / (1 - p)**(1 / self.alpha)

    def mean(self) -> float:
        if self.alpha <= 1:
            return float('inf')
        return self.alpha * self.xmin / (self.alpha - 1)

    def var(self) -> float:
        if self.alpha <= 2:
            return float('inf')
        return (self.xmin**2 * self.alpha) / ((self.alpha - 1)**2 * (self.alpha - 2))

    def pdf_to_probability(self, x: float, epsilon: Optional[float] = None) -> float:
        """
        Converts the PDF at x to a probability by integrating over [x-epsilon, x+epsilon].
        If epsilon is not provided, use 1% of xmin as a default scale.
        """
        if epsilon is None:
            epsilon = 0.01 * self.xmin
        a = max(self.xmin, x - epsilon)
        b = x + epsilon
        return self.cdf(b) - self.cdf(a)
