# PNDSPY1014

**Message** `pandas.core.series.Series.aggregate` has a partial mapping because there is a not supported scenario in Snowpark pandas.

**Category** Warning

## Description

This issue appears when the SMA identifies a [pandas.core.series.Series.aggregate](https://pandas.pydata.org/docs/reference/api/pandas.Series.aggregate.html) usage.
Snowpark pandas currently has limitations with `Series.aggregate`. Check [Supported Aggregation Functions](https://github.com/snowflakedb/snowpark-python/blob/main/docs/source/modin/supported/agg_supp.rst) for a list of supported functions.

## Scenario

An unsupported use of `pandas.core.series.Series.aggregate`.

### Input

The following example shows an unsupported use of `pandas.core.series.Series.aggregate`.

Copy code

```
import pandas as pd
import numpy as np

s = pd.Series([1, 2, 3, 4])
s.aggregate(['min', 'max'])
```

### Output

The SMA adds the EWI `PNDSPY1014` to the output code to indicate that it has a scenario not supported in Snowpark pandas.

Copy code

```
from snowflake.snowpark.modin import plugin
import modin.pandas as pd
import numpy as np

df = pd.DataFrame([[1, 2, 3],
                       [4, 5, 6],
                       [7, 8, 9],
                       [np.nan, np.nan, np.nan]],
                      columns=['A', 'B', 'C'])
#EWI: PNDSPY1014 => pandas.core.series.Series.aggregate does not support some combinations of parameters for specific aggregate functions. Check Snowpark pandas documentation for more detail.
df.aggregate(['sum', 'min'])
```

## Recommended fix

Since this is an error that applies to a range of partially supported aggregate functions, no specific fix applies to all cases. The appropriate action depends on the particular aggregate function in use.

Even though the element isn’t supported in some scenarios, you might still find a solution or workaround. This issue code only means that the SMA can’t convert the element automatically.
