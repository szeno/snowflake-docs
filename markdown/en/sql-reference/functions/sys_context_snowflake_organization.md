Categories:
:   [Context functions](/sql-reference/functions-context) (General)

# SYS\_CONTEXT (SNOWFLAKE$ORGANIZATION namespace)

Returns information about the current organization.

You can call this function in any account in the organization. In any other context, the function returns NULL.

See also:
:   [SYS\_CONTEXT](/sql-reference/functions/sys_context) ,
    [SYS\_CONTEXT (SNOWFLAKE$APPLICATION namespace)](/sql-reference/functions/sys_context_snowflake_application) ,
    [SYS\_CONTEXT (SNOWFLAKE$ENVIRONMENT namespace)](/sql-reference/functions/sys_context_snowflake_environment) ,
    [SYS\_CONTEXT (SNOWFLAKE$ORGANIZATION\_SESSION namespace)](/sql-reference/functions/sys_context_snowflake_organization_session) ,
    [SYS\_CONTEXT (SNOWFLAKE$SESSION namespace)](/sql-reference/functions/sys_context_snowflake_session) ,
    [IS\_GROUP\_ACTIVATED (SYS\_CONTEXT function)](/sql-reference/functions/is_group_activated) ,
    [IS\_GROUP\_IMPORTED (SYS\_CONTEXT function)](/sql-reference/functions/is_group_imported) ,
    [IS\_USER\_IMPORTED (SYS\_CONTEXT function)](/sql-reference/functions/is_user_imported)

## Syntax

**Syntax for calling functions:**

Copy code

```
SYS_CONTEXT(
  'SNOWFLAKE$ORGANIZATION' ,
  '<function>' , '<argument>' [ , ... ]
)
```

## Arguments

`'SNOWFLAKE$ORGANIZATION'`
:   Specifies that you want to retrieve a property or call a function to return context information about the current organization.

`'function'`
:   Name of the function that you want to call. You can call the following functions:

    - [IS\_GROUP\_ACTIVATED (SYS\_CONTEXT function)](/sql-reference/functions/is_group_activated)
    - [IS\_GROUP\_IMPORTED (SYS\_CONTEXT function)](/sql-reference/functions/is_group_imported)
    - [IS\_USER\_IMPORTED (SYS\_CONTEXT function)](/sql-reference/functions/is_user_imported)

`'argument' [ , ... ]`
:   Arguments to pass to the function that you want to call.

## Returns

The function returns a VARCHAR value or NULL:

- The return value depends on
  [the function that you are calling](/sql-reference/functions/sys_context_snowflake_organization#label-sys-context-snowflake-organization-function).
- If you call SYS\_CONTEXT with the SNOWFLAKE$ORGANIZATION namespace outside of
  [any of the supported contexts](/sql-reference/functions/sys_context_snowflake_organization#label-sys-content-snowflake-organization-contexts), the function returns NULL.

2026\_06 behavior change bundle

When the [2026\_06 behavior change bundle](/release-notes/bcr-bundles/2026_06_bundle) is [enabled in your account](/release-notes/bcr-bundles/managing-behavior-change-releases#label-manage-bcr-check-status), the `IS_USER_IMPORTED`, `IS_GROUP_IMPORTED`, and `IS_GROUP_ACTIVATED` functions
return `BOOLEAN`.

Existing casts, such as `::BOOLEAN` or `::NUMBER`, continue to work unchanged.

For the return type of every property and function by namespace, see
[SYS\_CONTEXT return types](/sql-reference/functions/sys_context#label-sys-context-returns).

## Usage notes

- If you are specifying the function call in a double-quoted string in a shell, escape the `$` character with a backslash
  (`\`) so that `$ORGANIZATION` is not interpreted as a shell variable.

  For example, if you are using Snowflake CLI and you are
  [specifying the SQL statement as a command-line argument](/developer-guide/snowflake-cli/sql/execute-sql) in double
  quotes:

  Copy code

  ```
  snow sql --query "SELECT SYS_CONTEXT('SNOWFLAKE\$ORGANIZATION', 'IS_USER_IMPORTED', 'my_user_name');"
  ```

## Examples

See the following topics:

- [IS\_GROUP\_ACTIVATED (SYS\_CONTEXT function)](/sql-reference/functions/is_group_activated)
- [IS\_GROUP\_IMPORTED (SYS\_CONTEXT function)](/sql-reference/functions/is_group_imported)
- [IS\_USER\_IMPORTED (SYS\_CONTEXT function)](/sql-reference/functions/is_user_imported)
