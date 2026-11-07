import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import captions_to_transcript as c  # noqa: E402


class ConvertTests(unittest.TestCase):
    def test_convert(self):
        data = {"events": [
            {"tStartMs": 0, "dDurationMs": 1},                       # no segs: skipped
            {"tStartMs": 240, "segs": [{"utf8": "Hi,"}, {"utf8": " my"}, {"utf8": " name"}]},
            {"tStartMs": 61999, "segs": [{"utf8": "a\nb "}]},
            {"tStartMs": 70000, "segs": [{"utf8": "\n"}]},            # empty: skipped
            {"tStartMs": 3725000, "segs": [{"utf8": "late"}]},
        ]}
        self.assertEqual(c.convert(data), [
            "[00:00] Hi, my name", "[01:01] a b", "[62:05] late"])


if __name__ == "__main__":
    unittest.main()
