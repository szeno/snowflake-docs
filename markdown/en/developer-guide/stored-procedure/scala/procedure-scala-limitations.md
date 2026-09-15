# Limitations for Scala in stored procedures created with SQL

Stored procedures have the following limitations:

- Concurrency is not supported. For example, from within your code, you cannot submit queries
  from multiple threads. Code that concurrently issues multiple queries will produce an error.
- If you are executing your stored procedure from a task, you must specify a warehouse when creating the task. (You cannot use
  serverless compute resources to run the task.)
- Keep in mind the following limitations for using some Snowpark APIs in your stored procedure.

  - When you use [APIs that execute PUT and GET commands](/developer-guide/snowpark/scala/working-with-dataframes#label-snowpark-dataframe-stages-file-operation) (including
    `Session.sql("PUT ...")` and `Session.sql("GET ...")`), you may write only to the `/tmp` directory in the memory-backed
    file system provided for the query calling the procedure.
  - Do not use [APIs that create new sessions](/developer-guide/snowpark/scala/creating-session#label-snowpark-creating-session) (for example,
    `Session.builder().configs(...).create()`).
  - Using `session.jdbcConnection` (and the connection returned from it) is not supported because it can result in unsafe behavior.
- Creating named temp objects is not supported in an owner’s rights stored procedure. An owner’s rights stored procedure is a stored
  procedure that runs with the privileges of the stored procedure owner.
  For more information, refer to [caller’s rights or owner’s rights](/developer-guide/stored-procedure/stored-procedures-rights).
