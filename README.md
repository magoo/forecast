# forecast

A command-line tool for tracking and scoring personal forecasts. Track your predictions over time and measure your forecasting accuracy using various probability distributions.

## Installation

```bash
git clone https://github.com/yourusername/forecast.git
cd forecast
```

Create a virtual environment

```bash
python -m venv env
```

Activate the virtual environment

```bash
source env/bin/activate
```

Install the dependencies

```bash
pip install -r requirements.txt
```

Install the package

```bash
pip install .
```

Then run the CLI

```bash
forecast
```

The first run will show you output with the pre-existing `.forecasts` directory. Take a look at the examples in that folder to get started.

## Usage

Show and score all existing forecasts. If `.forecasts` directory does not exist, it will prompt for creation. If none exist, it will exit.

```bash
forecast
```

Filter forecasts by tag:

```bash
forecast --tag <tag>
```

Show all forecasts by type:

```bash
forecast --type <type>
```


## Forecast Types

The tool supports several types of probabilistic forecasts:

- **Choice**: Discrete choices with assigned probabilities
- **Interval**: Min/max range with confidence level
- **PERT**: Three-point estimation (min/mode/max)
- **LogNormal**: Mode and max (95th percentile)
- **Pareto**: Power law distribution

## Creating Forecasts

Create `your_filename.forecast` files in your `.forecasts` directory. They look a lot like [Frontmatter](https://jekyllrb.com/docs/frontmatter/) files, with specific keys for metadata. Example:

```markdown
---
scenario: "Will it rain tomorrow?"
end_date: 2024-12-31
type: choice
options:
"Yes": 0.7
"No": 0.3
---

Some markdown text describing whether it will rain tomorrow.
```

Examples are in the `.forecasts` directory in the repo.
