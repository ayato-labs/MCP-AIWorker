import unittest


# Dummy implementation of merge logic for testing
def simulate_merge(full_content_lines, generated_code, start_line, end_line):
    s_idx = max(0, start_line - 1)
    e_idx = min(len(full_content_lines), end_line)

    new_lines = generated_code.splitlines(keepends=True)
    if generated_code and not generated_code.endswith("\n"):
        new_lines[-1] += "\n"

    return full_content_lines[:s_idx] + new_lines + full_content_lines[e_idx:]


class TestMergeLogic(unittest.TestCase):
    def test_middle_replacement(self):
        original = ["line1\n", "line2\n", "line3\n", "line4\n"]
        new_snippet = "new_line2\nnew_line3"
        # Replace lines 2 to 3
        result = simulate_merge(original, new_snippet, 2, 3)
        expected = ["line1\n", "new_line2\n", "new_line3\n", "line4\n"]
        self.assertEqual(result, expected)

    def test_start_replacement(self):
        original = ["line1\n", "line2\n"]
        new_snippet = "top"
        result = simulate_merge(original, new_snippet, 1, 1)
        expected = ["top\n", "line2\n"]
        self.assertEqual(result, expected)

    def test_end_replacement(self):
        original = ["line1\n", "line2\n"]
        new_snippet = "bottom"
        result = simulate_merge(original, new_snippet, 2, 2)
        expected = ["line1\n", "bottom\n"]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
