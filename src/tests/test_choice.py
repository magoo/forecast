import unittest
from forecast.models.choice import Choice
from frontmatter import Post # type:ignore


class TestChoice(unittest.TestCase):

    def setUp(self) -> None:
        self.post_with_outcome = Post(
            scenario="A test scenario",
            type="choice",
            end_date="2025-01-01",
            content="",
            options={"option1": 0.7, "option2": 0.3},
            outcome="option1",
        )
        self.post_without_outcome = Post(
            scenario="A test scenario",
            type="choice",
            end_date="2025-01-01",
            content="",
            options={"option1": 0.7, "option2": 0.3},
        )
        self.post_with_invalid_outcome = Post(
            scenario="A test scenario",
            type="choice",
            end_date="2025-01-01",
            content="",
            options={"option1": 0.7, "option2": 0.3},
            outcome="option3",
        )
        self.post_without_options = Post(content="")

    def test_init_with_valid_post(self) -> None:
        choice = Choice(self.post_with_outcome)
        self.assertEqual(choice.options, {"option1": 0.7, "option2": 0.3})
        self.assertEqual(choice.outcome, "option1")

    def test_init_without_options(self) -> None:
        with self.assertRaises(KeyError):
            Choice(self.post_without_options)

    def test_calc_with_valid_outcome(self) -> None:
        choice = Choice(self.post_with_outcome)
        self.assertAlmostEqual(choice.calc(), 0.18)

    def test_calc_without_outcome(self) -> None:
        choice = Choice(self.post_without_outcome)
        with self.assertRaises(ValueError):
            choice.calc()

    def test_calc_with_invalid_outcome(self) -> None:

        choice = Choice(self.post_with_invalid_outcome)
        with self.assertRaises(ValueError):
            choice.calc()


if __name__ == "__main__":
    unittest.main()
