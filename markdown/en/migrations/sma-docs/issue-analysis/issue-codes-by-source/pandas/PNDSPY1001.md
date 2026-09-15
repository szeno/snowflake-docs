# PNDSPY1001

**Message** < **element** > is not supported, pandas element is not supported yet.

**Category** Conversion Error

## Description

This issue appears when the SMA detects the use of a pandas element that isn’t supported in Snowpark pandas and doesn’t have its own error code. This is the generic error code that the SMA uses for an unsupported element.

## Scenario

A pandas element that isn’t supported by Snowpark.

### Input

The following example shows a pandas element that isn’t supported by Snowpark.

Copy code

```
import pandas as pd

pd.not_supported_function()
```

### Output

The SMA adds the EWI `PNDSPY1001` to the output code to let you know that this element isn’t supported by Snowpark.

Copy code

```
import snowflake.snowpark.modin.pandas as pd

#EWI: PNDSPY1001 => pandas.not_supported_function is not supported
pd.not_supported_function()
```

## Recommended fix

Since this is a generic error code that applies to a range of unsupported functions, no single fix applies to all cases. The appropriate action depends on the particular element in use.

Even though the element isn’t supported, you might still find a solution or workaround. This issue code only means that the SMA can’t convert the element automatically.

## Additional recommendations

If you believe that Snowpark pandas already supports this element or that a workaround exists, report that you encountered a conversion error on that particular element using [the Report an Issue option](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings) in the SMA and include any additional information that you think may be helpful.
