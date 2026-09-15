# PNDSPY1017

**Message** `pandas.core.reshape.encoding.get_dummies` has a partial mapping because there is a not supported scenario in Snowpark pandas.

**Category** Warning

## Description

This issue appears when the SMA identifies a [pandas.core.reshape.encoding.get\_dummies](https://pandas.pydata.org/docs/reference/api/pandas.get_dummies.html) usage.
Snowpark pandas currently has limitations with `pandas.get_dummies`. It’s supported if parameters “dummy\_na” and “drop\_first” are both false; otherwise it isn’t supported.

## Scenario

An unsupported use of `pandas.core.reshape.encoding.get_dummies`.

### Input

The following example shows an unsupported use of `pandas.core.reshape.encoding.get_dummies`.

Copy code

```
import pandas as pd
import numpy as np

s1 = ['a', 'b', np.nan]
pd.get_dummies(s1, dummy_na=True)

s2 = list('abcaa')
pd.get_dummies(s2, drop_first=True)
```

### Output

The SMA adds the EWI `PNDSPY1017` to the output code to indicate that it has a scenario not supported in Snowpark pandas.

Copy code

```
from snowflake.snowpark.modin import plugin
import modin.pandas as pd
import numpy as np

s1 = ['a', 'b', np.nan]
#EWI: PNDSPY1017 => pandas.core.reshape.encoding.get_dummies is supported if parameters "dummy_na" and "drop_first" are both false, otherwise it is not supported. Check Snowpark pandas documentation for more detail.
pd.get_dummies(s1, dummy_na=True)

s2 = list('abcaa')
#EWI: PNDSPY1017 => pandas.core.reshape.encoding.get_dummies is supported if parameters "dummy_na" and "drop_first" are both false, otherwise it is not supported. Check Snowpark pandas documentation for more detail.
pd.get_dummies(s2, drop_first=True)
```

## Recommended fix

### For the `dummy_na` parameter

This requires a manual adjustment:

1. Replace the `np.nan` value with an acceptable value such as `'np.nan'`.
2. Remove the use of the parameter `dummy_na`.
3. Rename the column `'np.nan'` to the original `np.nan` value.

To illustrate the recommended fix, here is the output code with the changes applied:

Copy code

```
s1 = s1.replace(np.nan, 'np.nan') if isinstance(s1, (pd.DataFrame, pd.Series)) else ['np.nan' if pd.isna(item) else item for item in s1]
pd.get_dummies(s1).rename(columns={'np.nan': np.nan})
```

### For the `drop_first` parameter

This requires a manual adjustment:

1. Remove the use of the parameter `drop_first`.
2. Remove the first column of the result (you can use the `iloc` indexer for it).

To illustrate the recommended fix, here is the output code with the changes applied:

Copy code

```
pd.get_dummies(s2).iloc[:, 1:]
```
