# run_agent.py
from agent_graph import build_graph

graph = build_graph()

# Example input
input_data = {
    "data": {
        "today": {
            "revenue": 1500,
            "cost": 1200,
            "customers": 30
        },
        "yesterday": {
            "revenue": 1200,
            "cost": 900,
            "customers": 35
        }
    }
}

result = graph.invoke(input_data)

print("=== Final Output ===")
from pprint import pprint
pprint(result["recommendations"])
