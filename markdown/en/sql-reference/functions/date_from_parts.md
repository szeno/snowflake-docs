Categories:
:   [Date & time functions](/sql-reference/functions-date-time)

# DATE\_FROM\_PARTS

Creates a date from individual numeric components that represent the year,
month, and day of the month.

Aliases:
:   DATEFROMPARTS

## Syntax

Copy code

```
DATE_FROM_PARTS( <year>, <month>, <day> )
```

## Arguments

`year`
:   The integer expression to use as a year for building a date.

`month`
:   The integer expression to use as a month for building a date, with
    January represented as 1, and December as 12.

`day`
:   The integer expression to use as a day for building a date, usually in
    the 1-31 range.

## Usage notes

DATE\_FROM\_PARTS is typically used to handle values in “normal” ranges
(e.g. months 1-12, days 1-31), but it also handles values from outside these
ranges. This allows, for example, choosing the N-th day in a year, which can
be used to simplify some computations.

Year, month, and day values can be negative (e.g. to calculate a date N months
prior to a specific date). The behavior of negative numbers is not entirely
intuitive; see the Examples section for details.

## Examples

Components in normal ranges:

> Copy code
>
> ```
> SELECT DATE_FROM_PARTS(1977, 8, 7);
> +-----------------------------+
> | DATE_FROM_PARTS(1977, 8, 7) |
> |-----------------------------|
> | 1977-08-07                  |
> +-----------------------------+
> ```

Components outside normal ranges:

> - 100th day (from January 1, 2010)
> - 24 months (from January 1, 2010)
>
> Copy code
>
> ```
> SELECT DATE_FROM_PARTS(2010, 1, 100), DATE_FROM_PARTS(2010, 1 + 24, 1);
> +-------------------------------+----------------------------------+
> | DATE_FROM_PARTS(2010, 1, 100) | DATE_FROM_PARTS(2010, 1 + 24, 1) |
> |-------------------------------+----------------------------------|
> | 2010-04-10                    | 2012-01-01                       |
> +-------------------------------+----------------------------------+
> ```

Components with zero or negative numbers:

> Copy code
>
> ```
> SELECT DATE_FROM_PARTS(2004, 1, 1),   -- January 1, 2004, as expected.
>        DATE_FROM_PARTS(2004, 0, 1),   -- This is one month prior to DATE_FROM_PARTS(2004, 1, 1), so it's December 1, 2003.
>                                       -- This is NOT a synonym for January 1, 2004.
>        DATE_FROM_PARTS(2004, -1, 1)   -- This is two months (not one month) before DATE_FROM_PARTS(2004, 1, 1), so it's November 1, 2003.
>        ;
> +-----------------------------+-----------------------------+------------------------------+
> | DATE_FROM_PARTS(2004, 1, 1) | DATE_FROM_PARTS(2004, 0, 1) | DATE_FROM_PARTS(2004, -1, 1) |
> |-----------------------------+-----------------------------+------------------------------|
> | 2004-01-01                  | 2003-12-01                  | 2003-11-01                   |
> +-----------------------------+-----------------------------+------------------------------+
> ```
>
> Copy code
>
> ```
> SELECT DATE_FROM_PARTS(2004, 2, 1),   -- February 1, 2004, as expected.
>        DATE_FROM_PARTS(2004, 2, 0),   -- This is one day prior to DATE_FROM_PARTS(2004, 2, 1), so it's January 31, 2004.
>        DATE_FROM_PARTS(2004, 2, -1);  -- Two days prior to DATE_FROM_PARTS(2004, 2, 1) so it's January 30, 2004.
> +-----------------------------+-----------------------------+------------------------------+
> | DATE_FROM_PARTS(2004, 2, 1) | DATE_FROM_PARTS(2004, 2, 0) | DATE_FROM_PARTS(2004, 2, -1) |
> |-----------------------------+-----------------------------+------------------------------|
> | 2004-02-01                  | 2004-01-31                  | 2004-01-30                   |
> +-----------------------------+-----------------------------+------------------------------+
> ```
>
> Copy code
>
> ```
> SELECT DATE_FROM_PARTS(2004, -1, -1);  -- Two months and two days prior to DATE_FROM_PARTS(2004, 1, 1), so it's October 30, 2003.
> +-------------------------------+
> | DATE_FROM_PARTS(2004, -1, -1) |
> |-------------------------------|
> | 2003-10-30                    |
> +-------------------------------+
> ```
