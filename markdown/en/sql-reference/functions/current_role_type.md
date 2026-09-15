Categories:
:   [Context functions](/sql-reference/functions-context) (Session Object)

# CURRENT\_ROLE\_TYPE

Calling the CURRENT\_ROLE\_TYPE function returns `ROLE` if the current active (primary) role in the session is an account role. Calling the
CURRENT\_ROLE\_TYPE function from a session running inside a Snowflake native application returns `APPLICATION_INSTANCE`.

## Syntax

Copy code

```
CURRENT_ROLE_TYPE()
```

## Arguments

None.

## Usage notes

The primary role in a session cannot be a database role. Therefore, this function will never return `DATABASE_ROLE`.

None.

## Examples

Copy code

```
SELECT CURRENT_ROLE_TYPE();

+---------------------+
| CURRENT_ROLE_TYPE() |
|---------------------|
| ROLE                |
+---------------------+
```
