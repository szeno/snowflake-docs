# Determining the number of rows affected by SQL statements

After a [DML command](/sql-reference/sql-dml) is executed (excluding the [TRUNCATE TABLE](/sql-reference/sql/truncate-table)
command), Snowflake Scripting sets the following global variables. You can use these variables to determine if the last
DML statement affected any rows, or how many rows were returned by a query.

| Variable | Description |
| --- | --- |
| `ACTIVITY_COUNT` | Number of rows affected by the last DML statement, or the number of rows returned by the last SELECT query. Set after each statement execution. |
| `SQLROWCOUNT` | Number of rows affected by the last DML statement.  This is equivalent to `getNumRowsAffected()` in JavaScript stored procedures. |
| `SQLFOUND` | `true` if the last DML statement affected one or more rows. |
| `SQLNOTFOUND` | `true` if the last DML statement affected zero rows. |

Expand

Show lessSee more

Note

The [2025\_01 behavior change bundle](/release-notes/bcr-bundles/2025_01_bundle) changes the behavior
of these variables. When the bundle is enabled, the variables return NULL when a non-DML statement is executed
after the last DML statement in a Snowflake Scripting block or stored procedure. The bundle is enabled by
default. For more information about the behavior change, see [Snowflake Scripting: Changes to global variables](/release-notes/bcr-bundles/2025_01/bcr-1850).

If the bundle is disabled, you can [enable it in your account](/release-notes/bcr-bundles/managing-behavior-change-releases#label-manage-bcr-enable-bundle) by
executing the following statement:

Copy code

```
SELECT SYSTEM$ENABLE_BEHAVIOR_CHANGE_BUNDLE('2025_01');
```

To disable the bundle, execute the following statement:

Copy code

```
SELECT SYSTEM$DISABLE_BEHAVIOR_CHANGE_BUNDLE('2025_01');
```

The examples in this section use the following table:

Copy code

```
CREATE OR REPLACE TABLE my_values (value NUMBER);
```

The following example uses the `SQLROWCOUNT` variable to return the number of rows affected by the last
DML statement (the INSERT statement).

Copy code

```
BEGIN
  LET sql_row_count_var INT := 0;
  INSERT INTO my_values VALUES (1), (2), (3);
  sql_row_count_var := SQLROWCOUNT;
  SELECT * from my_values;
  RETURN sql_row_count_var;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
BEGIN
  LET sql_row_count_var INT := 0;
  INSERT INTO my_values VALUES (1), (2), (3);
  sql_row_count_var := SQLROWCOUNT;
  SELECT * from my_values;
  RETURN sql_row_count_var;
END;
$$;
```

```
+-----------------+
| anonymous block |
|-----------------|
|               3 |
+-----------------+
```

The following example uses the `SQLFOUND` and `SQLNOTFOUND` variables to return the number of rows affected by the
last DML statement (the UPDATE statement).

Copy code

```
BEGIN
  LET sql_row_count_var INT := 0;
  LET sql_found_var BOOLEAN := NULL;
  LET sql_notfound_var BOOLEAN := NULL;
  IF ((SELECT MAX(value) FROM my_values) > 2) THEN
    UPDATE my_values SET value = 4 WHERE value < 3;
    sql_row_count_var := SQLROWCOUNT;
    sql_found_var := SQLFOUND;
    sql_notfound_var := SQLNOTFOUND;
  END IF;
  SELECT * from my_values;
  IF (sql_found_var = true) THEN
    RETURN 'Updated ' || sql_row_count_var || ' rows.';
  ELSEIF (sql_notfound_var = true) THEN
    RETURN 'No rows updated.';
  ELSE
    RETURN 'No DML statements executed.';
  END IF;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
BEGIN
  LET sql_row_count_var INT := 0;
  LET sql_found_var BOOLEAN := NULL;
  LET sql_notfound_var BOOLEAN := NULL;
  IF ((SELECT MAX(value) FROM my_values) > 2) THEN
    UPDATE my_values SET value = 4 WHERE value < 3;
    sql_row_count_var := SQLROWCOUNT;
    sql_found_var := SQLFOUND;
    sql_notfound_var := SQLNOTFOUND;
  END IF;
  SELECT * from my_values;
  IF (sql_found_var = true) THEN
    RETURN 'Updated ' || sql_row_count_var || ' rows.';
  ELSEIF (sql_notfound_var = true) THEN
    RETURN 'No rows updated.';
  ELSE
    RETURN 'No DML statements executed.';
  END IF;
END;
$$;
```

When the anonymous block runs, the `SQLFOUND` variable is `true` because the UPDATE statement updates two rows.

```
+-----------------+
| anonymous block |
|-----------------|
| Updated 2 rows. |
+-----------------+
```

Query the table to see the current values:

Copy code

```
SELECT * FROM my_values;
```

```
+-------+
| VALUE |
|-------|
|     4 |
|     4 |
|     3 |
+-------+
```

Run the same anonymous block again, and the results are the following:

- The UPDATE statement is executed because there is a value in the table that is greater than `2`. That is,
  the IF condition is satisfied.
- The `SQLNOTFOUND` variable is `true` because no rows are updated. The UPDATE statement doesn’t update
  any rows because none of the values in the table are less than `3` (specified in the WHERE clause).

The query returns the following output:

```
+------------------+
| anonymous block  |
|------------------|
| No rows updated. |
+------------------+
```

Now, update the table to set all of the values to `1`:

Copy code

```
UPDATE my_values SET value = 1;

SELECT * FROM my_values;
```

```
+-------+
| VALUE |
|-------|
|     1 |
|     1 |
|     1 |
+-------+
```

Run the same anonymous block again, and the UPDATE statement isn’t executed because none of the values
in the table are greater than `2`. That is, the IF condition isn’t satisfied, so the UPDATE statement
doesn’t execute.

```
+-----------------------------+
| anonymous block             |
|-----------------------------|
| No DML statements executed. |
+-----------------------------+
```

## ACTIVITY\_COUNT examples

Unlike `SQLROWCOUNT`, the `ACTIVITY_COUNT` variable is set after each statement execution, including
SELECT queries. This makes it useful for tracking both the number of rows affected by DML operations and the number
of rows returned by queries.

The following example demonstrates `ACTIVITY_COUNT` after an INSERT statement and a SELECT query:

Copy code

```
BEGIN
  INSERT INTO my_values VALUES (1), (2), (3);
  LET insert_count INT := ACTIVITY_COUNT;
  SELECT * FROM my_values WHERE value > 1;
  LET select_count INT := ACTIVITY_COUNT;
  RETURN 'Inserted ' || insert_count || ' rows, query returned ' || select_count || ' rows.';
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
BEGIN
  INSERT INTO my_values VALUES (1), (2), (3);
  LET insert_count INT := ACTIVITY_COUNT;
  SELECT * FROM my_values WHERE value > 1;
  LET select_count INT := ACTIVITY_COUNT;
  RETURN 'Inserted ' || insert_count || ' rows, query returned ' || select_count || ' rows.';
END;
$$;
```

After the INSERT, `ACTIVITY_COUNT` is `3` (three rows inserted). After the SELECT,
`ACTIVITY_COUNT` is `2` (two rows match the `WHERE value > 1` condition).

```
+-------------------------------------------+
| anonymous block                           |
|-------------------------------------------|
| Inserted 3 rows, query returned 2 rows.   |
+-------------------------------------------+
```
