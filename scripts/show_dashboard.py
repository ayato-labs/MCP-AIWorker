import sqlite3
import os
from tabulate import tabulate

DB_PATH = os.path.join(os.path.dirname(__file__), "metrics.db")

def show_dashboard():
    if not os.path.exists(DB_PATH):
        print("No metrics data found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            SUM(input_tokens) as total_input,
            SUM(output_tokens) as total_output,
            COUNT(*) as total_commands
        FROM token_metrics
    """)
    row = cursor.fetchone()
    
    total_input = row[0] or 0
    total_output = row[1] or 0
    total_commands = row[2] or 0
    
    # 仮のコスト計算 (Gemini Flash: input $0.075/1M, output $0.30/1M と仮定)
    estimated_cost = (total_input / 1_000_000 * 0.075) + (total_output / 1_000_000 * 0.30)
    
    print("=== MCP-AIWorker Token Observatory ===")
    print(f"Total Commands Executed: {total_commands}")
    print(f"Total Input Tokens: {total_input:,}")
    print(f"Total Output Tokens: {total_output:,}")
    print(f"Estimated Cost: ${estimated_cost:.4f}")
    print("=======================================")
    
    conn.close()

if __name__ == "__main__":
    show_dashboard()
