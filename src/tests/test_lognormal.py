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
                max=100,
                mode=10,
                outcome=15,
            )
        )
        self.assertAlmostEqual(lognormal.calc(), 1.895235588329737)

    def test_init_without_max(self) -> None:
        with self.assertRaises(KeyError):
            LogNormal(
            Post(
                scenario="A test scenario",
                type="lognormal",
                end_date="2025-01-01",
                content="",
                mode=10,
                outcome=15,
            )
        )

    def test_init_without_mode(self) -> None:
        with self.assertRaises(KeyError):
            LogNormal(
                Post(
                    scenario="A test scenario",
                    type="lognormal",
                    end_date="2025-01-01",
                    content="",
                    max=10,
                    outcome=15,
                )
            )

    def test_calc_without_outcome(self) -> None:
        with self.assertRaises(KeyError):
            test = LogNormal(
                Post(
                    scenario="A test scenario",
                    type="lognormal",
                    end_date="2025-01-01",
                    content="",
                    max=10,
                    mode=10,
                )
            )
            test.calc()

    def test_calc_with_valid_outcome(self) -> None:
        lognormal = LogNormal(
            Post(
                scenario="A test scenario",
                type="lognormal",
                end_date="2025-01-01",
                content="",
                max=100,
                mode=10,
                outcome=15,
            )
        )
        self.assertAlmostEqual(lognormal.calc(), 1.895235588329737)

    def test_calc_without_outcome(self) -> None:
        post_without_outcome = Post(
            scenario="A test scenario",
            type="lognormal",
            end_date="2025-01-01",
            content="",
            max=100,
            mode=10,
        )
        lognormal = LogNormal(post_without_outcome)
        
        with self.assertRaises(ValueError):
            lognormal.calc()


if __name__ == "__main__":
    unittest.main()
