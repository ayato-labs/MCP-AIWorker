import pytest
from mcp_ai_worker.server import draft_code


@pytest.fixture
def mock_llm(mocker):
    return mocker.patch("mcp_ai_worker.client.SubLLMClient.call_any")


def test_draft_code_syntax_repair(tmp_path, mock_llm):
    test_file = tmp_path / "test.py"
    test_file.write_text("def old():\n    pass\n", encoding="utf-8")

    # 1st call: Returns syntax error
    # 2nd call: Returns valid code
    mock_llm.side_effect = [
        "def new():\n    return True(",  # Invalid Python
        "def new():\n    return True\n",  # Valid Python
    ]

    result = draft_code(path=str(test_file), instruction="Update code", model="gemini")

    assert "Successfully wrote to" in result
    assert "def new():" in test_file.read_text()
    assert mock_llm.call_count == 2
