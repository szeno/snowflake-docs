# Calling an external function for AWS

This topic describes how to call an external function.

An external function is called like any other [UDF (user-defined function)](/developer-guide/udf/udf-overview). (And, like any
other UDF, an external function is called the same way regardless of platform.)

1. If you have not already done so, make sure that your session is using the database and schema that contain the function.

   (External functions are database objects; when you call the function, the database and schema containing the function must be in
   use in your session, or you must specify the fully-qualified name of the function.)

   Copy code

   ```
   USE DATABASE <database_name>;
   USE SCHEMA <schema_name>;
   ```
2. If appropriate, and if you have not already done so, grant USAGE privilege on the external function to one or more Snowflake
   roles that need to call the external function.

   (A role must have USAGE or OWNERSHIP privileges on an external function to call it.)

   Copy code

   ```
   GRANT USAGE ON FUNCTION <external_function_name>(<parameter_data_type>) TO <role_name>;
   ```

   For example:

   Copy code

   ```
   GRANT USAGE ON FUNCTION echo(INTEGER, VARCHAR) TO analyst_role;
   ```
3. Using an appropriate role, call your external function as part of an SQL statement. If you created one of the sample external
   functions supplied by Snowflake, you can call the function as shown below:

   > Copy code
   >
   > ```
   > SELECT echo(42, 'Adams');
   > ```

   If you used a function name other than `echo`, then replace `echo` with the actual function name.

   The returned value should be similar to:

   > Copy code
   >
   > ```
   > [0, 42, "Adams"]
   > ```

   Where:

   - `0` is the row number of the returned value.
   - `42, "Adams"` is the returned value.

Note

Although an external function can usually be called like other UDFs, there are a handful of exceptions. For details,
see [Execution-time limitations and issues](/sql-reference/external-functions-introduction#label-external-functions-limitations-execution).
