from agent_graph import build_graph

def run_test_case(name, input_data, expected_status=None, expected_alerts=None, expected_advice=None):
    print(f"\n=== Test Case: {name} ===")
    graph = build_graph()
    result = graph.invoke(input_data)
    recommendations = result["recommendations"]

    print("Status:", recommendations["status"])
    print("Alerts:", recommendations["alerts"])
    print("Advice:", recommendations["advice"])

    if expected_status:
        assert recommendations["status"] == expected_status, f"Expected status {expected_status}, got {recommendations['status']}"

    if expected_alerts:
        for alert in expected_alerts:
            assert alert in recommendations["alerts"], f"Expected alert missing: {alert}"

    if expected_advice:
        for advice in expected_advice:
            assert advice in recommendations["advice"], f"Expected advice missing: {advice}"

    print("✅ Passed")


# === TEST CASES ===

# 1. Profit scenario with growing revenue
run_test_case(
    "Growing Sales with Profit",
    input_data={
        "data": {
            "today": {"revenue": 2000, "cost": 1200, "customers": 40},
            "yesterday": {"revenue": 1500, "cost": 1100, "customers": 35}
        }
    },
    expected_status="Profit",
    expected_advice=[
        "Consider increasing advertising budget due to growing sales."
    ]
)

# 2. Loss scenario with negative profit and high cost
run_test_case(
    "Loss and High Cost",
    input_data={
        "data": {
            "today": {"revenue": 1000, "cost": 1200, "customers": 20},
            "yesterday": {"revenue": 1100, "cost": 900, "customers": 25}
        }
    },
    expected_status="Loss",
    expected_alerts=["CAC increased by more than 20%."],
    expected_advice=[
        "Reduce costs if profit remains negative.",
        "Review marketing campaigns due to increased CAC."
    ]
)

# 3. Low profit margin despite profit
run_test_case(
    "Low Profit Margin",
    input_data={
        "data": {
            "today": {"revenue": 1000, "cost": 920, "customers": 25},
            "yesterday": {"revenue": 1000, "cost": 800, "customers": 25}
        }
    },
    expected_status="Profit",
    expected_advice=["Improve operational efficiency to increase profit margin."]
)

# 4. Shrinking customer base
run_test_case(
    "Customer Drop",
    input_data={
        "data": {
            "today": {"revenue": 1100, "cost": 800, "customers": 20},
            "yesterday": {"revenue": 1000, "cost": 850, "customers": 25}
        }
    },
    expected_advice=[
        "Customer base is shrinking. Improve retention and sales funnel."
    ]
)

# 5. High cost-to-revenue ratio
run_test_case(
    "Cost > 90% of Revenue",
    input_data={
        "data": {
            "today": {"revenue": 1000, "cost": 950, "customers": 30},
            "yesterday": {"revenue": 1050, "cost": 800, "customers": 28}
        }
    },
    expected_alerts=["Costs are exceeding 90% of revenue."],
    expected_advice=[
        "Urgent: Implement cost-cutting or boost revenue streams."
    ]
)

# 6. Falling revenue per customer
run_test_case(
    "Revenue per Customer Decreasing",
    input_data={
        "data": {
            "today": {"revenue": 1000, "cost": 700, "customers": 50},
            "yesterday": {"revenue": 1000, "cost": 700, "customers": 30}
        }
    },
    expected_advice=[
        "Revenue per customer is falling. Review pricing or upsell strategies."
    ]
)

# 7. Stable performance (no major recommendations)
run_test_case(
    "Stable Scenario",
    input_data={
        "data": {
            "today": {"revenue": 1500, "cost": 1000, "customers": 30},
            "yesterday": {"revenue": 1480, "cost": 980, "customers": 29}
        }
    },
    expected_status="Profit"
)
