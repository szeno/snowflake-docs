Categories:
:   [Window functions](/sql-reference/functions-window) (General)

# CONDITIONAL\_CHANGE\_EVENT

Returns a window event number for each row within a window partition when the value of the argument `expr1` in
the current row is different from the value of `expr1` in the previous row. The window event number starts
from 0 and is incremented by 1 to indicate the number of changes so far within that window.

## Syntax

Copy code

```
CONDITIONAL_CHANGE_EVENT( <expr1> ) OVER ( [ PARTITION BY <expr2> ] ORDER BY <expr3> [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] )
```

## Arguments

`expr1`
:   This is an expression that gets compared with the expression of the previous row.

`expr2`
:   This is the optional expression to partition by.

`expr3`
:   This is the expression to order by within each partition.

## Usage notes

- The expression `CONDITIONAL_CHANGE_EVENT (expr1) OVER (window_frame)` is calculated as:

  `CONDITIONAL_TRUE_EVENT( <expr1> != LAG(<expr1>) OVER(window_frame)) OVER(window_frame)`

  For more information about CONDITIONAL\_TRUE\_EVENT, see [CONDITIONAL\_TRUE\_EVENT](/sql-reference/functions/conditional_true_event).

## Examples

This shows how to detect the number of times that the power failed and was
turned back on (i.e. the number of times that the voltage dropped to 0 or
was restored). (This example assumes that sampling the voltage every 15
minutes is sufficient. Because power failures can last less than 15 minutes,
you’d typically want more frequent samples, or you’d want to treat the
query results as an approximation.)

Create and load the table:

Copy code

```
CREATE TABLE voltage_readings (
  site_id INTEGER,  -- which refrigerator the measurement was taken in
  ts TIMESTAMP,     -- the time at which the temperature was measured
  voltage FLOAT
  );

INSERT INTO voltage_readings (site_id, ts, voltage) VALUES
  (1, '2019-10-30 13:00:00', 120),
  (1, '2019-10-30 13:15:00', 120),
  (1, '2019-10-30 13:30:00',   0),
  (1, '2019-10-30 13:45:00',   0),
  (1, '2019-10-30 14:00:00',   0),
  (1, '2019-10-30 14:15:00',   0),
  (1, '2019-10-30 14:30:00', 120)
  ;
```

This shows the samples for which the voltage was zero, whether or not those
zero-volt events were part of the same power failure or different power failures.

Copy code

```
SELECT site_id, ts, voltage
  FROM voltage_readings
  WHERE voltage = 0
  ORDER BY ts;
```

```
+---------+-------------------------+---------+
| SITE_ID | TS                      | VOLTAGE |
|---------+-------------------------+---------|
|       1 | 2019-10-30 13:30:00.000 |       0 |
|       1 | 2019-10-30 13:45:00.000 |       0 |
|       1 | 2019-10-30 14:00:00.000 |       0 |
|       1 | 2019-10-30 14:15:00.000 |       0 |
+---------+-------------------------+---------+
```

This shows the samples, along with a column indicating whether the voltage
changed:

Copy code

```
SELECT
    site_id,
    ts,
    voltage,
    CONDITIONAL_CHANGE_EVENT(voltage = 0) OVER (ORDER BY ts) AS power_changes
  FROM voltage_readings;
```

```
+---------+-------------------------+---------+---------------+
| SITE_ID | TS                      | VOLTAGE | POWER_CHANGES |
|---------+-------------------------+---------+---------------|
|       1 | 2019-10-30 13:00:00.000 |     120 |             0 |
|       1 | 2019-10-30 13:15:00.000 |     120 |             0 |
|       1 | 2019-10-30 13:30:00.000 |       0 |             1 |
|       1 | 2019-10-30 13:45:00.000 |       0 |             1 |
|       1 | 2019-10-30 14:00:00.000 |       0 |             1 |
|       1 | 2019-10-30 14:15:00.000 |       0 |             1 |
|       1 | 2019-10-30 14:30:00.000 |     120 |             2 |
+---------+-------------------------+---------+---------------+
```

This shows the times that the power stopped and restarted:

Copy code

