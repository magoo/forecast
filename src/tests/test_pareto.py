import unittest

from forecast.models.pareto import Pareto

from frontmatter import Post


class TestPareto(unittest.TestCase):

    def test_init_with_valid_post(self) -> None:
        Pareto = Pareto(
            Post(
                scenario="A test scenario",
                type="Pareto",
                end_date="2025-01-01",
                content="",
                min=1,
                max=100,
                percentile=0.95,
                outcome=15,
            )
        )
        self.assertAlmostEqual(Pareto.calc(), 1.895235588329737)

    def test_without_max(self) -> None:
        with self.assertRaises(KeyError):
            Pareto(
                Post(
                    scenario="A test scenario",
                    type="Pareto",
                    end_date="2025-01-01",
                    content="",
                    min=1,
                    percentile=0.95,
                )
            )

    def test_without_mode(self) -> None:
        with self.assertRaises(KeyError):
            Pareto(
                Post(
                    scenario="A test scenario",
                    type="Pareto",
                    end_date="2025-01-01",
                    content="",
                    min=1,
                    max=100,
                    percentile=0.95,
                )
            )

    def test_calc_without_outcome(self) -> None:
        with self.assertRaises(KeyError):
            test = Pareto(
                Post(
                    scenario="A test scenario",
                    type="Pareto",
                    end_date="2025-01-01",
                    content="",
                    min=1,
                    max=100,
                    percentile=0.95,
                )
            )
            test.calc()

    def test_calc_with_valid_outcome(self) -> None:
        pareto = Pareto(
            Post(
                scenario="A test scenario",
                type="Pareto",
                end_date="2025-01-01",
                content="",
                min=1,
                max=100,
                percentile=0.95,
                outcome=15,
            )
        )
        self.assertAlmostEqual(pareto.calc(), 1.895235588329737)

    def test_calc_without_outcome(self) -> None:
        post_without_outcome = Post(
            scenario="A test scenario",
            type="Pareto",
            end_date="2025-01-01",
            content="",
            min=1,
            max=100,
            percentile=0.95,
        )
        pareto = Pareto(post_without_outcome)
        with self.assertRaises(ValueError):
            pareto.calc()


if __name__ == "__main__":
    unittest.main()
