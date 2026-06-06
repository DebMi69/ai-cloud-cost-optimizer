import pandas as pd
import streamlit as st
from email_alert import send_alert

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Cloud Cost Optimizer",
    page_icon="☁️",
    layout="wide"
)

st.title("☁️ AI Cloud Cost Optimization Dashboard")

# --------------------------------------------------
# Load Data
# --------------------------------------------------

azure_df = pd.read_csv(
    "data/raw/azure_resources.csv"
)

cost_df = pd.read_csv(
    "data/raw/azure_costs.csv"
)

forecast_df = pd.read_csv(
    "data/processed/predicted_cost.csv"
)

# --------------------------------------------------
# Azure Resource KPIs
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "☁ Azure Resources",
        len(azure_df)
    )

with col2:
    vm_count = len(
        azure_df[
            azure_df["Resource_Type"] ==
            "Microsoft.Compute/virtualMachines"
        ]
    )

    st.metric(
        "🖥 Virtual Machines",
        vm_count
    )

st.divider()

# --------------------------------------------------
# Azure Cost KPIs
# --------------------------------------------------

total_spend = cost_df["Cost"].sum()

avg_daily_cost = cost_df["Cost"].mean()

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "💰 Actual Azure Spend",
        f"₹{total_spend:.2f}"
    )

with col2:
    st.metric(
        "📈 Avg Daily Cost",
        f"₹{avg_daily_cost:.2f}"
    )

st.divider()

# --------------------------------------------------
# Azure Resource Inventory
# --------------------------------------------------

st.subheader("☁ Azure Resource Inventory")

st.dataframe(
    azure_df,
    width="stretch"
)

st.divider()

# --------------------------------------------------
# Azure Monitor Metrics
# --------------------------------------------------

cpu_values = pd.Series(dtype=float)
latest_cpu = None

st.subheader("📈 Real Azure VM CPU Monitoring")

try:

    vm_metrics = pd.read_csv(
        "data/raw/azure_vm_metrics.csv"
    )

    vm_metrics["Timestamp"] = pd.to_datetime(
        vm_metrics["Timestamp"]
    )

    cpu_values = vm_metrics[
        "CPU_Percentage"
    ].dropna()

    col1, col2, col3 = st.columns(3)

    with col1:
        if not cpu_values.empty:
            latest_cpu = cpu_values.iloc[-1]

            st.metric(
                "Current CPU %",
                f"{latest_cpu:.2f}%"
            )

    with col2:
        if not cpu_values.empty:
            st.metric(
                "Maximum CPU %",
                f"{cpu_values.max():.2f}%"
            )

    with col3:
        if not cpu_values.empty:
            st.metric(
                "Average CPU %",
                f"{cpu_values.mean():.2f}%"
            )

    st.success(
        "Live metrics fetched from Azure Monitor"
    )

    st.line_chart(
        vm_metrics.set_index("Timestamp")[
            "CPU_Percentage"
        ]
    )

except Exception:
    st.warning(
        "Azure Monitor metrics not available."
    )

st.divider()

# --------------------------------------------------
# Azure Cost Trend
# --------------------------------------------------

st.subheader("💰 Azure Cost Trend")

cost_df["Date"] = pd.to_datetime(
    cost_df["Date"],
    format="%Y%m%d"
)

st.line_chart(
    cost_df.set_index("Date")["Cost"]
)

latest_cost = cost_df["Cost"].iloc[-1]

avg_cost = cost_df["Cost"].mean()

if latest_cost > avg_cost * 1.5:

    st.error(
        "🚨 Cost spike detected."
    )

else:

    st.success(
        "✅ Cost trend appears normal."
    )

st.divider()

# --------------------------------------------------
# AI Cost Forecast
# --------------------------------------------------

st.subheader("🔮 AI Cost Forecast")

st.line_chart(
    forecast_df.set_index("Day")[
        "Predicted_Cost"
    ]
)

predicted_month_end = (
    forecast_df["Predicted_Cost"]
    .sum()
)

st.metric(
    "Predicted Future Spend",
    f"₹{predicted_month_end:.2f}"
)

st.divider()

# --------------------------------------------------
# Smart Alerts
# --------------------------------------------------

st.subheader("🚨 Smart Alerts")

alerts = []

if latest_cpu is not None:

    if latest_cpu > 80:

        alerts.append(
            f"High CPU Utilization ({latest_cpu:.2f}%)"
        )

        if "cpu_alert_sent" not in st.session_state:

            send_alert(
                "Azure High CPU Alert",
                f"CPU utilization reached {latest_cpu:.2f}%"
            )

            st.session_state.cpu_alert_sent = True

    elif latest_cpu < 10:

        alerts.append(
            f"Underutilized VM ({latest_cpu:.2f}%)"
        )

if latest_cost > avg_cost * 1.5:

    alerts.append(
        "Cost Spike Detected"
    )

    if "cost_alert_sent" not in st.session_state:

        send_alert(
            "Azure Cost Spike Alert",
            f"Azure cost increased to ₹{latest_cost:.2f}"
        )

        st.session_state.cost_alert_sent = True

if len(alerts) == 0:

    st.success(
        "No active alerts"
    )

else:

    for alert in alerts:

        st.error(alert)

st.divider()

# --------------------------------------------------
# AI Optimization Advisor
# --------------------------------------------------

st.subheader("🤖 AI Optimization Advisor")

recommendations = []

if latest_cpu is not None:

    if latest_cpu < 10:

        recommendations.append(
            "VM utilization is extremely low. Consider downsizing or stopping the VM during non-business hours."
        )

    elif latest_cpu > 80:

        recommendations.append(
            "VM is heavily utilized. Consider scaling to a larger VM SKU."
        )

if latest_cost > avg_cost * 1.5:

    recommendations.append(
        "Cost trend indicates abnormal spending. Review recently provisioned Azure resources."
    )

if len(recommendations) == 0:

    st.success(
        "No optimization actions required."
    )

else:

    for rec in recommendations:

        st.info(rec)

st.divider()

# --------------------------------------------------
# Estimated Savings
# --------------------------------------------------

st.subheader("💵 Estimated Savings")

estimated_savings = 0

if latest_cpu is not None:

    if latest_cpu < 10:

        estimated_savings = total_spend * 0.30

st.metric(
    "Potential Monthly Savings",
    f"₹{estimated_savings:.2f}"
)

st.divider()

# --------------------------------------------------
# Environment Summary
# --------------------------------------------------

st.subheader("🩺 Azure Environment Summary")

resource_types = (
    azure_df["Resource_Type"]
    .value_counts()
)

st.bar_chart(resource_types)