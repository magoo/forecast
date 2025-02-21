import unittest
from models.pert import Pert
from frontmatter import Post


class TestPert(unittest.TestCase):

    def test_with_valid_post(self) -> None:
        pert = Pert(
            Post(
                content="",
                min=1,
                max=100,
                mode=10,
                outcome=15,
            )
        )
        self.assertAlmostEqual(pert.calc(), 1.8924186556059972)

    def test_without_max(self) -> None:
        with self.assertRaises(KeyError):
            Pert(
                Post(
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
                content="",
                min=1,
                max=100,
                mode=10,
                outcome=10,
            )
        )
        self.assertAlmostEqual(pert.calc(), 1.8872963768214517)


if __name__ == "__main__":
    unittest.main()
