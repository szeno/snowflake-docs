# PNDSPY1026

**Message** Pandas < **pandas.core.arrays.datetimes.DatetimeArray.tz\_localize** > has a partial mapping with a few scenarios not supported in Snowpark.

**Category** Warning

## Description

This issue appears when the SMA detects the use of a pandas element that has a direct equivalent in Snowpark pandas, but some scenarios might behave differently than pandas.

**Reason:** N if ambiguous or nonexistent are set to a non-default value. N if timezone format is not supported. Only timezones listed in pytz.all\_timezones are supported. For example, UTC is supported but UTC+/-<offset>, such as UTC+09:00, is not supported.

## Scenario

A method with a few scenarios that aren’t supported in Snowpark.

### Input

The following example shows a method with a few unsupported scenarios in Snowpark.

Copy code

```
import pandas as pd

s = pd.Series(pd.date_range('2023-01-01', periods=3))
result = s.dt.tz_localize
```

### Output

The SMA adds the EWI `PNDSPY1026` to the output code to let you know that this element has a few scenarios that aren’t supported in Snowpark.

Copy code

```
import snowflake.snowpark.modin.pandas as pd

#EWI: PNDSPY1026 => pandas.core.arrays.datetimes.DatetimeArray.tz_localize has a partial mapping, with few scenarios not supported. Check Snowpark pandas documentation for more detail.
s = pd.Series(pd.date_range('2023-01-01', periods=3))
result = s.dt.tz_localize
```

## Recommended fix

**Timezone handling difference**: N if ambiguous or nonexistent are set to a non-default value. N if timezone format is not supported. Only timezones listed in pytz.all\_timezones are supported. For example, UTC is supported but UTC+/-<offset>, such as UTC+09:00, is not supported.

When working with timezones in Snowpark pandas:

- Ensure your timezone strings are valid IANA timezone names (e.g., ‘UTC’, ‘America/New\_York’)
- Test timezone conversions with sample data before running on full dataset
- Consider using `.to_pandas()` for complex timezone operations if results differ

## Additional recommendations

Check the [Snowpark pandas documentation](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/supported/index) to verify which scenarios aren’t supported for that specific element.
