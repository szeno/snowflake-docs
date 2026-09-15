# Canceling Statements

The recommended way to cancel a statement is to use the interface of the application
in which the query is running (e.g. the Worksheet in the Snowflake web interface)
or the cancellation API provided by the Snowflake ODBC or JDBC driver. However,
in some cases, it is necessary to cancel a query using SQL.

Snowflake provides the following functions to support using SQL to cancel
running/active statements:

- [SYSTEM$CANCEL\_ALL\_QUERIES](/sql-reference/functions/system_cancel_all_queries)
- [SYSTEM$CANCEL\_QUERY](/sql-reference/functions/system_cancel_query)

## Example

The following Java sample code uses [SYSTEM$CANCEL\_ALL\_QUERIES](/sql-reference/functions/system_cancel_all_queries)
and other Snowflake functions to cancel a running statement in the current session
after 5 seconds:

1. The sample code first issues a SQL command for [CURRENT\_SESSION](/sql-reference/functions/current_session)
   to obtain the session identifier.
2. It then creates a task to be executed 5 seconds later. This task uses the
   session identifier as a parameter to SYSTEM$CANCEL\_ALL\_QUERIES.
3. Then a long running statement is executed using the [GENERATOR](/sql-reference/functions/generator)
   table function to generate rows for 120 seconds.

Copy code

```
public void testCancelQuery() throws IOException, SQLException
{
  Statement         statement         = null;
  ResultSet         resultSet         = null;
  ResultSetMetaData resultSetMetaData = null;
  final Connection  connection        = getConnection(true);
  try
  {
    // Get the current session identifier
    Statement getSessionIdStmt = connection.createStatement();
    resultSet                  = getSessionIdStmt.executeQuery("SELECT current_session()");
    resultSetMetaData          = resultSet.getMetaData();
    assertTrue(resultSet.next());
    final int sessionId = resultSet.getInt(1);

    // Use Timer to cancel all queries of session in 5 seconds
    Timer timer = new Timer();
    timer.schedule( new TimerTask()
    {
      @Override
      public void run()
      {
        try
        {
          // Cancel all queries on session
          PreparedStatement cancelAll;
          cancelAll = connection.prepareStatement(
                                    "call system$cancel_all_queries(?)");

          // bind the session identifier as first argument
          cancelAll.setInt(1, sessionId);
          cancelAll.executeQuery();
        }
        catch (SQLException ex)
        {
          logger.log(Level.SEVERE, "Cancel failed with exception {}", ex);
        }
      }
    }, 5000);

    // Use the internal row generator to execute a query for 120 seconds
    statement = connection.createStatement();
    resultSet = statement.executeQuery(
                   "SELECT count(*) FROM TABLE(generator(timeLimit => 120))");
    resultSetMetaData = resultSet.getMetaData();
    statement.close();
  }
  catch (SQLException ex)
  {
    // assert the sqlstate is what we expect (QUERY CANCELLED)
    assertEquals("sqlstate mismatch",
                 SqlState.QUERY_CANCELED, ex.getSQLState());
  }
  catch (Throwable ex)
  {
    logger.log(Level.SEVERE, "Test failed with exception: ", ex);
  }
  finally
  {
    if (resultSet != null)
      resultSet.close();
    if (statement != null)
      statement.close();
    // close connection
    if (connection != null)
      connection.close();
  }
}
```
