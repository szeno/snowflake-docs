# Window function syntax and usage

Snowflake supports a large number of analytic SQL functions known as *window functions*. The details for each function are documented on individual
reference pages. The purpose of this section is to provide general reference information that applies to some or all window functions, including
detailed syntax for the main components of the OVER clause:

- PARTITION BY clause
- ORDER BY clause
- Window frame syntax

Users who are not familiar with window functions might want to read the conceptual material in [Analyzing data with window functions](/user-guide/functions-window-using).

## Syntax

Copy code

```
<function> ( [ <arguments> ] ) OVER ( [ <windowDefinition> ] )
```

Where:

Copy code

```
windowDefinition ::=

[ PARTITION BY <expr1> [, ...] ]
[ ORDER BY <expr2> [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] [, ...] ]
[ <windowFrameClause> ]
```

Where:

Copy code

```
windowFrameClause ::=

{
    { ROWS | RANGE } UNBOUNDED PRECEDING
  | { ROWS | RANGE } <n> PRECEDING
  | { ROWS | RANGE } CURRENT ROW
  | { ROWS | RANGE } BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  | { ROWS | RANGE } BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
  | { ROWS | RANGE } BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  | { ROWS | RANGE } BETWEEN <n> { PRECEDING | FOLLOWING } AND <n> { PRECEDING | FOLLOWING }
  | { ROWS | RANGE } BETWEEN UNBOUNDED PRECEDING AND <n> { PRECEDING | FOLLOWING }
  | { ROWS | RANGE } BETWEEN <n> { PRECEDING | FOLLOWING } AND UNBOUNDED FOLLOWING
}
```

## Parameters

`OVER( [ windowDefinition ] )`
:   Specifies that the function is being used as a window function and specifies the window over which
    the function operates.
    The OVER clause must contain parentheses, but they may be empty, depending on the requirements of the
    function in question. An empty OVER clause has no partitions and an implied default window frame.

`PARTITION BY expr1`
:   Groups rows into partitions, by product, city, or year, for example. Input rows are grouped by partitions, then the function is
    computed over each partition. The PARTITION BY clause is optional; you can analyze a set of rows as a single partition.

