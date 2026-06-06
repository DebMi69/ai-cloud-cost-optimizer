subscription_id = "c1d21b22-45d6-4289-b08a-099b5c7dea3c"
from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
import pandas as pd


credential = AzureCliCredential()

resource_client = ResourceManagementClient(
    credential,
    subscription_id
)

resources = []

for resource in resource_client.resources.list():
    resources.append({
        "Resource_Name": resource.name,
        "Resource_Type": resource.type,
        "Resource_ID": resource.id
    })

df = pd.DataFrame(resources)

df.to_csv(
    "data/raw/azure_resources.csv",
    index=False
)

print(f"{len(resources)} resources exported")