# PNDSPY1004

**Message** Pandas < **element** > has a direct mapping, but it’s restricted to running on a single node. As a result, performance may be impacted, especially with large datasets.

**Category** Warning

## Description

This issue appears when the SMA detects the use of a pandas element that has a direct equivalent in Snowpark pandas, but it’s restricted to running on a single node, so its performance may be impacted.

## Scenario

A method that runs on a single node.

### Input

The following example shows a method that runs on a single node.

Copy code

```
import pandas as pd

ser = pd.Series([1, 2, 3, 3])
ser.plot(kind='hist', title="My plot")
```

### Output

The SMA adds the EWI `PNDSPY1004` to the output code to let you know that this element runs on a single node, and its performance may be impacted.

Copy code

```
import snowflake.snowpark.modin.pandas as pd

ser = pd.Series([1, 2, 3, 3])
#EWI: PNDSPY1004 => pandas.core.series.Series.plot has a direct mapping, but it's restricted to running on a single node. As a result, performance may be impacted,
especially with large datasets.
ser.plot(kind='hist', title="My plot")
```

## Recommended fix

Since this is a generic error code that applies to a range of partially supported functions, no single recommended fix exists.

## Additional recommendations

Check the [Snowpark pandas documentation](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/supported/index) to verify the pandas elements that run on a single node.
