import pytest
from mcp_server import clean_code_output, draft_code

def test_clean_code_output_removes_markdown():
    dirty = "```python\ndef hello():\n    pass\n```"
    clean = clean_code_output(dirty)
    assert clean == "def hello():\n    pass"

def test_clean_code_output_no_markdown():
    clean_input = "def hello():\n    pass"
    assert clean_code_output(clean_input) == clean_input

def test_clean_code_output_unclosed_markdown():
    dirty = "```python\ndef hello():\n    pass"
    clean = clean_code_output(dirty)
    assert clean == "def hello():\n    pass"

@pytest.fixture
def mock_gemini(mocker):
    return mocker.patch("mcp_server.SubLLMClient.call_gemini", return_value="def mock_func():\n    return 42")

@pytest.fixture
def mock_ollama(mocker):
    return mocker.patch("mcp_server.SubLLMClient.call_ollama", return_value="def mock_func():\n    return 42")

def test_draft_code_full_overwrite(tmp_path, mock_gemini):
    test_file = tmp_path / "test.py"
    test_file.write_text("old code\n")
    
    result = draft_code(
        path=str(test_file),
        instruction="rewrite",
        model="gemini"
    )
    
    assert "Successfully wrote to" in result
    assert test_file.read_text() == "def mock_func():\n    return 42\n"
    mock_gemini.assert_called_once()

def test_draft_code_partial_overwrite(tmp_path, mock_gemini):
    test_file = tmp_path / "test.py"
    original_content = "line 1\nline 2\nline 3\nline 4\n"
    test_file.write_text(original_content)
    
    # Let's say Gemini returns two lines to replace lines 2 and 3
    mock_gemini.return_value = "new line 2\nnew line 3"
    
    result = draft_code(
        path=str(test_file),
        instruction="update lines",
        start_line=2,
        end_line=3,
        model="gemini"
    )
    
    assert "Updated lines 2-3" in result
    expected_content = "line 1\nnew line 2\nnew line 3\nline 4\n"
    assert test_file.read_text() == expected_content
    mock_gemini.assert_called_once()

def test_draft_code_new_directory(tmp_path, mock_ollama):
    # Test file inside a directory that doesn't exist yet
    test_file = tmp_path / "new_dir" / "test.py"
    
    result = draft_code(
        path=str(test_file),
        instruction="create",
        model="ollama"
    )
    
    assert "Successfully wrote to" in result
    assert test_file.exists()
    assert test_file.read_text() == "def mock_func():\n    return 42\n"
    mock_ollama.assert_called_once()

def test_draft_code_invalid_lines(tmp_path):
    test_file = tmp_path / "test.py"
    
    result = draft_code(
        path=str(test_file),
        instruction="update",
        start_line=5,
        end_line=2
    )
    
    assert result == "Error: start_line cannot be greater than end_line."

