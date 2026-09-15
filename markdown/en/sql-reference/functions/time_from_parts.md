Categories:
:   [Date & time functions](/sql-reference/functions-date-time)

# TIME\_FROM\_PARTS

Creates a time from individual numeric components.

Aliases:
:   TIMEFROMPARTS

## Syntax

Copy code

```
TIME_FROM_PARTS( <hour>, <minute>, <second> [, <nanoseconds>] )
```

## Arguments

**Required:**

`hour`
:   An integer expression to use as an hour for building a time,
    usually in the 0-23 range.

`minute`
:   An integer expression to use as a minute for building a time,
    usually in the 0-59 range.

`second`
:   An integer expression to use as a second for building a time,
    usually in the 0-59 range.

**Optional:**

`nanoseconds`
:   A 9-digit integer expression to use as a nanosecond for building
    a time.

## Usage notes

TIME\_FROM\_PARTS is typically used to handle values in “normal” ranges
(e.g. hours 0-23, minutes 0-59), but it also handles values from outside
these ranges. This allows, for example, choosing the N-th minute in a day,
which can be used to simplify some computations.

## Examples

Copy code

```
ALTER SESSION SET TIME_OUTPUT_FORMAT='HH24:MI:SS.FF9';
```

Components in normal ranges:

> Copy code
>
> ```
> select time_from_parts(12, 34, 56, 987654321);
>
> ----------------------------------------+
>  TIME_FROM_PARTS(12, 34, 56, 987654321) |
> ----------------------------------------+
>  12:34:56.987654321                     |
> ----------------------------------------+
> ```

Components outside normal ranges:

- 100th minute (from midnight)
- 12345 seconds (from noon)

  Copy code

  ```
  select time_from_parts(0, 100, 0), time_from_parts(12, 0, 12345);

  ----------------------------+-------------------------------+
   TIME_FROM_PARTS(0, 100, 0) | TIME_FROM_PARTS(12, 0, 12345) |
  ----------------------------+-------------------------------+
   01:40:00.000000000         | 15:25:45.000000000            |
  ----------------------------+-------------------------------+
  ```
