# PNDSPY1013

**Message** `pandas.core.frame.DataFrame.aggregate` has a partial mapping because there is a not supported scenario in Snowpark pandas.

**Category** Warning

## Description

This issue appears when the SMA identifies a [pandas.core.frame.DataFrame.aggregate](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.aggregate.html) usage.
Snowpark pandas currently has limitations with `DataFrame.aggregate`. Check [Supported Aggregation Functions](https://github.com/snowflakedb/snowpark-python/blob/main/docs/source/modin/supported/agg_supp.rst) for a list of supported functions.

## Scenario

An unsupported use of `pandas.core.frame.DataFrame.aggregate`.

### Input

The following example shows an unsupported use of `pandas.core.frame.DataFrame.aggregate`.

Copy code

```
import pandas as pd
import numpy as np

df = pd.DataFrame([[1, 2, 3],
                       [4, 5, 6],
                       [7, 8, 9],
                       [np.nan, np.nan, np.nan]],
                      columns=['A', 'B', 'C'])
df.aggregate(['sum', 'min'])
```

### Output

The SMA adds the EWI `PNDSPY1013` to the output code to indicate that it has a scenario not supported in Snowpark pandas.

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
#EWI: PNDSPY1013 => pandas.core.frame.DataFrame.aggregate does not support some combinations of parameters for specific aggregate functions. Check Snowpark pandas documentation for more detail.
df.aggregate(['sum', 'min'])
```

## Recommended fix

Since this is an error that applies to a range of partially supported aggregate functions, no specific fix applies to all cases. The appropriate action depends on the particular aggregate function in use.

Even though the element isn’t supported in some scenarios, you might still find a solution or workaround. This issue code only means that the SMA can’t convert the element automatically.
