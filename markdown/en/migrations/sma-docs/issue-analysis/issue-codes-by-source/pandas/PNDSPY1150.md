# PNDSPY1150

**Message** Pandas < **pandas.core.indexes.datetimes.DatetimeIndex.tz\_localize** > has a partial mapping with a few scenarios not supported in Snowpark.

**Category** Warning

## Description

This issue appears when the SMA detects the use of a pandas element that has a direct equivalent in Snowpark pandas, but some scenarios might behave differently than pandas.

**Missing or Unsupported Parameters:** `ambiguous`, `nonexistent`

**Reason:** N if timezone format is not supported. Only timezones listed in pytz.all\_timezones are supported. For example, UTC is supported but UTC+/-<offset>, such as, UTC+09:00 is not supported.

## Scenario

A method with a few scenarios that aren’t supported in Snowpark.

### Input

The following example shows a method with a few unsupported scenarios in Snowpark.

Copy code

```
import pandas as pd

idx = pd.DatetimeIndex(['2023-01-01', '2023-02-01', '2023-03-01'])
result = idx.tz_localize()
```

### Output

The SMA adds the EWI `PNDSPY1150` to the output code to let you know that this element has a few scenarios that aren’t supported in Snowpark.

Copy code

```
import snowflake.snowpark.modin.pandas as pd

#EWI: PNDSPY1150 => pandas.core.indexes.datetimes.DatetimeIndex.tz_localize has a partial mapping, with few scenarios not supported. Check Snowpark pandas documentation for more detail.
idx = pd.DatetimeIndex(['2023-01-01', '2023-02-01', '2023-03-01'])
result = idx.tz_localize()
```

## Recommended fix

The following parameters are not supported in Snowpark pandas: `ambiguous`, `nonexistent`.

**Recommended approaches:**

1. **Avoid unsupported parameters**: Modify your code to not use these parameters if they are not essential.
2. **Use `.to_pandas()` for full compatibility**: If you need these parameters, convert to native pandas first:
   .. code-block:: python

   # Convert to native pandas when unsupported parameters are needed

   native\_df = df.to\_pandas()
   result = native\_df.tz\_localize(…) # Use all parameters
3. **Split the operation**: Perform supported operations in Snowpark pandas, then use native pandas only for the unsupported functionality.

**Timezone handling difference**: N if timezone format is not supported. Only timezones listed in pytz.all\_timezones are supported. For example, UTC is supported but UTC+/-<offset>, such as, UTC+09:00 is not supported.

When working with timezones in Snowpark pandas:

- Ensure your timezone strings are valid IANA timezone names (e.g., ‘UTC’, ‘America/New\_York’)
- Test timezone conversions with sample data before running on full dataset
- Consider using `.to_pandas()` for complex timezone operations if results differ

## Additional recommendations

Check the [Snowpark pandas documentation](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/supported/index) to verify which scenarios aren’t supported for that specific element.
