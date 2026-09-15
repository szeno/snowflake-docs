# PNDSPY1144

**Message** Pandas < **pandas.core.indexes.datetimes.DatetimeIndex.day\_name** > has a partial mapping with a few scenarios not supported in Snowpark.

**Category** Warning

## Description

This issue appears when the SMA detects the use of a pandas element that has a direct equivalent in Snowpark pandas, but some scenarios might behave differently than pandas.

**Missing or Unsupported Parameters:** `locale`

## Scenario

A method with a few scenarios that aren’t supported in Snowpark.

### Input

The following example shows a method with a few unsupported scenarios in Snowpark.

Copy code

```
import pandas as pd

idx = pd.DatetimeIndex(['2023-01-01', '2023-02-01', '2023-03-01'])
result = idx.day_name()
```

### Output

The SMA adds the EWI `PNDSPY1144` to the output code to let you know that this element has a few scenarios that aren’t supported in Snowpark.

Copy code

```
import snowflake.snowpark.modin.pandas as pd

#EWI: PNDSPY1144 => pandas.core.indexes.datetimes.DatetimeIndex.day_name has a partial mapping, with few scenarios not supported. Check Snowpark pandas documentation for more detail.
idx = pd.DatetimeIndex(['2023-01-01', '2023-02-01', '2023-03-01'])
result = idx.day_name()
```

## Recommended fix

The parameter `locale` is not supported in Snowpark pandas. If your code uses this parameter, consider one of these approaches:

1. **Remove the parameter**: If the parameter is not essential for your use case, simply remove it from the function call.
2. **Use default behavior**: The function will work with default values for the unsupported parameter.
3. **Post-process with native pandas**: If the parameter is critical, collect the result using `.to_pandas()` and apply the operation with native pandas:
   .. code-block:: python

   # Convert to native pandas for unsupported parameter

   result = df.to\_pandas().day\_name(locale=value)

## Additional recommendations

Check the [Snowpark pandas documentation](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/supported/index) to verify which scenarios aren’t supported for that specific element.
