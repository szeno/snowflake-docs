Categories:
:   [Context functions](/sql-reference/functions-context) (Session)

# CURRENT\_SESSION

Returns a unique system identifier for the Snowflake session corresponding to the present connection. This will generally be a system-generated alphanumeric string. It is NOT derived from the user name or user account.

## Syntax

Copy code

```
CURRENT_SESSION()
```

## Returns

The data type of the returned value is VARCHAR.

## Examples

Copy code

```
SELECT CURRENT_SESSION();
-------------------+
 CURRENT_SESSION() |
-------------------+
 34359980038       |
-------------------+
```
