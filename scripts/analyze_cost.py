import pandas as pd

df = pd.read_csv("data/raw/azure_metrics.csv")

recommendations = []

for _, row in df.iterrows():

    vm_name = row["VM_Name"]
    cpu = row["CPU_Usage"]
    memory = row["Memory_Usage"]
    cost = row["Monthly_Cost"]

    if cpu < 10 and memory < 30:
        recommendation = "Stop or Downsize VM"

    elif cpu < 20:
        recommendation = "Review VM Size"

    elif cpu > 80 and memory > 80:
        recommendation = "Scale Up VM"

    else:
        recommendation = "Healthy Resource"

    recommendations.append(
        {
            "VM_Name": vm_name,
            "CPU_Usage": cpu,
            "Memory_Usage": memory,
            "Monthly_Cost": cost,
            "Recommendation": recommendation
        }
    )

output_df = pd.DataFrame(recommendations)

output_df.to_csv(
    "data/processed/recommendations.csv",
    index=False
)

print("Recommendations saved successfully!")