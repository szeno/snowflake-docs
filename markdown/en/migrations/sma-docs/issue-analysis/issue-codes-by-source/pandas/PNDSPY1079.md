# PNDSPY1079

**Message** Pandas < **pandas.core.frame.DataFrame.pivot\_table** > has a partial mapping with a few scenarios not supported in Snowpark.

**Category** Warning

## Description

This issue appears when the SMA detects the use of a pandas element that has a direct equivalent in Snowpark pandas, but some scenarios might behave differently than pandas.

**Missing or Unsupported Parameters:** `observed`, `sort`

**Reason:** N if index, columns, or values is not str, list of str, or None; or MultiIndex; or any argfunc is not “count”, “mean”, “min”, “max”, or “sum”. N if index is None, margins is True and aggfunc is “count” or “mean” or a dictionary. N if index is None and aggfunc is a dictionary containing lists of aggfuncs to apply. N if aggfunc is an unsupported aggregation function <agg\_supp.html>\_ for pivot.

## Scenario

A method with a few scenarios that aren’t supported in Snowpark.

### Input

The following example shows a method with a few unsupported scenarios in Snowpark.

Copy code

```
import pandas as pd

df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
result = df.pivot_table()
```

### Output

The SMA adds the EWI `PNDSPY1079` to the output code to let you know that this element has a few scenarios that aren’t supported in Snowpark.

Copy code

```
import snowflake.snowpark.modin.pandas as pd

#EWI: PNDSPY1079 => pandas.core.frame.DataFrame.pivot_table has a partial mapping, with few scenarios not supported. Check Snowpark pandas documentation for more detail.
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
result = df.pivot_table()
```

## Recommended fix

The following parameters are not supported in Snowpark pandas: `observed`, `sort`.

**Recommended approaches:**

1. **Avoid unsupported parameters**: Modify your code to not use these parameters if they are not essential.
2. **Use `.to_pandas()` for full compatibility**: If you need these parameters, convert to native pandas first:
   .. code-block:: python

   # Convert to native pandas when unsupported parameters are needed

   native\_df = df.to\_pandas()
   result = native\_df.pivot\_table(…) # Use all parameters
3. **Split the operation**: Perform supported operations in Snowpark pandas, then use native pandas only for the unsupported functionality.

**NULL/NaN handling difference**: N if index, columns, or values is not str, list of str, or None; or MultiIndex; or any argfunc is not “count”, “mean”, “min”, “max”, or “sum”. N if index is None, margins is True and aggfunc is “count” or “mean” or a dictionary. N if index is None and aggfunc is a dictionary containing lists of aggfuncs to apply. N if aggfunc is an unsupported aggregation function <agg\_supp.html>\_ for pivot.

Snowpark pandas may handle NULL/NaN values differently:

- Pre-filter NULL values using `.dropna()` or `.fillna()` before the operation
- Verify NULL handling behavior with a small sample dataset
- Use explicit NULL checks: `df[df['column'].notna()]`

## Additional recommendations

Check the [Snowpark pandas documentation](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/supported/index) to verify which scenarios aren’t supported for that specific element.
