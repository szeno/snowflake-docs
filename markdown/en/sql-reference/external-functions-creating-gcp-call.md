# Calling an external function for GCP

This topic describes how to call an external function:

1. If appropriate, grant USAGE privilege on the external function to one or more Snowflake roles so that the roles can call the external
   function. A role must have USAGE or OWNERSHIP privileges on that external function.
2. Call your external function as you would execute any UDF. For example, if you create the sample function provided by Snowflake:

   Copy code

   ```
   select my_external_function(42, 'Life, the Universe, and Everything');
   ```

   If you customized the function name when you created the function, then replace `my_external_function` with the customized name.

   The returned value should be similar to:

   Copy code

   ```
   [42, "Life, the Universe, and Everything"]
   ```

Note

External functions are schema objects so the schema containing the function must be in use in your session or you must specify the
fully-qualified name of the function when calling it.