```
WITH power_change_events AS (
  SELECT
      site_id,
      ts,
      voltage,
      CONDITIONAL_CHANGE_EVENT(voltage = 0) OVER (ORDER BY ts) AS power_changes
    FROM voltage_readings
)
SELECT
    site_id,
    MIN(ts),
    voltage,
    power_changes
  FROM power_change_events
  GROUP BY site_id, power_changes, voltage
  ORDER BY 2;
```

```
+---------+-------------------------+---------+---------------+
| SITE_ID | MIN(TS)                 | VOLTAGE | POWER_CHANGES |
|---------+-------------------------+---------+---------------|
|       1 | 2019-10-30 13:00:00.000 |     120 |             0 |
|       1 | 2019-10-30 13:30:00.000 |       0 |             1 |
|       1 | 2019-10-30 14:30:00.000 |     120 |             2 |
+---------+-------------------------+---------+---------------+
```

This shows how many times the power stopped and restarted:

Copy code

```
WITH power_change_events AS (
  SELECT
      site_id,
      CONDITIONAL_CHANGE_EVENT(voltage = 0) OVER (ORDER BY ts) AS power_changes
    FROM voltage_readings
)
SELECT MAX(power_changes)
  FROM power_change_events
  GROUP BY site_id;
```

```
+--------------------+
| MAX(POWER_CHANGES) |
|--------------------|
|                  2 |
+--------------------+
```

This example illustrates that:

- The change number within a partition changes each time the specified value changes.
- NULL values are not considered a new or changed value.
- The change count starts over at 0 for each partition.

Create and load the table:

Copy code

```
CREATE TABLE table1 (province VARCHAR, o_col INTEGER, o2_col INTEGER);

INSERT INTO table1 (province, o_col, o2_col) VALUES
  ('Alberta', 0, 10),
  ('Alberta', 0, 10),
  ('Alberta', 13, 10),
  ('Alberta', 13, 11),
  ('Alberta', 14, 11),
  ('Alberta', 15, 12),
  ('Alberta', NULL, NULL),
  ('Manitoba', 30, 30);
```

Query the table:

Copy code

```
SELECT province, o_col,
    CONDITIONAL_CHANGE_EVENT(o_col)
      OVER (PARTITION BY province ORDER BY o_col)
        AS change_event
  FROM table1
  ORDER BY province, o_col;
```

```
+----------+-------+--------------+
| PROVINCE | O_COL | CHANGE_EVENT |
|----------+-------+--------------|
| Alberta  |     0 |            0 |
| Alberta  |     0 |            0 |
| Alberta  |    13 |            1 |
| Alberta  |    13 |            1 |
| Alberta  |    14 |            2 |
| Alberta  |    15 |            3 |
| Alberta  |  NULL |            3 |
| Manitoba |    30 |            0 |
+----------+-------+--------------+
```

The next example shows that:

- `expr1` can be an expression other than a column. This query uses the expression `o_col < 15`,
  and the output of the query shows when the value in o\_col changes from a value less than 15 to
  a value greater than or equal to 15.
- `expr3` does not need to match `expr1`. In other words, the expression in the ORDER BY
  sub-clause of the OVER clause does not need to match the expression in the CONDITIONAL\_CHANGE\_EVENT function.

Copy code

```
SELECT province, o_col,
    'o_col < 15' AS condition,
    CONDITIONAL_CHANGE_EVENT(o_col)
      OVER (PARTITION BY province ORDER BY o_col)
        AS change_event,
    CONDITIONAL_CHANGE_EVENT(o_col < 15)
      OVER (PARTITION BY province ORDER BY o_col)
        AS change_event_2
  FROM table1
  ORDER BY province, o_col;
```

```
+----------+-------+------------+--------------+----------------+
| PROVINCE | O_COL | CONDITION  | CHANGE_EVENT | CHANGE_EVENT_2 |
|----------+-------+------------+--------------+----------------|
| Alberta  |     0 | o_col < 15 |            0 |              0 |
| Alberta  |     0 | o_col < 15 |            0 |              0 |
| Alberta  |    13 | o_col < 15 |            1 |              0 |
| Alberta  |    13 | o_col < 15 |            1 |              0 |
| Alberta  |    14 | o_col < 15 |            2 |              0 |
| Alberta  |    15 | o_col < 15 |            3 |              1 |
| Alberta  |  NULL | o_col < 15 |            3 |              1 |
| Manitoba |    30 | o_col < 15 |            0 |              0 |
+----------+-------+------------+--------------+----------------+
```

