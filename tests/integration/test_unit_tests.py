import pytest
from unittest.mock import patch
from mcp_ai_worker.server import generate_unit_tests


@pytest.fixture
def mock_llm(mocker):
    return mocker.patch("mcp_ai_worker.client.SubLLMClient.call_any")


def test_generate_unit_tests_success(tmp_path, mock_llm):
    # Setup
    source_dir = tmp_path / "src"
    source_dir.mkdir()
    source_file = source_dir / "calculator.py"
    source_file.write_text("def add(a, b): return a + b", encoding="utf-8")

    test_output_dir = tmp_path / "tests"
    test_output_dir.mkdir()

    # Mock LLM response
    mock_plan = "<test_plan>\n- test_add_happy_path\n</test_plan>"
    mock_code = (
        "<draft_output>\nimport pytest\nfrom calculator import add\n\n"
        "def test_add_happy_path():\n    assert add(1, 2) == 3\n</draft_output>"
    )
    mock_llm.return_value = f"{mock_plan}\n{mock_code}"

    # Mock translation if needed (though additional_instruction uses translate_to_english,
    # and if it returns input as is, it's fine).
    # For safety let's patch translate_to_english in mcp_ai_worker.server
    with patch("mcp_ai_worker.server.translate_to_english", side_effect=lambda x: x):
        # Run
        result = generate_unit_tests(
            source_file_path=str(source_file),
            output_dir_path=str(test_output_dir),
            additional_instruction="Focus on addition logic.",
        )

    # Verify
    assert "✅ Successfully generated unit tests" in result
    assert "test_add_happy_path" in result

    test_file = test_output_dir / "test_calculator.py"
    assert test_file.exists()
    assert "def test_add_happy_path():" in test_file.read_text()

    mock_llm.assert_called_once()
