Categories:
:   [Context functions](/sql-reference/functions-context) (General)

# CURRENT\_CLIENT

Returns the version of the client from which the function was called. If called from an application using the JDBC or ODBC driver to connect to Snowflake, returns the version of the driver.

## Syntax

Copy code

```
CURRENT_CLIENT()
```

## Usage notes

- The Worksheet in the Snowflake web interface connects to Snowflake directly through the interface; it doesn’t use the JDBC or ODBC driver. As such, calling CURRENT\_CLIENT in the Worksheet returns a
  different value than calling the function from a client application.

## Examples

Call CURRENT\_CLIENT from within SnowSQL:

> Copy code
>
> ```
> SELECT CURRENT_CLIENT();
>
> +------------------+
> | CURRENT_CLIENT() |
> |------------------|
> | SnowSQL 1.1.18   |
> +------------------+
> ```

Call CURRENT\_CLIENT from within the Worksheet in Snowsight:

> Copy code
>
> ```
> SELECT CURRENT_CLIENT();
> ```
>
> Results
>
> |  |  |
> | --- | --- |
> | row# | CURRENT\_CLIENT() |
> | 1 | Snowflake UI 1434236365 |
>
> Expand
>
> Show lessSee more
