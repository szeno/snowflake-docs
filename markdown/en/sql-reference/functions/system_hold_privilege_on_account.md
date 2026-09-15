Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$HOLD\_PRIVILEGE\_ON\_ACCOUNT

Indicates if a privilege has been granted to a Snowflake Native App. For example, providers
can use this function in the setup script to check if the app has the necessary
privileges to create an object.

Note

This system function can only be called by a Snowflake Native App.

## Syntax

Copy code

```
SYSTEM$HOLD_PRIVILEGE_ON_ACCOUNT('<privilege_name>')
```

## Arguments

`'privilege_name'`
:   The name of the privilege.

## Returns

- Returns TRUE if the app has been granted the specified privilege. Otherwise,
  returns FALSE.

## Examples

Check if the app has been granted the CREATE COMPUTE POOL privilege:

Copy code

```
SELECT SYSTEM$HOLD_PRIVILEGE_ON_ACCOUNT('CREATE COMPUTE POOL');
```

Check if the app has been granted the IMPORTED PRIVILEGES ON SNOWFLAKE DB privilege:

Copy code

```
SELECT SYSTEM$HOLD_PRIVILEGE_ON_ACCOUNT('IMPORTED PRIVILEGES ON SNOWFLAKE DB');
```