The next example compares CONDITIONAL\_CHANGE\_EVENT and CONDITIONAL\_TRUE\_EVENT:

Copy code

```
SELECT province, o_col,
    CONDITIONAL_CHANGE_EVENT(o_col)
      OVER (PARTITION BY province ORDER BY o_col)
        AS change_event,
    CONDITIONAL_TRUE_EVENT(o_col)
      OVER (PARTITION BY province ORDER BY o_col)
        AS true_event
  FROM table1
  ORDER BY province, o_col;
```

```
+----------+-------+--------------+------------+
| PROVINCE | O_COL | CHANGE_EVENT | TRUE_EVENT |
|----------+-------+--------------+------------|
| Alberta  |     0 |            0 |          0 |
| Alberta  |     0 |            0 |          0 |
| Alberta  |    13 |            1 |          1 |
| Alberta  |    13 |            1 |          2 |
| Alberta  |    14 |            2 |          3 |
| Alberta  |    15 |            3 |          4 |
| Alberta  |  NULL |            3 |          4 |
| Manitoba |    30 |            0 |          1 |
+----------+-------+--------------+------------+
```

This example also compares CONDITIONAL\_CHANGE\_EVENT and CONDITIONAL\_TRUE\_EVENT:

Copy code

```
CREATE TABLE borrowers (
  name VARCHAR,
  status_date DATE,
  late_balance NUMERIC(11, 2),
  thirty_day_late_balance NUMERIC(11, 2)
  );

INSERT INTO borrowers (name, status_date, late_balance, thirty_day_late_balance) VALUES
  -- Pays late frequently, but catches back up rather than falling further behind.
  ('Geoffrey Flake', '2018-01-01'::DATE,    0.0,    0.0),
  ('Geoffrey Flake', '2018-02-01'::DATE, 1000.0,    0.0),
  ('Geoffrey Flake', '2018-03-01'::DATE, 2000.0, 1000.0),
  ('Geoffrey Flake', '2018-04-01'::DATE,    0.0,    0.0),
  ('Geoffrey Flake', '2018-05-01'::DATE, 1000.0,    0.0),
  ('Geoffrey Flake', '2018-06-01'::DATE, 2000.0, 1000.0),
  ('Geoffrey Flake', '2018-07-01'::DATE,    0.0,    0.0),
  ('Geoffrey Flake', '2018-08-01'::DATE,    0.0,    0.0),
  -- Keeps falling further behind.
  ('Cy Dismal', '2018-01-01'::DATE,    0.0,    0.0),
  ('Cy Dismal', '2018-02-01'::DATE,    0.0,    0.0),
  ('Cy Dismal', '2018-03-01'::DATE, 1000.0,    0.0),
  ('Cy Dismal', '2018-04-01'::DATE, 2000.0, 1000.0),
  ('Cy Dismal', '2018-05-01'::DATE, 3000.0, 2000.0),
  ('Cy Dismal', '2018-06-01'::DATE, 4000.0, 3000.0),
  ('Cy Dismal', '2018-07-01'::DATE, 5000.0, 4000.0),
  ('Cy Dismal', '2018-08-01'::DATE, 6000.0, 5000.0),
  -- Fell behind and isn't catching up, but isn't falling further behind.
  ('Leslie Safer', '2018-01-01'::DATE,    0.0,    0.0),
  ('Leslie Safer', '2018-02-01'::DATE,    0.0,    0.0),
  ('Leslie Safer', '2018-03-01'::DATE, 1000.0, 1000.0),
  ('Leslie Safer', '2018-04-01'::DATE, 2000.0, 1000.0),
  ('Leslie Safer', '2018-05-01'::DATE, 2000.0, 1000.0),
  ('Leslie Safer', '2018-06-01'::DATE, 2000.0, 1000.0),
  ('Leslie Safer', '2018-07-01'::DATE, 2000.0, 1000.0),
  ('Leslie Safer', '2018-08-01'::DATE, 2000.0, 1000.0),
  -- Always pays on time and in full.
  ('Ida Idyll', '2018-01-01'::DATE,    0.0,    0.0),
  ('Ida Idyll', '2018-02-01'::DATE,    0.0,    0.0),
  ('Ida Idyll', '2018-03-01'::DATE,    0.0,    0.0),
  ('Ida Idyll', '2018-04-01'::DATE,    0.0,    0.0),
  ('Ida Idyll', '2018-05-01'::DATE,    0.0,    0.0),
  ('Ida Idyll', '2018-06-01'::DATE,    0.0,    0.0),
  ('Ida Idyll', '2018-07-01'::DATE,    0.0,    0.0),
  ('Ida Idyll', '2018-08-01'::DATE,    0.0,    0.0)
  ;
```

