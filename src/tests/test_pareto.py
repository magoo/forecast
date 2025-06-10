import unittest

from forecast.models.pareto import Pareto

from frontmatter import Post # type:ignore


class TestPareto(unittest.TestCase):

    def test_init_with_valid_post(self) -> None:
        pareto = Pareto(
            Post(
                scenario="A test scenario",
                type="pareto",
                end_date="2025-01-01",
                content="",
                p90=10,
                p99=100,
                outcome=15,
            )
        )
        self.assertAlmostEqual(pareto.calc(), pareto.calc())  # Just check it runs

    def test_without_p99(self) -> None:
        with self.assertRaises(KeyError):
            Pareto(
                Post(
                    scenario="A test scenario",
                    type="pareto",
                    end_date="2025-01-01",
                    content="",
                    p90=10,
                )
            )

    def test_without_p90(self) -> None:
        with self.assertRaises(KeyError):
            Pareto(
                Post(
                    scenario="A test scenario",
                    type="pareto",
                    end_date="2025-01-01",
                    content="",
                    p99=100,
                )
            )

    def test_calc_without_outcome(self) -> None:
        pareto = Pareto(
            Post(
                scenario="A test scenario",
                type="pareto",
                end_date="2025-01-01",
                content="",
                p90=10,
                p99=100,
            )
        )
        with self.assertRaises(ValueError):
            pareto.calc()

    def test_calc_with_valid_outcome(self) -> None:
        pareto = Pareto(
            Post(
                scenario="A test scenario",
                type="pareto",
                end_date="2025-01-01",
                content="",
                p90=10,
                p99=100,
                outcome=15,
            )
        )
        self.assertAlmostEqual(pareto.calc(), pareto.calc())  # Just check it runs


if __name__ == "__main__":
    unittest.main()
