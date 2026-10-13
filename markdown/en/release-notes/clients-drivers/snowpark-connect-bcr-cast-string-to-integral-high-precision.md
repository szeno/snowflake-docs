# Migration guide: CAST(string AS BIGINT) precision fix

Config flag: `snowpark.connect.cast.stringToIntegralHighPrecision` (default: `true` from 1.46.0)

## Who is affected

- Workloads casting very large string integers (approximately 9.2×10¹⁸) to `BIGINT`/`long`.
  Such magnitudes are rare, and the change is silent (a wrong value becomes a correct value).
- **ANSI mode users** (`spark.sql.ansi.enabled = true`) casting a string just past the Long
  boundary: previously returned a wrong value, now raises.

## What changes

Casting a string to `LongType` (`BIGINT`) near (±9,223,372,036,854,775,807) previously
rounded to the nearest power of two, producing wrong overflow decisions.

After this change, casting values near the boundary are exact. As a side effect, ANSI-mode
Long overflow now correctly raises `NumberFormatException` where it previously returned a
wrong value.

Smaller integral targets (`INT`, `SHORT`, `BYTE`) are unchanged.

|  | Cast of a 19-digit string near `Long.MAX` |
| --- | --- |
| **Before** | wrong value or wrong `NULL` |
| **After (non-ANSI)** | exact value, or `NULL` if genuinely out of range |
| **After (ANSI)** | exact value, or raises `NumberFormatException` on real overflow |

Expand

Show lessSee more

## Example

Copy code

```
from pyspark.sql import functions as F
from pyspark.sql.types import LongType

# A value one past Long.MAX_VALUE (9223372036854775807).
df = spark.createDataFrame([("9223372036854775808",)], ["s"])

# --- Non-ANSI mode ---
df.select(F.col("s").cast(LongType())).show(truncate=False)
# BEFORE: a wrong value (DOUBLE rounded 9223372036854775808 -> 9223372036854775807)
# AFTER:  NULL (correctly detected as out of range)

# --- ANSI mode (spark.sql.ansi.enabled = true) ---
df.select(F.col("s").cast(LongType())).show()
# BEFORE: a wrong value, no error
# AFTER:  raises NumberFormatException / [CAST_INVALID_INPUT]
```

## How to migrate

- The new values are correct. Review any downstream logic that keyed on the old (wrong)
  results — for example a `WHERE id IS NULL` filter used to catch overflow, or a join that
  silently dropped the miscast rows.
- ANSI-mode jobs at the exact boundary should handle the new `NumberFormatException`, or
  use `try_cast` to tolerate malformed input and get `NULL` instead.

## How to opt out (restore old behavior)

Copy code

```
spark.conf.set("snowpark.connect.cast.stringToIntegralHighPrecision", "false")
```
