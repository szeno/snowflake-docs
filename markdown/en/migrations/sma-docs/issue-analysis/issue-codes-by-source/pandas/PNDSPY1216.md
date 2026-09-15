# PNDSPY1216

**Message** Pandas < **pandas.core.strings.accessor.StringMethods.**getitem**** > has a partial mapping with a few scenarios not supported in Snowpark.

**Category** Warning

## Description

This issue appears when the SMA detects the use of a pandas element that has a direct equivalent in Snowpark pandas, but some scenarios might behave differently than pandas.

**Reason:** For the column data type, only string, list, and dict values are supported. All column values must be of the same type.

## Scenario

A method with a few scenarios that aren’t supported in Snowpark.

### Input

The following example shows a method with a few unsupported scenarios in Snowpark.

Copy code

```
import pandas as pd

s = pd.Series(['abc', 'def', 'ghi'])
result = s.str.__getitem__
```

### Output

The SMA adds the EWI `PNDSPY1216` to the output code to let you know that this element has a few scenarios that aren’t supported in Snowpark.

Copy code

```
import snowflake.snowpark.modin.pandas as pd

#EWI: PNDSPY1216 => pandas.core.strings.accessor.StringMethods.__getitem__ has a partial mapping, with few scenarios not supported. Check Snowpark pandas documentation for more detail.
s = pd.Series(['abc', 'def', 'ghi'])
result = s.str.__getitem__
```

## Recommended fix

**Data type consideration**: For the column data type, only string, list, and dict values are supported. All column values must be of the same type.

Ensure data types are compatible:

- Check column dtypes with `df.dtypes` before the operation
- Use `.astype()` to convert columns to expected types
- Numeric operations may require explicit casting: `df['col'].astype(float)`

## Additional recommendations

Check the [Snowpark pandas documentation](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/supported/index) to verify which scenarios aren’t supported for that specific element.
