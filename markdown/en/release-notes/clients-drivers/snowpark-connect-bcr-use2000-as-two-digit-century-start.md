# Migration guide: two-digit year (yy) parsing change

Config flag: `snowpark.connect.use2000AsTwoDigitCenturyStart` (default: `true` from 1.46.0)

## Who is affected

Only **parsing** functions with a standalone `yy` format: `to_timestamp`, `to_date`,
`to_timestamp_ntz`, `to_timestamp_ltz`, and their `try_*` variants. Formatting
(`date_format`) is not affected.

## What changes

A standalone two-digit year token `yy` (in a parsing function) now maps to Spark’s fixed
2000-2099 window. Previously Snowpark Connect for Spark followed Snowflake’s native
`TWO_DIGIT_CENTURY_START` parameter (default 1970). Enabling this change sets
`TWO_DIGIT_CENTURY_START = 2000` for the session.

| Two-digit year | Before | After |
| --- | --- | --- |
| `00`-`69` | 2000-2069 | 2000-2069 (identical) |
| `70`-`99` | 1970-1999 | **2070-2099** |

Expand

Show lessSee more

The two windows differ only for values `70`-`99`. Values `00`-`69` are unchanged. A workload is
affected only if its runtime data actually contains a two-digit year in the `70`-`99` range.

This is a silent change. No error is raised. A `70`-`99` year that parsed to the 1900s now
parses to the 2000s — shifted forward by exactly 100 years.

## Example

Copy code

```
from pyspark.sql import functions as F

df = spark.createDataFrame([("85",), ("42",)], ["yy"])

# --- BEFORE (native 1970 window) ---
df.select(F.to_date(F.col("yy"), "yy").alias("d")).show()
# +----------+
# |         d|
# +----------+
# |1985-01-01|   <- 85 -> 1985
# |2042-01-01|   <- 42 -> 2042
# +----------+

# --- AFTER (Spark 2000 window, flag default true) ---
df.select(F.to_date(F.col("yy"), "yy").alias("d")).show()
# +----------+
# |         d|
# +----------+
# |2085-01-01|   <- 85 -> 2085 (shifted +100 years)
# |2042-01-01|   <- 42 -> 2042 (unchanged)
# +----------+
```

## How to migrate

- If your data represents years in the 2000s, the new behavior is correct and matches
  Spark — no action needed.
- If your data genuinely represents 1900s two-digit years (for example, historical GL records),
  you must opt out, or switch to a four-digit `yyyy` format in your source data.

## How to opt out (restore old behavior)

Copy code

```
spark.conf.set("snowpark.connect.use2000AsTwoDigitCenturyStart", "false")
```
