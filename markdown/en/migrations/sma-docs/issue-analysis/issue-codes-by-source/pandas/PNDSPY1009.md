# PNDSPY1009

**Message** `pandas.core.frame.DataFrame.apply` has a partial mapping because it has several scenarios not supported in Snowpark pandas.

**Category** Warning

## Description

This issue appears when the SMA identifies a [pandas.core.frame.DataFrame.apply](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.apply.html) usage.
Snowpark pandas offers a partial equivalent, but the current implementation has two unsupported scenarios.

## Scenarios

The following scenarios illustrate the two unsupported use cases.

### Scenario 1

Snowpark pandas `DataFrame.apply` API doesn’t yet support the `result_type` parameter.

#### Input

The following example shows an unsupported use of `pandas.core.frame.DataFrame.apply`.

Copy code

```
import pandas as pd

df = pd.DataFrame({"A": [1, 2], "B": [3, 4], "C": [5, 6]})
df.apply(np.mean, axis=1, result_type="expand")
```

#### Output

The SMA adds the EWI `PNDSPY1009` to the output code to indicate that it has a scenario not supported in Snowpark pandas.

Copy code

```
from snowflake.snowpark.modin import plugin
import modin.pandas as pd

df = pd.DataFrame({"A": [1, 2], "B": [3, 4], "C": [5, 6]})
#EWI: PNDSPY1009 => pandas.core.frame.DataFrame.apply has a partial mapping, because has several scenarios not supported in Snowpark pandas.
df.apply(np.mean, axis=1, result_type="expand")
```

#### Recommended fix

Ensure that the `apply` method doesn’t contain the `result_type` parameter.

### Scenario 2

Snowpark pandas `DataFrame.apply` API doesn’t yet support `DataFrame` or `Series` as `args` or `kwargs` parameters.

#### Input

The following example shows an unsupported use of `pandas.core.frame.DataFrame.apply`.

Copy code

```
import pandas as pd

df = pd.DataFrame({"A": [1, 2], "B": [3, 4], "C": [5, 6]})
ser = pd.Series([10, 20])

def custom_func(row, ser):
    return row["A"] + ser[row.name]

df.apply(custom_func, axis=1, args=(ser, ))
```

#### Output

The SMA adds the EWI `PNDSPY1009` to the output code to indicate that it has a scenario not supported in Snowpark pandas.

Copy code

```
from snowflake.snowpark.modin import plugin
import modin.pandas as pd

df = pd.DataFrame({"A": [1, 2], "B": [3, 4], "C": [5, 6]})
ser = pd.Series([10, 20])

def custom_func(row, ser):
    return row["A"] + ser[row.name]

#EWI: PNDSPY1009 => pandas.core.frame.DataFrame.apply has a partial mapping, because has several scenarios not supported in Snowpark pandas.
df.apply(custom_func, axis=1, args=(ser, ))
```

#### Recommended fix

For this scenario, use the `values` attribute of the Series and create a new column in the DataFrame to hold the Series values, then use the `apply` method without passing the `Series` as an argument.

Copy code

```
import pandas as pd

ser = pd.Series([10, 20])

df = pd.DataFrame({"A": [1, 2], "B":[3, 4], "C": [5, 6]})
df["extra"] = ser.values

def custom_func(row):
    return row["A"] + row["extra"]

df.apply(custom_func, axis=1)
```
