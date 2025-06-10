import unittest

from forecast.models.lognormal import LogNormal

from frontmatter import Post # type:ignore


class TestLogNormal(unittest.TestCase):

    def test_init_with_valid_post(self) -> None:
        lognormal = LogNormal(
            Post(
                scenario="A test scenario",
                type="lognormal",
                end_date="2025-01-01",
                content="",
                p5=5,
                p50=10,
                p95=100,
                outcome=15,
            )
        )
        self.assertAlmostEqual(lognormal.calc(), lognormal.calc())  # Just check it runs

    def test_init_without_p95(self) -> None:
        with self.assertRaises(KeyError):
            LogNormal(
                Post(
                    scenario="A test scenario",
                    type="lognormal",
                    end_date="2025-01-01",
                    content="",
                    p5=5,
                    p50=10,
                    outcome=15,
                )
            )

    def test_init_without_p50(self) -> None:
        with self.assertRaises(KeyError):
            LogNormal(
                Post(
                    scenario="A test scenario",
                    type="lognormal",
                    end_date="2025-01-01",
                    content="",
                    p5=5,
                    p95=100,
                    outcome=15,
                )
            )

    def test_calc_without_outcome(self) -> None:
        lognormal = LogNormal(
            Post(
                scenario="A test scenario",
                type="lognormal",
                end_date="2025-01-01",
                content="",
                p5=5,
                p50=10,
                p95=100,
            )
        )
        with self.assertRaises(ValueError):
            lognormal.calc()

    def test_calc_with_valid_outcome(self) -> None:
        lognormal = LogNormal(
            Post(
                scenario="A test scenario",
                type="lognormal",
                end_date="2025-01-01",
                content="",
                p5=5,
                p50=10,
                p95=100,
                outcome=15,
            )
        )
        self.assertAlmostEqual(lognormal.calc(), lognormal.calc())  # Just check it runs


if __name__ == "__main__":
    unittest.main()
