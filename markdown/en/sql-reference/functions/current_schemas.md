Categories:
:   [Context functions](/sql-reference/functions-context) (Session Object)

# CURRENT\_SCHEMAS

Returns active search path schemas.

For more information about search path, see [Object name resolution](/sql-reference/name-resolution).

## Syntax

Copy code

```
CURRENT_SCHEMAS()
```

## Arguments

None.

## Usage notes

Do not confuse this function with the similarly named function
[CURRENT\_SCHEMA](/sql-reference/functions/current_schema).

## Examples

Show the schemas that will be searched if a table or other database object
is referenced without a schema name:

> Copy code
>
> ```
> SELECT CURRENT_SCHEMAS();
> ```
>
> Output:
>
> Copy code
>
> ```
> +-----------------------------------------+
> | CURRENT_SCHEMAS()                       |
> |-----------------------------------------|
> | ["TEST_DB1.BILLING", "TEST_DB1.PUBLIC"] |
> +-----------------------------------------+
> ```
