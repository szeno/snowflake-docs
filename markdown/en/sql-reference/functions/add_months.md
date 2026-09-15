Categories:
:   [Date & time functions](/sql-reference/functions-date-time)

# ADD\_MONTHS

Adds or subtracts a specified number of months to a date or timestamp, preserving the end-of-month information.

## Syntax

Copy code

```
ADD_MONTHS( <date_or_timestamp_expr> , <num_months_expr> )
```

## Arguments

**Required:**

`date_or_timestamp_expr`
:   This is the date or timestamp expression to which you want to add
    a specified number of months.

`num_months_expr`
:   This is the number of months you want to add. This should be an
    integer. It may be positive or negative. If the value is a
    non-integer numeric value (for example, FLOAT) the value will be
    rounded to the nearest integer.

## Returns

The data type of the returned value is the same as the data type of the
first parameter. For example, if the input is a `DATE`, then the
output is a `DATE`. If the input is a `TIMESTAMP_NTZ`, then the
output is a `TIMESTAMP_NTZ`.

## Usage notes

- ADD\_MONTHS returns slightly different results than [DATEADD](/sql-reference/functions/dateadd) used with a `MONTH` component:

  - For both ADD\_MONTHS and [DATEADD](/sql-reference/functions/dateadd), if the result month has fewer days than the original day, the result day of the month is the last day of the result month.
  - For ADD\_MONTHS only, if the original day is the last day of the month, the result day of month will be the last day of the result month.
- `num_months_expr` can be a positive or negative integer to either add or subtract months, respectively.

## Examples

Add 2 months to a date and cast the date to a timestamp with no time zone:

> Copy code
>
> ```
> SELECT ADD_MONTHS('2016-05-15'::timestamp_ntz, 2) AS RESULT;
> +-------------------------+
> | RESULT                  |
> |-------------------------|
> | 2016-07-15 00:00:00.000 |
> +-------------------------+
> ```

Demonstrate preservation of end-of-month information:

> - Add one month to the last day of February 2016 (a leap year).
> - Subtract one month from the last day of May 2016.
>
>   > Copy code
>   >
>   > ```
>   > SELECT ADD_MONTHS('2016-02-29'::date, 1) AS RESULT;
>   > +------------+
>   > | RESULT     |
>   > |------------|
>   > | 2016-03-31 |
>   > +------------+
>   > ```
>   >
>   > Copy code
>   >
>   > ```
>   > SELECT ADD_MONTHS('2016-05-31'::date, -1) AS RESULT;
>   > +------------+
>   > | RESULT     |
>   > |------------|
>   > | 2016-04-30 |
>   > +------------+
>   > ```
