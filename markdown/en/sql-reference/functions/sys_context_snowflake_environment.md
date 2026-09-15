Categories:
:   [Context functions](/sql-reference/functions-context) (General)

# SYS\_CONTEXT (SNOWFLAKE$ENVIRONMENT namespace)

Returns information about the environment (the client, current account, and current region) in which the function is called.

See also:
:   [SYS\_CONTEXT](/sql-reference/functions/sys_context) ,
    [SYS\_CONTEXT (SNOWFLAKE$APPLICATION namespace)](/sql-reference/functions/sys_context_snowflake_application) ,
    [SYS\_CONTEXT (SNOWFLAKE$ORGANIZATION namespace)](/sql-reference/functions/sys_context_snowflake_organization) ,
    [SYS\_CONTEXT (SNOWFLAKE$ORGANIZATION\_SESSION namespace)](/sql-reference/functions/sys_context_snowflake_organization_session) ,
    [SYS\_CONTEXT (SNOWFLAKE$SESSION namespace)](/sql-reference/functions/sys_context_snowflake_session)

## Syntax

Copy code

```
SYS_CONTEXT(
  'SNOWFLAKE$ENVIRONMENT' ,
  '<property>'
)
```

## Arguments

`'SNOWFLAKE$ENVIRONMENT'`
:   Specifies that you want to retrieve a property to return context information about the environment in which the function is
    called.

`'property'`
:   Name of the property that you want to retrieve. You can specify the following properties:

    | Property | Description |
    | --- | --- |
    | `CLIENT` | Name and version of the client, driver, or library used to call the function.  If this function is called in Snowsight, the function returns the name and version of the Go Snowflake Driver.  If this function is called in Snowflake CLI, the function returns the name and version of the Snowflake Connector for Python.  The value of this property is the same as the return value of the [CURRENT\_CLIENT](/sql-reference/functions/current_client) function. |
    | `ACCOUNT` | The [account locator](/user-guide/admin-account-identifier#label-account-locator) of the account for the current session.  The value of this property is the same as the return value of the [CURRENT\_ACCOUNT](/sql-reference/functions/current_account) function. |
    | `REGION` | The name of the [region](/user-guide/intro-regions) of the account for the current session.  For organizations that have accounts in multiple [region groups](/user-guide/admin-account-identifier#label-region-groups), the value of the property is `region_group.region`.  The value of this property is the same as the return value of the [CURRENT\_REGION](/sql-reference/functions/current_region) function. |

    Expand

    Show lessSee more

## Returns

The function returns a VARCHAR value.

2026\_06 behavior change bundle

When the [2026\_06 behavior change bundle](/release-notes/bcr-bundles/2026_06_bundle) is [enabled in your account](/release-notes/bcr-bundles/managing-behavior-change-releases#label-manage-bcr-check-status), the properties
in this namespace continue to return `VARCHAR`.

Existing casts, such as `::BOOLEAN` or `::NUMBER`, continue to work unchanged.

For the return type of every property and function by namespace, see
[SYS\_CONTEXT return types](/sql-reference/functions/sys_context#label-sys-context-returns).

## Usage notes

- If you are specifying the function call in a double-quoted string in a shell, escape the `$` character with a backslash
  (`\`) so that `$ENVIRONMENT` is not interpreted as a shell variable.

  For example, if you are using Snowflake CLI and you are
  [specifying the SQL statement as a command-line argument](/developer-guide/snowflake-cli/sql/execute-sql) in double
  quotes:

  Copy code

  ```
  snow sql --query "SELECT SYS_CONTEXT('SNOWFLAKE\$ENVIRONMENT', 'CLIENT');"
  ```

## Examples

The following example returns the name and version of the client used to execute the command:

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$ENVIRONMENT', 'CLIENT');
```

The following example returns the account locator of the account for the current session:

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$ENVIRONMENT', 'ACCOUNT');
```

The following example returns the region of the account for the current session:

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$ENVIRONMENT', 'REGION');
```
