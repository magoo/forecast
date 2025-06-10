# pyre-strict
from frontmatter import Post # type:ignore

# import elicited as e # type:ignore
#import numpy as np
#from typing import Type
from .forecast import Forecast


class LogNormal(Forecast):
    """A forecast model for lognormally distributed predictions.

    This class implements the Forecast base class for scenarios where the outcome
    is expected to follow a lognormal distribution. The distribution is parameterized
    using three quantiles: p5, p50, and p95, which are used to fit the lognormal parameters.

    Attributes:
        scenario (str): Inherited from Forecast, the scenario being forecasted
        end_date (datetime.date): Inherited from Forecast, the end date of the forecast
        type (str): Inherited from Forecast, the type of forecast
        tags (list[str]): Inherited from Forecast, list of tags for the forecast
        p5 (float): The 5th percentile value of the distribution
        p50 (float): The 50th percentile (median) value of the distribution
        p95 (float): The 95th percentile value of the distribution
        outcome (float, optional): The actual outcome value, if known

    Args:
        post: A frontmatter Post object containing forecast metadata including:
            - p5: float for the 5th percentile value
            - p50: float for the 50th percentile (median) value
            - p95: float for the 95th percentile value
            - outcome: float (optional) the actual outcome if known
        Note: The Post type is untyped; type checking is suppressed.

    Raises:
        KeyError: If required 'p5', 'p50', or 'p95' fields are missing from metadata
        ValueError: If calculating Brier score without an outcome
    """

    def __init__(self, post: Post) -> None: # type: ignore
        Forecast.__init__(self, post) # type: ignore

        try:
            self.p5: float = post.metadata["p5"] # type: ignore
            self.p50: float = post.metadata["p50"] # type: ignore
            self.p95: float = post.metadata["p95"] # type: ignore

        except KeyError:
            raise KeyError(
                "Error: The lognormal forecast requires a 'p5', 'p50', and 'p95' metadata field.",
            )

        if "outcome" in post.metadata: # type: ignore
            self.outcome: float = post.metadata["outcome"] # type: ignore


    def calc(self) -> float:
        if hasattr(self, "outcome"):
            import forecast.models.math.lognormal as ln
            lognormal = ln.LogNormal(self.p5, self.p50, self.p95)
            outcome_probability: float = lognormal.pdf_to_probability(self.outcome)
            return self.brier_score(
                [1, 0], [outcome_probability, 1 - outcome_probability]
            )
        else:
            raise ValueError("Outcome not provided in post metadata.")
