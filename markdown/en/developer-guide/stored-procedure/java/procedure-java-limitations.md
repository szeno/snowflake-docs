# Java stored procedure limitations

## Limitations

Stored procedures have the following limitations:

- Concurrency isn’t supported. For example, from within your code, you can’t submit queries from multiple threads. Code that
  concurrently issues multiple queries will produce an error.
- Consider the following limitations when you use some Snowpark APIs in your stored procedure:

  - When you use [APIs that execute PUT and GET commands](/developer-guide/snowpark/java/working-with-dataframes#label-snowpark-java-dataframe-stages-file-operation) (including
    `Session.sql("PUT ...")` and `Session.sql("GET ...")`), you may write only to the /tmp directory in the memory-backed
    file system provided for the query calling the procedure.
  - Do not use [APIs that create new sessions](/developer-guide/snowpark/java/creating-session#label-snowpark-java-creating-session) (for example,
    `Session.builder().configs(...).create()`).
  - Using `session.jdbcConnection` (and the connection returned from it) is not supported because it may result in unsafe behavior.
- Creating named temp objects is not supported in an owner’s rights stored procedure. An owner’s rights stored procedure is a stored
  procedure that runs with the privileges of the stored procedure owner.
  For more information, refer to [caller’s rights or owner’s rights](/developer-guide/stored-procedure/stored-procedures-rights).
