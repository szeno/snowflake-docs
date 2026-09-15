# PNDSPY1007

**Message** `pandas.core.series.Series.str.slice` has a partial mapping because it has several scenarios not supported in Snowpark pandas.

**Category** Warning

## Description

This issue appears when the SMA identifies a [pandas.core.series.Series.str.slice](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.slice.html) usage.
Snowpark pandas offers a partial equivalent, but the current implementation has two unsupported scenarios.

## Scenarios

The following scenarios illustrate the two unsupported use cases.

### Scenario 1

The first scenario is when the method receives mixed data type columns, which causes it to behave unexpectedly.
All values within a column must be of the same type.

#### Input

The following example shows an unsupported use of `pandas.core.series.Series.str.slice`.

Copy code

```
import pandas as pd

s = pd.Series(["String", (1, 2, 3), ["a", "b", "c"], 123, -456, {1: "Hello", "2": "World"}])
print(s.str.slice(1))
```

#### Output

The SMA adds the EWI `PNDSPY1007` to the output code to indicate that it has a scenario not supported in Snowpark pandas.

Copy code

```
from snowflake.snowpark.modin import plugin
import modin.pandas as pd

s = pd.Series(["String", (1, 2, 3), ["a", "b", "c"], 123, -456, {1: "Hello", "2": "World"}])
#EWI: PNDSPY1007 => pandas.core.series.Series.str.slice has a partial mapping,because has several scenarios not supported in Snowpark pandas.
print(s.str.slice(1))
```

#### Recommended fix

Ensure that the Series contains only one type of data (all strings, all lists, or all dicts).
No code change is strictly required, but be aware that this operation might not work as expected in Snowpark pandas.

### Scenario 2

The second scenario is when a column contains list values and the `step` parameter is set to a value other than one.

#### Input

The following example shows an unsupported use of `pandas.core.series.Series.str.slice`.

Copy code

```
import pandas as pd

ser = pd.Series(["koala", "dog", "chameleon","cat", "mouse", "elephant","lion", "tiger", "bear"])
print(ser.str.slice(step=3))
```

#### Output

The SMA adds the EWI `PNDSPY1007` to the output code to indicate that it has a scenario not supported in Snowpark pandas.

Copy code

```
from snowflake.snowpark.modin import plugin
import modin.pandas as pd

ser = pd.Series(["koala", "dog", "chameleon","cat", "mouse", "elephant","lion", "tiger", "bear"])
#EWI: PNDSPY1007 => pandas.core.series.Series.str.slice has a partial mapping, because has several scenarios not supported in Snowpark pandas.
print(ser.str.slice(step=3))
```

#### Recommended fix

This requires a manual change. Use the [apply](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/pandas_api/modin.pandas.Series.apply) function to achieve the same behavior with a lambda function.
Here is the previous output code with the recommended fix:

Copy code

```
from snowflake.snowpark.modin import plugin
import modin.pandas as pd

ser = pd.Series(["koala", "dog", "chameleon","cat", "mouse", "elephant","lion", "tiger", "bear"])
print(ser.apply(lambda lst: lst[::3]))
```
