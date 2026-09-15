# Security Practices for UDFs and Procedures

This topic describes best practices for writing secure user-defined functions (UDFs) and procedures.

## Practices for UDF Handlers

Your function or method (and any library functions or methods that you call) must act as a pure function, acting only on the data it receives
and returning a value based on that data, without causing side-effects. Your code should not attempt to affect the
state of the underlying system, other than consuming a reasonable amount of memory and processor time.

## Practices for Procedure and UDF Handlers

Handler code executes within a restricted engine. Neither your code nor the code in library methods that you use
should employ any prohibited system calls, including:

- Access to the file system on which the handler is running.

  With the following exceptions, a handler should not read or write files:

  - A handler can read staged files specified in the IMPORTS clause. For more information, see [CREATE FUNCTION](/sql-reference/sql/create-function)
    or [CREATE PROCEDURE](/sql-reference/sql/create-procedure).
  - A handler can write files, such as log files, to the `/tmp` directory.

    Each query gets its own memory-backed file system in which its own `/tmp` is stored, so different queries cannot
    have file name conflicts.

    However, conflicts within a query are possible if a single query calls more than one UDF, and those UDFs
    try to write to the same file name.

    Note

    Also, because Python UDFs may execute in separate worker processes in parallel, you should
    be careful about writing into the /tmp directory.

    For more on writing files, see [Writing files](/developer-guide/udf/python/udf-python-examples#label-udf-python-write-files). For an example, see
    [Unzipping a staged file](/developer-guide/udf/python/udf-python-examples#label-udf-python-unzipping-file-from-stage).
  - A handler can write files to stages using user-defined functions (UDFs), vectorized UDFs, user-defined table functions (UDTFs), and vectorized UDTFs. For more information, see [Writing files from Snowpark Python UDFs and UDTFs](/developer-guide/snowpark/python/creating-udfs#label-snowpark-python-udf-write-files).
  - In the Snowpark sandbox, handler code can read `/etc/hosts`, `/etc/passwd`, and `/etc/shadow`.

    Note

    These files are provided by the sandbox environment and do not contain sensitive information from the underlying system. Accessing these files does not pose a security concern.
- Network access.

  You can’t use a handler to create sockets, but you can use a handler to
  [access resources on an external network](/developer-guide/external-network-access/external-network-access-overview).

  Note

  You cannot use the code in the Snowflake JDBC Driver to access the database. Your UDF cannot itself act as a client of Snowflake.

### For Handlers in Java or Scala

- When used within a [government region](/user-guide/intro-regions#label-us-gov-regions), Java UDFs support encryption algorithms that are validated to meet
  the Federal Information Processing Standard (140-2) (FIPS 140-2) requirements. Only cryptographic algorithms that are allowed in the
  FIPS approved mode of the BouncyCastle cryptography API for Java can be used.
  For information about FIPS 140-2, see [FIPS 140-2](https://csrc.nist.gov/publications/detail/fips/140/2/final).
