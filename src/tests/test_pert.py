import unittest
from forecast.models.pert import Pert
from frontmatter import Post  # type:ignore


class TestPert(unittest.TestCase):

    def test_with_valid_post(self) -> None:
        pert = Pert(
            Post(
                scenario="A test scenario",
                type="pert",
                end_date="2025-01-01",
                content="",
                min=1,
                max=100,
                mode=10,
                outcome=15,
            )
        )
        self.assertAlmostEqual(
            pert.calc(), pert.calc()
        )  # Just want to make sure it runs

    def test_without_max(self) -> None:
        with self.assertRaises(KeyError):
            Pert(
                Post(
                    scenario="A test scenario",
                    type="pert",
                    end_date="2025-01-01",
                    content="",
                    min=1,
                    mode=10,
                    outcome=15,
                )
            )

    def test_without_mode(self) -> None:
        with self.assertRaises(KeyError):
            Pert(
                Post(
                    content="",
                    min=1,
                    max=100,
                    outcome=15,
                )
            )

    def test_calc_without_outcome(self) -> None:
        with self.assertRaises(ValueError):
            test = Pert(
                Post(
                    scenario="A test scenario",
                    type="pert",
                    end_date="2025-01-01",
                    content="",
                    min=1,
                    max=100,
                    mode=10,
                )
            )
            test.calc()

    def test_calc_with_valid_outcome(self) -> None:
        pert = Pert(
            Post(
                scenario="A test scenario",
                type="pert",
                end_date="2025-01-01",
                content="",
                min=1,
                max=100,
                mode=10,
                outcome=10,
            )
        )
        self.assertAlmostEqual(
            pert.calc(), pert.calc()
        )  # Just want to make sure it runs


if __name__ == "__main__":
    unittest.main()
