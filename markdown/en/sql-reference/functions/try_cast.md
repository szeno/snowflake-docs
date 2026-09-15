Categories:
:   [Conversion functions](/sql-reference/functions-conversion)

# TRY\_CAST

A special version of [CAST , ::](/sql-reference/functions/cast) that is available for a subset of data type conversions. It performs the same operation (i.e. converts a value of one data type into another data type), but returns a NULL value instead of
raising an error when the conversion can not be performed.

For more information, see [Error-handling conversion functions](/sql-reference/functions-conversion#label-try-conversion-functions).

## Syntax

Copy code

```
TRY_CAST( <source_string_expr> AS <target_data_type> )
```

## Usage notes

- Only works for string expressions.
- `target_data_type` must be one of the following:
  - VARCHAR (or any of its synonyms)
  - NUMBER (or any of its synonyms)
  - DOUBLE
  - BOOLEAN
  - DATE
  - An interval variation
  - TIME
  - TIMESTAMP, TIMESTAMP\_LTZ, TIMESTAMP\_NTZ, or TIMESTAMP\_TZ

## Examples

The following code samples show how to use the `TRY_CAST` function with
valid and invalid values:

> Copy code
>
> ```
> SELECT TRY_CAST('05-Mar-2016' AS TIMESTAMP);
> +--------------------------------------+
> | TRY_CAST('05-MAR-2016' AS TIMESTAMP) |
> |--------------------------------------|
> | 2016-03-05 00:00:00.000              |
> +--------------------------------------+
> ```
>
> Copy code
>
> ```
> SELECT TRY_CAST('05/16' AS TIMESTAMP);
> +--------------------------------+
> | TRY_CAST('05/16' AS TIMESTAMP) |
> |--------------------------------|
> | NULL                           |
> +--------------------------------+
> ```
>
> Copy code
>
> ```
> SELECT TRY_CAST('ABCD' AS CHAR(2));
> +-----------------------------+
> | TRY_CAST('ABCD' AS CHAR(2)) |
> |-----------------------------|
> | NULL                        |
> +-----------------------------+
> ```
>
> Copy code
>
> ```
> SELECT TRY_CAST('ABCD' AS VARCHAR(10));
> +---------------------------------+
> | TRY_CAST('ABCD' AS VARCHAR(10)) |
> |---------------------------------|
> | ABCD                            |
> +---------------------------------+
> ```
