import unittest

from gencontent import extract_title

# This class contains unit tests for the extract_title function
class TestExtractTitle(unittest.TestCase):
    # Tests the extract_title function with a simple title
    def test_eq(self):
        actual = extract_title("# This is a title")
        self.assertEqual(actual, "This is a title")

    # Tests the extract_title function with a title and some text
    def test_eq_double(self):
        actual = extract_title(
            """
# This is a title

# This is a second title that should be ignored
"""
        )
        self.assertEqual(actual, "This is a title")

    # Tests the extract_title function with a title, text and a list
    def test_eq_long(self):
        actual = extract_title(
            """
# title

this is a bunch

of text

- and
- a
- list
"""
        )
        self.assertEqual(actual, "title")

    # Tests the extract_title function without a title
    def test_none(self):
        try:
            extract_title(
                """
no title
"""
            )
            self.fail("Should have raised an exception")
        except Exception as e:
            pass


if __name__ == "__main__":
    unittest.main()
