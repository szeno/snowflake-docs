# PNDSPY1010

**Message** `pandas.core.groupby.grouper.Grouper` has a partial mapping because there is a not supported scenario in Snowpark pandas.

**Category** Warning

## Description

This issue appears when the SMA identifies a [pandas.core.groupby.grouper.Grouper](https://pandas.pydata.org/docs/reference/api/pandas.Grouper.html) usage.
Snowpark pandas currently has limitations with `Grouper` parameters. It doesn’t support `origin`, `offset`, `dropna`, or `closed`.

## Scenario

An unsupported use of `pandas.core.groupby.grouper.Grouper`.

### Input

The following example shows an unsupported use of `pandas.core.groupby.grouper.Grouper`.

Copy code

```
import pandas as pd

df = pd.DataFrame({
        "date": pd.to_datetime([
            "2023-01-01", "2023-01-02", "2023-01-03", None, "2023-01-05", "2023-01-06", None
        ]),
        "value": [0, 1, 2, 3, 4, 5, 6]
    })

df.groupby(pd.Grouper(key="date", freq="3D", origin="epoch" offset="1D", dropna=True)).sum()
```

### Output

The SMA adds the EWI `PNDSPY1010` to the output code to indicate that it has a scenario not supported in Snowpark pandas.

Copy code

```
from snowflake.snowpark.modin import plugin
import modin.pandas as pd

df = pd.DataFrame({
        "date": pd.to_datetime([
            "2023-01-01", "2023-01-02", "2023-01-03", None, "2023-01-05", "2023-01-06", None
        ]),
        "value": [0, 1, 2, 3, 4, 5, 6]
    })

#EWI: PNDSPY1010 => pandas.core.groupby.grouper.Grouper has a partial mapping, because there is a not supported scenario in Snowpark pandas.
df.groupby(pd.Grouper(key="date", freq="3D", origin="epoch" offset="1D", dropna=True)).sum()
```

## Recommended fix

This requires a manual adjustment based on the parameters used in the `Grouper` method, essentially mimicking its behavior:

- Sort and Dropna: These parameters can be replaced with the ones in the [groupby](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/pandas_api/modin.pandas.DataFrame.groupby) method.
- Offset and Origin: You can use `pd.Timedelta` to represent these values and manually adjust the datetime column by subtracting the `offset` or `origin` before using `groupby`.

The `groupby` doesn’t have a frequency parameter, so you can use the `pd.Timedelta` to create a new column that represents the period you want to group by.

To illustrate the recommended fix, here is the output code with the changes applied:

Copy code

```
from snowflake.snowpark.modin import plugin
import modin.pandas as pd

df = pd.DataFrame({
        "date": pd.to_datetime([
            "2023-01-01", "2023-01-02", "2023-01-03", None, "2023-01-05", "2023-01-06", None
        ]),
        "value": [0, 1, 2, 3, 4, 5, 6]
    })

freq = pd.Timedelta("3D")

origin = pd.Timestamp("1970-01-01")

origin += pd.Timedelta("1D")

df["period"] = origin + ((df["date"] - origin) // freq) * freq
result = df.groupby("period", dropna=True)["value"].sum()
```
