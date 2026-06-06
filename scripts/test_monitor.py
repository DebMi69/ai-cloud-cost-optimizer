from azure.identity import AzureCliCredential
from azure.monitor.query import MetricsQueryClient

credential = AzureCliCredential()

client = MetricsQueryClient(credential)

resource_id = "/subscriptions/c1d21b22-45d6-4289-b08a-099b5c7dea3c/resourceGroups/AICloudOmptimizer/providers/Microsoft.Compute/virtualMachines/AICloudVM"

response = client.query_resource(
    resource_uri=resource_id,
    metric_names=["Percentage CPU"]
)

print(response.metrics)