# PNDSPY1016

**Message** `pandas.core.series.Series.interpolate` has a partial mapping because there is a not supported scenario in Snowpark pandas.

**Category** Warning

## Description

This issue appears when the SMA identifies a [pandas.core.series.Series.interpolate](https://pandas.pydata.org/docs/reference/api/pandas.Series.interpolate.html) usage.
Snowpark pandas currently has limitations with `Series.interpolate`. It isn’t supported if axis == 1, limit is set, limit\_area is “outside”, or method isn’t “linear”, “bfill”, “backfill”, “ffill”, or “pad”. Also, limit\_area=”inside” is supported only when method is linear.

## Scenario

An unsupported use of `pandas.core.series.Series.interpolate`.

### Input

The following example shows an unsupported use of `pandas.core.series.Series.interpolate`.

Copy code

```
import pandas as pd
import numpy as np

s = pd.Series([0, 2, np.nan, 8])
s.interpolate(method='polynomial', order=2)
```

### Output

The SMA adds the EWI `PNDSPY1016` to the output code to indicate that it has a scenario not supported in Snowpark pandas.

Copy code

```
from snowflake.snowpark.modin import plugin
import modin.pandas as pd
import numpy as np

df = pd.DataFrame([(0.0, np.nan, -1.0, 1.0),
                   (np.nan, 2.0, np.nan, np.nan),
                   (2.0, 3.0, np.nan, 9.0),
                   (np.nan, 4.0, -4.0, 16.0)],
                  columns=list('abcd'))
#EWI: PNDSPY1016 => pandas.core.series.Series.interpolate is not support if axis == 1, limit is set, limit_area is "outside", or method is not "linear", "bfill", "backfill", "ffill", or "pad". And limit_area="inside" is supported only when method is linear. Check Snowpark pandas documentation for more detail.
df['d'].interpolate(method='polynomial', order=2)
```

## Recommended fix

Since this is an error that applies to a range of partially supported parameters, no specific fix applies to all cases. The appropriate action depends on the particular parameter combination in use.

Even though the element isn’t supported in some scenarios, you might still find a solution or workaround. This issue code only means that the SMA can’t convert the element automatically.
