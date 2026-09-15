# Python stored procedure limitations

Stored procedures have the following limitations:

- Creating processes is not supported in stored procedures.
- Running concurrent queries is not supported in stored procedures.
- You cannot use APIs that execute PUT and GET commands, including `Session.sql("PUT ...")` and `Session.sql("GET ...")`.
- When you download files from a stage using `session.file.get`, pattern matching is not supported.
- Creating named temp objects is not supported in an owner’s rights stored procedure. An owner’s rights stored procedure is a stored
  procedure that runs with the privileges of the stored procedure owner.
  For more information, refer to [caller’s rights or owner’s rights](/developer-guide/stored-procedure/stored-procedures-rights).
