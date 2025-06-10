#!/usr/bin/env python3
# pyre-strict
import frontmatter  # type: ignore
from frontmatter import Post # type:ignore  # type: ignore
import os
import sys
import click
from forecast.models.forecast import Forecast
from forecast.factory import create_forecast

from typing import Optional, List
import datetime
from rich.console import Console
from rich.table import Table

@click.group(invoke_without_command=True)
@click.option("--tag", help="Tag to filter forecasts by.")
@click.option(
    "--type",
    help="Type to filter forecasts by. (interval, choice, pert, lognormal, pareto)",
)
@click.pass_context
def entrypoint(
    ctx: click.core.Context, tag: Optional[str], type: Optional[str]
) -> None:
    if ctx.invoked_subcommand is None:
        forecast_dir = ".forecasts"

        # If the .forecasts doesn't exist, create it
        first_run(forecast_dir)

        # Enumerate all .forecast files in the directory
        forecasts = process_forecast_files(forecast_dir, type, tag)

        # Sorting. Potentially by open date, scenario name, or default to end date. TODO
        forecasts = sorted(forecasts, key=lambda x: x.end_date, reverse=False)

        # Build the table and display it
        display_forecasts(forecasts)
    else:
        pass


@click.command()
def help() -> None:
    click.echo(
        "Place `your_filename.forecast` files in the `.forecast` directory to get started."
    )
    click.echo("They are markdown files with YAML frontmatter.")
    click.echo("Examples are in the `.forecasts` directory in this codebase.")
    click.echo(
        "When you have a forecast, run `forecast` with no arguments to see the status of your forecasts and calculate scores."
    )
    click.echo(
        "If you have many forecasts, you can use `--tag` and `--type` to filter them."
    )


entrypoint.add_command(help)


def print_days_away(days: str) -> str:
    return f"{days} days"


# Define valid forecast types as a Literal typ

def display_welcome_banner() -> None:
    click.secho(
        "FORECAST",
        bold=True,
        fg="green",
    )
    click.echo("---------------------------------------------")
    click.secho(
        "A tool for tracking and scoring forecasts with git. See examples in the `.forecasts` directory.",
        bold=True,
        fg="green",
    )
    click.echo("---------------------------------------------")


def process_forecast_files(
    forecast_dir: str, type: Optional[str], tag: Optional[str]
) -> List[Forecast]:
    forecasts: List[Forecast] = []
    for filename in os.listdir(forecast_dir):
        if filename.endswith(".forecast"):
            filepath = os.path.join(forecast_dir, filename)
            post: Post = frontmatter.load(filepath)

            forecast: Forecast = create_forecast(post)

            # First, process types if the option is set
            if type is None:
                pass
            elif type == forecast.type:
                pass
            else:
                continue

            # Process tags if the option is set
            if tag is None:
                forecasts.append(forecast)
            elif tag in forecast.tags:
                forecasts.append(forecast)

    if not forecasts:
        click.echo("No forecast files found in the '.forecast' directory.")
        sys.exit(0)

    return forecasts


def first_run(forecast_dir: str) -> None:
    if not os.path.exists(forecast_dir):
        display_welcome_banner()

        make_dir = click.confirm(
            "Create the directory '.forecast'?",
            default=False,
            abort=False,
            prompt_suffix=": ",
            show_default=True,
            err=False,
        )

        if make_dir:
            os.makedirs(forecast_dir)
            click.echo(
                "Directory created. You can now add forecast files into `.forecast` and run the command again."
            )
            click.echo(
                "If you need help getting started, there are example `.forecast` files in the `.forecasts` directory of the repository."
            )
        else:
            click.echo("Exiting.")
            sys.exit(1)


def display_forecasts(forecasts: List[Forecast]) -> None:
    console = Console()
    table = Table(title="Forecasts", show_header=True, header_style="bold white")

    table.add_column("Status", justify="center", style="cyan", no_wrap=True)
    table.add_column("Days until close", justify="center", style="white")
    table.add_column("Scenario", justify="center", style="white")
    table.add_column("Brier Score", justify="center", style="white")

    for forecast in forecasts:
        # Load this into a forecast object (Question + Answer)

        # If the forecast has an outcome, calculate the Brier score
        if hasattr(forecast, "outcome"):
            brier_score = forecast.calc()
            table.add_row(
                "[bold green]Closed[/bold green]",
                "-",
                forecast.scenario,
                f"[cyan]{brier_score:.4f}[/cyan]",
            )

        # If the forecast has an end date, calculate the days away
        elif hasattr(forecast, "end_date"):
            days_away = (forecast.end_date - datetime.date.today()).days

            if days_away < 0:
                table.add_row(
                    "[bold red]Overdue[/bold red]",
                    f"[red]{days_away}[/red]",
                    forecast.scenario,
                    "-",
                )

            else:
                table.add_row(
                    "[bold yellow]Open[/bold yellow]",
                    f"[yellow]{days_away}[/yellow]",
                    forecast.scenario,
                    "-",
                )

    console.print(table)


if __name__ == "__main__":
    entrypoint()
