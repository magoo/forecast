import math

class LogNormal:
    def __init__(self, mode: float, max_95: float):
        if mode <= 0 or max_95 <= 0:
            raise ValueError("Mode and max_95 must be positive")
        if max_95 <= mode:
            raise ValueError("max_95 must be greater than mode")

        self.mode = mode
        self.max_95 = max_95

        # Estimate mu and sigma using the properties:
        # mode = exp(mu - sigma^2)
        # 95th percentile = exp(mu + 1.64485 * sigma)
        log_mode = math.log(mode)
        log_max = math.log(max_95)

        # Derive sigma
        self.sigma = (log_max - log_mode) / (1.64485 + 1.0)
        # Derive mu
        self.mu = log_mode + self.sigma

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
        if p <= 0.0 or p >= 1.0:
            raise ValueError("p must be in (0, 1)")
        z = self._sqrt2_inv() * self._erfinv(2 * p - 1)
        return math.exp(self.mu + self.sigma * z)

    @staticmethod
    def _erf(x: float) -> float:
        # Approximation to the error function using Abramowitz & Stegun formula 7.1.26
        # https://en.wikipedia.org/wiki/Error_function#Approximation_with_elementary_functions
        sign = 1 if x >= 0 else -1
        x = abs(x)
        a1 = 0.254829592
        a2 = -0.284496736
        a3 = 1.421413741
        a4 = -1.453152027
        a5 = 1.061405429
        p = 0.3275911

        t = 1 / (1 + p * x)
        y = 1 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x)
        return sign * y

    @staticmethod
    def _erfinv(y: float) -> float:
        # Approximate inverse error function
        # Reference: https://stackoverflow.com/questions/27229371/inverse-error-function-in-python
        a = 0.147  # Magic constant
        if y <= -1 or y >= 1:
            raise ValueError("erfinv only defined for -1 < y < 1")
        ln = math.log(1 - y**2)
        s = (2 / (math.pi * a)) + (ln / 2)
        root = math.sqrt(s**2 - ln / a)
        return math.copysign(math.sqrt(root - s), y)

    @staticmethod
    def _sqrt2_inv() -> float:
        return 1 / math.sqrt(2)