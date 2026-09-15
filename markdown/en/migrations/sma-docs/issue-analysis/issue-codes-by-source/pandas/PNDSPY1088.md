# PNDSPY1088

**Message** Pandas < **pandas.core.frame.DataFrame.resample** > has a partial mapping with a few scenarios not supported in Snowpark.

**Category** Warning

## Applies to

This EWI applies to the following elements (same implementation):

- `pandas.core.frame.DataFrame.resample`
- `pandas.core.generic.NDFrame.resample`
- `pandas.core.series.Series.resample`

## Description

This issue appears when the SMA detects the use of a pandas element that has a direct equivalent in Snowpark pandas, but some scenarios might behave differently than pandas.

**Missing or Unsupported Parameters:** `axis`, `label`, `convention`, `kind`, , `level`, `origin`, , `offset`, `group_keys`

**Reason:** Only DatetimeIndex is supported and its freq will be lost. rule frequencies ‘s’, ‘min’, ‘h’, and ‘D’ are supported. rule frequencies ‘W’, ‘ME’, and ‘YE’ are supported with closed = “left”.

## Scenario

A method with a few scenarios that aren’t supported in Snowpark.

### Input

The following example shows a method with a few unsupported scenarios in Snowpark.

Copy code

```
import pandas as pd

df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
result = df.resample()
```

### Output

The SMA adds the EWI `PNDSPY1088` to the output code to let you know that this element has a few scenarios that aren’t supported in Snowpark.

Copy code

```
import snowflake.snowpark.modin.pandas as pd

#EWI: PNDSPY1088 => pandas.core.frame.DataFrame.resample has a partial mapping, with few scenarios not supported. Check Snowpark pandas documentation for more detail.
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
result = df.resample()
```

## Recommended fix

The following parameters are not supported in Snowpark pandas: `axis`, `label`, `convention`, `kind`, `level`, `origin`, `offset`, `group_keys`.

**Recommended approaches:**

1. **Avoid unsupported parameters**: Modify your code to not use these parameters if they are not essential.
2. **Use `.to_pandas()` for full compatibility**: If you need these parameters, convert to native pandas first:
   .. code-block:: python

   # Convert to native pandas when unsupported parameters are needed

   native\_df = df.to\_pandas()
   result = native\_df.resample(…) # Use all parameters
3. **Split the operation**: Perform supported operations in Snowpark pandas, then use native pandas only for the unsupported functionality.

**Behavioral note**: Only DatetimeIndex is supported and its freq will be lost. rule frequencies ‘s’, ‘min’, ‘h’, and ‘D’ are supported. rule frequencies ‘W’, ‘ME’, and ‘YE’ are supported with closed = “left”.

This behavior may differ from native pandas. Recommended actions:

- Test with a representative sample of your data
- Compare results with native pandas if precision is critical
- Use `.to_pandas()` if exact pandas behavior is required

## Additional recommendations

Check the [Snowpark pandas documentation](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/supported/index) to verify which scenarios aren’t supported for that specific element.
