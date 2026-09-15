Categories:
:   [Date & time functions](/sql-reference/functions-date-time)

# CONVERT\_TIMEZONE

Converts a timestamp to another time zone.

## Syntax

Copy code

```
CONVERT_TIMEZONE( <source_tz> , <target_tz> , <source_timestamp_ntz> )

CONVERT_TIMEZONE( <target_tz> , <source_timestamp> )
```

## Arguments

`source_tz`
:   String specifying the time zone for the input timestamp. Required for timestamps with no time zone (that is, TIMESTAMP\_NTZ).

`target_tz`
:   String specifying the time zone to which the input timestamp is converted.

`source_timestamp_ntz`
:   For the 3-argument version, string specifying the timestamp to convert (must be TIMESTAMP\_NTZ).

`source_timestamp`
:   For the 2-argument version, the timestamp to convert. Can be any timestamp variant (TIMESTAMP\_LTZ,
    TIMESTAMP\_NTZ, or TIMESTAMP\_TZ) or a DATE value. For how the source time zone is determined for each
    of these types, see the usage notes below.

## Returns

Returns a value of type TIMESTAMP\_NTZ, TIMESTAMP\_TZ, or NULL:

- For the 3-argument version, returns a value of type TIMESTAMP\_NTZ.
- For the 2-argument version, returns a value of type TIMESTAMP\_TZ.
- If any argument is NULL, returns NULL.

## Usage notes

