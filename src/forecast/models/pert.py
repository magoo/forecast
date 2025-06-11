# pyre-strict
from frontmatter import Post  # type:ignore
from .forecast import Forecast

# from typing import Type
# import elicited as e # type:ignore

# Note: The Post type from frontmatter is untyped; type checking is suppressed with # type: ignore


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

    Args:
        post: A frontmatter Post object containing forecast metadata including:
            - min: float for the minimum value
            - mode: float for the most likely value
            - max: float for the maximum value
            - outcome: float (optional) the actual outcome if known
        Note: The Post type is untyped; type checking is suppressed.

    Raises:
        KeyError: If required 'min', 'mode', or 'max' fields are missing from metadata
        ValueError: If calculating Brier score without an outcome
    """

    def __init__(self, post: Post) -> None:  # type: ignore
        # Accepts a frontmatter.Post object; type checking is suppressed due to lack of type hints in frontmatter
        Forecast.__init__(self, post)

        try:
            try:
                self.min: float = float(post.metadata["min"])  # type: ignore
                self.mode: float = float(post.metadata["mode"])  # type: ignore
                self.max: float = float(post.metadata["max"])  # type: ignore
            except (ValueError, TypeError) as e:
                raise ValueError(
                    f"Pert forecast: min, mode, and max must be numbers. Got: min={post.metadata.get('min')}, mode={post.metadata.get('mode')}, max={post.metadata.get('max')}"
                ) from e
        except KeyError:
            raise KeyError(
                "Error: The pert forecast requires a 'min', 'mode', and 'max' metadata field."
            )

        if "outcome" in post.metadata:  # type: ignore
            self.outcome: float = post.metadata["outcome"]  # type: ignore

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
