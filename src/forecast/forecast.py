#!/usr/bin/env python3
# pyre-strict

import frontmatter
from frontmatter import Post
import os
import sys
import click
from .models.forecast import Forecast
import datetime
from .util import load_answer


@click.group(invoke_without_command=True)
@click.option("--tag", help="Tag to filter forecasts by.")
@click.option(
    "--type",
    help="Type to filter forecasts by. (interval, choice, pert, lognormal, pareto)",
)
@click.pass_context
def entrypoint(ctx, tag, type) -> None:  # pyre-ignore

    if ctx.invoked_subcommand is None:  # We execute the default command
        forecast_dir = ".forecasts"
        forecasts = []

        if not os.path.exists(forecast_dir):
            click.echo(
                "███████╗ ██████╗ ██████╗ ███████╗ ██████╗ █████╗ ███████╗████████╗"
            )
            click.echo(
                "██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗██╔════╝╚══██╔══╝"
            )
            click.echo(
                "█████╗  ██║   ██║██████╔╝█████╗  ██║     ███████║███████╗   ██║   "
            )
            click.echo(
                "██╔══╝  ██║   ██║██╔══██╗██╔══╝  ██║     ██╔══██║╚════██║   ██║   "
            )
            click.echo(
                "██║     ╚██████╔╝██║  ██║███████╗╚██████╗██║  ██║███████║   ██║   "
            )
            click.echo(
                "╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝   ╚═╝   "
            )
            click.echo("---------------------------------------------")
            click.secho(
                "A tool for tracking and scoring forecasts with git. See examples in the `examples` directory.",
                bold=True,
                fg="green",
            )
            click.echo("---------------------------------------------")

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
                    "If you need help getting started, there are example `.forecast` files in the `examples` directory of the repository."
                )
            else:
                click.echo("Exiting.")
                sys.exit(1)

        # Enumerate all .forecast files in the directory

        for filename in os.listdir(forecast_dir):
            if filename.endswith(".forecast"):
                filepath = os.path.join(forecast_dir, filename)
                post: Post = frontmatter.load(filepath)

                forecast: Forecast = load_answer(post, filepath)

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

        # Sorting. Potentially by open date, scenario name, or default to end date. TODO
        forecasts = sorted(forecasts, key=lambda x: x.end_date, reverse=False)

        for forecast in forecasts:
            # Load this into a forecast object (Question + Answer)

            # If the forecast has an outcome, calculate the Brier score
            if hasattr(forecast, "outcome"):
                click.echo(
                    print_columns(
                        "0",
                        forecast.scenario,
                        forecast.calc(),
                    )
                )
            # If the forecast has an end date, calculate the days away
            elif hasattr(forecast, "end_date"):
                days_away = (forecast.end_date - datetime.date.today()).days

                if days_away < 0:
                    click.echo(
                        print_columns(
                            "x", forecast.scenario, f"overdue by {abs(days_away)} days"
                        )
                    )
                else:
                    click.echo(
                        print_columns(
                            "_",
                            forecast.scenario,
                            print_days_away(days_away),
                        )
                    )
    else:
        # Display help message if no subcommand is provided
        pass


@click.command()
def help() -> None:
    click.echo(
        "Place `foobar.forecast` files in the `.forecast` directory to get started."
    )
    click.echo("They are markdown files with YAML frontmatter.")
    click.echo("Examples are in the `examples` directory in this codebase.")
    click.echo(
        "When you have a forecast, run `forecast` with no arguments to see the status of your forecasts and calculate scores."
    )
    click.echo(
        "If you have many forecasts, you can use `--tag` and `--type` to filter them."
    )


entrypoint.add_command(help)


# @click.command()
# def stat() -> None:
#     click.echo(
#         "Average Brier Score, average brier score across tags, and calibration plot"
#     )
#
# entrypoint.add_command(stat)


def print_columns(indicator: str, text: str, text2: str) -> str:
    return "{: <1}: {: <30} {: <30}".format(indicator, text, text2)


def print_days_away(days: str) -> str:
    return f"closes in {days} days"


