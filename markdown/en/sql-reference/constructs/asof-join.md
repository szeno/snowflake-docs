Categories:
:   [Query syntax](/sql-reference/constructs)

# ASOF JOIN

An ASOF JOIN operation combines rows from two tables based on timestamp values that follow each
other, precede each other, or match exactly. For each row in the first (or left) table, the join finds a single
row in the second (or right) table that has the closest timestamp value. The qualifying row on the right side
is the closest match, which could be equal in time, earlier in time, or later in time, depending on the specified
comparison operator.

This topic describes how to use the ASOF JOIN construct in the [FROM](/sql-reference/constructs/from) clause. For a more detailed conceptual
explanation of ASOF joins, see [Analyzing time-series data](/user-guide/querying-time-series-data).

See also [JOIN](/sql-reference/constructs/join), which covers the syntax for other standard join types, such as
inner and outer joins.

## Syntax

The following FROM clause syntax is specific to ASOF JOIN:

Copy code

```
FROM <left_table> ASOF JOIN <right_table>
  MATCH_CONDITION ( <left_table.timecol> <comparison_operator> <right_table.timecol> )
  [ ON <table.col> = <table.col> [ AND ... ] | USING ( <column_list> ) ]
```

## Parameters

`FROM`
:   The first (or left) table in the FROM clause is assumed to contain records that either follow (in time),
    precede, or are exactly synchronized with, the records in the second (or right) table. When there is no
    match for a row in the left table, the columns from the right table are null-padded.

    In addition to regular tables and views, any object reference can be used in an ASOF JOIN.
    See [FROM](/sql-reference/constructs/from).

    ASOF JOIN can be used in most contexts where joins are supported. For information about some restrictions, see [Usage Notes](#usage-notes).

`MATCH_CONDITION ( left_table.timecol comparison_operator right_table.timecol )`
:   This condition names the specific timestamp columns to be compared in each table.

    - The order of tables is important in the condition. The left table must be named first.
    - The parentheses are required.
    - The comparison operator must be one of the following: `>=`, `<=`, `>`, `<`. The equals operator (`=`) is
      not supported.
    - All of the following data types are supported: DATE, TIME, DATETIME, TIMESTAMP, TIMESTAMP\_LTZ, TIMESTAMP\_NTZ, TIMESTAMP\_TZ.
    - You can also use NUMBER columns in the match condition. For example, you might have NUMBER columns that contain UNIX
      timestamps (which define the number of seconds that have elapsed since January 1st, 1970).
    - The data types of the two matched columns don’t have to be exactly the same, but they must be
      [compatible](/sql-reference/intro-summary-data-types).

`ON table.col = table.col [ AND ... ] | USING (column_list)`
:   The optional ON or USING clause defines one or more equality conditions on columns in the two tables, for the purpose of
    logically grouping the results of the query.

    For general information about ON and USING, see [JOIN](/sql-reference/constructs/join). Note that a join specified with USING
    projects one of the joining columns in its intermediate result set, not both. A join specified with an ON clause projects both
    joining columns.

    The following notes are specific to ASOF JOIN:

    - The comparison operator in the ON clause must be the equal sign (=).
    - The ON clause cannot contain disjuncts (conditions connected with OR). Conditions connected with AND are supported.
    - Each side of a condition must refer to only one of the two tables in the join. However, the order of the table references doesn’t matter.
    - Each condition can be enclosed in parentheses, but they aren’t required.

See also [More Details on Join Behavior](#more-details-on-join-behavior) and [Specifying a USING condition instead of an ON condition](#label-asof-join-using).

## Usage notes

- If no match is found in the right table for a given row, the result is null-padded for the selected columns from the right table. (ASOF joins are similar to left outer joins in this respect.)
- If you use TIME columns in the match condition (as opposed to one of the [timestamp types](/sql-reference/data-types-datetime#label-datatypes-timestamp)), you might need to set the TIME\_OUTPUT\_FORMAT parameter in order to see the exact TIME values that are being compared when you look at ASOF JOIN query results. By default, the display of a TIME column truncates milliseconds. See [TIME columns in the match condition](#time-columns-in-the-match-condition).
- You can use more than one ASOF join in the same query as long as all of the syntax rules are followed for each join. Each join must be immediately followed by its own MATCH\_CONDITION. You cannot apply a single MATCH\_CONDITION to multiple ASOF joins. See [Multiple ASOF joins in a query](#multiple-asof-joins-in-a-query).
- ASOF joins are not supported for joins with LATERAL table functions or LATERAL inline views. For more information about lateral joins, see [LATERAL](/sql-reference/constructs/join-lateral).
- An ASOF join with a self-reference is not allowed in a RECURSIVE common table expression (CTE). For information about CTEs, see [WITH](/sql-reference/constructs/with).
- The EXPLAIN output for ASOF JOIN queries identifies the ON (or USING) conditions and the MATCH\_CONDITION. For example, in text or tabular format, output similar to the following text appears above the table scans in the plan:

  ```
  ->ASOF Join  joinKey: (S.LOCATION = R.LOCATION) AND (S.STATE = R.STATE),
    matchCondition: (S.OBSERVED >= R.OBSERVED)
  ```
- [Query profiles](/user-guide/ui-snowsight-activity) also clearly identify the ASOF JOIN operation in the plan. In this example, you can see that the table scan reads 22M rows from the left table, which are all preserved by the join. The profile also shows the match condition for the join.

![Query profile that shows table scans feeding rows to the ASOF JOIN operator above it.](/static/images/screens/asof_join_profile.png)

- You can specify the ASOF keyword in a [semantic view](/user-guide/views-semantic/overview) to perform the ASOF JOIN
  operation on two logical tables in the view. For information, see [Using a date, time, timestamp, or numeric range to join logical tables](/user-guide/views-semantic/sql#label-semantic-views-create-relationships-asof).

## More details on join behavior

The optional ON (or USING) conditions for ASOF JOIN provide a way of grouping or partitioning table rows before the final matching rows
are singled out by the required match condition. If you want the rows from the joined tables to be grouped on one or more dimensions
that the tables share (stock symbol, location, city, state, company name, etc.), use an ON condition.
If you don’t use an ON condition, each row from the left table may be matched (by time) with any row from the right table
in the final result set.

In the following example, tables `left_table` and `right_table` have values `A`, `B`, etc.
in column `c1`, and values `1`, `2`, etc. in column `c2`. Column `c3` is a TIME column, and `c4` is a numeric value (column of interest).

First, create and load the two tables:

Copy code

```
CREATE OR REPLACE TABLE left_table (
  c1 VARCHAR(1),
  c2 TINYINT,
  c3 TIME,
  c4 NUMBER(3,2)
);

CREATE OR REPLACE TABLE right_table (
  c1 VARCHAR(1),
  c2 TINYINT,
  c3 TIME,
  c4 NUMBER(3,2)
);

INSERT INTO left_table VALUES
  ('A',1,'09:15:00',3.21),
  ('A',2,'09:16:00',3.22),
  ('B',1,'09:17:00',3.23),
  ('B',2,'09:18:00',4.23);

INSERT INTO right_table VALUES
  ('A',1,'09:14:00',3.19),
  ('B',1,'09:16:00',3.04);
```

Copy code

```
SELECT * FROM left_table ORDER BY c1, c2;
```

```
+----+----+----------+------+
| C1 | C2 | C3       |   C4 |
|----+----+----------+------|
| A  |  1 | 09:15:00 | 3.21 |
| A  |  2 | 09:16:00 | 3.22 |
| B  |  1 | 09:17:00 | 3.23 |
| B  |  2 | 09:18:00 | 4.23 |
+----+----+----------+------+
```

Copy code

```
SELECT * FROM right_table ORDER BY c1, c2;
```

```
+----+----+----------+------+
| C1 | C2 | C3       |   C4 |
|----+----+----------+------|
| A  |  1 | 09:14:00 | 3.19 |
| B  |  1 | 09:16:00 | 3.04 |
+----+----+----------+------+
```

If `c1` and `c2` are both ON condition columns in the query, a row in the left table only matches a row in the right table
when `A` and `1`, `A` and `2`, `B` and `1`, or `B` and `2` are found in both tables.
If no match is found for such values, the right table columns are null-padded.

Copy code

```
SELECT *
  FROM left_table l ASOF JOIN right_table r
    MATCH_CONDITION(l.c3>=r.c3)
    ON(l.c1=r.c1 and l.c2=r.c2)
  ORDER BY l.c1, l.c2;
```

```
+----+----+----------+------+------+------+----------+------+
| C1 | C2 | C3       |   C4 | C1   | C2   | C3       |   C4 |
|----+----+----------+------+------+------+----------+------|
| A  |  1 | 09:15:00 | 3.21 | A    |  1   | 09:14:00 | 3.19 |
| A  |  2 | 09:16:00 | 3.22 | NULL | NULL | NULL     | NULL |
| B  |  1 | 09:17:00 | 3.23 | B    |  1   | 09:16:00 | 3.04 |
| B  |  2 | 09:18:00 | 4.23 | NULL | NULL | NULL     | NULL |
+----+----+----------+------+------+------+----------+------+
```

If the ON conditions are removed, any combination of values in `c1` and `c2` may be matched in the final result.
Only the match condition determines the results.

Copy code

```
SELECT *
  FROM left_table l ASOF JOIN right_table r
    MATCH_CONDITION(l.c3>=r.c3)
  ORDER BY l.c1, l.c2;
```

```
+----+----+----------+------+----+----+----------+------+
| C1 | C2 | C3       |   C4 | C1 | C2 | C3       |   C4 |
|----+----+----------+------+----+----+----------+------|
| A  |  1 | 09:15:00 | 3.21 | A  |  1 | 09:14:00 | 3.19 |
| A  |  2 | 09:16:00 | 3.22 | B  |  1 | 09:16:00 | 3.04 |
| B  |  1 | 09:17:00 | 3.23 | B  |  1 | 09:16:00 | 3.04 |
| B  |  2 | 09:18:00 | 4.23 | B  |  1 | 09:16:00 | 3.04 |
+----+----+----------+------+----+----+----------+------+
```

## Expected behavior when “ties” exist in the right table

ASOF JOIN queries always attempt to match a single row in the left table with a single row in the right table.
This behavior is true even if two (or more) rows in the right table are identical and qualify for the join. When
such ties exist and you run the same join query multiple times, you might get different results. The results are
non-deterministic because any one of the tying rows might be returned. If you’re unsure about the results of ASOF JOIN
queries, check for exact matches in the timestamp values for rows in the right table.

For example, using the same tables from the examples in the previous section, add a `right_id` column to `right_table`
and insert the following rows:

Copy code

```
CREATE OR REPLACE TABLE right_table
  (c1 VARCHAR(1),
  c2 TINYINT,
  c3 TIME,
  c4 NUMBER(3,2),
  right_id VARCHAR(2));

INSERT INTO right_table VALUES
  ('A',1,'09:14:00',3.19,'A1'),
  ('A',1,'09:14:00',3.19,'A2'),
  ('B',1,'09:16:00',3.04,'B1');

SELECT * FROM right_table ORDER BY 1, 2;
```

```
+----+----+----------+------+----------+
| C1 | C2 | C3       |   C4 | RIGHT_ID |
|----+----+----------+------+----------|
| A  |  1 | 09:14:00 | 3.19 | A1       |
| A  |  1 | 09:14:00 | 3.19 | A2       |
| B  |  1 | 09:16:00 | 3.04 | B1       |
+----+----+----------+------+----------+
```

Two of the rows are identical except for their `right_id` values. Now run the following ASOF JOIN query:

Copy code

```
SELECT *
  FROM left_table l ASOF JOIN right_table r
    MATCH_CONDITION(l.c3>=r.c3)
  ORDER BY l.c1, l.c2;
```

```
+----+----+----------+------+----+----+----------+------+----------+
| C1 | C2 | C3       |   C4 | C1 | C2 | C3       |   C4 | RIGHT_ID |
|----+----+----------+------+----+----+----------+------+----------|
| A  |  1 | 09:15:00 | 3.21 | A  |  1 | 09:14:00 | 3.19 | A2       |
| A  |  2 | 09:16:00 | 3.22 | B  |  1 | 09:16:00 | 3.04 | B1       |
| B  |  1 | 09:17:00 | 3.23 | B  |  1 | 09:16:00 | 3.04 | B1       |
| B  |  2 | 09:18:00 | 4.23 | B  |  1 | 09:16:00 | 3.04 | B1       |
+----+----+----------+------+----+----+----------+------+----------+
```

Note that rows `A1` and `A2` from `right_table` both qualify for the join, but only `A2` is returned. On a
subsequent run of the same query, `A1` could be returned instead.

## Rewriting ASOF JOIN queries to reduce scans on the right table

When the cardinality of the ON or USING join column in the left table is lower than the cardinality of the
join column in the right table, the optimizer does not [prune](/user-guide/tables-clustering-micropartitions#label-micropartitions-query-pruning)
the unmatched rows from the right table. Therefore, more rows than are needed for the join will be scanned
from the right table. This behavior typically occurs when the query includes a highly selective filter on a
non-join column from the left table, and the filter reduces the cardinality of the join column.

You can work around this problem by manually reducing the rows that qualify for the join. For example, the
original query has the following pattern, and `t1.c1` has lower cardinality than `t2.c1`:

Copy code

```
SELECT ...
  FROM t1
    ASOF JOIN t2
      MATCH_CONDITION(...)
      ON t1.c1 = t2.c1
  WHERE t1 ...;
```

You can rewrite the query as follows to manually select the rows from `t2` where `t2.c1` values are
found in `t1.c1`:

Copy code

```
WITH t1 AS (SELECT * FROM t1 WHERE t1 ...)
SELECT ...
  FROM t1
    ASOF JOIN (SELECT * FROM t2 WHERE t2.c1 IN (SELECT t1.c1 FROM t1)) AS t2
      MATCH_CONDITION(...)
      ON t1.c1 = t2.c1;
```

## Using ASOF and MATCH\_CONDITION as object names and aliases

Use of the ASOF and MATCH\_CONDITION keywords in SELECT command syntax is restricted:

- If a SELECT statement uses ASOF or MATCH\_CONDITION as the name of a table, view, or inline view, you must identify it
  as follows:

  - If the object was created with double quotes in the name, use the same double-quoted name.
  - If the object was created without double quotes in the name, use double quotes and capital letters.

  For example, the following statements are no longer allowed and return errors:

  Copy code

  ```
  SELECT * FROM asof;

  WITH match_condition AS (SELECT * FROM T1) SELECT * FROM match_condition;
  ```

  If you created the objects with double quotes, fix the problem by using double quotes:

  Copy code

  ```
  SELECT * FROM "asof";

  WITH "match_condition" AS (SELECT * FROM T1) SELECT * FROM "match_condition";
  ```

  If you created the objects without double quotes, fix the problem by using double quotes and capital letters:

  Copy code

  ```
  SELECT * FROM "ASOF";

  WITH "MATCH_CONDITION" AS (SELECT * FROM T1) SELECT * FROM "MATCH_CONDITION";
  ```

  See also [Unquoted identifiers](/sql-reference/identifiers-syntax#label-unquoted-identifier).
- If a SELECT statement uses ASOF or MATCH\_CONDITION as an alias, you must use AS before the alias or double-quote the
  alias. For example, the following statements are no longer allowed and return errors:

  Copy code

  ```
  SELECT * FROM t1 asof;

  SELECT * FROM t2 match_condition;
  ```

  Fix the problem in one of the following ways:

  Copy code

  ```
  SELECT * FROM t1 AS asof;

  SELECT * FROM t1 "asof";

  SELECT * FROM t2 AS match_condition;

  SELECT * FROM t2 "match_condition";
  ```

## Examples

The following examples demonstrate the expected behavior of ASOF JOIN queries.
Start by running the query under [Joining two tables on the closest match (alignment)](/user-guide/querying-time-series-data#label-conceptual-asof-join-example), then proceed with
the examples here.

### NULL-padded results

Insert a new row into the `trades` table with a date that’s a day earlier than the existing rows in both
`trades` and `quotes`:

Copy code

```
INSERT INTO trades VALUES('SNOW','2023-09-30 12:02:55.000',3000);
```

```
+-------------------------+
| number of rows inserted |
|-------------------------|
|                       1 |
+-------------------------+
```

Now run the first example query again. Note that the query returns four rows, but the new row is null-padded.
There is no row in the `quotes` table that qualifies for the match condition.
The columns from `trades` are returned, and the corresponding columns from `quotes` are null-padded.

Copy code

```
SELECT t.stock_symbol, t.trade_time, t.quantity, q.quote_time, q.price
  FROM trades t ASOF JOIN quotes q
    MATCH_CONDITION(t.trade_time >= quote_time)
    ON t.stock_symbol=q.stock_symbol
  ORDER BY t.stock_symbol;
```

```
+--------------+-------------------------+----------+-------------------------+--------------+
| STOCK_SYMBOL | TRADE_TIME              | QUANTITY | QUOTE_TIME              |        PRICE |
|--------------+-------------------------+----------+-------------------------+--------------|
| AAPL         | 2023-10-01 09:00:05.000 |     2000 | 2023-10-01 09:00:03.000 | 139.00000000 |
| SNOW         | 2023-09-30 12:02:55.000 |     3000 | NULL                    |         NULL |
| SNOW         | 2023-10-01 09:00:05.000 |     1000 | 2023-10-01 09:00:02.000 | 163.00000000 |
| SNOW         | 2023-10-01 09:00:10.000 |     1500 | 2023-10-01 09:00:08.000 | 165.00000000 |
+--------------+-------------------------+----------+-------------------------+--------------+
```

### Using a different comparison operator in the match condition

Following on from the previous example, the results of the query change again when the comparison operator in the
match condition is changed. The following query specifies the `<=` operator (instead of `>=`):

Copy code

```
SELECT t.stock_symbol, t.trade_time, t.quantity, q.quote_time, q.price
  FROM trades t ASOF JOIN quotes q
    MATCH_CONDITION(t.trade_time <= quote_time)
    ON t.stock_symbol=q.stock_symbol
  ORDER BY t.stock_symbol;
```

```
+--------------+-------------------------+----------+-------------------------+--------------+
| STOCK_SYMBOL | TRADE_TIME              | QUANTITY | QUOTE_TIME              |        PRICE |
|--------------+-------------------------+----------+-------------------------+--------------|
| AAPL         | 2023-10-01 09:00:05.000 |     2000 | 2023-10-01 09:00:07.000 | 142.00000000 |
| SNOW         | 2023-10-01 09:00:10.000 |     1500 | NULL                    |         NULL |
| SNOW         | 2023-10-01 09:00:05.000 |     1000 | 2023-10-01 09:00:07.000 | 166.00000000 |
| SNOW         | 2023-09-30 12:02:55.000 |     3000 | 2023-10-01 09:00:01.000 | 166.00000000 |
+--------------+-------------------------+----------+-------------------------+--------------+
```

See also [Less than and greater than comparison operators](#less-than-and-greater-than-comparison-operators).

### Specifying a USING condition instead of an ON condition

You can use an ON condition or a USING condition with ASOF JOIN queries. The following query is equivalent to the
previous query, but it replaces ON with USING. The syntax `USING(stock_symbol)` implies the condition
`t.stock_symbol=q.stock_symbol`.

Copy code

```
SELECT t.stock_symbol, t.trade_time, t.quantity, q.quote_time, q.price
  FROM trades t ASOF JOIN quotes q
    MATCH_CONDITION(t.trade_time <= quote_time)
    USING(stock_symbol)
  ORDER BY t.stock_symbol;
```

### Inner join to a third table

The following example adds a third `companies` table to the join in order to pick the company name for each stock symbol.
You can use a regular INNER JOIN with an ON condition (or some other standard join syntax) to add the third table.
However, note that `USING(stock_symbol)` would not work here because the reference to `stock_symbol` would be ambiguous.

Copy code

```
CREATE OR REPLACE TABLE companies(
  stock_symbol VARCHAR(4),
  company_name VARCHAR(100)
);

 INSERT INTO companies VALUES
  ('NVDA','NVIDIA Corp'),
  ('TSLA','Tesla Inc'),
  ('SNOW','Snowflake Inc'),
  ('AAPL','Apple Inc')
;
```

Copy code

```
SELECT t.stock_symbol, c.company_name, t.trade_time, t.quantity, q.quote_time, q.price
  FROM trades t ASOF JOIN quotes q
    MATCH_CONDITION(t.trade_time >= quote_time)
    ON t.stock_symbol=q.stock_symbol
    INNER JOIN companies c ON c.stock_symbol=t.stock_symbol
  ORDER BY t.stock_symbol;
```

```
+--------------+---------------+-------------------------+----------+-------------------------+--------------+
| STOCK_SYMBOL | COMPANY_NAME  | TRADE_TIME              | QUANTITY | QUOTE_TIME              |        PRICE |
|--------------+---------------+-------------------------+----------+-------------------------+--------------|
| AAPL         | Apple Inc     | 2023-10-01 09:00:05.000 |     2000 | 2023-10-01 09:00:03.000 | 139.00000000 |
| SNOW         | Snowflake Inc | 2023-09-30 12:02:55.000 |     3000 | NULL                    |         NULL |
| SNOW         | Snowflake Inc | 2023-10-01 09:00:05.000 |     1000 | 2023-10-01 09:00:02.000 | 163.00000000 |
| SNOW         | Snowflake Inc | 2023-10-01 09:00:10.000 |     1500 | 2023-10-01 09:00:08.000 | 165.00000000 |
+--------------+---------------+-------------------------+----------+-------------------------+--------------+
```

### Numbers as timestamps

The following example demonstrates that the match condition can compare numeric values.
In this case, the tables have UNIX timestamp values stored in NUMBER(38,0) columns. `1696150805`
is equivalent to `2023-10-30 10:20:05.000` (three seconds later than `1696150802`).

Copy code

```
SELECT * FROM trades_unixtime;
```

```
+--------------+------------+----------+--------------+
| STOCK_SYMBOL | TRADE_TIME | QUANTITY |        PRICE |
|--------------+------------+----------+--------------|
| SNOW         | 1696150805 |      100 | 165.33300000 |
+--------------+------------+----------+--------------+
```

Copy code

```
SELECT * FROM quotes_unixtime;
```

```
+--------------+------------+----------+--------------+--------------+
| STOCK_SYMBOL | QUOTE_TIME | QUANTITY |          BID |          ASK |
|--------------+------------+----------+--------------+--------------|
| SNOW         | 1696150802 |      100 | 166.00000000 | 165.00000000 |
+--------------+------------+----------+--------------+--------------+
```

Copy code

```
SELECT *
  FROM trades_unixtime tu
    ASOF JOIN quotes_unixtime qu
    MATCH_CONDITION(tu.trade_time>=qu.quote_time);
```

```
+--------------+------------+----------+--------------+--------------+------------+----------+--------------+--------------+
| STOCK_SYMBOL | TRADE_TIME | QUANTITY |        PRICE | STOCK_SYMBOL | QUOTE_TIME | QUANTITY |          BID |          ASK |
|--------------+------------+----------+--------------+--------------+------------+----------+--------------+--------------|
| SNOW         | 1696150805 |      100 | 165.33300000 | SNOW         | 1696150802 |      100 | 166.00000000 | 165.00000000 |
+--------------+------------+----------+--------------+--------------+------------+----------+--------------+--------------+
```

### TIME columns in the match condition

The following examples join tables that contain weather observations. The observations in these tables are recorded in TIME columns.
You can create and load the tables as follows:

Copy code

```
CREATE OR REPLACE TABLE raintime(
  observed TIME(9),
  location VARCHAR(40),
  state VARCHAR(2),
  observation NUMBER(5,2)
);

INSERT INTO raintime VALUES
  ('14:42:59.230', 'Ahwahnee', 'CA', 0.90),
  ('14:42:59.001', 'Oakhurst', 'CA', 0.50),
  ('14:42:44.435', 'Reno', 'NV', 0.00)
;

CREATE OR REPLACE TABLE preciptime(
  observed TIME(9),
  location VARCHAR(40),
  state VARCHAR(2),
  observation NUMBER(5,2)
);

INSERT INTO preciptime VALUES
  ('14:42:59.230', 'Ahwahnee', 'CA', 0.91),
  ('14:42:59.001', 'Oakhurst', 'CA', 0.51),
  ('14:41:44.435', 'Las Vegas', 'NV', 0.01),
  ('14:42:44.435', 'Reno', 'NV', 0.01),
  ('14:40:34.000', 'Bozeman', 'MT', 1.11)
;

CREATE OR REPLACE TABLE snowtime(
  observed TIME(9),
  location VARCHAR(40),
  state VARCHAR(2),
  observation NUMBER(5,2)
);

INSERT INTO snowtime VALUES
  ('14:42:59.199', 'Fish Camp', 'CA', 3.20),
  ('14:42:44.435', 'Reno', 'NV', 3.00),
  ('14:43:01.000', 'Lake Tahoe', 'CA', 4.20),
  ('14:42:45.000', 'Bozeman', 'MT', 1.80)
;
```

When you run the first query, some of the TIME values appear to be exactly the same in the result set (`14:42:59`, `14:42:44`).

Copy code

```
SELECT * FROM preciptime p ASOF JOIN snowtime s MATCH_CONDITION(p.observed>=s.observed)
  ORDER BY p.observed;
```

```
+----------+-----------+-------+-------------+----------+-----------+-------+-------------+
| OBSERVED | LOCATION  | STATE | OBSERVATION | OBSERVED | LOCATION  | STATE | OBSERVATION |
|----------+-----------+-------+-------------+----------+-----------+-------+-------------|
| 14:40:34 | Bozeman   | MT    |        1.11 | NULL     | NULL      | NULL  |        NULL |
| 14:41:44 | Las Vegas | NV    |        0.01 | NULL     | NULL      | NULL  |        NULL |
| 14:42:44 | Reno      | NV    |        0.01 | 14:42:44 | Reno      | NV    |        3.00 |
| 14:42:59 | Oakhurst  | CA    |        0.51 | 14:42:45 | Bozeman   | MT    |        1.80 |
| 14:42:59 | Ahwahnee  | CA    |        0.91 | 14:42:59 | Fish Camp | CA    |        3.20 |
+----------+-----------+-------+-------------+----------+-----------+-------+-------------+
```

To return a more precise display of TIME values, including milliseconds, run the following [ALTER SESSION](/sql-reference/sql/alter-session) command,
then run the ASOF JOIN query again:

Copy code

```
ALTER SESSION SET TIME_OUTPUT_FORMAT = 'HH24:MI:SS.FF3';
```

```
+----------------------------------+
| status                           |
|----------------------------------|
| Statement executed successfully. |
+----------------------------------+
```

Copy code

```
SELECT * FROM preciptime p ASOF JOIN snowtime s MATCH_CONDITION(p.observed>=s.observed)
  ORDER BY p.observed;
```

```
+--------------+-----------+-------+-------------+--------------+-----------+-------+-------------+
| OBSERVED     | LOCATION  | STATE | OBSERVATION | OBSERVED     | LOCATION  | STATE | OBSERVATION |
|--------------+-----------+-------+-------------+--------------+-----------+-------+-------------|
| 14:40:34.000 | Bozeman   | MT    |        1.11 | NULL         | NULL      | NULL  |        NULL |
| 14:41:44.435 | Las Vegas | NV    |        0.01 | NULL         | NULL      | NULL  |        NULL |
| 14:42:44.435 | Reno      | NV    |        0.01 | 14:42:44.435 | Reno      | NV    |        3.00 |
| 14:42:59.001 | Oakhurst  | CA    |        0.51 | 14:42:45.000 | Bozeman   | MT    |        1.80 |
| 14:42:59.230 | Ahwahnee  | CA    |        0.91 | 14:42:59.199 | Fish Camp | CA    |        3.20 |
+--------------+-----------+-------+-------------+--------------+-----------+-------+-------------+
```

### Multiple ASOF joins in a query

The following example shows how to connect a sequence of two or more ASOF joins in a single query block.
The three tables (`snowtime`, `raintime`, `preciptime`) all contain weather observations that were recorded in
specific locations at specific times. The column of interest is the `observation` column. The rows are logically grouped by state.

Copy code

```
ALTER SESSION SET TIME_OUTPUT_FORMAT = 'HH24:MI:SS.FF3';

SELECT *
  FROM snowtime s
    ASOF JOIN raintime r
      MATCH_CONDITION(s.observed>=r.observed)
      ON s.state=r.state
    ASOF JOIN preciptime p
      MATCH_CONDITION(s.observed>=p.observed)
      ON s.state=p.state
  ORDER BY s.observed;
```

```
+--------------+------------+-------+-------------+--------------+----------+-------+-------------+--------------+----------+-------+-------------+
| OBSERVED     | LOCATION   | STATE | OBSERVATION | OBSERVED     | LOCATION | STATE | OBSERVATION | OBSERVED     | LOCATION | STATE | OBSERVATION |
|--------------+------------+-------+-------------+--------------+----------+-------+-------------+--------------+----------+-------+-------------|
| 14:42:44.435 | Reno       | NV    |        3.00 | 14:42:44.435 | Reno     | NV    |        0.00 | 14:42:44.435 | Reno     | NV    |        0.01 |
| 14:42:45.000 | Bozeman    | MT    |        1.80 | NULL         | NULL     | NULL  |        NULL | 14:40:34.000 | Bozeman  | MT    |        1.11 |
| 14:42:59.199 | Fish Camp  | CA    |        3.20 | 14:42:59.001 | Oakhurst | CA    |        0.50 | 14:42:59.001 | Oakhurst | CA    |        0.51 |
| 14:43:01.000 | Lake Tahoe | CA    |        4.20 | 14:42:59.230 | Ahwahnee | CA    |        0.90 | 14:42:59.230 | Ahwahnee | CA    |        0.91 |
+--------------+------------+-------+-------------+--------------+----------+-------+-------------+--------------+----------+-------+-------------+
```

### Less than and greater than comparison operators

Following on from the previous example, two ASOF joins are specified, but this time the first match condition uses the `>`
operator and the second uses the `<` operator. The result is a single row that returns data from all three tables, and three rows
that return data from two of the tables. Many of the columns in the result set are null-padded.

Logically, the query finds only one row where the observed time from the `snowtime` table was later than the observed time from the
`raintime` table but earlier than the observed time from the `preciptime` table.

Copy code

```
SELECT *
  FROM snowtime s
    ASOF JOIN raintime r
      MATCH_CONDITION(s.observed>r.observed)
      ON s.state=r.state
    ASOF JOIN preciptime p
      MATCH_CONDITION(s.observed<p.observed)
      ON s.state=p.state
  ORDER BY s.observed;
```

```
+--------------+------------+-------+-------------+--------------+-----------+-------+-------------+--------------+----------+-------+-------------+
| OBSERVED     | LOCATION   | STATE | OBSERVATION | OBSERVED     | LOCATION  | STATE | OBSERVATION | OBSERVED     | LOCATION | STATE | OBSERVATION |
|--------------+------------+-------+-------------+--------------+-----------+-------+-------------+--------------+----------+-------+-------------|
| 14:42:44.435 | Reno       | NV    |        3.00 | 14:41:44.435 | Las Vegas | NV    |        0.00 | NULL         | NULL     | NULL  |        NULL |
| 14:42:45.000 | Bozeman    | MT    |        1.80 | NULL         | NULL      | NULL  |        NULL | NULL         | NULL     | NULL  |        NULL |
| 14:42:59.199 | Fish Camp  | CA    |        3.20 | 14:42:59.001 | Oakhurst  | CA    |        0.50 | 14:42:59.230 | Ahwahnee | CA    |        0.91 |
| 14:43:01.000 | Lake Tahoe | CA    |        4.20 | 14:42:59.230 | Ahwahnee  | CA    |        0.90 | NULL         | NULL     | NULL  |        NULL |
+--------------+------------+-------+-------------+--------------+-----------+-------+-------------+--------------+----------+-------+-------------+
```

### Examples of expected error cases

The following examples show queries that return expected syntax errors.

Having declared that `snowtime s` is the left table, you cannot begin the match condition with a reference to the right table, `preciptime p`:

Copy code

```
SELECT * FROM snowtime s ASOF JOIN preciptime p MATCH_CONDITION(p.observed>=s.observed);
```

```
010002 (42601): SQL compilation error:
MATCH_CONDITION clause is invalid: The left side allows only column references from the left side table, and the right side allows only column references from the right side table.
```

Only the `>=`, `<=`, `>`, and `<` operators are allowed in match conditions:

Copy code

```
SELECT * FROM preciptime p ASOF JOIN snowtime s MATCH_CONDITION(p.observed=s.observed);
```

```
010001 (42601): SQL compilation error:
MATCH_CONDITION clause is invalid: Only comparison operators '>=', '>', '<=' and '<' are allowed. Keywords such as AND and OR are not allowed.
```

The ON clause for ASOF JOIN must contain equality conditions:

Copy code

```
SELECT *
  FROM preciptime p ASOF JOIN snowtime s
  MATCH_CONDITION(p.observed>=s.observed)
  ON s.state>=p.state;
```

```
010010 (42601): SQL compilation error:
ON clause for ASOF JOIN must contain conjunctions of equality conditions only. Disjunctions are not allowed. Each side of an equality condition must only refer to either the left table or the right table. S.STATE >= P.STATE is invalid.
```

An ON clause equality condition cannot contain disjunctions:

Copy code

```
SELECT *
  FROM preciptime p ASOF JOIN snowtime s
  MATCH_CONDITION(p.observed>=s.observed)
  ON s.state=p.state OR s.location=p.location;
```

```
010010 (42601): SQL compilation error:
ON clause for ASOF JOIN must contain conjunctions of equality conditions only. Disjunctions are not allowed. Each side of an equality condition must only refer to either the left table or the right table. (S.STATE = P.STATE) OR (S.LOCATION = P.LOCATION) is invalid.
```

ASOF joins cannot be used with LATERAL inline views:

Copy code

```
SELECT t1.a "t1a", t2.a "t2a"
  FROM t1 ASOF JOIN
    LATERAL(SELECT a FROM t2 WHERE t1.b = t2.b) t2
    MATCH_CONDITION(t1.a >= t2.a)
  ORDER BY 1,2;
```

```
010004 (42601): SQL compilation error:
ASOF JOIN is not supported for joins with LATERAL table functions or LATERAL views.
```
