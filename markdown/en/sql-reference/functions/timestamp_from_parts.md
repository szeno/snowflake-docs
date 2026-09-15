Categories:
:   [Date & time functions](/sql-reference/functions-date-time)

# TIMESTAMP\_FROM\_PARTS

Creates a timestamp from individual numeric components. If no time zone is in effect, the function can be used to create a timestamp from a date expression and a time expression.

Aliases:
:   TIMESTAMPFROMPARTS

Variations (and Aliases):
:   TIMESTAMP\_LTZ\_FROM\_PARTS , TIMESTAMPLTZFROMPARTS

    TIMESTAMP\_NTZ\_FROM\_PARTS , TIMESTAMPNTZFROMPARTS

    TIMESTAMP\_TZ\_FROM\_PARTS , TIMESTAMPTZFROMPARTS

## Syntax

Copy code

```
TIMESTAMP_FROM_PARTS( <year>, <month>, <day>, <hour>, <minute>, <second> [, <nanosecond> ] [, <time_zone> ] )

TIMESTAMP_FROM_PARTS( <date_expr>, <time_expr> )
```

Copy code

```
TIMESTAMP_LTZ_FROM_PARTS( <year>, <month>, <day>, <hour>, <minute>, <second> [, <nanosecond>] )
```

Copy code

```
TIMESTAMP_NTZ_FROM_PARTS( <year>, <month>, <day>, <hour>, <minute>, <second> [, <nanosecond>] )

TIMESTAMP_NTZ_FROM_PARTS( <date_expr>, <time_expr> )
```

Copy code

```
TIMESTAMP_TZ_FROM_PARTS( <year>, <month>, <day>, <hour>, <minute>, <second> [, <nanosecond>] [, <time_zone>] )
```

Note

