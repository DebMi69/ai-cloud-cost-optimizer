from azure.identity import AzureCliCredential
import requests
import pandas as pd
import time

# --------------------------------------------------
# Azure Subscription ID
# --------------------------------------------------

subscription_id = "c1d21b22-45d6-4289-b08a-099b5c7dea3c"

# --------------------------------------------------
# Azure Authentication
# --------------------------------------------------

credential = AzureCliCredential()

token = credential.get_token(
    "https://management.azure.com/.default"
).token

# --------------------------------------------------
# Cost Management API Endpoint
# --------------------------------------------------

url = (
    f"https://management.azure.com/subscriptions/"
    f"{subscription_id}"
    "/providers/Microsoft.CostManagement/query"
    "?api-version=2023-03-01"
)

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# --------------------------------------------------
# Request Body
# --------------------------------------------------

body = {
    "type": "ActualCost",
    "timeframe": "MonthToDate",
    "dataset": {
        "granularity": "Daily",
        "aggregation": {
            "Cost": {
                "name": "Cost",
                "function": "Sum"
            }
        }
    }
}

# --------------------------------------------------
# API Call
# --------------------------------------------------

response = requests.post(
    url,
    headers=headers,
    json=body
)

# Retry once if Azure throttles
if response.status_code == 429:

    print("Rate limited. Waiting 30 seconds...")

    time.sleep(30)

    response = requests.post(
        url,
        headers=headers,
        json=body
    )

# --------------------------------------------------
# Handle Response
# --------------------------------------------------

print("Status Code:", response.status_code)

if response.status_code != 200:

    print(response.text)
    exit()

# --------------------------------------------------
# Parse JSON
# --------------------------------------------------

data = response.json()

rows = data["properties"]["rows"]

cost_records = []

for row in rows:

    cost_records.append({
        "Cost": row[0],
        "Date": str(row[1]),
        "Currency": row[2]
    })

# --------------------------------------------------
# Save CSV
# --------------------------------------------------

cost_df = pd.DataFrame(cost_records)

cost_df.to_csv(
    "data/raw/azure_costs.csv",
    index=False
)

print("\nAzure costs exported successfully!\n")

print(cost_df.head())