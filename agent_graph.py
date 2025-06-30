from langgraph.graph import StateGraph
from typing import TypedDict, List, Dict, Any
import copy


# -------- State Definition --------
class BusinessState(TypedDict):
    data: Dict[str, Any]
    metrics: Dict[str, Any]
    recommendations: Dict[str, Any]


# -------- Node: Input Node --------
def input_node(state: BusinessState) -> BusinessState:
    # Just forward the input state, nothing changes here
    return state


# -------- Node: Processing Node --------
def processing_node(state: BusinessState) -> BusinessState:
    data = state["data"]

    today = data["today"]
    yesterday = data["yesterday"]

    revenue_today = today["revenue"]
    cost_today = today["cost"]
    customers_today = today["customers"]

    revenue_yesterday = yesterday["revenue"]
    cost_yesterday = yesterday["cost"]
    customers_yesterday = yesterday["customers"]

    profit = revenue_today - cost_today
    profit_margin = (profit / revenue_today) * 100 if revenue_today else 0
    revenue_change_pct = ((revenue_today - revenue_yesterday) / revenue_yesterday) * 100 if revenue_yesterday else 0
    cost_change_pct = ((cost_today - cost_yesterday) / cost_yesterday) * 100 if cost_yesterday else 0

    cac_today = cost_today / max(customers_today, 1)
    cac_yesterday = cost_yesterday / max(customers_yesterday, 1)
    cac_change_pct = ((cac_today - cac_yesterday) / cac_yesterday) * 100 if cac_yesterday else 0

    customer_growth_rate = ((customers_today - customers_yesterday) / customers_yesterday) * 100 if customers_yesterday else 0
    cost_per_customer = cac_today
    revenue_per_customer_today = revenue_today / max(customers_today, 1)
    revenue_per_customer_yesterday = revenue_yesterday / max(customers_yesterday, 1)
    rpc_change = (revenue_per_customer_today - revenue_per_customer_yesterday) / revenue_per_customer_yesterday
    cost_to_revenue_ratio = cost_today / revenue_today if revenue_today else 1

    state["metrics"] = {
        "profit": profit,
        "profit_margin": profit_margin,
        "revenue_change_pct": revenue_change_pct,
        "cost_change_pct": cost_change_pct,
        "cac_today": cac_today,
        "cac_yesterday": cac_yesterday,
        "cac_change_pct": cac_change_pct,
        "customer_growth_rate": customer_growth_rate,
        "cost_per_customer": cost_per_customer,
        "revenue_per_customer_today": revenue_per_customer_today,
        "revenue_per_customer_yesterday": revenue_per_customer_yesterday,
        "rpc_change" : rpc_change,
        "cost_to_revenue_ratio": cost_to_revenue_ratio,
    }

    return state


# -------- Node: Recommendation Node --------
def recommendation_node(state: BusinessState) -> BusinessState:
    m = state["metrics"]
    recommendations = []
    alerts = []

    if m["profit"] < 0:
        recommendations.append("Reduce costs if profit remains negative.")

    if m["cac_change_pct"] > 20:
        alerts.append("CAC increased by more than 20%.")
        recommendations.append("Review marketing campaigns due to increased CAC.")

    if m["revenue_change_pct"] > 10:
        recommendations.append("Consider increasing advertising budget due to growing sales.")

    if m["profit_margin"] < 10:
        recommendations.append("Improve operational efficiency to increase profit margin.")

    if m["cost_per_customer"] > m["cac_yesterday"] * 1.15:
        recommendations.append("Investigate rising customer acquisition or fulfillment costs.")

    if m["customer_growth_rate"] < 0:
        recommendations.append("Customer base is shrinking. Improve retention and sales funnel.")

    if (m["rpc_change"] < -0.10):
        recommendations.append("Revenue per customer is falling. Review pricing or upsell strategies.")

    if m["cost_to_revenue_ratio"] > 0.9:
        alerts.append("Costs are exceeding 90% of revenue.")
        recommendations.append("Urgent: Implement cost-cutting or boost revenue streams.")

    state["recommendations"] = {
        "status": "Profit" if m["profit"] >= 0 else "Loss",
        "alerts": alerts,
        "advice": recommendations,
    }

    return state


# -------- Build the Graph --------
def build_graph():
    builder = StateGraph(BusinessState)

    builder.add_node("InputNode", input_node)
    builder.add_node("ProcessingNode", processing_node)
    builder.add_node("RecommendationNode", recommendation_node)

    builder.set_entry_point("InputNode")
    builder.add_edge("InputNode", "ProcessingNode")
    builder.add_edge("ProcessingNode", "RecommendationNode")
    builder.set_finish_point("RecommendationNode")

    return builder.compile()

graph = build_graph()