# PNDSPY1092

**Message** Pandas < **pandas.core.frame.DataFrame.rolling** > has a partial mapping with a few scenarios not supported in Snowpark.

**Category** Warning

## Applies to

This EWI applies to the following elements (same implementation):

- `pandas.core.frame.DataFrame.rolling`
- `pandas.core.generic.NDFrame.rolling`
- `pandas.core.series.Series.rolling`

## Description

This issue appears when the SMA detects the use of a pandas element that has a direct equivalent in Snowpark pandas, but some scenarios might behave differently than pandas.

**Missing or Unsupported Parameters:** `method is ignored`, `step`, `win_type`, `closed`, `on`

**Reason:** N for non-integer window, axis = 1, or min\_periods = 0.

## Scenario

A method with a few scenarios that aren’t supported in Snowpark.

### Input

The following example shows a method with a few unsupported scenarios in Snowpark.

Copy code

```
import pandas as pd

df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
result = df.rolling()
```

### Output

The SMA adds the EWI `PNDSPY1092` to the output code to let you know that this element has a few scenarios that aren’t supported in Snowpark.

Copy code

```
import snowflake.snowpark.modin.pandas as pd

#EWI: PNDSPY1092 => pandas.core.frame.DataFrame.rolling has a partial mapping, with few scenarios not supported. Check Snowpark pandas documentation for more detail.
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
result = df.rolling()
```

## Recommended fix

The following parameters are not supported in Snowpark pandas: `method is ignored`, `step`, `win_type`, `closed`, `on`.

**Recommended approaches:**

1. **Avoid unsupported parameters**: Modify your code to not use these parameters if they are not essential.
2. **Use `.to_pandas()` for full compatibility**: If you need these parameters, convert to native pandas first:
   .. code-block:: python

   # Convert to native pandas when unsupported parameters are needed

   native\_df = df.to\_pandas()
   result = native\_df.rolling(…) # Use all parameters
3. **Split the operation**: Perform supported operations in Snowpark pandas, then use native pandas only for the unsupported functionality.

**Behavioral note**: N for non-integer window, axis = 1, or min\_periods = 0.

This behavior may differ from native pandas. Recommended actions:

- Test with a representative sample of your data
- Compare results with native pandas if precision is critical
- Use `.to_pandas()` if exact pandas behavior is required

## Additional recommendations

Check the [Snowpark pandas documentation](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/supported/index) to verify which scenarios aren’t supported for that specific element.
