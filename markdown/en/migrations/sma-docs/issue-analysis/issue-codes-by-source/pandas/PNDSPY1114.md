# PNDSPY1114

**Message** Pandas < **pandas.core.frame.DataFrame.where** > has a partial mapping with a few scenarios not supported in Snowpark.

**Category** Warning

## Applies to

This EWI applies to the following elements (same implementation):

- `pandas.core.frame.DataFrame.where`
- `pandas.core.generic.NDFrame.where`
- `pandas.core.series.Series.where`

## Description

This issue appears when the SMA detects the use of a pandas element that has a direct equivalent in Snowpark pandas, but some scenarios might behave differently than pandas.

**Reason:** See mask.

## Scenario

A method with a few scenarios that aren’t supported in Snowpark.

### Input

The following example shows a method with a few unsupported scenarios in Snowpark.

Copy code

```
import pandas as pd

df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
result = df.where()
```

### Output

The SMA adds the EWI `PNDSPY1114` to the output code to let you know that this element has a few scenarios that aren’t supported in Snowpark.

Copy code

```
import snowflake.snowpark.modin.pandas as pd

#EWI: PNDSPY1114 => pandas.core.frame.DataFrame.where has a partial mapping, with few scenarios not supported. Check Snowpark pandas documentation for more detail.
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
result = df.where()
```

## Recommended fix

**Behavioral note**: See mask.

This behavior may differ from native pandas. Recommended actions:

- Test with a representative sample of your data
- Compare results with native pandas if precision is critical
- Use `.to_pandas()` if exact pandas behavior is required

## Additional recommendations

Check the [Snowpark pandas documentation](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/supported/index) to verify which scenarios aren’t supported for that specific element.
