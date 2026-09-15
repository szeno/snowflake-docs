Categories:
:   [Context functions](/sql-reference/functions-context) (General)

# SYS\_CONTEXT (SNOWFLAKE$ORGANIZATION\_SESSION namespace)

Returns information about the session in which the function is called and the current organization user.

You can call this function in the following contexts:

- You can call this function directly in the current session.
- You can run a caller’s rights executable (for example, a caller’s rights stored procedure) that calls this function.
- You can run an owner’s rights executable (for example, an owner’s rights stored procedure) that calls this function, provided
  that:
  - The owner role has been granted the READ SESSION privilege on the account.
  - The account containing the owner role is the same organization as the current account for the session.

In any other context, the function returns NULL.

See also:
:   [SYS\_CONTEXT](/sql-reference/functions/sys_context) ,
    [SYS\_CONTEXT (SNOWFLAKE$APPLICATION namespace)](/sql-reference/functions/sys_context_snowflake_application) ,
    [SYS\_CONTEXT (SNOWFLAKE$ENVIRONMENT namespace)](/sql-reference/functions/sys_context_snowflake_environment) ,
    [SYS\_CONTEXT (SNOWFLAKE$ORGANIZATION namespace)](/sql-reference/functions/sys_context_snowflake_organization)

## Syntax

**Syntax for retrieving properties:**

Copy code

```
SYS_CONTEXT(
  'SNOWFLAKE$ORGANIZATION_SESSION' ,
  '<property>'
)
```

## Arguments

`'SNOWFLAKE$ORGANIZATION_SESSION'`
:   Specifies that you want to retrieve a property or call a function to return information about the session in which the function
    is called, when the current account is in an organization.

`'property'`
:   Name of the property that you want to retrieve. You can specify the following properties:

    | Property | Description |
    | --- | --- |
    | `PRINCIPAL_NAME` | Name of the principal (the [organization user](/user-guide/organization-users)) that started the session.  If the current user is not an organization user, the value of this property is NULL. |

    Expand

    Show lessSee more

## Returns

The function returns a VARCHAR value or NULL:

- The return value depends on
  [the property that you are retrieving](/sql-reference/functions/sys_context_snowflake_organization_session#label-sys-context-snowflake-organization-session-property).
- If you call SYS\_CONTEXT with the SNOWFLAKE$ORGANIZATION\_SESSION namespace outside of
  [any of the supported contexts](/sql-reference/functions/sys_context_snowflake_organization_session#label-sys-content-snowflake-organization-session-contexts), the function returns NULL.

2026\_06 behavior change bundle

When the [2026\_06 behavior change bundle](/release-notes/bcr-bundles/2026_06_bundle) is [enabled in your account](/release-notes/bcr-bundles/managing-behavior-change-releases#label-manage-bcr-check-status), the properties
in this namespace continue to return `VARCHAR`.

Existing casts, such as `::BOOLEAN` or `::NUMBER`, continue to work unchanged.

For the return type of every property and function by namespace, see
[SYS\_CONTEXT return types](/sql-reference/functions/sys_context#label-sys-context-returns).

## Usage notes

- If you are specifying the function call in a double-quoted string in a shell, escape the `$` character with a backslash
  (`\`) so that `$ORGANIZATION_SESSION` is not interpreted as a shell variable.

  For example, if you are using Snowflake CLI and you are
  [specifying the SQL statement as a command-line argument](/developer-guide/snowflake-cli/sql/execute-sql) in double
  quotes:

  Copy code

  ```
  snow sql --query "SELECT SYS_CONTEXT('SNOWFLAKE\$ORGANIZATION_SESSION', 'PRINCIPAL_NAME');"
  ```

## Examples

The following example returns the name of the organization user for the current session:

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$ORGANIZATION_SESSION', 'PRINCIPAL_NAME');
```

```
+-----------------------------------------------------------------+
| SYS_CONTEXT('SNOWFLAKE$ORGANIZATION_SESSION', 'PRINCIPAL_NAME') |
|-----------------------------------------------------------------|
| my_organization_user_name                                       |
+-----------------------------------------------------------------+
```
