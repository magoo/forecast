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
        lognormal (scipy.stats.lognorm): The fitted lognormal distribution

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

    def __init__(self, post: Post) -> None:
        Forecast.__init__(self, post)

        try:
            self.mode: float = post.metadata["mode"] # type: ignore
            self.max: float = post.metadata["max"] # type: ignore

        except KeyError:
            raise KeyError(
                "Error: The lognormal forecast requires a 'mode' and 'max' metadata field.",
            )

        if "outcome" in post.metadata:
            self.outcome: float = post.metadata["outcome"] # type: ignore

            if "quantP" in post.metadata:
                self.quantP = post.metadata["quantP"]
            else:
                self.quantP = 0.95


    def calc(self) -> float:

        if hasattr(self, "outcome"):


            #import scipy # type:ignore
            #from scipy.stats import lognorm # type:ignore
#
            #mean, stdv = e.elicitLogNormal(self.mode, self.max, quantP=self.quantP) # type: ignore
            #self.lognormal: Type[scipy.stats._distn_infrastructure.rv_continuous_frozen] = (
            #    lognorm(s=stdv[0], scale=np.exp(mean[0])) # type: ignore
            #)  # TODO, may be a bug here. Unsure why elicitLogNormal returns a list
#
            #outcome_probability: float = self.lognormal.pdf(  # type: ignore
            #    x=self.outcome
            #)

            import forecast.models.math.lognormal as ln

            lognormal = ln.LogNormal(self.mode, self.max)

            outcome_probability: float = lognormal.pdf(self.outcome)

            return self.brier_score(
                [1, 0], [outcome_probability, 1 - outcome_probability]
            )
        else:
            raise ValueError("Outcome not provided in post metadata.")
