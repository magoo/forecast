import unittest
from models.interval import Interval

from frontmatter import Post


class TestInterval(unittest.TestCase):

    def test_init_with_valid_post(self) -> None:
        interval = Interval(
            Post(
                scenario="A test scenario",
                type="interval",
                end_date="2025-01-01",
                content="",
                min=1,
                max=10,
                confidence=1,
                outcome=5,
            )
        )
        # Verify the object was initialized with correct values
        self.assertEqual(interval.min, 1)
        self.assertEqual(interval.max, 10)
        self.assertEqual(interval.confidence, 1)
        self.assertEqual(interval.outcome, 5)

    def test_init_without_interval(self) -> None:
        with self.assertRaisesRegex(KeyError, "'min'|'max'|'confidence'"):
            Interval(
            Post(
                scenario="A test scenario",
                type="interval",
                end_date="2025-01-01",
                content="",
                outcome=5,
            )
        )

    def test_calc_with_correct_outcome(self) -> None:
        interval = Interval(
            Post(
                scenario="A test scenario",
                type="interval",
                end_date="2025-01-01",
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
                scenario="A test scenario",
                type="interval",
                end_date="2025-01-01",
                content="",
                min=1,
                max=10,
                confidence=1,
                outcome=100,
            )
        )
        self.assertAlmostEqual(interval.calc(), 2)


if __name__ == "__main__":
    unittest.main()
