import math
from typing import Optional


class LogNormal:
    def __init__(self, p5: float, p50: float, p95: float):
        if p50 <= 0 or p95 <= 0:
            raise ValueError("p50 and p95 must be positive")
        if p95 <= p50:
            raise ValueError("p95 must be greater than p50")

        self.p50 = p50
        self.p95 = p95
        self.p5 = p5

        log_p50 = math.log(p50)
        log_p95 = math.log(p95)

        z95 = 1.64485  # Z-score for 95th percentile

        if p5 <= 0 or p5 >= p50:
            raise ValueError("p5 must be positive and less than p50")

        log_p5 = math.log(p5)
        z5 = -1.64485
        # Fit using both tails
        self.sigma = (log_p95 - log_p5) / (z95 - z5)

        self.mu = log_p50

    def pdf(self, x: float) -> float:
        if x <= 0:
            return 0.0
        coeff = 1 / (x * self.sigma * math.sqrt(2 * math.pi))
        exponent = -((math.log(x) - self.mu) ** 2) / (2 * self.sigma**2)
        return coeff * math.exp(exponent)

    def cdf(self, x: float) -> float:
        if x <= 0:
            return 0.0
        z = (math.log(x) - self.mu) / (self.sigma * math.sqrt(2))
        return 0.5 * (1 + self._erf(z))

    def ppf(self, p: float) -> float:
        if not (0 < p < 1):
            raise ValueError("p must be in (0, 1)")
        z = self._sqrt2_inv() * self._erfinv(2 * p - 1)
        return math.exp(self.mu + self.sigma * z)

    @staticmethod
    def _erf(x: float) -> float:
        sign = 1 if x >= 0 else -1
        x = abs(x)
        a1, a2, a3, a4, a5 = (
            0.254829592,
            -0.284496736,
            1.421413741,
            -1.453152027,
            1.061405429,
        )
        p = 0.3275911
        t = 1 / (1 + p * x)
        y = 1 - (((((a5 * t + a4) * t + a3) * t + a2) * t + a1) * t * math.exp(-x * x))
        return sign * y

    @staticmethod
    def _erfinv(y: float) -> float:
        a = 0.147
        if y <= -1 or y >= 1:
            raise ValueError("erfinv only defined for -1 < y < 1")
        ln = math.log(1 - y**2)
        s = (2 / (math.pi * a)) + (ln / 2)
        return math.copysign(math.sqrt(math.sqrt(s**2 - ln / a) - s), y)

    @staticmethod
    def _sqrt2_inv() -> float:
        return 1 / math.sqrt(2)

    def pdf_to_probability(self, x: float, epsilon: Optional[float] = None) -> float:
        if epsilon is None:
            epsilon = 0.01 * self.p50
        a = max(0, x - epsilon)
        b = x + epsilon
        return self.cdf(b) - self.cdf(a)
