# PNDSPY1142

**Message** Pandas < **pandas.core.indexes.base.Index.sort\_values** > has a partial mapping with a few scenarios not supported in Snowpark.

**Category** Warning

## Description

This issue appears when the SMA detects the use of a pandas element that has a direct equivalent in Snowpark pandas, but some scenarios might behave differently than pandas.

**Missing or Unsupported Parameters:** `key`

**Reason:** Snowpark pandas currently uses stable sort when sorting the index values. pandas uses quicksort.

## Scenario

A method with a few scenarios that aren’t supported in Snowpark.

### Input

The following example shows a method with a few unsupported scenarios in Snowpark.

Copy code

```
import pandas as pd

idx = pd.Index([1, 2, 3, 4, 5])
result = idx.sort_values()
```

### Output

The SMA adds the EWI `PNDSPY1142` to the output code to let you know that this element has a few scenarios that aren’t supported in Snowpark.

Copy code

```
import snowflake.snowpark.modin.pandas as pd

#EWI: PNDSPY1142 => pandas.core.indexes.base.Index.sort_values has a partial mapping, with few scenarios not supported. Check Snowpark pandas documentation for more detail.
idx = pd.Index([1, 2, 3, 4, 5])
result = idx.sort_values()
```

## Recommended fix

The parameter `key` is not supported in Snowpark pandas. If your code uses this parameter, consider one of these approaches:

1. **Remove the parameter**: If the parameter is not essential for your use case, simply remove it from the function call.
2. **Use default behavior**: The function will work with default values for the unsupported parameter.
3. **Post-process with native pandas**: If the parameter is critical, collect the result using `.to_pandas()` and apply the operation with native pandas:
   .. code-block:: python

   # Convert to native pandas for unsupported parameter

   result = df.to\_pandas().sort\_values(key=value)

**Behavioral note**: Snowpark pandas currently uses stable sort when sorting the index values. pandas uses quicksort.

This behavior may differ from native pandas. Recommended actions:

- Test with a representative sample of your data
- Compare results with native pandas if precision is critical
- Use `.to_pandas()` if exact pandas behavior is required

## Additional recommendations

Check the [Snowpark pandas documentation](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/supported/index) to verify which scenarios aren’t supported for that specific element.
