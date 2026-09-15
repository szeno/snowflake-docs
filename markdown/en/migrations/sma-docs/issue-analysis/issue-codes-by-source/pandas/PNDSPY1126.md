# PNDSPY1126

**Message** Pandas < **pandas.core.groupby.groupby.GroupBy.apply** > has a partial mapping with a few scenarios not supported in Snowpark.

**Category** Warning

## Description

This issue appears when the SMA detects the use of a pandas element that has a direct equivalent in Snowpark pandas, but some scenarios might behave differently than pandas.

**Missing or Unsupported Parameters:** `axis other than 0 is not implemented.`

**Reason:** Y if the following are true, otherwise N: - func is a callable that always returns either a pandas DataFrame, a pandas Series, or objects that are neither DataFrame nor Series. - grouping on axis=0 - Not applying transform to a dataframe with a non-unique index - Not applying func that returns two dataframes that have different labels for the column at a given position - Not applying func that returns two dataframes that have different names for a given index label - Not applying func that returns two Series that have different labels for the row at a given position - Not applying func that returns two Series that have different names - Not grouping by an “external” by, i.e. an object that is not a label for a column or level of the dataframe.

## Scenario

A method with a few scenarios that aren’t supported in Snowpark.

### Input

The following example shows a method with a few unsupported scenarios in Snowpark.

Copy code

```
import pandas as pd

df = pd.DataFrame({'A': ['foo', 'bar', 'foo', 'bar'], 'B': [1, 2, 3, 4]})
grouped = df.groupby('A')
result = grouped.apply()
```

### Output

The SMA adds the EWI `PNDSPY1126` to the output code to let you know that this element has a few scenarios that aren’t supported in Snowpark.

Copy code

```
import snowflake.snowpark.modin.pandas as pd

#EWI: PNDSPY1126 => pandas.core.groupby.groupby.GroupBy.apply has a partial mapping, with few scenarios not supported. Check Snowpark pandas documentation for more detail.
df = pd.DataFrame({'A': ['foo', 'bar', 'foo', 'bar'], 'B': [1, 2, 3, 4]})
grouped = df.groupby('A')
result = grouped.apply()
```

## Recommended fix

The parameter `axis other than 0 is not implemented.` is not supported in Snowpark pandas. If your code uses this parameter, consider one of these approaches:

1. **Remove the parameter**: If the parameter is not essential for your use case, simply remove it from the function call.
2. **Use default behavior**: The function will work with default values for the unsupported parameter.
3. **Post-process with native pandas**: If the parameter is critical, collect the result using `.to_pandas()` and apply the operation with native pandas:
   .. code-block:: python

   # Convert to native pandas for unsupported parameter

   result = df.to\_pandas().apply(axis other than 0 is not implemented.=value)

**NULL/NaN handling difference**: Y if the following are true, otherwise N: - func is a callable that always returns either a pandas DataFrame, a pandas Series, or objects that are neither DataFrame nor Series. - grouping on axis=0 - Not applying transform to a dataframe with a non-unique index - Not applying func that returns two dataframes that have different labels for the column at a given position - Not applying func that returns two dataframes that have different names for a given index label - Not applying func that returns two Series that have different labels for the row at a given position - Not applying func that returns two Series that have different names - Not grouping by an “external” by, i.e. an object that is not a label for a column or level of the dataframe.

Snowpark pandas may handle NULL/NaN values differently:

- Pre-filter NULL values using `.dropna()` or `.fillna()` before the operation
- Verify NULL handling behavior with a small sample dataset
- Use explicit NULL checks: `df[df['column'].notna()]`

## Additional recommendations

Check the [Snowpark pandas documentation](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/supported/index) to verify which scenarios aren’t supported for that specific element.
