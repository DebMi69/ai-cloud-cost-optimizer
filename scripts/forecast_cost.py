import pandas as pd
from sklearn.linear_model import LinearRegression

# Load Azure Cost Data

df = pd.read_csv(
    "data/raw/azure_costs.csv"
)

# Create day sequence

df["Day"] = range(
    1,
    len(df) + 1
)

X = df[["Day"]]
y = df["Cost"]

# Train Model

model = LinearRegression()

model.fit(X, y)

# Predict next 30 days

future_days = pd.DataFrame({
    "Day": range(
        len(df) + 1,
        len(df) + 31
    )
})

predictions = model.predict(
    future_days
)

forecast_df = pd.DataFrame({
    "Day": future_days["Day"],
    "Predicted_Cost": predictions
})

forecast_df.to_csv(
    "data/processed/predicted_cost.csv",
    index=False
)

print("Forecast generated successfully!")