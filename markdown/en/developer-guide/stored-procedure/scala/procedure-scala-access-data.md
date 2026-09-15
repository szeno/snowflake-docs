# Accessing data with Scala from stored procedures created with SQL

To access data with a stored procedure handler written in Scala, use the Snowpark library APIs.

When handling a call to your Scala stored procedure, Snowflake creates a Snowpark `Session` object and passes the object to
the method or function for your stored procedure.

As is the case with stored procedures whose handlers are written in other languages, the context for the session (including the privileges,
current database and schema, and so on) is determined by whether the stored procedure runs with caller’s rights or owner’s rights. For
details, see [Accessing and setting the session state](/developer-guide/stored-procedure/stored-procedures-rights#label-stored-procedure-session-state).

You can use this `Session` object to call APIs in the
[Snowpark library](https://docs.snowflake.com/en/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/index.html).
For example, you can [create a DataFrame for a table](/developer-guide/snowpark/scala/working-with-dataframes) or execute a
SQL statement.

See the [Snowpark Developer Guide for Scala](/developer-guide/snowpark/scala/index) for more information.

Note

For information about limitations, including limitations on accessing data, see [Limitations for Scala in stored procedures created with SQL](/developer-guide/stored-procedure/scala/procedure-scala-limitations).

## Data access example

The following is an example of a Scala method that copies a specified number of rows from one table to another table. The method
takes the following arguments:

- A Snowpark `Session` object
- The name of the table to copy the rows from
- The name of the table to save the rows to
- The number of rows to copy

The method in this example returns a string.

Copy code

```
object MyObject
{
  def myProcedure(session: com.snowflake.snowpark.Session, fromTable: String, toTable: String, count: Int): String =
  {
    session.table(fromTable).limit(count).write.saveAsTable(toTable)
    return "Success"
  }
}
```

The following example defines a function, rather than a method:

Copy code

```
object MyObject
{
  val myProcedure = (session: com.snowflake.snowpark.Session, fromTable: String, toTable: String, count: Int): String =>
  {
    session.table(fromTable).limit(count).write.saveAsTable(toTable)
    "Success"
  }
}
```
