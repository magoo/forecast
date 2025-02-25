from frontmatter import Post
import click
from scipy.stats import beta
import elicited as e
from .forecast import Forecast
from typing import Type


class Interval(Forecast):
    """A forecast model for interval predictions.

    This class implements the Forecast base class for scenarios where the outcome
    is predicted to fall within a specified interval with a given confidence level.
    The forecast consists of a minimum value, maximum value, and the probability
    that the actual outcome will fall within that range.

    Attributes:
        scenario (str): Inherited from Forecast, the scenario being forecasted
        end_date (datetime.date): Inherited from Forecast, the end date of the forecast
        type (str): Inherited from Forecast, the type of forecast
        tags (list[str]): Inherited from Forecast, list of tags for the forecast
        min (float): The minimum value of the predicted interval
        max (float): The maximum value of the predicted interval
        confidence (float): The probability (between 0 and 1) that the outcome falls in the interval
        outcome (float, optional): The actual outcome value, if known

    Args:
        post (Post): A frontmatter Post object containing forecast metadata including:
            - min: float for minimum value of interval
            - max: float for maximum value of interval
            - confidence: float for probability of outcome in interval
            - outcome: float (optional) the actual outcome if known

    Raises:
        KeyError: If required 'min', 'max', or 'confidence' fields are missing from metadata
        ValueError: If calculating Brier score without an outcome
    """
    def __init__(self, post: Post) -> None:
        Forecast.__init__(self, post)

        try:
            self.min: float = float(post.metadata["min"])
            self.max: float = float(post.metadata["max"])
            self.confidence: float = float(post.metadata["confidence"])
        except KeyError:
            raise KeyError(
                "Error: The interval forecast requires a 'min', 'max', and 'confidence' metadata field."
            )

        if "outcome" in post.metadata:
            self.outcome: float = post.metadata["outcome"]

    def calc(self) -> float:

        if hasattr(self, "outcome"):

            if self.min <= self.outcome <= self.max:
                return self.brier_score([1, 0], [self.confidence, 1 - self.confidence])
            else:
                return self.brier_score([0, 1], [self.confidence, 1 - self.confidence])

        else:
            raise ValueError("Outcome not provided in post metadata.")