The date and time expression version of TIMESTAMP\_FROM\_PARTS is only valid when the [TIMESTAMP\_TYPE\_MAPPING](/sql-reference/parameters#label-timestamp-type-mapping) session parameter is set to TIMESTAMP\_NTZ.

## Arguments

**Required:**

`year`
:   An integer expression to use as a year for building a timestamp.

`month`
:   An integer expression to use as a month for building a timestamp, with January represented as `1`, and December as `12`.

`day`
:   An integer expression to use as a day for building a timestamp, usually in the `1`-`31` range.

`hour`
:   An integer expression to use as an hour for building a timestamp, usually in the `0`-`23` range.

`minute`
:   An integer expression to use as a minute for building a timestamp, usually in the `0`-`59` range.

`second`
:   An integer expression to use as a second for building a timestamp, usually in the `0`-`59` range.

`date_expr` , `time_expr`
:   Specifies the date and time expressions to use for building a timestamp where `date_expr` provides the year, month, and day for the timestamp and `time_expr` provides the hour,
    minute, second, and nanoseconds within the day. Only valid for:

    - TIMESTAMP\_FROM\_PARTS (when the [TIMESTAMP\_TYPE\_MAPPING](/sql-reference/parameters#label-timestamp-type-mapping) session parameter is set to TIMESTAMP\_NTZ)
    - TIMESTAMP\_NTZ\_FROM\_PARTS

**Optional:**

`nanoseconds`
:   An integer expression to use as a nanosecond for building a timestamp, usually in the `0`-`999999999` range.

`time_zone`
:   A string expression to use as a time zone for building a timestamp (e.g. `America/Los_Angeles`). Only valid for:

    - TIMESTAMP\_FROM\_PARTS (when the [TIMESTAMP\_TYPE\_MAPPING](/sql-reference/parameters#label-timestamp-type-mapping) session parameter is set to TIMESTAMP\_TZ)
    - TIMESTAMP\_TZ\_FROM\_PARTS

## Usage notes

- TIMESTAMP\_FROM\_PARTS variations are typically used to handle values in the “normal” value ranges (e.g. months `1`-`12`, days `1`-`31`, hours `0`-`23`, etc.); however, they can also
  handle values from outside these ranges. This allows choosing the Nth day in a year or Nth second in a day, which can be useful for simplifying some computations.
- TIMESTAMP\_FROM\_PARTS is equivalent to the variation specified by the [TIMESTAMP\_TYPE\_MAPPING](/sql-reference/parameters#label-timestamp-type-mapping) session parameter (default is TIMESTAMP\_NTZ).

## Examples

Set the session variables that control output format and time zone:

> Copy code
>
> ```
> ALTER SESSION SET TIMESTAMP_OUTPUT_FORMAT='YYYY-MM-DD HH24:MI:SS.FF9 TZH:TZM';
> ALTER SESSION SET TIMESTAMP_NTZ_OUTPUT_FORMAT='YYYY-MM-DD HH24:MI:SS.FF9 TZH:TZM';
> ALTER SESSION SET TIMEZONE='America/New_York';
> ```

Using `TIMESTAMP_LTZ_FROM_PARTS`:

> Copy code
>
> ```
> SELECT TIMESTAMP_LTZ_FROM_PARTS(2013, 4, 5, 12, 00, 00);
> +--------------------------------------------------+
> | TIMESTAMP_LTZ_FROM_PARTS(2013, 4, 5, 12, 00, 00) |
> |--------------------------------------------------|
> | 2013-04-05 12:00:00.000000000 -0400              |
> +--------------------------------------------------+
> ```

Using `TIMESTAMP_NTZ_FROM_PARTS`:

> Copy code
>
> ```
> select timestamp_ntz_from_parts(2013, 4, 5, 12, 00, 00, 987654321);
> +-------------------------------------------------------------+
> | TIMESTAMP_NTZ_FROM_PARTS(2013, 4, 5, 12, 00, 00, 987654321) |
> |-------------------------------------------------------------|
> | 2013-04-05 12:00:00.987654321                               |
> +-------------------------------------------------------------+
> ```

Using `TIMESTAMP_NTZ_FROM_PARTS` with a date and time rather than with
year, month, day, hour, etc.:

> Copy code
>
> ```
> select timestamp_ntz_from_parts(to_date('2013-04-05'), to_time('12:00:00'));
> +----------------------------------------------------------------------+
> | TIMESTAMP_NTZ_FROM_PARTS(TO_DATE('2013-04-05'), TO_TIME('12:00:00')) |
> |----------------------------------------------------------------------|
> | 2013-04-05 12:00:00.000000000                                        |
> +----------------------------------------------------------------------+
> ```

Using `TIMESTAMP_TZ_FROM_PARTS` with a session-default time zone (‘America/New\_York’/-0400):

> Copy code
>
> ```
> select timestamp_tz_from_parts(2013, 4, 5, 12, 00, 00);
> +-------------------------------------------------+
> | TIMESTAMP_TZ_FROM_PARTS(2013, 4, 5, 12, 00, 00) |
> |-------------------------------------------------|
> | 2013-04-05 12:00:00.000000000 -0400             |
> +-------------------------------------------------+
> ```

Using `TIMESTAMP_TZ_FROM_PARTS` with a specified time zone (‘America/Los\_Angeles’/-0700); note also the use of 0 as the nanoseconds argument:

> Copy code
>
> ```
> select timestamp_tz_from_parts(2013, 4, 5, 12, 00, 00, 0, 'America/Los_Angeles');
> +---------------------------------------------------------------------------+
> | TIMESTAMP_TZ_FROM_PARTS(2013, 4, 5, 12, 00, 00, 0, 'AMERICA/LOS_ANGELES') |
> |---------------------------------------------------------------------------|
> | 2013-04-05 12:00:00.000000000 -0700                                       |
> +---------------------------------------------------------------------------+
> ```

Handling values outside normal ranges (subtracting 1 hour by specifying -3600 seconds):

> Copy code
>
> ```
> select timestamp_from_parts(2013, 4, 5, 12, 0, -3600);
> +------------------------------------------------+
> | TIMESTAMP_FROM_PARTS(2013, 4, 5, 12, 0, -3600) |
> |------------------------------------------------|
> | 2013-04-05 11:00:00.000000000                  |
> +------------------------------------------------+
> ```
