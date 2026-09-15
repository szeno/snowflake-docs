# PNDSPY1262

**Message** Pandas < **pandas.io.parsers.readers.read\_csv** > has a partial mapping with a few scenarios not supported in Snowpark.

**Category** Warning

## Description

This issue appears when the SMA detects the use of a pandas element that has a direct equivalent in Snowpark pandas, but some scenarios might behave differently than pandas.

**Reason:** Reads both local and staged file(s) into a Snowpark pandas DataFrame. Note that the order of rows in the result may differ from the order of rows in the original file(s) if using staged CSVs. Local files are parsed with native pandas and thus support most of the parameters supported by pandas itself. The usecols and names parameters are applied after creating a temp table in Snowflake. Previously staged files will use the Snowflake COPY FROM parser and schema inference. If you need to use staged files often, it’s recommended that you upload these as Parquet files to improve performance. You can force the use of the Snowflake parser with engine=snowflake.

## Scenario

A method with a few scenarios that aren’t supported in Snowpark.

### Input

The following example shows a method with a few unsupported scenarios in Snowpark.

Copy code

```
import pandas as pd

result = pd.read_csv('data.csv')
```

### Output

The SMA adds the EWI `PNDSPY1262` to the output code to let you know that this element has a few scenarios that aren’t supported in Snowpark.

Copy code

```
import snowflake.snowpark.modin.pandas as pd

#EWI: PNDSPY1262 => pandas.io.parsers.readers.read_csv has a partial mapping, with a few scenarios not supported. Check Snowpark pandas documentation for more detail.
result = pd.read_csv('data.csv')
```

## Recommended fix

**NULL/NaN handling difference**

Snowpark pandas may handle NULL/NaN values differently:

- Pre-filter NULL values using `.dropna()` or `.fillna()` before the operation
- Verify NULL handling behavior with a small sample dataset
- Use explicit NULL checks: `df[df['column'].notna()]`

## Additional recommendations

Check the [Snowpark pandas documentation](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/supported/index) to verify which scenarios aren’t supported for that specific element.
