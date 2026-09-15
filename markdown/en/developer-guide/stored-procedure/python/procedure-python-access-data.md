# Accessing data from a Python stored procedure

You can access data from a stored procedure by using the Snowpark library APIs.

You can use the `Session` object that Snowflake creates for your stored procedure to access data by calling APIs in the
[Snowpark library](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/index).
For example, you can [create a DataFrame for a table](/developer-guide/snowpark/python/working-with-dataframes#label-snowpark-python-dataframes) or execute a SQL statement.

The context for the session (including the privileges, current database and schema, and so on) is determined by whether the stored
procedure runs with [caller’s rights or owner’s rights](/developer-guide/stored-procedure/stored-procedures-rights). For details,
see [Accessing and setting the session state](/developer-guide/stored-procedure/stored-procedures-rights#label-stored-procedure-session-state).

See the [Snowpark Developer Guide](/developer-guide/snowpark/python/index) for more information.

## Data access example

In the following example, a Python method copies a specified number of rows from one table to another table. The method takes the
following arguments:

- A Snowpark `Session` object
- The name of the table to copy the rows from
- The name of the table to save the rows to
- The number of rows to copy

The method in this example returns a string. If you run this example in a
[Python worksheet](/developer-guide/snowpark/python/python-worksheets),
[change the return type for the worksheet](/developer-guide/snowpark/python/python-worksheets#label-snowsight-py-worksheets-return) to a **String**

Copy code

```
def run(session, from_table, to_table, count):

  session.table(from_table).limit(count).write.save_as_table(to_table)

  return "SUCCESS"
```
