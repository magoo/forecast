import unittest
from models.interval import Interval

from frontmatter import Post


class TestInterval(unittest.TestCase):

    def test_init_with_valid_post(self) -> None:
        interval = Interval(
            Post(
                content="",
                min=1,
                max=10,
                confidence=1,
                outcome=5,
            )
        )

    def test_init_without_interval(self) -> None:
        with self.assertRaises(KeyError):
            Interval(Post(content=""))

    def test_calc_with_correct_outcome(self) -> None:
        interval = Interval(
            Post(
                content="",
                min=1,
                max=10,
                confidence=1,
                outcome=5,
            )
        )
        self.assertAlmostEqual(interval.calc(), 0)

    def test_calc_with_incorrect_outcome(self) -> None:
        interval = Interval(
            Post(
                content="",
                min=1,
                max=10,
                confidence=1,
                outcome=11,
            )
        )
        self.assertAlmostEqual(interval.calc(), 2)


if __name__ == "__main__":
    unittest.main()
