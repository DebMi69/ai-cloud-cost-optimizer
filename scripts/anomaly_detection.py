import pandas as pd

df = pd.read_csv("data/raw/cost_history.csv")

mean_cost = df["Cost"].mean()
std_cost = df["Cost"].std()

threshold = mean_cost + (2 * std_cost)

anomalies = df[df["Cost"] > threshold]

print("=== Cost Anomalies ===")

if anomalies.empty:
    print("No anomalies detected.")
else:
    print(anomalies)