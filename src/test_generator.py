import unittest
from generator import extract_title


class TestExtractTitle(unittest.TestCase):
    def runTest(self):
        self.assertEqual(
            extract_title("# Hi"),
            "Hi"
        )

        with self.assertRaises(Exception):
            extract_title("###My beautiful text.\nOh right\n## The header :))")
        


if __name__ == "__main__":
    unittest.main()