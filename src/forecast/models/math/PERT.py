import math
from typing import Optional

class PERT:
    def __init__(self, xmin: float, mode: float, xmax: float):
        if not (xmin <= mode <= xmax):
            raise ValueError("mode must be between xmin and xmax")
        if xmin == xmax:
            raise ValueError("xmin and xmax must be different")

        self.xmin = xmin
        self.xmax = xmax
        self.mode = mode
        self.range = xmax - xmin

        # Calculate alpha and beta parameters
        self.alpha = 1 + 4 * (mode - xmin) / self.range
        self.beta = 1 + 4 * (xmax - mode) / self.range

    def _beta_pdf(self, x: float) -> float:
        # Beta PDF on [0, 1]
        if x <= 0 or x >= 1:
            return 0.0
        B = math.gamma(self.alpha) * math.gamma(self.beta) / math.gamma(self.alpha + self.beta)
        return (x ** (self.alpha - 1)) * ((1 - x) ** (self.beta - 1)) / B

    def _beta_cdf(self, x: float) -> float:
        # Approximate Beta CDF using continued fraction for regularized incomplete beta function
        # We'll use a simple numerical integration fallback here
        steps = 100
        total = 0
        dx = x / steps
        for i in range(1, steps + 1):
            total += self._beta_pdf(i * dx)
        return total * dx

    def pdf(self, x: float) -> float:
        if x < self.xmin or x > self.xmax:
            return 0.0
        scaled_x = (x - self.xmin) / self.range
        return self._beta_pdf(scaled_x) / self.range

    def cdf(self, x: float) -> float:
        if x <= self.xmin:
            return 0.0
        if x >= self.xmax:
            return 1.0
        scaled_x = (x - self.xmin) / self.range
        return self._beta_cdf(scaled_x)

    def mean(self) -> float:
        return (self.xmin + self.xmax + 4 * self.mode) / 6

    def variance(self) -> float:
        return ((self.xmax - self.xmin) ** 2 * (1 + 4)) / (36 * (1 + 4 + 1))

    def ppf(self, p: float) -> float:
        # Approximate inverse CDF via bisection search
        if not (0 < p < 1):
            raise ValueError("p must be between 0 and 1")
        low = self.xmin
        high = self.xmax
        for _ in range(100):
            mid = (low + high) / 2
            cdf_val = self.cdf(mid)
            if abs(cdf_val - p) < 1e-5:
                return mid
            if cdf_val < p:
                low = mid
            else:
                high = mid
        return (low + high) / 2

    def pdf_to_probability(self, x: float, epsilon: Optional[float] = None) -> float:
        """
        Converts the PDF at x to a probability by integrating over [x-epsilon, x+epsilon].
        If epsilon is not provided, use 1% of the range.
        """
        if epsilon is None:
            epsilon = 0.01 * self.range
        a = max(self.xmin, x - epsilon)
        b = min(self.xmax, x + epsilon)
        return self.cdf(b) - self.cdf(a)