`ORDER BY expr2`
:   Orders rows within each partition, or within the entire set of rows if no partition is specified.
    This ORDER BY clause is distinct from the ORDER BY clause that controls the order of all the rows that are
    returned in the final result of a query. Although the ORDER BY clause is optional for some window functions, it is required for others.
    For example, ranking window functions such as RANK and NTILE require their input data to be in a meaningful order.

    The ORDER BY clause for a window function follows rules similar to those for the main ORDER BY clause in a query,
    with respect to ASC/DESC (ascending/descending) order and NULL handling. For details, see [ORDER BY](/sql-reference/constructs/order-by).

    Note

    The ORDER BY clause for window functions does not support the use of an ordinal position, such as `OVER (PARTITION BY 1 ORDER BY 2)`.
    In this context, `2` is interpreted as the constant `2`; it does not refer to the second column in the query.

    Different functions handle the ORDER BY clause in different ways:

    - Some window functions require an ORDER BY clause.
    - Some window functions prohibit an ORDER BY clause.
    - Some window functions use an ORDER BY clause if one is present, but do not require it.
    - Some window functions apply an implicit window frame to the ORDER BY clause. (For more information, see
      [Usage notes for window frames](#label-window-frames).)

`{ ROWS | RANGE }`
:   Specifies the type or mode of window frame, which defines either a physical number of rows (ROWS) or a logically computed set of rows (RANGE).
    See [Range-based versus row-based window frames](/user-guide/functions-window-using#label-range-and-row-window-frames).

    Both types of frame specify starting and ending points, using either implicit named boundaries or explicit offset values.
    A named boundary is defined with the keywords CURRENT ROW, UNBOUNDED PRECEDING, and UNBOUNDED FOLLOWING. Explicit offsets are
    defined with numbers or intervals (`n PRECEDING` or `n FOLLOWING`).

`{ RANGE BETWEEN n PRECEDING | n FOLLOWING }`
:   Specifies a range-based window frame with explicit offsets.

    RANGE BETWEEN window frames with explicit offsets must have only one ORDER BY expression.
    The following data types are supported for that expression:

    - DATE, TIMESTAMP, TIMESTAMP\_LTZ , TIMESTAMP\_NTZ (DATETIME) , TIMESTAMP\_TZ
    - NUMBER, including INT, FLOAT, and so on

    TIME and other Snowflake data types are not supported when this type of window frame is used. For other window frames, other data types,
    such as VARCHAR, can be used in the ORDER BY expression.

    For RANGE BETWEEN window frames, *n* must be an unsigned constant (a positive numeric value, including 0) or a positive INTERVAL constant:

    - If `expr2` is a numeric data type, `n` must be an unsigned constant.
    - If `expr2` is a TIMESTAMP data type, `n` must be an [INTERVAL constant](/sql-reference/data-types-datetime#label-interval-constants).
      For example: `INTERVAL '12 hours'` or `INTERVAL '3 days'`.
    - If `expr2` is a DATE data type, `n` can be an unsigned constant or an INTERVAL constant, but the start and end of the frame must use the same data type for the `n` value.

    When the ORDER BY expression is ascending (ASC), the syntax `n FOLLOWING` means “rows with values greater than (or later than) *x*,” and
    `n PRECEDING` means “rows with values less than (or earlier than) *x*,” where *x* is the ORDER BY value for the current row. When the ORDER BY expression is descending (DESC), the opposite is true. (The offsets `0 PRECEDING` and `0 FOLLOWING` are equivalent to CURRENT ROW.)

### RANGE BETWEEN limitations

The following subset of window functions support the RANGE BETWEEN syntax with explicit offsets:

> - [COUNT](/sql-reference/functions/count), [SUM](/sql-reference/functions/sum), [MIN](/sql-reference/functions/min),
>   [MAX](/sql-reference/functions/max), [AVG](/sql-reference/functions/avg)
> - [STDDEV, STDDEV\_SAMP](/sql-reference/functions/stddev), [STDDEV\_POP](/sql-reference/functions/stddev_pop) (and aliases)
> - [VARIANCE , VARIANCE\_SAMP](/sql-reference/functions/variance), [VARIANCE\_POP](/sql-reference/functions/variance_pop) (and aliases)
> - [COUNT\_IF](/sql-reference/functions/count_if)
> - [FIRST\_VALUE](/sql-reference/functions/first_value), [LAST\_VALUE](/sql-reference/functions/last_value)
> - [ARRAY\_AGG](/sql-reference/functions/array_agg)

In addition, note that:

- DISTINCT versions of these functions do not support this syntax.
- The following limitations apply when the COUNT window function is used with this syntax.

  - Only one input argument is supported.
  - `COUNT(table.*)` wildcard queries are not supported. For example, you cannot specify:

    Copy code

    ```
    COUNT(t1.*) OVER(ORDER BY col1 RANGE BETWEEN 1 PRECEDING AND 1 FOLLOWING)
    ```
- You cannot specify a frame that results in a logical reversal of the frame start and end positions. For example, the following frames return
  errors because the ending row of the frame precedes the starting row:

  Copy code

  ```
  ORDER BY col1 ASC RANGE BETWEEN 2 PRECEDING AND 4 PRECEDING
  ORDER BY col1 ASC RANGE BETWEEN 2 FOLLOWING AND 2 PRECEDING
  ```

### RANGE BETWEEN behavior when the ORDER BY expression contains NULL values

Note the following behavior when a RANGE BETWEEN window frame is used and the ORDER BY column contains NULL values:

- When the ORDER BY clause specifies NULLS FIRST, rows with NULL in the ORDER BY column are included in UNBOUNDED PRECEDING frames.
- When the ORDER BY clause specifies NULLS LAST, rows with NULL in the ORDER BY column are included in UNBOUNDED FOLLOWING frames.
- Rows with NULL in the ORDER BY column are included in an explicit-offset frame boundary only when the ORDER BY value of the current row is NULL.

See [RANGE BETWEEN examples with NULL values in the ORDER BY clause](#label-range-between-order-by-nulls-examples).

### Correlated columns in window functions

Using correlated columns inside window functions (such as in the PARTITION BY or ORDER BY clauses) is not supported.
This limitation applies when window functions are used in [LATERAL](/sql-reference/constructs/join-lateral)
joins or correlated subqueries, where the window function attempts to reference columns from outer query blocks.

The following example demonstrates this limitation. The query uses [FLATTEN](/sql-reference/functions/flatten) in a lateral join
with the [ROW\_NUMBER](/sql-reference/functions/row_number) window function to process JSON data. When the `completed_on` column (which is
explicitly correlated with the lateral join) is used in the ORDER BY clause of the function, the query returns an error:

Copy code

```
WITH data AS (
  SELECT
    PARSE_JSON('[
                  {"completed_on": "2024-06-03T20:17:08.621001019Z"},
                  {"completed_on": "2024-06-03T18:26:08.691858742Z"},
                  {"completed_on": "2024-06-03T14:43:40.215726239Z"}
                 ]'
               ) d
  )
SELECT
    fields.*
  FROM data,
    LATERAL FLATTEN(d) AS f,
    LATERAL (SELECT
             f.value:completed_on AS completed_on,
             ROW_NUMBER() OVER(ORDER BY f.value:completed_on DESC) rn
            )fields;
```

```
SQL compilation error: Window function [ROW_NUMBER() OVER (ORDER BY GET(F.VALUE, 'completed_on') DESC NULLS FIRST)] contains a correlation.
```

To solve this problem, don’t use correlated columns inside window functions. Move the window function to the outer
query where the correlation no longer exists. For example:

Copy code

```
WITH data AS (
  SELECT
    PARSE_JSON('[
                  {"completed_on": "2024-06-03T20:17:08.621001019Z"},
                  {"completed_on": "2024-06-03T18:26:08.691858742Z"},
                  {"completed_on": "2024-06-03T14:43:40.215726239Z"}
                 ]') d
  )
SELECT
    fields.*,
    ROW_NUMBER() OVER(ORDER BY completed_on DESC) rn
  FROM
    data,
    LATERAL FLATTEN(d) AS f,
    LATERAL (SELECT
             f.value:completed_on AS completed_on
            )fields;
```

This query executes successfully and returns:

```
+--------------------------------------+----+
| COMPLETED_ON                         | RN |
|--------------------------------------+----|
| "2024-06-03T20:17:08.621001019Z"     |  1 |
| "2024-06-03T18:26:08.691858742Z"     |  2 |
| "2024-06-03T14:43:40.215726239Z"     |  3 |
+--------------------------------------+----+
```

When you move the ROW\_NUMBER() function to the outer query, the `completed_on` column is no longer correlated,
and the window function can process it correctly.

## Usage notes for window frames

- All window functions support window frames. However, support for window frame syntax
  varies by function. If no window frame is specified, the default depends on the function:

  - For non-ranking functions (such as [COUNT](/sql-reference/functions/count), [MAX](/sql-reference/functions/max),
    [MIN](/sql-reference/functions/min), and [SUM](/sql-reference/functions/sum)), the
    default is the following window frame (in accordance with the ANSI standard):

    Copy code

    ```
    RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ```
  - For ranking functions (such as [FIRST\_VALUE](/sql-reference/functions/first_value), [LAST\_VALUE](/sql-reference/functions/last_value),
    [NTH\_VALUE](/sql-reference/functions/nth_value)), the default is the entire window:

    Copy code

    ```
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ```

    Note that this behavior *does not comply* with the ANSI standard.

    Note

    For clarity, Snowflake recommends avoiding implicit window frames. If your query uses a window frame, define an explicit window frame.
- Window frames require the data in the window to be in a known order. Therefore, the ORDER BY clause inside the OVER
  clause is *required* for window frame syntax, even though that ORDER BY clause is generally optional.

## Examples

This section contains examples that show how to use window functions in different ways. For additional examples, see
[Analyzing data with window functions](/user-guide/functions-window-using) and the pages for individual functions.

### Introductory example

Suppose that you own a chain of stores. The following query shows the percentage of
the chain’s total profit that is generated by each store. The query uses the RATIO\_TO\_REPORT function, which takes a
value (`net_profit`) from the current row and divides it by the sum of the corresponding values from all the other rows:

Create and load the table:

Copy code

```
CREATE TRANSIENT TABLE store_sales (
    branch_ID    INTEGER,
    city        VARCHAR,
    gross_sales NUMERIC(9, 2),
    gross_costs NUMERIC(9, 2),
    net_profit  NUMERIC(9, 2)
    );

INSERT INTO store_sales (branch_ID, city, gross_sales, gross_costs)
    VALUES
    (1, 'Vancouver', 110000, 100000),
    (2, 'Vancouver', 140000, 125000),
    (3, 'Montreal', 150000, 140000),
    (4, 'Montreal', 155000, 146000);

UPDATE store_sales SET net_profit = gross_sales - gross_costs;
```

Query the table:

Copy code

```
SELECT branch_ID,
       net_profit,
       100 * RATIO_TO_REPORT(net_profit) OVER () AS percent_of_chain_profit
    FROM store_sales AS s1
    ORDER BY branch_ID;
+-----------+------------+-------------------------+
| BRANCH_ID | NET_PROFIT | PERCENT_OF_CHAIN_PROFIT |
|-----------+------------+-------------------------|
|         1 |   10000.00 |             22.72727300 |
|         2 |   15000.00 |             34.09090900 |
|         3 |   10000.00 |             22.72727300 |
|         4 |    9000.00 |             20.45454500 |
+-----------+------------+-------------------------+
```

### Window frame with an unbounded starting position

Create and populate a table with values:

Copy code

```
CREATE OR REPLACE TABLE example_cumulative (p INT, o INT, i INT);

INSERT INTO example_cumulative VALUES
    (  0, 1, 10), (0, 2, 20), (0, 3, 30),
    (100, 1, 10),(100, 2, 30),(100, 2, 5),(100, 3, 11),(100, 3, 120),
    (200, 1, 10000),(200, 1, 200),(200, 1, 808080),(200, 2, 33333),(200, 3, null), (200, 3, 4),
    (300, 1, null), (300, 1, null);
```

Run a query that uses a window frame with an unbounded starting position and show the output.
Return cumulative COUNT, SUM, AVG, MIN, and MAX values for each row in each partition:

Copy code

```
SELECT
    p, o, i,
    COUNT(i) OVER (PARTITION BY p ORDER BY o ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) count_i_Rows_Pre,
    SUM(i)   OVER (PARTITION BY p ORDER BY o ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) sum_i_Rows_Pre,
    AVG(i)   OVER (PARTITION BY p ORDER BY o ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) avg_i_Rows_Pre,
    MIN(i)   OVER (PARTITION BY p ORDER BY o ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) min_i_Rows_Pre,
    MAX(i)   OVER (PARTITION BY p ORDER BY o ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) max_i_Rows_Pre
  FROM example_cumulative
  ORDER BY p,o;
+-----+---+--------+------------------+----------------+----------------+----------------+----------------+
|   P | O |      I | COUNT_I_ROWS_PRE | SUM_I_ROWS_PRE | AVG_I_ROWS_PRE | MIN_I_ROWS_PRE | MAX_I_ROWS_PRE |
|-----+---+--------+------------------+----------------+----------------+----------------+----------------|
|   0 | 1 |     10 |                1 |             10 |         10.000 |             10 |             10 |
|   0 | 2 |     20 |                2 |             30 |         15.000 |             10 |             20 |
|   0 | 3 |     30 |                3 |             60 |         20.000 |             10 |             30 |
| 100 | 1 |     10 |                1 |             10 |         10.000 |             10 |             10 |
| 100 | 2 |     30 |                2 |             40 |         20.000 |             10 |             30 |
| 100 | 2 |      5 |                3 |             45 |         15.000 |              5 |             30 |
| 100 | 3 |     11 |                4 |             56 |         14.000 |              5 |             30 |
| 100 | 3 |    120 |                5 |            176 |         35.200 |              5 |            120 |
| 200 | 1 |  10000 |                1 |          10000 |      10000.000 |          10000 |          10000 |
| 200 | 1 |    200 |                2 |          10200 |       5100.000 |            200 |          10000 |
| 200 | 1 | 808080 |                3 |         818280 |     272760.000 |            200 |         808080 |
| 200 | 2 |  33333 |                4 |         851613 |     212903.250 |            200 |         808080 |
| 200 | 3 |   NULL |                4 |         851613 |     212903.250 |            200 |         808080 |
| 200 | 3 |      4 |                5 |         851617 |     170323.400 |              4 |         808080 |
| 300 | 1 |   NULL |                0 |           NULL |           NULL |           NULL |           NULL |
| 300 | 1 |   NULL |                0 |           NULL |           NULL |           NULL |           NULL |
+-----+---+--------+------------------+----------------+----------------+----------------+----------------+
```

Return the same results as the above query by using the default window frame (that is,
`ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`):

Copy code

```
SELECT
    p, o, i,
    COUNT(i) OVER (PARTITION BY p ORDER BY o) count_i_Range_Pre,
    SUM(i)   OVER (PARTITION BY p ORDER BY o) sum_i_Range_Pre,
    AVG(i)   OVER (PARTITION BY p ORDER BY o) avg_i_Range_Pre,
    MIN(i)   OVER (PARTITION BY p ORDER BY o) min_i_Range_Pre,
    MAX(i)   OVER (PARTITION BY p ORDER BY o) max_i_Range_Pre
  FROM example_cumulative
  ORDER BY p,o;
+-----+---+--------+-------------------+-----------------+-----------------+-----------------+-----------------+
|   P | O |      I | COUNT_I_RANGE_PRE | SUM_I_RANGE_PRE | AVG_I_RANGE_PRE | MIN_I_RANGE_PRE | MAX_I_RANGE_PRE |
|-----+---+--------+-------------------+-----------------+-----------------+-----------------+-----------------|
|   0 | 1 |     10 |                 1 |              10 |       10.000000 |              10 |              10 |
|   0 | 2 |     20 |                 2 |              30 |       15.000000 |              10 |              20 |
|   0 | 3 |     30 |                 3 |              60 |       20.000000 |              10 |              30 |
| 100 | 1 |     10 |                 1 |              10 |       10.000000 |              10 |              10 |
| 100 | 2 |     30 |                 3 |              45 |       15.000000 |               5 |              30 |
| 100 | 2 |      5 |                 3 |              45 |       15.000000 |               5 |              30 |
| 100 | 3 |     11 |                 5 |             176 |       35.200000 |               5 |             120 |
| 100 | 3 |    120 |                 5 |             176 |       35.200000 |               5 |             120 |
| 200 | 1 |  10000 |                 3 |          818280 |   272760.000000 |             200 |          808080 |
| 200 | 1 |    200 |                 3 |          818280 |   272760.000000 |             200 |          808080 |
| 200 | 1 | 808080 |                 3 |          818280 |   272760.000000 |             200 |          808080 |
| 200 | 2 |  33333 |                 4 |          851613 |   212903.250000 |             200 |          808080 |
| 200 | 3 |   NULL |                 5 |          851617 |   170323.400000 |               4 |          808080 |
| 200 | 3 |      4 |                 5 |          851617 |   170323.400000 |               4 |          808080 |
| 300 | 1 |   NULL |                 0 |            NULL |            NULL |            NULL |            NULL |
| 300 | 1 |   NULL |                 0 |            NULL |            NULL |            NULL |            NULL |
+-----+---+--------+-------------------+-----------------+-----------------+-----------------+-----------------+
```

### Window frames with explicit offsets

Create and populate a table with values:

Copy code

```
CREATE TABLE example_sliding
  (p INT, o INT, i INT, r INT, s VARCHAR(100));

INSERT INTO example_sliding VALUES
  (100,1,1,70,'seventy'),(100,2,2,30, 'thirty'),(100,3,3,40,'forty'),(100,4,NULL,90,'ninety'),
  (100,5,5,50,'fifty'),(100,6,6,30,'thirty'),
  (200,7,7,40,'forty'),(200,8,NULL,NULL,'n_u_l_l'),(200,9,NULL,NULL,'n_u_l_l'),(200,10,10,20,'twenty'),
  (200,11,NULL,90,'ninety'),
  (300,12,12,30,'thirty'),
  (400,13,NULL,20,'twenty');
```

Return MIN function results for two columns (numeric and string) over sliding windows before, after, and including the current row:

Copy code

```
select p, o, i AS i_col,
    MIN(i) OVER (PARTITION BY p ORDER BY o ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING) min_i_3P_1P,
    MIN(i) OVER (PARTITION BY p ORDER BY o ROWS BETWEEN 1 FOLLOWING AND 3 FOLLOWING) min_i_1F_3F,
    MIN(i) OVER (PARTITION BY p ORDER BY o ROWS BETWEEN 1 PRECEDING AND 3 FOLLOWING) min_i_1P_3F,
    s,
    MIN(s) OVER (PARTITION BY p ORDER BY o ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING) min_s_3P_1P,
    MIN(s) OVER (PARTITION BY p ORDER BY o ROWS BETWEEN 1 FOLLOWING AND 3 FOLLOWING) min_s_1F_3F,
    MIN(s) OVER (PARTITION BY p ORDER BY o ROWS BETWEEN 1 PRECEDING AND 3 FOLLOWING) min_s_1P_3F
  FROM example_sliding
  ORDER BY p, o;
+-----+----+-------+-------------+-------------+-------------+---------+-------------+-------------+-------------+
|   P |  O | I_COL | MIN_I_3P_1P | MIN_I_1F_3F | MIN_I_1P_3F | S       | MIN_S_3P_1P | MIN_S_1F_3F | MIN_S_1P_3F |
|-----+----+-------+-------------+-------------+-------------+---------+-------------+-------------+-------------|
| 100 |  1 |     1 |        NULL |           2 |           1 | seventy | NULL        | forty       | forty       |
| 100 |  2 |     2 |           1 |           3 |           1 | thirty  | seventy     | fifty       | fifty       |
| 100 |  3 |     3 |           1 |           5 |           2 | forty   | seventy     | fifty       | fifty       |
| 100 |  4 |  NULL |           1 |           5 |           3 | ninety  | forty       | fifty       | fifty       |
| 100 |  5 |     5 |           2 |           6 |           5 | fifty   | forty       | thirty      | fifty       |
| 100 |  6 |     6 |           3 |        NULL |           5 | thirty  | fifty       | NULL        | fifty       |
| 200 |  7 |     7 |        NULL |          10 |           7 | forty   | NULL        | n_u_l_l     | forty       |
| 200 |  8 |  NULL |           7 |          10 |           7 | n_u_l_l | forty       | n_u_l_l     | forty       |
| 200 |  9 |  NULL |           7 |          10 |          10 | n_u_l_l | forty       | ninety      | n_u_l_l     |
| 200 | 10 |    10 |           7 |        NULL |          10 | twenty  | forty       | ninety      | n_u_l_l     |
| 200 | 11 |  NULL |          10 |        NULL |          10 | ninety  | n_u_l_l     | NULL        | ninety      |
| 300 | 12 |    12 |        NULL |        NULL |          12 | thirty  | NULL        | NULL        | thirty      |
| 400 | 13 |  NULL |        NULL |        NULL |        NULL | twenty  | NULL        | NULL        | twenty      |
+-----+----+-------+-------------+-------------+-------------+---------+-------------+-------------+-------------+
```

Return MAX function results for two columns (numeric and string) over sliding windows before, after, and including the current row:

Copy code

```
SELECT p, o, i AS i_col,
    MAX(i) OVER (PARTITION BY p ORDER BY o ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING) max_i_3P_1P,
    MAX(i) OVER (PARTITION BY p ORDER BY o ROWS BETWEEN 1 FOLLOWING AND 3 FOLLOWING) max_i_1F_3F,
    MAX(i) OVER (PARTITION BY p ORDER BY o ROWS BETWEEN 1 PRECEDING AND 3 FOLLOWING) max_i_1P_3F,
    s,
    MAX(s) OVER (PARTITION BY p ORDER BY o ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING) max_s_3P_1P,
    MAX(s) OVER (PARTITION BY p ORDER BY o ROWS BETWEEN 1 FOLLOWING AND 3 FOLLOWING) max_s_1F_3F,
    MAX(s) OVER (PARTITION BY p ORDER BY o ROWS BETWEEN 1 PRECEDING AND 3 FOLLOWING) max_s_1P_3F
  FROM example_sliding
  ORDER BY p, o;
+-----+----+-------+-------------+-------------+-------------+---------+-------------+-------------+-------------+
|   P |  O | I_COL | MAX_I_3P_1P | MAX_I_1F_3F | MAX_I_1P_3F | S       | MAX_S_3P_1P | MAX_S_1F_3F | MAX_S_1P_3F |
|-----+----+-------+-------------+-------------+-------------+---------+-------------+-------------+-------------|
| 100 |  1 |     1 |        NULL |           3 |           3 | seventy | NULL        | thirty      | thirty      |
| 100 |  2 |     2 |           1 |           5 |           5 | thirty  | seventy     | ninety      | thirty      |
| 100 |  3 |     3 |           2 |           6 |           6 | forty   | thirty      | thirty      | thirty      |
| 100 |  4 |  NULL |           3 |           6 |           6 | ninety  | thirty      | thirty      | thirty      |
| 100 |  5 |     5 |           3 |           6 |           6 | fifty   | thirty      | thirty      | thirty      |
| 100 |  6 |     6 |           5 |        NULL |           6 | thirty  | ninety      | NULL        | thirty      |
| 200 |  7 |     7 |        NULL |          10 |          10 | forty   | NULL        | twenty      | twenty      |
| 200 |  8 |  NULL |           7 |          10 |          10 | n_u_l_l | forty       | twenty      | twenty      |
| 200 |  9 |  NULL |           7 |          10 |          10 | n_u_l_l | n_u_l_l     | twenty      | twenty      |
| 200 | 10 |    10 |           7 |        NULL |          10 | twenty  | n_u_l_l     | ninety      | twenty      |
| 200 | 11 |  NULL |          10 |        NULL |          10 | ninety  | twenty      | NULL        | twenty      |
| 300 | 12 |    12 |        NULL |        NULL |          12 | thirty  | NULL        | NULL        | thirty      |
| 400 | 13 |  NULL |        NULL |        NULL |        NULL | twenty  | NULL        | NULL        | twenty      |
+-----+----+-------+-------------+-------------+-------------+---------+-------------+-------------+-------------+
```

Return the sum of a number column across sliding windows before, after, and encompassing the current row:

Copy code

```
SELECT p, o, r AS r_col,
    SUM(r) OVER (PARTITION BY p ORDER BY o ROWS BETWEEN 4 PRECEDING AND 2 PRECEDING) sum_r_4P_2P,
    sum(r) over (partition by p ORDER BY o ROWS BETWEEN 2 FOLLOWING AND 4 FOLLOWING) sum_r_2F_4F,
    sum(r) over (partition by p ORDER BY o ROWS BETWEEN 2 PRECEDING AND 4 FOLLOWING) sum_r_2P_4F
  FROM example_sliding
  ORDER BY p, o;
+-----+----+-------+-------------+-------------+-------------+
|   P |  O | R_COL | SUM_R_4P_2P | SUM_R_2F_4F | SUM_R_2P_4F |
|-----+----+-------+-------------+-------------+-------------|
| 100 |  1 |    70 |        NULL |         180 |         280 |
| 100 |  2 |    30 |        NULL |         170 |         310 |
| 100 |  3 |    40 |          70 |          80 |         310 |
| 100 |  4 |    90 |         100 |          30 |         240 |
| 100 |  5 |    50 |         140 |        NULL |         210 |
| 100 |  6 |    30 |         160 |        NULL |         170 |
| 200 |  7 |    40 |        NULL |         110 |         150 |
| 200 |  8 |  NULL |        NULL |         110 |         150 |
| 200 |  9 |  NULL |          40 |          90 |         150 |
| 200 | 10 |    20 |          40 |        NULL |         110 |
| 200 | 11 |    90 |          40 |        NULL |         110 |
| 300 | 12 |    30 |        NULL |        NULL |          30 |
| 400 | 13 |    20 |        NULL |        NULL |          20 |
+-----+----+-------+-------------+-------------+-------------+
```

### Ranking function examples

The following example shows how to rank sales based on the total amount (in dollars) that each salesperson has sold. The ORDER BY clause within the
OVER clause sorts the totals in descending order (highest to lowest). The query calculates the rank of each salesperson relative to all other salespeople.

Create the table and insert the data:

Copy code

```
CREATE TABLE sales_table (salesperson_name VARCHAR, sales_in_dollars INTEGER);
INSERT INTO sales_table (salesperson_name, sales_in_dollars) VALUES
    ('Smith', 600),
    ('Jones', 1000),
    ('Torkelson', 700),
    ('Dolenz', 800);
```

Now query the data:

Copy code

```
SELECT
    salesperson_name,
    sales_in_dollars,
    RANK() OVER (ORDER BY sales_in_dollars DESC) AS sales_rank
  FROM sales_table;
+------------------+------------------+------------+
| SALESPERSON_NAME | SALES_IN_DOLLARS | SALES_RANK |
|------------------+------------------+------------|
| Jones            |             1000 |          1 |
| Dolenz           |              800 |          2 |
| Torkelson        |              700 |          3 |
| Smith            |              600 |          4 |
+------------------+------------------+------------+
```

The output is not necessarily ordered by rank. To display results ordered by rank, specify an ORDER BY clause for the query itself (in addition
to the ORDER BY clause for the window function), as shown here:

Copy code

```
SELECT
    salesperson_name,
    sales_in_dollars,
    RANK() OVER (ORDER BY sales_in_dollars DESC) AS sales_rank
  FROM sales_table
  ORDER BY 3;
+------------------+------------------+------------+
| SALESPERSON_NAME | SALES_IN_DOLLARS | SALES_RANK |
|------------------+------------------+------------|
| Jones            |             1000 |          1 |
| Dolenz           |              800 |          2 |
| Torkelson        |              700 |          3 |
| Smith            |              600 |          4 |
+------------------+------------------+------------+
```

The preceding example has *two* ORDER BY clauses:

- One controls the order of the ranking.
- One controls the order of the output.

These clauses are independent. For example, you could order the rankings based on total sales (as shown above), but
order the output rows based on the salesperson’s last name:

Copy code

```
SELECT
    salesperson_name,
    sales_in_dollars,
    RANK() OVER (ORDER BY sales_in_dollars DESC) AS sales_rank
  FROM sales_table
  ORDER BY salesperson_name;
+------------------+------------------+------------+
| SALESPERSON_NAME | SALES_IN_DOLLARS | SALES_RANK |
|------------------+------------------+------------|
| Dolenz           |              800 |          2 |
| Jones            |             1000 |          1 |
| Smith            |              600 |          4 |
| Torkelson        |              700 |          3 |
+------------------+------------------+------------+
```

### RANGE BETWEEN example with explicit numeric offsets

The following example uses RANGE BETWEEN syntax with explicit numeric offsets.
To run this example, follow these instructions: [Create and load the menu\_items table](/sql-reference/functions/stddev#label-create-and-load-menu-items-table).
For similar examples that use INTERVAL offsets, see [Using windowed aggregations for rolling calculations](/user-guide/querying-time-series-data#label-window-aggs-range-between-interval).

The following query computes the average cost of goods sold for categories of menu items available from a food truck.
The window function does not partition the results; therefore, the averages are computed across the complete result set,
subject to a range-based frame.

The boundary of the frame is the cost of goods value in the current row, plus two (the first row = 0.50 + 2.00, for example).
Rows qualify for the frame when they fall within this two-dollar range.

Copy code

```
SELECT menu_category, menu_cogs_usd,
    AVG(menu_cogs_usd)
      OVER(ORDER BY menu_cogs_usd RANGE BETWEEN CURRENT ROW AND 2 FOLLOWING) avg_cogs
  FROM menu_items
  WHERE menu_category IN('Beverage','Dessert','Snack')
  GROUP BY menu_category, menu_cogs_usd
  ORDER BY menu_category, menu_cogs_usd;
```

```
+---------------+---------------+----------+
| MENU_CATEGORY | MENU_COGS_USD | AVG_COGS |
|---------------+---------------+----------|
| Beverage      |          0.50 |  1.18333 |
| Beverage      |          0.65 |  1.37857 |
| Beverage      |          0.75 |  1.50000 |
| Dessert       |          0.50 |  1.18333 |
| Dessert       |          1.00 |  1.87500 |
| Dessert       |          1.25 |  2.05000 |
| Dessert       |          2.50 |  3.16666 |
| Dessert       |          3.00 |  3.50000 |
| Snack         |          1.25 |  2.05000 |
| Snack         |          2.25 |  2.93750 |
| Snack         |          4.00 |  4.00000 |
+---------------+---------------+----------+
```

For example, the `avg_cogs` value for the first row is 1.1833. This is computed as the sum of all the `menu_cogs_usd` values that fall
between 0.50 and 2.50, divided by the count of those rows:

`(0.50 + 0.65 + 0.75 + 0.50 + 1.00 + 1.25 + 2.50 + 1.25 + 2.25) / 9 = 1.18333`

The second to last row has an avg\_cogs value of 2.93750. This is computed as the sum of all the `menu_cogs_usd` values that fall between 2.25 and 4.25,
divided by the count of those rows:

`(2.25 + 2.50 + 3.00 + 4.00) / 4 = 2.93750`

The last row returns 4.0 for both the `avg_cogs` and `menu_cogs_usd`. This result is accurate because only this row belongs to the frame; 4.0 is the
maximum `menu_cogs_usd` value in the entire result, so it becomes a single-row frame. It has no “following” rows.

Note that this query has an ORDER BY clause for the window function and an ORDER BY clause for the final results of the query. The final ORDER BY output
does not influence the calculation of the window function results. The ordered result set for computing the function is an intermediate result set that the
final query does not display.

#### RANGE BETWEEN examples with NULL values in the ORDER BY clause

The `nulls` table contains five rows, and two have NULL values in the `c1` column. Create and
load the table as follows:

Copy code

```
CREATE OR REPLACE TABLE nulls(c1 int, c2 int);

INSERT INTO nulls VALUES
  (1,10),
  (2,20),
  (3,30),
  (NULL,20),
  (NULL,50);
```

When NULLS LAST is specified, and the window frame uses explicit offsets, rows with NULL in `c1`
are included in the frame only when the ORDER BY value of the current row is NULL.
The following query returns a sum of `50` when row `3` is the current row.
The following NULL row is not included in the frame.

Copy code

```
SELECT c1 c1_nulls_last, c2,
    SUM(c2) OVER(ORDER BY c1 NULLS LAST RANGE BETWEEN 1 PRECEDING AND 1 FOLLOWING) sum_c2
  FROM nulls;
```

```
+---------------+----+--------+
| C1_NULLS_LAST | C2 | SUM_C2 |
|---------------+----+--------|
|             1 | 10 |     30 |
|             2 | 20 |     60 |
|             3 | 30 |     50 |
|          NULL | 20 |     70 |
|          NULL | 50 |     70 |
+---------------+----+--------+
```

When NULLS LAST is specified, and the window frame uses UNBOUNDED FOLLOWING, rows with NULL in `c1`
are included in the frame. The following query returns a sum of `120` when row `3` is the current row.
Both following NULL rows are included in the frame.

Copy code

```
SELECT c1 c1_nulls_last, c2,
    SUM(c2) OVER(ORDER BY c1 NULLS LAST RANGE BETWEEN 1 PRECEDING AND UNBOUNDED FOLLOWING) sum_c2
  FROM nulls;
```

```
+---------------+----+--------+
| C1_NULLS_LAST | C2 | SUM_C2 |
|---------------+----+--------|
|             1 | 10 |    130 |
|             2 | 20 |    130 |
|             3 | 30 |    120 |
|          NULL | 20 |     70 |
|          NULL | 50 |     70 |
+---------------+----+--------+
```

### Create and load the heavy\_weather table

To create and insert rows into the `heavy_weather` table, which is used in some window function
[examples](#label-range-between-examples), run this script.

Copy code

```
CREATE OR REPLACE TABLE heavy_weather
  (start_time TIMESTAMP, precip NUMBER(3,2), city VARCHAR(20), county VARCHAR(20));

INSERT INTO heavy_weather VALUES
('2021-12-23 06:56:00.000',0.08,'Mount Shasta','Siskiyou'),
('2021-12-23 07:51:00.000',0.09,'Mount Shasta','Siskiyou'),
('2021-12-23 16:23:00.000',0.56,'South Lake Tahoe','El Dorado'),
('2021-12-23 17:24:00.000',0.38,'South Lake Tahoe','El Dorado'),
('2021-12-23 18:30:00.000',0.28,'South Lake Tahoe','El Dorado'),
('2021-12-23 19:35:00.000',0.37,'Mammoth Lakes','Mono'),
('2021-12-23 19:36:00.000',0.80,'South Lake Tahoe','El Dorado'),
('2021-12-24 04:43:00.000',0.25,'Alta','Placer'),
('2021-12-24 05:26:00.000',0.34,'Alta','Placer'),
('2021-12-24 05:35:00.000',0.42,'Big Bear City','San Bernardino'),
('2021-12-24 06:49:00.000',0.17,'South Lake Tahoe','El Dorado'),
('2021-12-24 07:40:00.000',0.07,'Alta','Placer'),
('2021-12-24 08:36:00.000',0.07,'Alta','Placer'),
('2021-12-24 11:52:00.000',0.08,'Alta','Placer'),
('2021-12-24 12:52:00.000',0.38,'Alta','Placer'),
('2021-12-24 15:44:00.000',0.13,'Alta','Placer'),
('2021-12-24 15:53:00.000',0.07,'South Lake Tahoe','El Dorado'),
('2021-12-24 16:55:00.000',0.09,'Big Bear City','San Bernardino'),
('2021-12-24 21:53:00.000',0.07,'Montague','Siskiyou'),
('2021-12-25 02:52:00.000',0.07,'Alta','Placer'),
('2021-12-25 07:52:00.000',0.07,'Alta','Placer'),
('2021-12-25 08:52:00.000',0.08,'Alta','Placer'),
('2021-12-25 09:48:00.000',0.18,'Alta','Placer'),
('2021-12-25 12:52:00.000',0.10,'Alta','Placer'),
('2021-12-25 17:21:00.000',0.23,'Alturas','Modoc'),
('2021-12-25 17:52:00.000',1.54,'Alta','Placer'),
('2021-12-26 01:52:00.000',0.61,'Alta','Placer'),
('2021-12-26 05:43:00.000',0.16,'South Lake Tahoe','El Dorado'),
('2021-12-26 05:56:00.000',0.08,'Bishop','Inyo'),
('2021-12-26 06:52:00.000',0.75,'Bishop','Inyo'),
('2021-12-26 06:53:00.000',0.08,'Lebec','Los Angeles'),
('2021-12-26 07:52:00.000',0.65,'Alta','Placer'),
('2021-12-26 09:52:00.000',2.78,'Alta','Placer'),
('2021-12-26 09:55:00.000',0.07,'Big Bear City','San Bernardino'),
('2021-12-26 14:22:00.000',0.32,'Alta','Placer'),
('2021-12-26 14:52:00.000',0.34,'Alta','Placer'),
('2021-12-26 15:43:00.000',0.35,'Alta','Placer'),
('2021-12-26 17:31:00.000',5.24,'Alta','Placer'),
('2021-12-26 22:52:00.000',0.07,'Alta','Placer'),
('2021-12-26 23:15:00.000',0.52,'Alta','Placer'),
('2021-12-27 02:52:00.000',0.08,'Alta','Placer'),
('2021-12-27 03:52:00.000',0.14,'Alta','Placer'),
('2021-12-27 04:52:00.000',1.52,'Alta','Placer'),
('2021-12-27 14:37:00.000',0.89,'Alta','Placer'),
('2021-12-27 14:53:00.000',0.07,'South Lake Tahoe','El Dorado'),
('2021-12-27 17:53:00.000',0.07,'South Lake Tahoe','El Dorado'),
('2021-12-30 11:23:00.000',0.12,'Lebec','Los Angeles'),
('2021-12-30 11:43:00.000',0.98,'Lebec','Los Angeles'),
('2021-12-30 13:53:00.000',0.23,'Lebec','Los Angeles'),
('2021-12-30 14:53:00.000',0.13,'Lebec','Los Angeles'),
('2021-12-30 15:15:00.000',0.29,'Lebec','Los Angeles'),
('2021-12-30 17:53:00.000',0.10,'Lebec','Los Angeles'),
('2021-12-30 18:53:00.000',0.09,'Lebec','Los Angeles'),
('2021-12-30 19:53:00.000',0.07,'Lebec','Los Angeles'),
('2021-12-30 20:53:00.000',0.07,'Lebec','Los Angeles')
;
```
