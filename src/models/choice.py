from frontmatter import Post
import click
from typing import Dict
from models.forecast import Forecast


class Choice(Forecast):
    """A forecast model for discrete choice predictions.

    This class implements the Forecast base class for scenarios where the outcome
    is one of several discrete options. Each option is assigned a probability,
    and the sum of all probabilities should equal 1.

    Attributes:
        scenario (str): Inherited from Forecast, the scenario being forecasted
        end_date (datetime.date): Inherited from Forecast, the end date of the forecast
        type (str): Inherited from Forecast, the type of forecast
        tags (list[str]): Inherited from Forecast, list of tags for the forecast
        options (Dict[str, float]): Dictionary mapping option names to their probabilities
        outcome (str, optional): The actual outcome, if known

    Args:
        post (Post): A frontmatter Post object containing forecast metadata including:
            - options: Dict[str, float] mapping choices to probabilities
            - outcome: str (optional) the actual outcome if known

    Raises:
        KeyError: If required 'options' field is missing from metadata
        ValueError: If calculating Brier score with invalid outcome
    """
    def __init__(self, post: Post) -> None:
        Forecast.__init__(self, post)

        try:
            self.options: Dict[str, float] = post.metadata["options"]
        except KeyError:
            click.echo(
                "Error: The choice forecast requires an 'options' metadata field."
            )
            raise

        if "outcome" in post.metadata:
            self.outcome: str = post.metadata["outcome"]

    def calc(self) -> float:

        if hasattr(self, "outcome"):
            scoring = []

            for s, _ in self.options.items():
                if s == self.outcome:
                    scoring.append(1)
                else:
                    scoring.append(0)

            if self.outcome in self.options:
                return self.brier_score(scoring, list(self.options.values()))
            else:
                raise ValueError("The provided outcome was not in options.")
        else:
            raise ValueError("Outcome not provided in post metadata.")
