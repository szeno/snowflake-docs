# PNDSPY1097

**Message** Pandas < **pandas.core.frame.DataFrame.sample** > has a partial mapping with a few scenarios not supported in Snowpark.

**Category** Warning

## Applies to

This EWI applies to the following elements (same implementation):

- `pandas.core.frame.DataFrame.sample`
- `pandas.core.generic.NDFrame.sample`
- `pandas.core.series.Series.sample`

## Description

This issue appears when the SMA detects the use of a pandas element that has a direct equivalent in Snowpark pandas, but some scenarios might behave differently than pandas.

**Reason:** N if weights is specified when axis = 0, or if random\_state is not either an integer or None. Setting random\_state to a value other than None may slow down this method because the sample implementation will use a sort instead of the Snowflake warehouse’s built-in SAMPLE construct.

## Scenario

A method with a few scenarios that aren’t supported in Snowpark.

### Input

The following example shows a method with a few unsupported scenarios in Snowpark.

Copy code

```
import pandas as pd

df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
result = df.sample()
```

### Output

The SMA adds the EWI `PNDSPY1097` to the output code to let you know that this element has a few scenarios that aren’t supported in Snowpark.

Copy code

```
import snowflake.snowpark.modin.pandas as pd

#EWI: PNDSPY1097 => pandas.core.frame.DataFrame.sample has a partial mapping, with few scenarios not supported. Check Snowpark pandas documentation for more detail.
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
result = df.sample()
```

## Recommended fix

**Performance consideration**: N if weights is specified when axis = 0, or if random\_state is not either an integer or None. Setting random\_state to a value other than None may slow down this method because the sample implementation will use a sort instead of the Snowflake warehouse’s built-in SAMPLE construct.

For better performance:

- Filter data before applying this operation to reduce data volume
- Consider breaking the operation into smaller chunks
- Use Snowflake’s native SQL functions via `session.sql()` for large datasets

## Additional recommendations

Check the [Snowpark pandas documentation](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/supported/index) to verify which scenarios aren’t supported for that specific element.
