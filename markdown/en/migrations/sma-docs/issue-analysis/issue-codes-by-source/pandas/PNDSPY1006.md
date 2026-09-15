# PNDSPY1006

**Message** `pandas.core.series.Series.apply` has a partial mapping because Snowpark pandas does not support a non-callable function as parameter.

**Category** Warning

## Description

This issue appears when the SMA identifies a [pandas.core.series.Series.apply](https://pandas.pydata.org/docs/reference/api/pandas.Series.apply.html) usage.
Snowpark pandas offers a partial equivalent, but it doesn’t support non-callable values as a parameter.

## Scenario

An unsupported use of `pandas.core.series.Series.apply`.

### Input

The following example shows an unsupported use of `pandas.core.series.Series.apply`.

Copy code

```
import pandas as pd

ser = pd.Series([20, 21, 12], index=['London', 'New York', 'Helsinki'])
print(ser.apply(5))
```

### Output

The SMA adds the EWI `PNDSPY1006` to the output code to indicate that it has a scenario not supported in Snowpark pandas.

Copy code

```
from snowflake.snowpark.modin import plugin
import modin.pandas as pd

ser = pd.Series([20, 21, 12], index=['London', 'New York', 'Helsinki'])
#EWI: PNDSPY1006 => pandas.core.series.Series.apply has a partial mapping, because Snowpark pandas does not support callable functions as parameter.
print(ser.apply(5))
```

## Recommended fix

Ensure that the function used within the apply method is callable.

Copy code

```
import pandas as pd

def my_function(x):
    return x * 5

ser = pd.Series([20, 21, 12], index=['London', 'New York', 'Helsinki'])
print(ser.apply(my_function))
```
