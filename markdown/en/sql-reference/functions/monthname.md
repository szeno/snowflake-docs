Categories:
:   [Date & time functions](/sql-reference/functions-date-time)

# MONTHNAME

Returns the three-letter month name for the specified date or timestamp.

## Syntax

Copy code

```
MONTHNAME( <date_or_timestamp_expr> )
```

## Arguments

`date_or_timestamp_expr`
:   A date or a timestamp, or an expression that can be evaluated to a date or a timestamp.

## Returns

This function returns a value of type VARCHAR.

## Usage notes

To return the full month name instead of the three-letter month name, you can use the
[TO\_CHAR](/sql-reference/functions/to_char) function with the [TO\_DATE](/sql-reference/functions/to_date) or [TO\_TIMESTAMP](/sql-reference/functions/to_timestamp)
function. The following example uses the TO\_CHAR and TO\_DATE functions to return the full month name for
the date `2025-01-01`:

Copy code

```
SELECT TO_CHAR(TO_DATE('2025-01-01'), 'MMMM') AS full_month_name;
```

```
+-----------------+
| FULL_MONTH_NAME |
|-----------------|
| January         |
+-----------------+
```

## Examples

The following examples use the MONTHNAME function.

Return the three-letter month name of a date:

Copy code

```
SELECT MONTHNAME(TO_DATE('2025-01-01')) AS month;
```

```
+-------+
| MONTH |
|-------|
| Jan   |
+-------+
```

Return the three-letter month name of a timestamp:

Copy code

```
SELECT MONTHNAME(TO_TIMESTAMP('2025-04-03 10:00')) AS month;
```

```
+-------+
| MONTH |
|-------|
| Apr   |
+-------+
```

Return the three-letter month name of DATE values in a column.

First, create a table with a DATE column and insert various DATE values:

Copy code

```
CREATE OR REPLACE TABLE monthname_function_demo (d DATE);

INSERT INTO monthname_function_demo (d) VALUES
  ('2024-01-01'::DATE),
  ('2024-02-02'::DATE),
  ('2024-03-03'::DATE),
  ('2024-04-04'::DATE),
  ('2024-05-05'::DATE),
  ('2024-06-06'::DATE),
  ('2024-07-07'::DATE),
  ('2024-08-08'::DATE),
  ('2024-09-09'::DATE),
  ('2024-10-10'::DATE),
  ('2024-11-11'::DATE),
  ('2024-12-12'::DATE);
```

Use the MONTHNAME function in a query to return the three-letter month name of each
value in the `d` column:

Copy code

```
SELECT d,
       MONTHNAME(d) AS month
  FROM monthname_function_demo;
```

```
+------------+-------+
| D          | MONTH |
|------------+-------|
| 2024-01-01 | Jan   |
| 2024-02-02 | Feb   |
| 2024-03-03 | Mar   |
| 2024-04-04 | Apr   |
| 2024-05-05 | May   |
| 2024-06-06 | Jun   |
| 2024-07-07 | Jul   |
| 2024-08-08 | Aug   |
| 2024-09-09 | Sep   |
| 2024-10-10 | Oct   |
| 2024-11-11 | Nov   |
| 2024-12-12 | Dec   |
+------------+-------+
```
