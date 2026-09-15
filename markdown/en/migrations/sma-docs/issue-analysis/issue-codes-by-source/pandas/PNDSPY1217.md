# PNDSPY1217

**Message** Pandas < **pandas.core.strings.accessor.StringMethods.contains** > has a partial mapping with a few scenarios not supported in Snowpark.

**Category** Warning

## Description

This issue appears when the SMA detects the use of a pandas element that has a direct equivalent in Snowpark pandas, but some scenarios might behave differently than pandas.

**Reason:** N if the na parameter is set to a non-bool value.

## Scenario

A method with a few scenarios that aren’t supported in Snowpark.

### Input

The following example shows a method with a few unsupported scenarios in Snowpark.

Copy code

```
import pandas as pd

s = pd.Series(['abc', 'def', 'ghi'])
result = s.str.contains
```

### Output

The SMA adds the EWI `PNDSPY1217` to the output code to let you know that this element has a few scenarios that aren’t supported in Snowpark.

Copy code

```
import snowflake.snowpark.modin.pandas as pd

#EWI: PNDSPY1217 => pandas.core.strings.accessor.StringMethods.contains has a partial mapping, with few scenarios not supported. Check Snowpark pandas documentation for more detail.
s = pd.Series(['abc', 'def', 'ghi'])
result = s.str.contains
```

## Recommended fix

**NULL/NaN handling difference**: N if the na parameter is set to a non-bool value.

Snowpark pandas may handle NULL/NaN values differently:

- Pre-filter NULL values using `.dropna()` or `.fillna()` before the operation
- Verify NULL handling behavior with a small sample dataset
- Use explicit NULL checks: `df[df['column'].notna()]`

## Additional recommendations

Check the [Snowpark pandas documentation](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/supported/index) to verify which scenarios aren’t supported for that specific element.
