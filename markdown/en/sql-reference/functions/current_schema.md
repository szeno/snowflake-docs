Categories:
:   [Context functions](/sql-reference/functions-context) (Session Object)

# CURRENT\_SCHEMA

Returns the name of the current schema, which varies depending on where you call the function:

- If you call this function outside of a policy, UDF, or view, it returns the schema that is in use for the current session.
- If you call this function in the body of a policy, for example a masking policy, it returns the schema that contains the table or view
  that is protected by the policy.
- If you call this function in the handler code of a UDF, it returns the schema that contains the UDF.
- If you call this function in the definition of a view, it returns the schema that contains the view.

## Syntax

Copy code

```
CURRENT_SCHEMA()
```

## Arguments

None.

## Usage notes

- Do not confuse this function with the similarly named function [CURRENT\_SCHEMAS](/sql-reference/functions/current_schemas).

## Examples

Show the current warehouse, database, and schema:

> Copy code
>
> ```
> SELECT CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA();
> ```
>
> Output:
>
> Copy code
>
> ```
> +---------------------+--------------------+------------------+
> | CURRENT_WAREHOUSE() | CURRENT_DATABASE() | CURRENT_SCHEMA() |
> |---------------------+--------------------+------------------|
> | DEV_WAREHOUSE       | TEST_DATABASE      | UDF_TEST_SCHEMA  |
> +---------------------+--------------------+------------------+
> ```
