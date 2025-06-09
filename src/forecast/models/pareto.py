# pyre-strict
from frontmatter import Post # type:ignore
from .forecast import Forecast
# import elicited as e # type:ignore


class Pareto(Forecast):
    """A forecast model for Pareto distributed predictions.

    This class implements the Forecast base class for scenarios where the outcome
    is expected to follow a Pareto distribution. The distribution is parameterized
    using a minimum value, maximum value, and a percentile value which are used to
    fit the Pareto parameter.

    Attributes:
        scenario (str): Inherited from Forecast, the scenario being forecasted
        end_date (datetime.date): Inherited from Forecast, the end date of the forecast
        type (str): Inherited from Forecast, the type of forecast
        tags (list[str]): Inherited from Forecast, list of tags for the forecast
        min (float): The minimum value of the distribution
        max (float): The maximum value used to fit the distribution
        percentile (float): The probability percentile for fitting (between 0 and 1)
        outcome (float, optional): The actual outcome value, if known

    Args:
        post (Post): A frontmatter Post object containing forecast metadata including:
            - min: float for the minimum value
            - max: float for the maximum value
            - percentile: float for the probability percentile (between 0 and 1)
            - outcome: float (optional) the actual outcome if known

    Raises:
        KeyError: If required 'min', 'max', or 'percentile' fields are missing from metadata
        ValueError: If percentile is not between 0 and 1 or if calculating Brier score without an outcome
    """
    def __init__(self, post: Post) -> None:# type: ignore
        Forecast.__init__(self, post)# type: ignore
        try:
            self.p90: float = float(post.metadata["p90"]) # type: ignore
            self.p99: float = float(post.metadata["p99"]) # type: ignore

        except KeyError:
            raise KeyError(
                "Error: The pareto forecast requires a 'p90' and 'p99' field."
            )

        if "outcome" in post.metadata: # type: ignore
            self.outcome: float = post.metadata["outcome"] # type: ignore

    def calc(self) -> float:
        if hasattr(self, "outcome"):
            import forecast.models.math.pareto as p
            pareto = p.Pareto(self.p90, self.p99)
            outcome_probability: float = pareto.pdf_to_probability(self.outcome)
            return self.brier_score(
                [1, 0], [outcome_probability, 1 - outcome_probability]
            )
        else:
            raise ValueError("Outcome not provided in post metadata.")
