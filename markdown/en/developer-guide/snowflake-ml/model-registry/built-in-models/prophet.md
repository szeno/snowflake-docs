# Prophet

The Snowflake ML Model Registry supports time series forecasting models created using Prophet (`prophet.Prophet`).

Note

Prophet models can currently only be deployed in the Snowflake warehouse for inference. Model serving in
Snowpark Container Services (SPCS) is not supported for Prophet models at this time.

The following additional options can be used in the `options` dictionary when you call `log_model`:

| Option | Description |
| --- | --- |
| `target_methods` | A list of the names of the methods available on the model object. The default target method is `predict`. |
| `date_column` | The name of the column containing datetime values in your input data. If specified, this column will be automatically mapped to Prophet’s required `ds` column. If not specified, your data must contain a column named `ds`. |
| `target_column` | The name of the column containing target values in your input data. If specified, this column will be automatically mapped to Prophet’s required `y` column. If not specified, your data must contain a column named `y`. |

Expand

Show lessSee more

You must specify either the `sample_input_data` or `signatures` parameter when logging a Prophet model so
that the registry knows the signatures of the target methods.

## Data Format Requirements

Prophet models require input data in a specific format:

- A datetime column (named `ds` by default, or use `date_column` option to map a custom name)
- A target value column (named `y` by default, or use `target_column` option to map a custom name)
- Optional additional regressor columns (if the model was trained with regressors)

For forecasting future periods, provide a DataFrame with future dates in the `ds` column and `NaN` values
in the `y` column.

## Example

In the following examples, `reg` is an instance of `snowflake.ml.registry.Registry`. For information on
creating a registry object, see [Snowflake Model Registry](/developer-guide/snowflake-ml/model-registry/overview).

### Basic Prophet Model

Copy code

```
import prophet
import pandas as pd
import numpy as np

# Create sample time series data
dates = pd.date_range(start="2020-01-01", periods=365, freq="D")
values = np.linspace(100, 200, 365) + 10 * np.sin(2 * np.pi * np.arange(365) / 365.25)

training_data = pd.DataFrame({
    "ds": dates,
    "y": values
})

# Train Prophet model
model = prophet.Prophet(
    daily_seasonality=True,
    weekly_seasonality=True,
    yearly_seasonality=True,
)
model.fit(training_data)

# Create future data for forecasting
last_date = training_data["ds"].max()
future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=30, freq="D")
future_data = pd.DataFrame({
    "ds": future_dates,
    "y": [float("nan")] * 30  # NaN indicates periods to forecast
})

# Log the model
model_ref = reg.log_model(
    model=model,
    model_name="my_prophet_model",
    version_name="v1",
    sample_input_data=training_data[:10],
)

# Make predictions
result_df = model_ref.run(future_data, function_name="predict")
```

### Prophet Model with Custom Column Names

Copy code

```
import prophet
import pandas as pd
import numpy as np

# Create sample time series data with custom column names
dates = pd.date_range(start="2020-01-01", periods=365, freq="D")
values = np.linspace(100, 200, 365) + 10 * np.sin(2 * np.pi * np.arange(365) / 365.25)

training_data = pd.DataFrame({
    "date": dates,        # Custom date column name
    "sales": values       # Custom target column name
})

# Rename columns to Prophet format for training
prophet_training_data = training_data.rename(columns={"date": "ds", "sales": "y"})

# Train Prophet model
model = prophet.Prophet()
model.fit(prophet_training_data)

# Create future data with custom column names
last_date = training_data["date"].max()
future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=30, freq="D")
future_data = pd.DataFrame({
    "date": future_dates,
    "sales": [float("nan")] * 30
})

# Log the model with column mapping options
model_ref = reg.log_model(
    model=model,
    model_name="my_prophet_model_custom_cols",
    version_name="v1",
    sample_input_data=training_data[:10],
    options={
        "date_column": "date",
        "target_column": "sales",
    },
)

# Make predictions using custom column names
result_df = model_ref.run(future_data, function_name="predict")
```

### Prophet Model with Regressors

Copy code

```
import prophet
import pandas as pd
import numpy as np

# Create sample time series data with additional regressors
dates = pd.date_range(start="2020-01-01", periods=365, freq="D")
values = np.linspace(100, 200, 365) + 10 * np.sin(2 * np.pi * np.arange(365) / 365.25)

training_data = pd.DataFrame({
    "ds": dates,
    "y": values,
    "holiday": (dates.dayofweek >= 5).astype(int),  # Weekend indicator
    "temperature": 20 + 5 * np.sin(2 * np.pi * np.arange(365) / 365.25)
})

# Train Prophet model with regressors
model = prophet.Prophet()
model.add_regressor("holiday")
model.add_regressor("temperature")
model.fit(training_data)

# Create future data with regressor values
last_date = training_data["ds"].max()
future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=30, freq="D")
future_data = pd.DataFrame({
    "ds": future_dates,
    "y": [float("nan")] * 30,
    "holiday": (future_dates.dayofweek >= 5).astype(int),
    "temperature": [22.0] * 30  # Predicted future temperatures
})

# Log the model
model_ref = reg.log_model(
    model=model,
    model_name="my_prophet_model_regressors",
    version_name="v1",
    sample_input_data=training_data[:10],
)

# Make predictions
result_df = model_ref.run(future_data, function_name="predict")
```

## Prediction Output

The `predict` method returns a DataFrame with the following columns:

- `ds`: The datetime for each prediction
- `yhat`: The predicted value
- `yhat_lower`: Lower bound of the prediction interval
- `yhat_upper`: Upper bound of the prediction interval
- Additional columns for trend and seasonality components (e.g., `trend`, `weekly`, `yearly`)
