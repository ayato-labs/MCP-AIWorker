import json
import sys
from pathlib import Path

# Placeholder costs per 1M tokens (USD)
# Users can update these based on actual provider pricing
COSTS = {
    "gemini-3.1-flash-lite": {"input": 0.05, "output": 0.10}, 
    "ollama": {"input": 0.0, "output": 0.0},  # Local is free
}

def analyze():
    usage_file = Path("data/token_usage.json")
    if not usage_file.exists():
        print("No usage data found.")
        return

    with open(usage_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    total_input = 0
    total_output = 0
    total_cost = 0.0

    print(f"{'Timestamp':<20} | {'Provider':<10} | {'Model':<25} | {'In':<8} | {'Out':<8} | {'Est. Cost ($)':<12}")
    print("-" * 100)

    for entry in data:
        model = entry["model"]
        input_t = entry["input_tokens"]
        output_t = entry["output_tokens"]
        
        total_input += input_t
        total_output += output_t
        
        cost_info = COSTS.get(model.replace("models/", ""), {"input": 0.0, "output": 0.0})
        cost = (input_t / 1_000_000 * cost_info["input"]) + (output_t / 1_000_000 * cost_info["output"])
        total_cost += cost
        
        print(f"{entry['timestamp'][:19]:<20} | {entry['provider']:<10} | {model:<25} | {input_t:<8} | {output_t:<8} | {cost:<12.6f}")

    print("-" * 100)
    print(f"Total Tokens: In={total_input}, Out={total_output}")
    print(f"Total Estimated Cost: ${total_cost:.6f}")

if __name__ == "__main__":
    analyze()
