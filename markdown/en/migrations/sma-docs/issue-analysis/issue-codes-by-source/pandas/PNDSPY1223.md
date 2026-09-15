# PNDSPY1223

**Message** Pandas < **pandas.core.strings.accessor.StringMethods.replace** > has a partial mapping with a few scenarios not supported in Snowpark.

**Category** Warning

## Description

This issue appears when the SMA detects the use of a pandas element that has a direct equivalent in Snowpark pandas, but some scenarios might behave differently than pandas.

**Reason:** N if pat is non-string, repl is a non-string, or n is non-numeric or zero.

## Scenario

A method with a few scenarios that aren’t supported in Snowpark.

### Input

The following example shows a method with a few unsupported scenarios in Snowpark.

Copy code

```
import pandas as pd

s = pd.Series(['abc', 'def', 'ghi'])
result = s.str.replace
```

### Output

The SMA adds the EWI `PNDSPY1223` to the output code to let you know that this element has a few scenarios that aren’t supported in Snowpark.

Copy code

```
import snowflake.snowpark.modin.pandas as pd

#EWI: PNDSPY1223 => pandas.core.strings.accessor.StringMethods.replace has a partial mapping, with few scenarios not supported. Check Snowpark pandas documentation for more detail.
s = pd.Series(['abc', 'def', 'ghi'])
result = s.str.replace
```

## Recommended fix

**Behavioral note**: N if pat is non-string, repl is a non-string, or n is non-numeric or zero.

This behavior may differ from native pandas. Recommended actions:

- Test with a representative sample of your data
- Compare results with native pandas if precision is critical
- Use `.to_pandas()` if exact pandas behavior is required

## Additional recommendations

Check the [Snowpark pandas documentation](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/supported/index) to verify which scenarios aren’t supported for that specific element.
