import unittest
from extract_title import extract_title

class TestExtract_Title(unittest.TestCase):
    def test_extract_title_1(self):
        title = extract_title("# Heading")
        self.assertEqual(title, "Heading")

    def test_extract_title_2(self):
        title = extract_title("""
# Heading
""")
        self.assertEqual(title, "Heading")

    def test_extract_title_3(self):
        title = extract_title("""
## Fake Heading

# Heading
""")
        self.assertEqual(title, "Heading")

    def test_extract_title_4(self):
        with self.assertRaises(Exception):
            title = extract_title("""
## Fake Heading

### real Heading
""")
        