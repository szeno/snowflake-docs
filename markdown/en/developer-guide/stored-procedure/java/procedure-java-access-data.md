# Accessing data from a Java stored procedure

To access data with a stored procedure handler written in Java, use the Snowpark library APIs.

When handling a call to your Java stored procedure, Snowflake creates a Snowpark `Session` object and passes the object to
the method for your stored procedure.

As is the case with stored procedures in other languages, the context for the session (including the privileges, current database and
schema, and so on) is determined by whether the stored procedure runs with caller’s rights or owner’s rights. For details, see
[Accessing and setting the session state](/developer-guide/stored-procedure/stored-procedures-rights#label-stored-procedure-session-state).

You can use this `Session` object to call APIs in the
[Snowpark library](https://docs.snowflake.com/en/developer-guide/snowpark/reference/java/index.html).
For example, you can [create a DataFrame for a table](/developer-guide/snowpark/java/working-with-dataframes) or execute an
SQL statement.

See the [Snowpark Developer Guide for Java](/developer-guide/snowpark/java/index) for more information.

Note

For information about limitations, including limitations on accessing data, see [Java stored procedure limitations](/developer-guide/stored-procedure/java/procedure-java-limitations).

## Data access example

In the following example, a Java method copies a specified number of rows from one table to another table. The method takes the following
arguments:

- A Snowpark `Session` object
- The name of the table to copy the rows from
- The name of the table to save the rows to
- The number of rows to copy

The method in this example returns a string.

Copy code

```
import com.snowflake.snowpark_java.*;

public class MyClass
{
  public String myMethod(Session session, String fromTable, String toTable, int count)
  {
    session.table(fromTable).limit(count).write().saveAsTable(toTable);
    return "Success";
  }
}
```
