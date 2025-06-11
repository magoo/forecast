# pyre-strict
from frontmatter import Post  # type:ignore
from abc import ABC, abstractmethod
import datetime


class Forecast(ABC):
    """Abstract base class for forecast models.

    This class serves as a template for different types of forecasting models,
    providing common functionality for handling forecast metadata and calculating
    Brier scores.

    Attributes:
        scenario (str): The scenario being forecasted
        end_date (datetime.date): The end date of the forecast
        type (str): The type of forecast
        tags (list[str]): List of tags associated with the forecast

    Args:
        post (Post): A frontmatter Post object containing forecast metadata
    """

    @abstractmethod
    def calc(self) -> float:
        """Calculate the forecast score based on the outcome.

        This method must be implemented by all forecast types to compute
        their specific scoring mechanism.

        Returns:
            float: The calculated score for this forecast
        """
        pass

    def __init__(self, post: Post) -> None:  # type: ignore
        try:
            self.scenario: str = post.metadata["scenario"]  # type: ignore
            end_date_raw = post.metadata["end_date"]  # type: ignore
            if isinstance(end_date_raw, datetime.date):
                end_date = end_date_raw
            else:
                try:
                    end_date = datetime.datetime.strptime(
                        str(end_date_raw), "%Y-%m-%d"
                    ).date()
                except Exception:
                    raise ValueError(
                        f"end_date '{end_date_raw}' is not a valid YYYY-MM-DD date string."
                    )

            self.end_date: datetime.date = end_date
            self.type: str = post.metadata["type"]  # type: ignore
            self.tags: list[str] = post.metadata.get("tags", [""])  # type: ignore
        except KeyError:
            raise KeyError(
                "Error: The scenario metadata is incorrect. Please refer to an example file to troubleshoot. "
            )

    #  if "outcome" in post.metadata:
    #     self.brier: float = self.calc()

    def brier_score(self, outcomes: list[float], forecasts: list[float]) -> float:
        """Calculate the Brier score between actual outcomes and forecasted probabilities.

        The Brier score measures the accuracy of probabilistic predictions, where a lower
        score indicates better accuracy. The score is calculated as the sum of squared
        differences between each outcome (typically 0 or 1) and its forecasted probability.

        Args:
            outcome: List of actual outcomes, typically 0s and 1s
            forecast: List of forecasted probabilities, between 0 and 1

        Returns:
            float: The Brier score (sum of squared errors, as used by GJ Open)

        Raises:
            ValueError: If outcome and forecast lists have different lengths
        """

        if len(outcomes) != len(forecasts):
            raise ValueError(
                "The outcome and forecast lists must be of the same length."
            )

        total_score = 0

        for outcome, forecast in zip(outcomes, forecasts):
            total_score += (outcome - forecast) ** 2

        return total_score
