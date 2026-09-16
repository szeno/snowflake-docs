# Python stored procedure limitations

Stored procedures have the following limitations:

- The built-in Python `multiprocessing` module is not supported. To run CPU-bound tasks in parallel, use the `Parallel` class from the `joblib` library instead. For more information, see [Running concurrent tasks with worker processes](/developer-guide/stored-procedure/python/procedure-python-examples#running-concurrent-tasks-with-worker-processes).
- You cannot use APIs that execute PUT and GET commands, including `Session.sql("PUT ...")` and `Session.sql("GET ...")`.
- When you download files from a stage using `session.file.get`, pattern matching is not supported.
- Creating named temp objects is not supported in an owner’s rights stored procedure. An owner’s rights stored procedure is a stored
  procedure that runs with the privileges of the stored procedure owner.
  For more information, refer to [caller’s rights or owner’s rights](/developer-guide/stored-procedure/stored-procedures-rights).