Copy code

```
SELECT name, status_date, late_balance AS "OVERDUE",
    thirty_day_late_balance AS "30 DAYS OVERDUE",
    CONDITIONAL_CHANGE_EVENT(thirty_day_late_balance)
      OVER (PARTITION BY name ORDER BY status_date) AS change_event_cnt,
    CONDITIONAL_TRUE_EVENT(thirty_day_late_balance)
      OVER (PARTITION BY name ORDER BY status_date) AS true_cnt
  FROM borrowers
  ORDER BY name, status_date;
```

```
+----------------+-------------+---------+-----------------+------------------+----------+
| NAME           | STATUS_DATE | OVERDUE | 30 DAYS OVERDUE | CHANGE_EVENT_CNT | TRUE_CNT |
|----------------+-------------+---------+-----------------+------------------+----------|
| Cy Dismal      | 2018-01-01  |    0.00 |            0.00 |                0 |        0 |
| Cy Dismal      | 2018-02-01  |    0.00 |            0.00 |                0 |        0 |
| Cy Dismal      | 2018-03-01  | 1000.00 |            0.00 |                0 |        0 |
| Cy Dismal      | 2018-04-01  | 2000.00 |         1000.00 |                1 |        1 |
| Cy Dismal      | 2018-05-01  | 3000.00 |         2000.00 |                2 |        2 |
| Cy Dismal      | 2018-06-01  | 4000.00 |         3000.00 |                3 |        3 |
| Cy Dismal      | 2018-07-01  | 5000.00 |         4000.00 |                4 |        4 |
| Cy Dismal      | 2018-08-01  | 6000.00 |         5000.00 |                5 |        5 |
| Geoffrey Flake | 2018-01-01  |    0.00 |            0.00 |                0 |        0 |
| Geoffrey Flake | 2018-02-01  | 1000.00 |            0.00 |                0 |        0 |
| Geoffrey Flake | 2018-03-01  | 2000.00 |         1000.00 |                1 |        1 |
| Geoffrey Flake | 2018-04-01  |    0.00 |            0.00 |                2 |        1 |
| Geoffrey Flake | 2018-05-01  | 1000.00 |            0.00 |                2 |        1 |
| Geoffrey Flake | 2018-06-01  | 2000.00 |         1000.00 |                3 |        2 |
| Geoffrey Flake | 2018-07-01  |    0.00 |            0.00 |                4 |        2 |
| Geoffrey Flake | 2018-08-01  |    0.00 |            0.00 |                4 |        2 |
| Ida Idyll      | 2018-01-01  |    0.00 |            0.00 |                0 |        0 |
| Ida Idyll      | 2018-02-01  |    0.00 |            0.00 |                0 |        0 |
| Ida Idyll      | 2018-03-01  |    0.00 |            0.00 |                0 |        0 |
| Ida Idyll      | 2018-04-01  |    0.00 |            0.00 |                0 |        0 |
| Ida Idyll      | 2018-05-01  |    0.00 |            0.00 |                0 |        0 |
| Ida Idyll      | 2018-06-01  |    0.00 |            0.00 |                0 |        0 |
| Ida Idyll      | 2018-07-01  |    0.00 |            0.00 |                0 |        0 |
| Ida Idyll      | 2018-08-01  |    0.00 |            0.00 |                0 |        0 |
| Leslie Safer   | 2018-01-01  |    0.00 |            0.00 |                0 |        0 |
| Leslie Safer   | 2018-02-01  |    0.00 |            0.00 |                0 |        0 |
| Leslie Safer   | 2018-03-01  | 1000.00 |         1000.00 |                1 |        1 |
| Leslie Safer   | 2018-04-01  | 2000.00 |         1000.00 |                1 |        2 |
| Leslie Safer   | 2018-05-01  | 2000.00 |         1000.00 |                1 |        3 |
| Leslie Safer   | 2018-06-01  | 2000.00 |         1000.00 |                1 |        4 |
| Leslie Safer   | 2018-07-01  | 2000.00 |         1000.00 |                1 |        5 |
| Leslie Safer   | 2018-08-01  | 2000.00 |         1000.00 |                1 |        6 |
+----------------+-------------+---------+-----------------+------------------+----------+
```

