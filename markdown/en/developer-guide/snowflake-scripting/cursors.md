# Working with cursors

You can use a cursor to iterate through query results one row at a time.

## Introduction

To retrieve data from the results of a query, you can use a cursor. To iterate over the rows in the results,
you can use a cursor in [loops](/developer-guide/snowflake-scripting/loops).

To use a cursor, do the following:

1. In the [DECLARE](/sql-reference/snowflake-scripting/declare) section,
   [declare the cursor](#label-snowscript-cursors-declare). The declaration includes the query for the cursor.
2. Before you use the cursor for the first time, execute the [OPEN](/sql-reference/snowflake-scripting/open) command to
   [open the cursor](#label-snowscript-cursors-open). This executes the query and loads the results into the cursor.
3. Execute the [FETCH](/sql-reference/snowflake-scripting/fetch) command to
   [fetch one or more rows](#label-snowscript-cursors-fetch) and process those rows.
4. When you are done with the results or the cursor is no longer needed, execute the [CLOSE](/sql-reference/snowflake-scripting/close)
   command to [close the cursor](#label-snowscript-cursors-close).

Note

You can also use a RESULTSET to retrieve the results of a query when you use Snowflake Scripting. For information
about the differences between a cursor and a RESULTSET, see [Understanding the differences between a cursor and a RESULTSET](/developer-guide/snowflake-scripting/resultsets#label-snowscript-resultsets-cursor-diff).

## Setting up the data for the examples

The examples in this section uses the following data:

Copy code

```
CREATE OR REPLACE TABLE invoices (id INTEGER, price NUMBER(12, 2));

INSERT INTO invoices (id, price) VALUES
  (1, 11.11),
  (2, 22.22);
```

## Declaring a cursor

You can declare a cursor for a SELECT statement or a [RESULTSET](/developer-guide/snowflake-scripting/resultsets).

You declare a cursor in the [DECLARE](/sql-reference/snowflake-scripting/declare) section of a block or in the
[BEGIN … END](/sql-reference/snowflake-scripting/begin) section of the block:

- Within the DECLARE section, use the syntax described in [Cursor declaration syntax](/sql-reference/snowflake-scripting/declare#label-snowscript-declare-syntax-cursor).

  For example, to declare a cursor for a query:

  Copy code

  ```
  DECLARE
    ...
    c1 CURSOR FOR SELECT price FROM invoices;
  ```

  To declare a cursor for a RESULTSET:

  Copy code

  ```
  DECLARE
    ...
    res RESULTSET DEFAULT (SELECT price FROM invoices);
    c1 CURSOR FOR res;
  ```
- Within the BEGIN … END block, use the syntax described in [Cursor assignment syntax](/sql-reference/snowflake-scripting/let#label-snowscript-let-syntax-cursor). For example:

  Copy code

  ```
  BEGIN
    ...
    LET c1 CURSOR FOR SELECT price FROM invoices;
  ```

In the SELECT statement, you can specify bind parameters (`?` characters) that you can bind to variables when opening the
cursor. To bind variables to the parameters, specify the variables in the USING clause of the OPEN command. For example:

Copy code

```
DECLARE
  id INTEGER DEFAULT 0;
  minimum_price NUMBER(13,2) DEFAULT 22.00;
  maximum_price NUMBER(13,2) DEFAULT 33.00;
  c1 CURSOR FOR SELECT id FROM invoices WHERE price > ? AND price < ?;
BEGIN
  OPEN c1 USING (minimum_price, maximum_price);
  FETCH c1 INTO id;
  RETURN id;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
DECLARE
  id INTEGER DEFAULT 0;
  minimum_price NUMBER(13,2) DEFAULT 22.00;
  maximum_price NUMBER(13,2) DEFAULT 33.00;
  c1 CURSOR FOR SELECT id FROM invoices WHERE price > ? AND price < ?;
BEGIN
  OPEN c1 USING (minimum_price, maximum_price);
  FETCH c1 INTO id;
  RETURN id;
END;
$$
;
```

```
+-----------------+
| anonymous block |
|-----------------|
|               2 |
+-----------------+
```

## Opening a cursor

Although the statement that declares a cursor defines the query associated with that cursor, the query is not executed until you
open the cursor by executing the [OPEN](/sql-reference/snowflake-scripting/open) command. For example:

Copy code

```
OPEN c1;
```

Note

- When using a cursor in a [FOR](/developer-guide/snowflake-scripting/loops#label-snowscript-loop-for) loop, you do not need to open the cursor explicitly.
- If you declare a cursor for a RESULTSET object, the query is executed when you associate the object with the query. In this
  case, opening the cursor does not cause the query to be executed again.

If your query contains any bind parameters (`?` characters), add a USING clause to specify the list of variables to bind
to those parameters. For example:

Copy code

```
LET c1 CURSOR FOR SELECT id FROM invoices WHERE price > ? AND price < ?;
OPEN c1 USING (minimum_price, maximum_price);
```

Opening the cursor executes the query, retrieves the specified rows into the cursor, and sets up an internal pointer that points
to the first row. You can use the FETCH command to
[fetch (read) individual rows using the cursor](#label-snowscript-cursors-fetch).

As with any SQL query, if the query definition does not contain an ORDER BY at the outermost level, then the result set has no
defined order. When the result set for the cursor is created, the order of the rows is persistent until the cursor is closed.
If you declare or open the cursor again, the rows might be in a different order. Similarly, if you close the cursor and
the underlying table is updated before you open the cursor again, the result set can change.

## Using a cursor to fetch data

Use the [FETCH](/sql-reference/snowflake-scripting/fetch) command to retrieve the current row from the result set and
advance the internal current row pointer to point to the next row in the result set.

In the INTO clause, specify the variables that hold the values from the row.

For example:

Copy code

```
FETCH c1 INTO var_for_column_value;
```

If the number of variables does not match the number of expressions in the SELECT clause of the cursor declaration, Snowflake
attempts to match the variables with the columns by position:

- If there are more variables than columns, Snowflake leaves the remaining variables unset.
- If there are more columns than variables, Snowflake ignores the remaining columns.

Each subsequent FETCH command that you execute gets the next row until the last row has been fetched. If you try to FETCH
a row after the last row, you get NULL values.

A RESULTSET or cursor does not necessarily cache all the rows of the result set at the time that the query is executed. FETCH operations can experience latency.

## Using a cursor to retrieve a GEOGRAPHY value

If the results include a column of the type GEOGRAPHY, the type of the value in the column is OBJECT, not GEOGRAPHY. This means
that you cannot directly pass this value to [geospatial functions](/sql-reference/functions-geospatial) that accept a
GEOGRAPHY object as input:

Copy code

```
DECLARE
  geohash_value VARCHAR;
BEGIN
  LET res RESULTSET := (SELECT TO_GEOGRAPHY('POINT(1 1)') AS GEOGRAPHY_VALUE);
  LET cur CURSOR FOR res;
  FOR row_variable IN cur DO
    geohash_value := ST_GEOHASH(row_variable.geography_value);
  END FOR;
  RETURN geohash_value;
END;
```

Copy code

```
001044 (42P13): Uncaught exception of type 'EXPRESSION_ERROR' on line 7 at position 21 : SQL compilation error: ...
Invalid argument types for function 'ST_GEOHASH': (OBJECT)
```

To work around this, cast the column value to the GEOGRAPHY type:

Copy code

```
geohash_value := ST_GEOHASH(TO_GEOGRAPHY(row_variable.geography_value));
```

## Returning a table for a cursor

If you need to return a table of data from a cursor, you can pass the cursor to `RESULTSET_FROM_CURSOR(cursor)`, which in
turn you can pass to `TABLE(...)`.

The following block returns a table of data from a cursor:

Copy code

```
DECLARE
  c1 CURSOR FOR SELECT * FROM invoices;
BEGIN
  OPEN c1;
  RETURN TABLE(RESULTSET_FROM_CURSOR(c1));
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
DECLARE
  c1 CURSOR FOR SELECT * FROM invoices;
BEGIN
  OPEN c1;
  RETURN TABLE(RESULTSET_FROM_CURSOR(c1));
END;
$$
;
```

```
+----+-------+
| ID | PRICE |
|----+-------|
|  1 | 11.11 |
|  2 | 22.22 |
+----+-------+
```

Even if you have already used the cursor to [fetch rows](#label-snowscript-cursors-fetch),
`RESULTSET_FROM_CURSOR` still returns a RESULTSET containing all of the rows, not just the rows starting from the internal
row pointer.

As shown above, the example fetches the first row and sets the internal row pointer to the second row.
`RESULTSET_FROM_CURSOR` returns a RESULTSET containing both rows (not just the second row).

## Closing a cursor

When you are done with the result set, close the cursor by executing the [CLOSE](/sql-reference/snowflake-scripting/close)
command. For example:

Copy code

```
CLOSE c1;
```

Note

When using a cursor in a [FOR](/developer-guide/snowflake-scripting/loops#label-snowscript-loop-for) loop, you do not need to close the cursor explicitly.

You cannot execute the FETCH command on a cursor that has been closed.

In addition, after you close a cursor, the current row pointer becomes invalid. If you open the cursor again, the pointer points
to the first row in the new result set.

## Example of using a cursor

This example uses data that you set up in [Setting up the data for the examples](#label-snowscript-cursors-example-setup).

Here is an anonymous block that uses a cursor to read two rows and sum the prices in those rows:

Copy code

```
DECLARE
  row_price FLOAT;
  total_price FLOAT;
  c1 CURSOR FOR SELECT price FROM invoices;
BEGIN
  row_price := 0.0;
  total_price := 0.0;
  OPEN c1;
  FETCH c1 INTO row_price;
  total_price := total_price + row_price;
  FETCH c1 INTO row_price;
  total_price := total_price + row_price;
  CLOSE c1;
  RETURN total_price;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
DECLARE
    row_price FLOAT;
    total_price FLOAT;
    c1 CURSOR FOR SELECT price FROM invoices;
BEGIN
    row_price := 0.0;
    total_price := 0.0;
    OPEN c1;
    FETCH c1 INTO row_price;
    total_price := total_price + row_price;
    FETCH c1 INTO row_price;
    total_price := total_price + row_price;
    CLOSE c1;
    RETURN total_price;
END;
$$
;
```

```
+-----------------+
| anonymous block |
|-----------------|
|           33.33 |
+-----------------+
```

You can achieve the same result by using a cursor with a [FOR loop](/developer-guide/snowflake-scripting/loops#label-snowscript-loop-for):

Copy code

```
DECLARE
  total_price FLOAT;
  c1 CURSOR FOR SELECT price FROM invoices;
BEGIN
  total_price := 0.0;
  FOR record IN c1 DO
    total_price := total_price + record.price;
  END FOR;
  RETURN total_price;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
DECLARE
  total_price FLOAT;
  c1 CURSOR FOR SELECT price FROM invoices;
BEGIN
  total_price := 0.0;
  FOR record IN c1 DO
    total_price := total_price + record.price;
  END FOR;
  RETURN total_price;
END;
$$
;
```

```
+-----------------+
| anonymous block |
|-----------------|
|           33.33 |
+-----------------+
```

## Troubleshooting problems with cursors

The following section describes common problems with cursors and identifies a possible cause and solution in each case.

### Symptom: Cursor retrieves every second row rather than every row

- **Possible cause:** You might have executed FETCH inside a FOR `<record>` IN `<cursor>` loop. A FOR loop over a cursor
  automatically fetches the next row. If you do another fetch inside the loop, you get every second row.
- **Possible solution:** Remove any unneeded FETCH commands inside a FOR loop.

### Symptom: FETCH command retrieves unexpected NULL values

- **Possible cause:** You might have executed FETCH inside a FOR `<record>` IN `<cursor>` loop. A FOR loop over a cursor
  automatically fetches the next row. If you do another fetch inside the loop, you get every second row. If
  there is an odd number of rows, the last fetch will try to fetch a row beyond the last row, and the
  values will be NULL.
- **Possible solution:** Remove any unneeded FETCH commands inside a FOR loop.
