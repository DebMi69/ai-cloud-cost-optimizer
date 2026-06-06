from azure.identity import AzureCliCredential
import requests

credential = AzureCliCredential()

resource_id = "/subscriptions/c1d21b22-45d6-4289-b08a-099b5c7dea3c/resourceGroups/AICloudOmptimizer/providers/Microsoft.Compute/virtualMachines/AICloudVM"

token = credential.get_token(
    "https://management.azure.com/.default"
).token

url = (
    f"https://management.azure.com{resource_id}"
    "/providers/microsoft.insights/metrics"
    "?metricnames=Percentage CPU"
    "&timespan=PT1H"
    "&interval=PT5M"
    "&api-version=2023-10-01"
)

headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get(url, headers=headers)

print(response.status_code)
data = response.json()
import pandas as pd

rows = []

for metric in data["value"]:

    for series in metric["timeseries"]:

        for point in series["data"]:

            rows.append({
                "Timestamp": point.get("timeStamp"),
                "CPU_Percentage": point.get("average")
            })

df = pd.DataFrame(rows)

df.to_csv(
    "data/raw/azure_vm_metrics.csv",
    index=False
)

print("Metrics exported successfully")