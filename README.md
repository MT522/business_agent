# 📊 Business Intelligence LangGraph Agent
This project implements a simple AI agent using LangGraph that analyzes basic business data (daily revenue, costs, customers) and generates automated insights and recommendations.

## 🚀 Features
### 🧮 Calculates:

  - Profit/Loss
  - Customer Acquisition Cost (CAC)
  - Revenue per Customer
  - Day-over-day changes (revenue, cost, CAC)

### 📢 Generates actionable recommendations:

  - Reduce costs if profit is negative
  - Alert if CAC increases by more than 20%
  - Suggest marketing adjustments based on trends
  - Identify shrinking customer base or falling revenue per customer
  - Highlight low margins or high cost ratios

🧠 Built using LangGraph for agent-based flow and state management

## 📦 Installation

1. Create and activate virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Usage
Run the agent on sample input:

```python
from agent_graph import graph

sample_input = {
    "data": {
        "today": {"revenue": 2000, "cost": 1200, "customers": 40},
        "yesterday": {"revenue": 1500, "cost": 1100, "customers": 35}
    }
}

result = graph.invoke(sample_input)
print(result["recommendations"])
```

Output Format:
```json
{
  "recommendations": {
    "status": "Profit",
    "alerts": ["CAC increased by more than 20%."],
    "advice": [
      "Review marketing campaigns due to increased CAC.",
      "Consider increasing advertising budget due to growing sales."
    ]
  }
}
```

## ✅ Testing
Run tests to validate various business scenarios:

```bash
python test_agent.py
```

### Test cases include:

  - Profit and growth
  - Loss and rising CAC
  - Shrinking customer base
  - Low margin alerts
  - Falling revenue per customer
  - Stable scenario
