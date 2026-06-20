import sqlite3
import time
import os
from datetime import datetime
from typing import Callable, Any, Optional
from functools import wraps
from contextvars import ContextVar
from mcp_ai_worker.logger import logger

DB_PATH = os.path.join(os.path.dirname(__file__), "metrics.db")

# ツール実行中のトークン情報を保持するコンテキスト変数
current_tool_context: ContextVar[Optional[dict]] = ContextVar("current_tool_context", default=None)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS token_metrics(
            id INTEGER PRIMARY KEY,
            tool_name TEXT,
            input_tokens INTEGER,
            output_tokens INTEGER,
            saved_tokens INTEGER,
            estimated_cost REAL,
            execution_time REAL,
            created_at DATETIME
        )
    """)
    conn.commit()
    conn.close()

def track_metrics(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        # コンテキストを初期化
        token_data = {"input": 0, "output": 0}
        token = current_tool_context.set(token_data)
        
        start_time = time.perf_counter()
        
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            execution_time = time.perf_counter() - start_time
            # コンテキストから集計結果を取得
            data = current_tool_context.get()
            
            record_metrics(
                tool_name=func.__name__,
                input_tokens=data["input"],
                output_tokens=data["output"],
                saved_tokens=0, # TODO: 実装
                estimated_cost=0.0, # TODO: 実装
                execution_time=execution_time
            )
            current_tool_context.reset(token)
            
    return wrapper

def add_tokens_to_current_tool(input_tokens: int, output_tokens: int):
    data = current_tool_context.get()
    if data is not None:
        data["input"] += input_tokens
        data["output"] += output_tokens

def record_metrics(tool_name, input_tokens, output_tokens, saved_tokens, estimated_cost, execution_time):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO token_metrics 
        (tool_name, input_tokens, output_tokens, saved_tokens, estimated_cost, execution_time, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (tool_name, input_tokens, output_tokens, saved_tokens, estimated_cost, execution_time, datetime.now()))
    conn.commit()
    conn.close()
    logger.info(f"Metrics recorded for {tool_name}: {input_tokens}in/{output_tokens}out")

init_db()
