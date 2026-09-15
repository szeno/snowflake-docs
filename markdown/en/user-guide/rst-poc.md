# Pipeline Comparison POC

This page demonstrates the documentation component set. Compare it with the MDX version to see rendering differences between the two pipelines.

Note

This is a **note** admonition.

Warning

Watch out

This is a warning with a custom title.

Here is a SQL code block:

Copy code

```
SELECT *
FROM my_table
WHERE created_at > DATEADD(day, -7, CURRENT_TIMESTAMP())
ORDER BY created_at DESC;
```

Copy code

```
import snowflake.connector

conn = snowflake.connector.connect(
    user='myuser',
    password='mypassword',
    account='myaccount'
)
```

## Tabs example

SQLPython

Copy code

```
CREATE TABLE my_table (id INT, name STRING);
```

Copy code

```
cur.execute("CREATE TABLE my_table (id INT, name STRING)")
```

## Table example

| Column A | Column B | Column C |
| --- | --- | --- |
| Row 1 | Value | 100 |
| Row 2 | Value | 200 |
| Row 3 | Value | 300 |

Expand

Show lessSee more

Standard Edition Feature

This feature requires Snowflake Standard Edition or higher.
