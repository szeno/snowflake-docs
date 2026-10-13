# Migration guide: datetime format and parsing fixes

Config flag: `snowpark.connect.useUdfForUnsupportedDateTimeFormats` (default: `true` from 1.46.0)

## Who is affected

Any workload that calls `date_format`, `to_timestamp`, `to_date`, or `to_unix_timestamp`
with a format string containing less common tokens. See the [Categories of change](#categories-of-change)
section below for the full token list. Workloads using only common tokens (`yyyy`, `MM`, `dd`,
`HH`, `mm`, `ss`, `SSS`) are not affected.

## What changes

This change fixes several issues with date-time formatting and parsing for less common patterns.
Previously these produced empty output, a literal character, garbage, or a crash. After this
change:

1. **Validation** — patterns that Spark itself rejects now raise the same error Spark raises
   (instead of silently emitting garbage).
2. **UDF fallback** — patterns that are legal in Spark but that Snowflake’s
   `TO_CHAR`/`TO_TIMESTAMP` cannot reproduce are routed through a Java UDF backed by
   `java.time.format.DateTimeFormatter`, so the output matches Spark 3.5 exactly.

This applies to `date_format`, `to_timestamp`, `to_date`, and `to_unix_timestamp`.

## Categories of change

All examples in this section use `date_format("2018-11-17 13:33:33", <pattern>)`
with a session timezone of `America/New_York` (EST, UTC−5), unless noted otherwise.
November 17, 2018 is day 321 of the year and falls in Q4; 13:33 is 1:33 PM.

### A. Output value corrected — the old result looked plausible but was wrong

| Pattern | What it means | Before | After |
| --- | --- | --- | --- |
| `X` | UTC offset, **hours only**. Emits `Z` when the offset is UTC+0. One letter = short form. | `-05:00` (used the long `XXX` form) | `-05` |
| `x` | Same as `X` but never emits `Z`; always a signed offset | `-05:00` (used the long `xxx` form) | `-05` |
| `k` | Clock-hour of day, **1–24**. Midnight is hour 24, not 0. | `00` (used Snowflake `HH24`, which counts midnight as 0) | `24` |
| `kk` | Same, zero-padded to at least 2 digits | `00` | `24` |

Expand

Show lessSee more

**`X` vs `XXX`:** The number of `X` letters controls how much precision is shown. `X` = hours
only (`-05`), `XX` = hours + minutes no colon (`-0500`), `XXX` = hours + colon + minutes
(`-05:00`). The old code always emitted the `XXX` form regardless of how many `X` letters
you wrote.

**`k`/`kk`:** The difference from `H`/`HH` only appears at midnight. For any other hour the
numeric value is identical.

### B. Old output was empty string or a literal — now produces the correct value

| Pattern | What it means | Before | After |
| --- | --- | --- | --- |
| `G` | Era designator, abbreviated (`BC` / `AD`) | `G` — the letter itself, not a value | `AD` |
| `GG` | Era designator, abbreviated (same output as `G`) | `GG` — the letters themselves | `AD` |
| `GGGG` | Era designator, full text | `GGGG` — the letters themselves | `Anno Domini` |
| `q` | Quarter number, unpadded | (empty) | `4` |
| `qq` | Quarter number, zero-padded to 2 digits | (empty) | `04` |
| `qqq` | Quarter short label | (empty) | `Q4` |
| `Q` | Quarter number, unpadded (same output as `q`) | (empty) | `4` |
| `QQQ` | Quarter short label (same output as `qqq`) | (empty) | `Q4` |
| `D` | Day of year, unpadded (Jan 1 = 1) | (empty) | `321` |
| `DD` | Day of year, minimum 2 digits | (empty) | `321` |
| `F` | Which occurrence of this weekday in the month (Nov 17 = 3rd Saturday) | (empty) | `3` |
| `K` | Hour in AM/PM cycle, **0–11** (midnight = 0, noon = 0, 1 PM = 1) | (empty) | `1` |
| `KK` | Same, zero-padded to at least 2 digits | (empty) | `01` |
| `VV` | Full IANA timezone ID | (empty) | `America/New_York` |
| `z` / `zz` | Short timezone abbreviation | (empty) | `EST` |
| `zzzz` | Full timezone name | (empty) | `Eastern Standard Time` |
| `O` | Localized UTC offset, short form | (empty) | `GMT-5` |
| `OOOO` | Localized UTC offset, full form | (empty) | `GMT-05:00` |
| `ZZZZ` | Localized UTC offset, full form (same output as `OOOO`) | (empty) | `GMT-05:00` |

Expand

Show lessSee more

Compound patterns fill in every unsupported token. For example:

Copy code

```
date_format("2018-11-17 13:33:33", "yyyy-MM-dd 'Q'Q G")
  Before: "2018-11-17 Q G"          <- Q and G were dropped
  After:  "2018-11-17 Q4 AD"

date_format("2018-11-17 13:33:33", "yyyy 'day' D 'of year'")
  Before: "2018 day  of year"       <- D was dropped (note the double space)
  After:  "2018 day 321 of year"
```

### C. Now raises — used to return something (highest risk)

These patterns produced a result before the flag. After the flag they raise the same error Spark
raises. Your job will now fail instead of continuing with a silently wrong value.

| Pattern | What it meant | Before — what Snowpark Connect for Spark returned | After — error raised |
| --- | --- | --- | --- |
| `u` | Week-based year (Spark has rejected this since 3.0) | The letter `u` as a literal | `Fail to recognize 'u' pattern in the DateTimeFormatter` |
| `uuuu` | Week-based year, 4-digit form | The string `uuuu` as a literal | `Fail to recognize 'uuuu' pattern in the DateTimeFormatter` |
| `c` | Week-based day-of-week (removed in Spark 3.0) | The letter `c` as a literal | `All week-based patterns are unsupported since Spark 3.0, detected: c` |
| `A` | Not a valid Spark pattern letter | The letter `A` as a literal | `Illegal pattern character: A` |
| `B` | Not a valid Spark pattern letter | The letter `B` as a literal | `Illegal pattern character: B` |
| `n` | Not a valid Spark pattern letter | The letter `n` as a literal | `Illegal pattern character: n` |
| `p` | Not a valid Spark pattern letter | The letter `p` as a literal | `Illegal pattern character: p` |
| `E`, `F`, `q`, `Q` in a **parse** format | Legal in `date_format` for output; illegal as parse tokens | Returned a result or `NULL` | Raises: these tokens cannot appear in a parse format string |

Expand

Show lessSee more

### D. Parse path — z timezone abbreviation token

`z` matches a timezone abbreviation (such as `EST`, `GMT`, `UTC`) in a string being parsed.
Before this change, Snowpark Connect for Spark could not route `z` through a parser that understands
abbreviations, so parsing silently returned `NULL`. After this change, the abbreviation is honored.

| Function | Format string | Input string | Before | After |
| --- | --- | --- | --- | --- |
| `to_timestamp` | `yyyy-MM-dd HH:mm:ss.SSS z` | `"2018-11-17 13:33:33.333 GMT"` | `NULL` | `2018-11-17 08:33:33` |

Expand

Show lessSee more

The after result shows `08:33:33` because `GMT` (UTC+0) at `13:33:33` is the same instant as
`08:33:33` in EST (UTC−5). The session is `America/New_York` so the timestamp is displayed
in that zone.

## Examples

Copy code

```
from pyspark.sql import functions as F

df = spark.createDataFrame([("2024-01-06 13:30:00",)], ["ts"])

# Category B: quarter pattern 'Q' — was empty, now correct.
df.select(F.date_format("ts", "Q").alias("q")).show()
# BEFORE: "" (empty)
# AFTER:  "1" (Q1)

# Category A: full day name 'EEEE' — was abbreviated, now full.
df.select(F.date_format("ts", "EEEE").alias("day")).show()
# BEFORE: "Sat"
# AFTER:  "Saturday"

# Category C: week-based year 'YYYY' — was wrong, now raises (matches Spark).
df.select(F.date_format("ts", "YYYY")).show()
# BEFORE: returned a (wrong) year value
# AFTER:  raises: "All week-based patterns are unsupported since Spark 3.0,
#         detected: Y, Please use the SQL function EXTRACT instead"

# Category C: doubled-quote literal in a parse — was lenient, now raises.
df2 = spark.createDataFrame([("2024-01-06T13:30:00",)], ["s"])
df2.select(F.to_timestamp("s", "yyyy-MM-dd''T''HH:mm:ss")).show()
# BEFORE: parsed leniently
# AFTER:  raises "Unknown pattern letter: T" (quote your literal 'T' instead)
```

## How to migrate

- **Category A / B / D changes** make your output correct and Spark-compatible. Verify
  downstream consumers can accept the corrected values (for example, `Saturday` instead of
  `Sat`).
- **Category C changes** require you to fix the format string, matching what OSS Spark expects:
  - Replace week-based `YYYY`/`Y` with `yyyy` (calendar year), unless you truly want
    ISO week-year semantics (use SQL `EXTRACT`).
  - Quote literal letters properly: use `yyyy-MM-dd'T'HH:mm:ss` (single quotes),
    not `yyyy-MM-dd''T''HH:mm:ss`.
  - Do not use `E`, `F`, `q`, `Q` in a **parse** format (they are only valid for formatting).

## How to opt out (restore old behavior)

Copy code

```
spark.conf.set("snowpark.connect.useUdfForUnsupportedDateTimeFormats", "false")
```
