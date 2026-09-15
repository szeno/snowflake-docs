# PNDSPY1005

**Message** `pandas.core.series.Series.str.get` has a partial mapping because in one scenario it has a different behavior in Snowpark.

**Category** Warning

## Description

This issue appears when the SMA identifies a [pandas.core.series.Series.str.get](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.get.html) usage.
Snowpark pandas offers a partial equivalent, but when it comes to columns with mixed data types the method may not behave as expected. All values within a column must be of the same type.

## Scenario

An unsupported use of `pandas.core.series.Series.str.get`.

### Input

The following example shows an unsupported use of `pandas.core.series.Series.str.get`.

Copy code

```
import pandas as pd

s = pd.Series(["String", (1, 2, 3), ["a", "b", "c"], 123, -456, {1: "Hello", "2": "World"}])
print(s.str.get(1))
```

### Output

The SMA adds the EWI `PNDSPY1005` to the output code to indicate that in one scenario it has a different behavior in Snowpark.

Copy code

```
from snowflake.snowpark.modin import plugin
import modin.pandas as pd

s = pd.Series(["String", (1, 2, 3), ["a", "b", "c"], 123, -456, {1: "Hello", "2": "World"}])
#EWI: PNDSPY1005 => pandas.core.series.Series.str.get has a partial mapping, because in one scenario it has a different behavior in Snowpark.
print(s.str.get(1))
```

## Recommended fix

Ensure that the Series contains only one type of data (all strings, all lists, or all dicts).
No code change is strictly required, but be aware that this operation might not work as expected in Snowpark pandas.
