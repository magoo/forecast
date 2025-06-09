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
    using a mode (most likely value) and a maximum value, which are used to fit
    the lognormal parameters.

    Attributes:
        scenario (str): Inherited from Forecast, the scenario being forecasted
        end_date (datetime.date): Inherited from Forecast, the end date of the forecast
        type (str): Inherited from Forecast, the type of forecast
        tags (list[str]): Inherited from Forecast, list of tags for the forecast
        mode (float): The most likely value (mode) of the distribution
        max (float): The maximum value used to fit the distribution
        outcome (float, optional): The actual outcome value, if known
        lognormal: The fitted lognormal distribution

    Args:
        post (Post): A frontmatter Post object containing forecast metadata including:
            - mode: float for the most likely value
            - max: float for the maximum value
            - quantP: float (optional) the probability quantile for fitting (default 0.95)
            - outcome: float (optional) the actual outcome if known

    Raises:
        KeyError: If required 'mode' or 'max' fields are missing from metadata
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
