# PNDSPY1012

**Message** `pandas.core.frame.DataFrame.query` has a partial mapping because there is an unsupported scenario in Snowpark pandas.

**Category** Warning

## Description

This issue appears when the SMA detects the use of [pandas.core.frame.DataFrame.query](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.query.html).
This method is commonly used for filtering data in pandas DataFrames, but Snowpark pandas currently has limitations in supporting it.
Specifically, it doesn’t support DataFrames that have a row MultiIndex, which can lead to compatibility issues during migration or execution.

## Scenario

Using `query()` with a row MultiIndex.

### Input

The following example shows how `query()` behaves with a row MultiIndex.

Copy code

```
import modin.pandas as pd

data = {
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank'],
    'age': [25, 30, 35, 28, 32, 45],
    'salary': [50000, 60000, 75000, 55000, 80000, 90000],
    'department': ['Sales', 'IT', 'HR', 'Sales', 'IT', 'HR']
}

df = pd.DataFrame(data)

df = df.set_index('name')

print("DataFrame with single-level index:")
print(df)

result = df.query("age > 30 and salary < 85000")

data = {
    'A': [1, 2, 3, 4, 5, 6],
    'B': [10, 20, 30, 40, 50, 60],
    'C': ['x', 'y', 'x', 'y', 'x', 'y']
}

df = pd.DataFrame(data)

df = df.set_index([
    pd.Index(['group1', 'group1', 'group2', 'group2', 'group3', 'group3']),
    pd.Index(['a', 'b', 'a', 'b', 'a', 'b'])
])
df.index.names = ['group', 'subgroup']

result = df.query("A > 2 and B < 55")
```

### Output

The SMA adds the EWI `PNDSPY1012` to the output code to indicate that it has a scenario not supported in Snowpark pandas.

Copy code

```
from snowflake.snowpark.modin import plugin
import modin.pandas as pd

data = {
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank'],
    'age': [25, 30, 35, 28, 32, 45],
    'salary': [50000, 60000, 75000, 55000, 80000, 90000],
    'department': ['Sales', 'IT', 'HR', 'Sales', 'IT', 'HR']
}

df = pd.DataFrame(data)

df = df.set_index('name')

print("DataFrame with single-level index:")
print(df)

#EWI: PNDSPY1012 => pandas.core.frame.DataFrame.query does not support DataFrames that have a row MultiIndex. Check Snowpark pandas documentation for more detail.
result = df.query("age > 30 and salary < 85000")

data = {
    'A': [1, 2, 3, 4, 5, 6],
    'B': [10, 20, 30, 40, 50, 60],
    'C': ['x', 'y', 'x', 'y', 'x', 'y']
}

df = pd.DataFrame(data)

df = df.set_index([
    pd.Index(['group1', 'group1', 'group2', 'group2', 'group3', 'group3']),
    pd.Index(['a', 'b', 'a', 'b', 'a', 'b'])
])
df.index.names = ['group', 'subgroup']

#EWI: PNDSPY1012 => pandas.core.frame.DataFrame.query does not support DataFrames that have a row MultiIndex. Check Snowpark pandas documentation for more detail.
result = df.query("A > 2 and B < 55")
```

## Recommended fix

If the DataFrame contains a MultiIndex, validate the behavior of the `query()` method in Snowpark pandas. Ensure that the DataFrame structure is compatible with Snowpark pandas’ limitations, as MultiIndex rows aren’t supported. Consider restructuring the DataFrame to use a single-level index or alternative filtering methods.
