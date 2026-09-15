# PNDSPY1066

**Message** Pandas < **pandas.core.frame.DataFrame.mask** > has a partial mapping with a few scenarios not supported in Snowpark.

**Category** Warning

## Applies to

This EWI applies to the following elements (same implementation):

- `pandas.core.frame.DataFrame.mask`
- `pandas.core.generic.NDFrame.mask`
- `pandas.core.series.Series.mask`

## Description

This issue appears when the SMA detects the use of a pandas element that has a direct equivalent in Snowpark pandas, but some scenarios might behave differently than pandas.

**Reason:** N if given axis when other is a DataFrame or level parameters; N if cond or other is Callable.

## Scenario

A method with a few scenarios that aren’t supported in Snowpark.

### Input

The following example shows a method with a few unsupported scenarios in Snowpark.

Copy code

```
import pandas as pd

df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
result = df.mask()
```

### Output

The SMA adds the EWI `PNDSPY1066` to the output code to let you know that this element has a few scenarios that aren’t supported in Snowpark.

Copy code

```
import snowflake.snowpark.modin.pandas as pd

#EWI: PNDSPY1066 => pandas.core.frame.DataFrame.mask has a partial mapping, with few scenarios not supported. Check Snowpark pandas documentation for more detail.
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
result = df.mask()
```

## Recommended fix

**Behavioral note**: N if given axis when other is a DataFrame or level parameters; N if cond or other is Callable.

This behavior may differ from native pandas. Recommended actions:

- Test with a representative sample of your data
- Compare results with native pandas if precision is critical
- Use `.to_pandas()` if exact pandas behavior is required

## Additional recommendations

Check the [Snowpark pandas documentation](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/supported/index) to verify which scenarios aren’t supported for that specific element.
