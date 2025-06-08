# pyre-strict
from frontmatter import Post # type:ignore
from .forecast import Forecast
#from typing import Type
#import elicited as e # type:ignore


class Pert(Forecast):
    """A forecast model for PERT distributed predictions.

    This class implements the Forecast base class for scenarios where the outcome
    is expected to follow a PERT (Program Evaluation and Review Technique) distribution.
    The distribution is parameterized using minimum, most likely (mode), and maximum
    values which are used to fit the beta distribution parameters.

    Attributes:
        scenario (str): Inherited from Forecast, the scenario being forecasted
        end_date (datetime.date): Inherited from Forecast, the end date of the forecast
        type (str): Inherited from Forecast, the type of forecast
        tags (list[str]): Inherited from Forecast, list of tags for the forecast
        min (float): The minimum value of the distribution
        mode (float): The most likely value (mode) of the distribution
        max (float): The maximum value of the distribution
        outcome (float, optional): The actual outcome value, if known
        pert (scipy.stats.beta): The fitted beta distribution with PERT parameters

    Args:
        post (Post): A frontmatter Post object containing forecast metadata including:
            - min: float for the minimum value
            - mode: float for the most likely value
            - max: float for the maximum value
            - outcome: float (optional) the actual outcome if known

    Raises:
        KeyError: If required 'min', 'mode', or 'max' fields are missing from metadata
        ValueError: If calculating Brier score without an outcome
    """

    def __init__(self, post: Post) -> None:
        Forecast.__init__(self, post)

        try:
            self.min: float = float(post.metadata["min"]) # type: ignore
            self.mode: float = float(post.metadata["mode"]) # type: ignore
            self.max: float = float(post.metadata["max"]) # type: ignore
        except KeyError:
            raise KeyError(
                "Error: The pert forecast requires a 'min', 'mode', and 'max' metadata field."
            )

        if "outcome" in post.metadata:
            self.outcome: float = post.metadata["outcome"] # type: ignore





    def calc(self) -> float:
        if hasattr(self, "outcome"):
            import forecast.models.math.PERT as p
            pert = p.PERT(self.min, self.mode, self.max)
            outcome_probability: float = pert.pdf_to_probability(self.outcome)
            return self.brier_score(
                [1, 0], [outcome_probability, 1 - outcome_probability]
            )
        else:
            raise ValueError("Outcome not provided in post metadata.")
