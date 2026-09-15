# PNDSPY1003

**Message** < **element** > is not recognized, pandas element is not recognized yet.

**Category** Conversion Error

## Description

This issue appears when the SMA encounters a pandas element that it doesn’t yet recognize.

This issue can occur for different reasons, such as:

- An element that doesn’t exist in pandas.
- An element that was added in a pandas version that the SMA doesn’t yet support.
- An internal error of the SMA when processing the element.

## Scenarios

The following scenarios illustrate different reasons why this issue might occur.

### Scenario 1

An element that doesn’t exist in pandas.

#### Input

The following example shows an element that doesn’t exist in pandas.

Copy code

```
import pandas as pd

df = pd.DataFrame(
    {
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [25, 30, 35],
        "City": ["New York", "Los Angeles", "Chicago"],
    }
)

df.non_existent_function()
```

#### Output

Since the element doesn’t exist in pandas, the tool adds the EWI to the output code.

Copy code

```
import snowflake.snowpark.modin.pandas as pd

df = pd.DataFrame(
    {
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [25, 30, 35],
        "City": ["New York", "Los Angeles", "Chicago"],
    }
)

#EWI: PNDSPY1003 => pandas.core.frame.DataFrame.non_existent_function is not yet recognized
df.non_existent_function()
```

#### Recommended fix

Check the [pandas documentation](https://pandas.pydata.org/docs/reference/index.html) to verify whether the element exists in pandas.

If it’s a valid pandas element, report that you encountered a conversion error on that particular element using [the Report an Issue option](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings) in the SMA and include any additional information that you think may be helpful.

If it isn’t a valid pandas element, remove it and use a valid pandas function.

Copy code

```
import snowflake.snowpark.modin.pandas as pd

df = pd.DataFrame(
    {
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [25, 30, 35],
        "City": ["New York", "Los Angeles", "Chicago"],
    }
)

df.valid_existent_function()
```

### Scenario 2

An element that was added in a pandas version that the SMA doesn’t yet support.

#### Input

The following example shows an element that was added in a pandas version that the SMA doesn’t yet support.

Copy code

```
import pandas as pd

df = pd.DataFrame(
    {
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [25, 30, 35],
        "City": ["New York", "Los Angeles", "Chicago"],
    }
)

df.valid_function_since_x.x.x_version()
```

#### Output

Since the element was added in a pandas version that the tool doesn’t yet support, the tool adds the EWI to the output code.

Copy code

```
import snowflake.snowpark.modin.pandas as pd

df = pd.DataFrame(
    {
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [25, 30, 35],
        "City": ["New York", "Los Angeles", "Chicago"],
    }
)

#EWI: PNDSPY1003 => pandas.core.frame.DataFrame.valid_function_since_x.x.x_version is not yet recognized
df.valid_function_since_x.x.x_version()
```

#### Recommended fix

Verify the [Snowpark pandas documentation](https://docs.snowflake.com/developer-guide/snowpark/reference/python/latest/modin/index). If it’s a valid pandas element, report that you encountered a conversion error on that particular element using [the Report an Issue option](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings) in the SMA and include any additional information that you think may be helpful.

### Scenario 3

An internal error of the SMA when processing an element.

#### Input

The following example shows an internal error of the SMA when processing an element.

Copy code

```
import pandas as pd

df = pd.DataFrame(
    {
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [25, 30, 35],
        "City": ["New York", "Los Angeles", "Chicago"],
    }
)

df.valid_function()
```

#### Output

If an error occurred while processing the element and the tool can’t recognize it, the tool adds the EWI to the output code.

Copy code

```
import snowflake.snowpark.modin.pandas as pd

df = pd.DataFrame(
    {
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [25, 30, 35],
        "City": ["New York", "Los Angeles", "Chicago"],
    }
)

#EWI: PNDSPY1003 => pandas.core.frame.DataFrame.valid_function is not yet recognized
df.valid_function()
```

#### Recommended fix

Verify whether the element exists in the [pandas documentation](https://pandas.pydata.org/docs/reference/index.html) and also check the [Snowpark pandas documentation](https://docs.snowflake.com/developer-guide/snowpark/reference/python/latest/modin/index).
If it’s a valid pandas element, report that you encountered a conversion error on that particular element using [the Report an Issue option](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings) in the SMA and include any additional information that you think may be helpful.
