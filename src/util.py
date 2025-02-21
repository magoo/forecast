from frontmatter import Post
from models.interval import Interval
from models.choice import Choice
from models.pert import Pert
from models.lognormal import LogNormal
from models.forecast import Forecast
from models.pareto import Pareto
import click


def load_answer(post: Post, filepath: str) -> Forecast:
    # What type of answer are we given?
    post_type: str = post.metadata["type"]

    if post_type == "interval":
        return Interval(post)
    elif post_type == "choice":
        return Choice(post)
    elif post_type == "pert":
        return Pert(post)
    elif post_type == "lognormal":
        return LogNormal(post)
    elif post_type == "pareto":
        return Pareto(post)

    raise ValueError("Invalid forecast type:" + post_type)
