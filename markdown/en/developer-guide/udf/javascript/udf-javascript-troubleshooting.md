# Troubleshooting JavaScript UDFs

This topic provides information about troubleshooting JavaScript UDFs.

## Tips

- JavaScript is case sensitive, but SQL forces names to upper case. This can affect UDF input parameter names, for example.
  JavaScript code should reference input parameter names by using all upper case.
- If using a JavaScript UDF in a [masking policy](/sql-reference/sql/create-masking-policy), ensure the data type of the column, UDF,
  and masking policy match.

## Troubleshooting

# Error Message: `Variable is not defined`

Cause:
:   If you see this error message when running commands in SnowSQL, the cause might be an ampersand (`&`) inside a
    [CREATE FUNCTION](/sql-reference/sql/create-function) command. (The ampersand is the SnowSQL variable substitution character.) For
    example, executing the following in SnowSQL causes this error:

    Copy code

    ```
    create function mask_bits(...)
        ...
        as
        $$
        var masked = (x & y);
        ...
        $$;
    ```

    The error occurs when the function is created, not when the function is called.

Solution:
:   If you do not intend to use variable substitution in SnowSQL, you can explicitly disable variable substitution by executing the
    following command:

    Copy code

    ```
    !set variable_substitution=false;
    ```

    For more information about variable substitution, see [Using variables](/user-guide/snowsql-use#label-snowsql-variables).
