import unittest

from models.lognormal import LogNormal

from frontmatter import Post


class TestLogNormal(unittest.TestCase):

    def test_with_valid_post(self) -> None:
        lognormal = LogNormal(
            Post(
                content="",
                max=100,
                mode=10,
                outcome=15,
            )
        )
        self.assertAlmostEqual(lognormal.calc(), 1.895235588329737)

    def test_without_max(self) -> None:
        with self.assertRaises(KeyError):
            LogNormal(
                Post(
                    content="",
                    mode=10,
                    outcome=15,
                )
            )

    def test_without_mode(self) -> None:
        with self.assertRaises(KeyError):
            LogNormal(
                Post(
                    content="",
                    max=10,
                    outcome=15,
                )
            )

    def test_calc_without_outcome(self) -> None:
        with self.assertRaises(KeyError):
            test = LogNormal(
                Post(
                    content="",
                    max=10,
                )
            )
            test.calc()

    def test_calc_with_valid_outcome(self) -> None:
        lognormal = LogNormal(
            Post(
                content="",
                max=100,
                mode=10,
                outcome=15,
            )
        )
        self.assertAlmostEqual(lognormal.calc(), 1.895235588329737)

    def test_calc_without_outcome(self) -> None:
        post_without_outcome = Post(
            content="",
            max=100,
            mode=10,
        )
        lognormal = LogNormal(post_without_outcome)
        with self.assertRaises(ValueError):
            lognormal.calc()


if __name__ == "__main__":
    unittest.main()