Here is a more extensive example:

Copy code

```
CREATE OR REPLACE TABLE tbl
  (p INT, o INT, i INT, r INT, s VARCHAR(100));

INSERT INTO tbl VALUES
  (100, 1, 1, 70, 'seventy'),
  (100, 2, 2, 30, 'thirty'),
  (100, 3, 3, 40, 'fourty'),
  (100, 4, NULL, 90, 'ninety'),
  (100, 5, 5, 50, 'fifty'),
  (100, 6, 6, 30, 'thirty'),
  (200, 7, 7, 40, 'fourty'),
  (200, 8, NULL, NULL, 'n_u_l_l'),
  (200, 9, NULL, NULL, 'n_u_l_l'),
  (200, 10, 10, 20, 'twenty'),
  (200, 11, NULL, 90, 'ninety'),
  (300, 12, 12, 30, 'thirty'),
  (400, 13, NULL, 20, 'twenty');
```

Copy code

```
SELECT *
  FROM tbl
  ORDER BY p, o, i;
```

```
+-----+----+--------+--------+---------+
|  P  | O  |   I    |   R    |    S    |
+-----+----+--------+--------+---------+
| 100 | 1  | 1      | 70     | seventy |
| 100 | 2  | 2      | 30     | thirty  |
| 100 | 3  | 3      | 40     | fourty  |
| 100 | 4  | [NULL] | 90     | ninety  |
| 100 | 5  | 5      | 50     | fifty   |
| 100 | 6  | 6      | 30     | thirty  |
| 200 | 7  | 7      | 40     | fourty  |
| 200 | 8  | [NULL] | [NULL] | n_u_l_l |
| 200 | 9  | [NULL] | [NULL] | n_u_l_l |
| 200 | 10 | 10     | 20     | twenty  |
| 200 | 11 | [NULL] | 90     | ninety  |
| 300 | 12 | 12     | 30     | thirty  |
| 400 | 13 | [NULL] | 20     | twenty  |
+-----+----+--------+--------+---------+
```

Copy code

```
SELECT p, o,
    CONDITIONAL_CHANGE_EVENT(o) OVER (PARTITION BY p ORDER BY o)
  FROM tbl
  ORDER BY p, o;
```

```
+-----+----+--------------------------------------------------------------+
|   P |  O | CONDITIONAL_CHANGE_EVENT(O) OVER (PARTITION BY P ORDER BY O) |
|-----+----+--------------------------------------------------------------|
| 100 |  1 |                                                            0 |
| 100 |  2 |                                                            1 |
| 100 |  3 |                                                            2 |
| 100 |  4 |                                                            3 |
| 100 |  5 |                                                            4 |
| 100 |  6 |                                                            5 |
| 200 |  7 |                                                            0 |
| 200 |  8 |                                                            1 |
| 200 |  9 |                                                            2 |
| 200 | 10 |                                                            3 |
| 200 | 11 |                                                            4 |
| 300 | 12 |                                                            0 |
| 400 | 13 |                                                            0 |
+-----+----+--------------------------------------------------------------+
```
