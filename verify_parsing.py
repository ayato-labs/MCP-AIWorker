import re
from loguru import logger
import sys

# Mocking the logger to capture warnings for the test
class MockLogger:
    def __init__(self):
        self.warnings = []
    def warning(self, msg):
        self.warnings.append(msg)

logger = MockLogger()

def clean_code_output(text: str) -> str:
    """
    A robust code parsing function.
    It performs multi-stage extraction of XML tags, removal of Markdown, and cleansing of noise (explanatory text).
    """
    if not text:
        return ""

    cleaned = text.strip()

    # 1. Extraction by XML tag (<draft_output>)
    xml_pattern = re.compile(r"<draft_output>\s*\n?(.*?)\n?\s*</draft_output>", re.DOTALL | re.IGNORECASE)
    match = xml_pattern.search(cleaned)
    if match:
        cleaned = match.group(1).strip()
    else:
        # Fallback: Recovery when tags are not closed due to token restrictions, etc.
        partial_xml_pattern = re.compile(r"<draft_output>\s*\n?(.*)", re.DOTALL | re.IGNORECASE)
        partial_match = partial_xml_pattern.search(cleaned)
        if partial_match:
            logger.warning("Unclosed <draft_output> tag detected. Rescuing partial content.")
            cleaned = partial_match.group(1).strip()

    # 2. Removing Markdown Code Blocks
    md_pattern = re.compile(r"```(?:\w+)?\n?(.*?)\n?```", re.DOTALL)
    md_match = md_pattern.search(cleaned)
    if md_match:
        cleaned = md_match.group(1).strip()
    else:
        # Fallback: simple stripping if not properly wrapped
        cleaned = cleaned.replace("```python", "").replace("```", "").strip()

    # 3. Final noise cleansing (only if the result is short and contains common phrases)
    noise_phrases = ["Here is the updated code", "I have modified", "The following code"]
    for phrase in noise_phrases:
        if phrase in cleaned and len(cleaned.splitlines()) < 5:
            cleaned = cleaned.replace(phrase, "")

    return cleaned.strip()

# Test cases
test_cases = [
    {
        "name": "Perfect XML",
        "input": "Here is the result:\n<draft_output>\ndef hello():\n    print('world')\n</draft_output>\nHope this helps!",
        "expected": "def hello():\n    print('world')"
    },
    {
        "name": "Partial XML (Truncated)",
        "input": "Some text\n<draft_output>\ndef hello():\n    print('world'",
        "expected": "def hello():\n    print('world'"
    },
    {
        "name": "Markdown Only",
        "input": "Sure, here is the code:\n```python\ndef hello():\n    print('world')\n```",
        "expected": "def hello():\n    print('world')"
    },
    {
        "name": "Mixed XML and Markdown",
        "input": "<draft_output>\n```python\ndef hello():\n    print('world')\n```\n</draft_output>",
        "expected": "def hello():\n    print('world')"
    },
    {
        "name": "Noise phrase alone",
        "input": "Here is the updated code\ndef hello():\n    print('world')",
        "expected": "def hello():\n    print('world')"
    },
    {
        "name": "Empty input",
        "input": "",
        "expected": ""
    }
]

for tc in test_cases:
    result = clean_code_output(tc["input"])
    if result == tc["expected"]:
        print(f"✅ {tc['name']} passed")
    else:
        print(f"❌ {tc['name']} failed")
        print(f"   Input: {tc['input']!r}")
        print(f"   Expected: {tc['expected']!r}")
        print(f"   Result: {result!r}")

if "Unclosed <draft_output> tag detected. Rescuing partial content." in logger.warnings:
    print("✅ Partial XML warning verified")
else:
    print("❌ Partial XML warning NOT verified")
