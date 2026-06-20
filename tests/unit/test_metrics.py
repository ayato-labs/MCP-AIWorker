import pytest
import sqlite3
import os
from mcp_ai_worker.metrics import track_metrics, add_tokens_to_current_tool, DB_PATH

# テスト用DBを一時的に使用
@pytest.fixture(autouse=True)
def setup_db():
    # 元のDBを退避させないよう、テスト用にパスを一時的に変更するか、
    # 既存のDBをそのまま使ってテスト後にクリーンアップする
    yield
    # テスト後に不要なレコードを削除
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        conn.execute("DELETE FROM token_metrics WHERE tool_name = 'test_tool'")
        conn.commit()
        conn.close()

def test_track_metrics():
    @track_metrics
    def test_tool():
        add_tokens_to_current_tool(100, 50)
        return "result"

    result = test_tool()
    
    assert result == "result"
    
    # DBを確認
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT input_tokens, output_tokens FROM token_metrics WHERE tool_name = 'test_tool'")
    row = cursor.fetchone()
    conn.close()
    
    assert row is not None
    assert row[0] == 100
    assert row[1] == 50
