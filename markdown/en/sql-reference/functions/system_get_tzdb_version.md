Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_TZDB\_VERSION

Returns the release of the [IANA Time Zone Database](https://www.iana.org/time-zones) that Snowflake uses for the current session.

Snowflake uses this database for time zone names, UTC offsets, and daylight saving time rules, for example in
[CONVERT\_TIMEZONE](/sql-reference/functions/convert_timezone) and the [TIMEZONE](/sql-reference/parameters#label-timezone) parameter.

See also:
:   [CONVERT\_TIMEZONE](/sql-reference/functions/convert_timezone) , [TIMEZONE](/sql-reference/parameters#label-timezone)

## Syntax

Copy code

```
SYSTEM$GET_TZDB_VERSION()
```

## Arguments

None.

## Returns

Returns a VARCHAR value that contains the identifier of the currently active IANA Time Zone Database release.
The identifier is a four-digit year followed by a letter, for example `2026c`.

## Access control requirements

Any user in the account can execute the `SYSTEM$GET_TZDB_VERSION` function.

## Usage notes

- IANA publishes a new release of the Time Zone Database when real-world time zone information changes (for example,
  time zone names, UTC offsets, and daylight saving time rules). Snowflake periodically adopts new releases so that
  time zone calculations continue to return correct results.
- For the changes included in each release, see
  [News for the tz database](https://data.iana.org/time-zones/tzdb/NEWS).

## Examples

The following example returns the IANA Time Zone Database release that Snowflake is using. In this example, the
release is `2026c`:

Copy code

```
SELECT SYSTEM$GET_TZDB_VERSION();
```

```
+---------------------------+
| SYSTEM$GET_TZDB_VERSION() |
|---------------------------|
| 2026c                     |
+---------------------------+
```
