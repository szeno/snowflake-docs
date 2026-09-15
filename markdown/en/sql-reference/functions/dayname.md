Categories:
:   [Date & time functions](/sql-reference/functions-date-time)

# DAYNAME

Extracts the three-letter day-of-week name from the specified date or timestamp.

Note

To return the full name for the day of the week instead of the three-letter day-of-week name,
you can use the EXTRACT function, the DECODE function, and the `dayofweek` part. See
[EXTRACT](/sql-reference/functions/extract) for an example.

## Syntax

Copy code

```
DAYNAME( <date_or_timestamp_expr> )
```

## Arguments

`date_or_timestamp_expr`
:   A date or a timestamp, or an expression that can be evaluated to a date or a timestamp.

## Returns

Returns a value of VARCHAR data type.

## Examples

Use the [TO\_DATE](/sql-reference/functions/to_date) function to get the abbreviation for the day of the week of April 1, 2024:

Copy code

```
SELECT DAYNAME(TO_DATE('2024-04-01')) AS DAY;
```

```
+-----+
| DAY |
|-----|
| Mon |
+-----+
```

Use the [TO\_TIMESTAMP\_NTZ](/sql-reference/functions/to_timestamp) function to get the abbreviation for the day of the week of April 2, 2024:

Copy code

```
SELECT DAYNAME(TO_TIMESTAMP_NTZ('2024-04-02 10:00')) AS DAY;
```

```
+-----+
| DAY |
|-----|
| Tue |
+-----+
```

Get the abbreviation for the day of the week for each day from January 1, 2024, to January 8, 2024:

Copy code

```
CREATE OR REPLACE TABLE dates (d DATE);
```

Copy code

```
INSERT INTO dates (d) VALUES 
  ('2024-01-01'::DATE),
  ('2024-01-02'::DATE),
  ('2024-01-03'::DATE),
  ('2024-01-04'::DATE),
  ('2024-01-05'::DATE),
  ('2024-01-06'::DATE),
  ('2024-01-07'::DATE),
  ('2024-01-08'::DATE);
```

Copy code

```
SELECT d, DAYNAME(d) 
  FROM dates
  ORDER BY d;
```

```
+------------+------------+
| D          | DAYNAME(D) |
|------------+------------|
| 2024-01-01 | Mon        |
| 2024-01-02 | Tue        |
| 2024-01-03 | Wed        |
| 2024-01-04 | Thu        |
| 2024-01-05 | Fri        |
| 2024-01-06 | Sat        |
| 2024-01-07 | Sun        |
| 2024-01-08 | Mon        |
+------------+------------+
```