- The display format for timestamps in the output is determined by the
  [timestamp output format](/sql-reference/date-time-input-output#label-session-parameters-for-dates-times-timestamps) for the current
  session and the data type of the returned timestamp value.
- For the 3-argument version, the “wallclock” time in the result represents the same moment in time as the input “wallclock”
  in the input time zone, but in the target time zone.
- For the 2-argument version, the source time zone is determined by the data type of the
  `source_timestamp` argument:

  - **TIMESTAMP\_TZ:** The time zone is taken from the value itself.
  - **TIMESTAMP\_LTZ:** The time zone is the current session time zone (set by the
    [TIMEZONE](/sql-reference/parameters#label-timezone) parameter).
  - **TIMESTAMP\_NTZ:** The value has no time zone, so it’s interpreted as a “wallclock” time in the
    current session time zone, and that session time zone is used as the source.
  - **DATE:** The value is cast to TIMESTAMP\_NTZ with the time set to midnight (`00:00:00`), and then
    handled the same way as TIMESTAMP\_NTZ (the current session time zone is used as the source).
- For `source_tz` and `target_tz`, you can specify a [time zone name](https://data.iana.org/time-zones/tzdb-2025b/zone1970.tab) or a [link name](https://data.iana.org/time-zones/tzdb-2025b/backward) from release
  2025b of the [IANA Time Zone Database](https://www.iana.org/time-zones) (for example, `America/Los_Angeles`, `Europe/London`, `UTC`,
  `Etc/GMT`, and so on).

  Note

  - Time zone names are case-sensitive and must be enclosed in single quotes (e.g. `'UTC'`).
  - Snowflake does not support the majority of timezone [abbreviations](https://en.wikipedia.org/wiki/List_of_time_zone_abbreviations) (e.g. `PDT`, `EST`, etc.) because a
    given abbreviation might refer to one of several different time zones. For example, `CST` might refer to Central
    Standard Time in North America (UTC-6), Cuba Standard Time (UTC-5), and China Standard Time (UTC+8).

## Examples

To use the default [timestamp output format](/sql-reference/date-time-input-output#label-session-parameters-for-dates-times-timestamps)
for the timestamps returned in the examples, unset the TIMESTAMP\_OUTPUT\_FORMAT parameter in the current session:

Copy code

```
ALTER SESSION UNSET TIMESTAMP_OUTPUT_FORMAT;
```

### Examples that specify a source time zone

The following examples use the 3-argument version of the CONVERT\_TIMEZONE function and specify a `source_tz`
value. These examples return TIMESTAMP\_NTZ values.

Convert a “wallclock” time in Los Angeles to the matching “wallclock” time in New York:

Copy code

```
SELECT CONVERT_TIMEZONE(
  'America/Los_Angeles',
  'America/New_York',
  '2024-01-01 14:00:00'::TIMESTAMP_NTZ
) AS conv;
```

```
+-------------------------+
| CONV                    |
|-------------------------|
| 2024-01-01 17:00:00.000 |
+-------------------------+
```

Convert a “wallclock” time in Warsaw to the matching “wallclock” time in UTC:

Copy code

```
SELECT CONVERT_TIMEZONE(
  'Europe/Warsaw',
  'UTC',
  '2024-01-01 00:00:00'::TIMESTAMP_NTZ
) AS conv;
```

```
+-------------------------+
| CONV                    |
|-------------------------|
| 2023-12-31 23:00:00.000 |
+-------------------------+
```

### Examples that do not specify a source time zone

The following examples use the 2-argument version of the CONVERT\_TIMEZONE function. These examples return
TIMESTAMP\_TZ values. Therefore, the returned values include an offset that shows the difference between
the timestamp’s time zone and Coordinated Universal Time (UTC). For example, the `America/Los_Angeles`
time zone has an offset of `-0700` to show that it is seven hours behind UTC.

Convert a string specifying a TIMESTAMP\_TZ value to a different time zone:

Copy code

```
SELECT CONVERT_TIMEZONE(
  'America/Los_Angeles',
  '2024-04-05 12:00:00 +02:00'
) AS time_in_la;
```

```
+-------------------------------+
| TIME_IN_LA                    |
|-------------------------------|
| 2024-04-05 03:00:00.000 -0700 |
+-------------------------------+
```

Show the current “wallclock” time in different time zones:

Copy code

```
SELECT
  CURRENT_TIMESTAMP() AS now_in_la,
  CONVERT_TIMEZONE('America/New_York', CURRENT_TIMESTAMP()) AS now_in_nyc,
  CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP()) AS now_in_paris,
  CONVERT_TIMEZONE('Asia/Tokyo', CURRENT_TIMESTAMP()) AS now_in_tokyo;
```

```
+-------------------------------+-------------------------------+-------------------------------+-------------------------------+
| NOW_IN_LA                     | NOW_IN_NYC                    | NOW_IN_PARIS                  | NOW_IN_TOKYO                  |
|-------------------------------+-------------------------------+-------------------------------+-------------------------------|
| 2024-06-12 08:52:53.114 -0700 | 2024-06-12 11:52:53.114 -0400 | 2024-06-12 17:52:53.114 +0200 | 2024-06-13 00:52:53.114 +0900 |
+-------------------------------+-------------------------------+-------------------------------+-------------------------------+
```

### Example with TIMESTAMP\_LTZ input

The following example uses the 2-argument version with a TIMESTAMP\_LTZ value. A TIMESTAMP\_LTZ value is
interpreted in the current session time zone, so that session time zone is used as the source. The example
sets the session time zone to `America/Los_Angeles` first:

Copy code

```
ALTER SESSION SET TIMEZONE = 'America/Los_Angeles';
```

Convert a TIMESTAMP\_LTZ value to UTC. The input `09:00:00` is interpreted in the session time zone
(`America/Los_Angeles`, which is seven hours behind UTC), so the result is offset accordingly:

Copy code

```
SELECT CONVERT_TIMEZONE('UTC', '2024-04-05 09:00:00'::TIMESTAMP_LTZ) AS ltz_in_utc;
```

```
+-------------------------------+
| LTZ_IN_UTC                    |
|-------------------------------|
| 2024-04-05 16:00:00.000 +0000 |
+-------------------------------+
```

### Examples with TIMESTAMP\_NTZ and DATE input

The following examples use the 2-argument version with a TIMESTAMP\_NTZ value and a DATE value. Because
neither type carries a time zone, the current session time zone is used as the source time zone. These
examples set the session time zone to `America/Los_Angeles` first:

Copy code

```
ALTER SESSION SET TIMEZONE = 'America/Los_Angeles';
```

Convert a TIMESTAMP\_NTZ value to UTC. The input is interpreted as a “wallclock” time in the session
time zone (`America/Los_Angeles`), so the result is offset accordingly:

Copy code

```
SELECT CONVERT_TIMEZONE('UTC', '2024-04-05 12:00:00'::TIMESTAMP_NTZ) AS ntz_in_utc;
```

```
+-------------------------------+
| NTZ_IN_UTC                    |
|-------------------------------|
| 2024-04-05 19:00:00.000 +0000 |
+-------------------------------+
```

Convert a DATE value to UTC. The DATE is cast to TIMESTAMP\_NTZ at midnight in the session time zone
(`America/Los_Angeles`), then converted:

Copy code

```
SELECT CONVERT_TIMEZONE('UTC', '2024-04-05'::DATE) AS date_in_utc;
```

```
+-------------------------------+
| DATE_IN_UTC                   |
|-------------------------------|
| 2024-04-05 07:00:00.000 +0000 |
+-------------------------------+
```
