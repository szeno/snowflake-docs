# PNDSPY1106

**Message** Pandas < **pandas.core.frame.DataFrame.to\_csv** > has a partial mapping with a few scenarios not supported in Snowpark.

**Category** Warning

## Applies to

This EWI applies to the following elements (same implementation):

- `pandas.core.frame.DataFrame.to_csv`
- `pandas.core.generic.NDFrame.to_csv`
- `pandas.core.series.Series.to_csv`

## Description

This issue appears when the SMA detects the use of a pandas element that has a direct equivalent in Snowpark pandas, but some scenarios might behave differently than pandas.

**Reason:** Supports writing to both local and snowflake stage. Filepath starting with @ is treated as snowflake stage location. Writing to local file supports all parameters. Writing to snowflake state does not support float\_format, mode, encoding, quoting, quotechar, lineterminator, doublequote and decimal parameters.

## Scenario

A method with a few scenarios that aren’t supported in Snowpark.

### Input

The following example shows a method with a few unsupported scenarios in Snowpark.

Copy code

```
import pandas as pd

df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
result = df.to_csv()
```

### Output

The SMA adds the EWI `PNDSPY1106` to the output code to let you know that this element has a few scenarios that aren’t supported in Snowpark.

Copy code

```
import snowflake.snowpark.modin.pandas as pd

#EWI: PNDSPY1106 => pandas.core.frame.DataFrame.to_csv has a partial mapping, with few scenarios not supported. Check Snowpark pandas documentation for more detail.
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
result = df.to_csv()
```

## Recommended fix

**NULL/NaN handling difference**: Supports writing to both local and snowflake stage. Filepath starting with @ is treated as snowflake stage location. Writing to local file supports all parameters. Writing to snowflake state does not support float\_format, mode, encoding, quoting, quotechar, lineterminator, doublequote and decimal parameters.

Snowpark pandas may handle NULL/NaN values differently:

- Pre-filter NULL values using `.dropna()` or `.fillna()` before the operation
- Verify NULL handling behavior with a small sample dataset
- Use explicit NULL checks: `df[df['column'].notna()]`

## Additional recommendations

Check the [Snowpark pandas documentation](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/supported/index) to verify which scenarios aren’t supported for that specific element.
