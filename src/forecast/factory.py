from frontmatter import Post # type:ignore # type: ignore
from forecast.models.forecast import Forecast
from forecast.models.interval import Interval
from forecast.models.choice import Choice
from forecast.models.pert import Pert
from forecast.models.lognormal import LogNormal
from forecast.models.pareto import Pareto


def create_forecast(post: Post) -> Forecast:
    """Factory function to create the appropriate forecast type."""
    forecast_type = post.metadata["type"]
    forecast_classes = {
        "interval": Interval,
        "choice": Choice,
        "pert": Pert,
        "lognormal": LogNormal,
        "pareto": Pareto,
    }
    
    if forecast_type in forecast_classes:
        return forecast_classes[forecast_type](post)
        
    raise ValueError(f"Invalid forecast type: {forecast_type}")
