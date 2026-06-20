import pytest
from unittest.mock import patch, MagicMock, ANY
import sqlite3
from datetime import datetime

# Import the components from the source module
# Assuming the source code is in a file named metrics.py
from metrics import (
    init_db, 
    track_metrics, 
    add_tokens_to_current_tool, 
    record_metrics, 
    current_tool_context
)

@pytest.fixture
def mock_db():
    with patch("sqlite3.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        yield mock_connect, mock_conn, mock_cursor

@pytest.fixture
def mock_logger():
    with patch("metrics.logger") as mock_log:
        yield mock_log

class TestMetricsSystem:

    def test_init_db_creates_table(self, mock_db):
        # Arrange
        mock_connect, mock_conn, mock_cursor = mock_db

        # Act
        init_db()

        # Assert
        mock_cursor.execute.assert_called_once()
        args, _ = mock_cursor.execute.call_args
        assert "CREATE TABLE IF NOT EXISTS token_metrics" in args[0]
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    def test_track_metrics_happy_path(self, mock_db, mock_logger):
        # Arrange
        mock_connect, mock_conn, mock_cursor = mock_db
        
        # Mock time.perf_counter to return 0.0 then 1.5 (execution time = 1.5s)
        with patch("time.perf_counter", side_effect=[0.0, 1.5]):
            
            @track_metrics
            def sample_tool():
                add_tokens_to_current_tool(100, 50)
                return "success"

            # Act
            result = sample_tool()

            # Assert
            assert result == "success"
            # Verify record_metrics was triggered via the DB call
            # The decorator calls record_metrics, which calls sqlite3.connect
            mock_connect.assert_called()
            
            # Check if the INSERT statement was called with correct token values
            # record_metrics is called with: tool_name="sample_tool", input=100, output=50, saved=0, cost=0.0, time=1.5
            mock_cursor.execute.assert_called_once()
            call_args = mock_cursor.execute.call_args[0]
            sql = call_args[0]
            params = call_args[1]
            
            assert "INSERT INTO token_metrics" in sql
            assert params[0] == "sample_tool" # tool_name
            assert params[1] == 100           # input_tokens
            assert params[2] == 50            # output_tokens
            assert params[5] == 1.5           # execution_time

    def test_track_metrics_exception_path(self, mock_db):
        # Arrange
        mock_connect, mock_conn, mock_cursor = mock_db
        
        with patch("time.perf_counter", side_effect=[0.0, 0.5]):
            @track_metrics
            def failing_tool():
                add_tokens_to_current_tool(10, 10)
                raise ValueError("Tool failed")

            # Act & Assert
            with pytest.raises(ValueError, match="Tool failed"):
                failing_tool()

            # Verify that metrics were still recorded despite the exception
            mock_cursor.execute.assert_called_once()
            params = mock_cursor.execute.call_args[0][1]
            assert params[0] == "failing_tool"
            assert params[1] == 10
            assert params[2] == 10

    def test_add_tokens_to_current_tool_without_context(self):
        # Arrange
        # Ensure context is empty
        token = current_tool_context.set(None)
        
        try:
            # Act & Assert
            # This should not raise any exception because of the 'if data is not None' check
            add_tokens_to_current_tool(10, 10)
        finally:
            current_tool_context.reset(token)

    def test_record_metrics_db_insertion(self, mock_db, mock_logger):
        # Arrange
        mock_connect, mock_conn, mock_cursor = mock_db
        tool_name = "test_tool"
        in_t, out_t, saved_t, cost, exec_t = 10, 20, 5, 0.01, 0.123

        # Act
        record_metrics(tool_name, in_t, out_t, saved_t, cost, exec_t)

        # Assert
        mock_cursor.execute.assert_called_once()
        sql, params = mock_cursor.execute.call_args[0]
        
        assert "INSERT INTO token_metrics" in sql
        assert params[0] == tool_name
        assert params[1] == in_t
        assert params[2] == out_t
        assert params[3] == saved_t
        assert params[4] == cost
        assert params[5] == exec_t
        assert isinstance(params[6], datetime)
        
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        mock_logger.info.assert_called_once()

    def test_context_isolation(self, mock_db):
        # Arrange
        mock_connect, mock_conn, mock_cursor = mock_db
        
        @track_metrics
        def tool_a():
            add_tokens_to_current_tool(10, 10)
            
        @track_metrics
        def tool_b():
            add_tokens_to_current_tool(20, 20)

        # Act
        tool_a()
        tool_b()

        # Assert
        # Verify two separate records were created with their respective values
        assert mock_cursor.execute.call_count == 2
        
        # First call params
        args_a = mock_cursor.execute.call_args_list[0][0][1]
        assert args_a[0] == "tool_a"
        assert args_a[1] == 10
        
        # Second call params
        args_b = mock_cursor.execute.call_args_list[1][0][1]
        assert args_b[0] == "tool_b"
        assert args_b[1] == 20