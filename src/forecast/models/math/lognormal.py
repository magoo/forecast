import math
from typing import Optional

class LogNormal:
    def __init__(self, mode: float, max_95: float):
        if mode <= 0 or max_95 <= 0:
            raise ValueError("Mode and max_95 must be positive")
        if max_95 <= mode:
            raise ValueError("max_95 must be greater than mode")

        self.mode = mode
        self.max_95 = max_95
        z = 1.64485  # Approx Z-score for 95%

        log_mode = math.log(mode)
        log_max = math.log(max_95)
        D = log_max - log_mode

        # Solve quadratic: sigma^2 + z*sigma - D = 0
        a, b, c = 1, z, -D
        sqrt_term = math.sqrt(b * b - 4 * a * c)
        self.sigma = (-b + sqrt_term) / (2 * a)

        # Now compute mu from mode = exp(mu - sigma^2)
        self.mu = log_mode + self.sigma ** 2

    def pdf(self, x: float) -> float:
        if x <= 0:
            return 0.0
        coeff = 1 / (x * self.sigma * math.sqrt(2 * math.pi))
        exponent = -((math.log(x) - self.mu) ** 2) / (2 * self.sigma ** 2)
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
        # Approximation from Abramowitz & Stegun
        sign = 1 if x >= 0 else -1
        x = abs(x)
        a1, a2, a3, a4, a5 = 0.254829592, -0.284496736, 1.421413741, -1.453152027, 1.061405429
        p = 0.3275911
        t = 1 / (1 + p * x)
        y = 1 - (((((a5 * t + a4) * t + a3) * t + a2) * t + a1) * t * math.exp(-x * x))
        return sign * y

    @staticmethod
    def _erfinv(y: float) -> float:
        # Approximate inverse erf (based on Winitzki approximation)
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
        """
        Converts the PDF at x to a probability by integrating over [x-epsilon, x+epsilon].
        If epsilon is not provided, use 1% of the mode as a default scale.
        """
        if epsilon is None:
            epsilon = 0.01 * self.mode
        a = max(0, x - epsilon)
        b = x + epsilon
        return self.cdf(b) - self.cdf(a)
