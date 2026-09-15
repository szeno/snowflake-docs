# PNDSPY1002

**Message** Pandas < **element** > has a partial mapping with a few scenarios not supported in Snowpark.

**Category** Warning

## Description

This issue appears when the SMA detects the use of a pandas element that has a direct equivalent in Snowpark pandas, but some scenarios might behave differently than pandas.

## Scenario

A method with a few scenarios that aren’t supported in Snowpark.

### Input

The following example shows a method with a few unsupported scenarios in Snowpark.

Copy code

```
import pandas as pd

pd.melt(df, id_vars=['A'], value_vars=['B'])
```

### Output

The SMA adds the EWI `PNDSPY1002` to the output code to let you know that this element has a few scenarios that aren’t supported in Snowpark.

Copy code

```
import snowflake.snowpark.modin.pandas as pd

#EWI: PNDSPY1002 => pandas.core.reshape.melt.melt has a partial mapping, with few scenarios not supported. Check Snowpark pandas documentation for more detail.
pd.melt(df, id_vars=['A'], value_vars=['B'])
```

## Recommended fix

Since this is a generic error code that applies to a range of partially supported functions, no single fix applies to all cases. The appropriate action depends on the particular element in use.

Even though the element isn’t supported in some scenarios, you might still find a solution or workaround. This issue code only means that the SMA can’t convert the element automatically.

## Additional recommendations

Check the [Snowpark pandas documentation](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/supported/index) to verify which scenarios aren’t supported for that specific element.
