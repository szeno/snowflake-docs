# Designing Handlers that Stay Within Snowflake-Imposed Constraints

To ensure stability within the Snowflake environment, Snowflake places the following constraints on handler code. Unless stated otherwise,
these limitations are enforced when the handler is executed, not when it is created.

## Avoid Consuming Too Much Memory

Avoid the following, which can consume large amounts of memory:

- Large data values. These can include binary values, as well as large arrays, objects, or variant.

  Snowflake converts between SQL data types and corresponding types in the handler language. For more information, see
  [Data Type Mappings Between SQL and Handler Languages](/developer-guide/udf-stored-procedure-data-type-mapping).
- Excessive stack depth. Snowflake has tested simple function calls nested 50 levels deep without error. The practical maximum limit
  depends upon how much information is put on the stack.

Handler code will return an error if it consumes too much memory. The specific limit is subject to change.

## Avoid Algorithms That Take a Large Amount of Time Per Call

If a handler takes too long to complete, Snowflake kills the SQL statement and returns an error to the user. This limits
the impact and cost of errors such as infinite loops.

## Don’t Use Libraries That Could Introduce Security Vulnerabilities

Although your handler can use functionality in external libraries, Snowflake security restrictions disable some
capabilities, such as writing to files. For details about library restrictions, see
[Security Practices for UDFs and Procedures](/developer-guide/udf-stored-procedure-security-practices).
