Categories:
:   [Context functions](/sql-reference/functions-context) (General)

# SYS\_CONTEXT (SNOWFLAKE$APPLICATION namespace)

Returns information about the context in which a statement is executed within a
[Snowflake Native App](/developer-guide/native-apps/native-apps-about).

You can call this function in the following contexts:

- A stored procedure or Streamlit app that is configured to use
  [owner’s rights](/developer-guide/native-apps/restricted-callers-rights) and is within or owned by a Snowflake Native App.
- A UDF, view, or policy that is owned by a Snowflake Native App.
- A UDF, view, or policy that is part of the [shared data content](/developer-guide/native-apps/preparing-data-content) of a
  Snowflake Native App.

In any other context, the function returns NULL.

See also:
:   [SYS\_CONTEXT](/sql-reference/functions/sys_context),
    [SYS\_CONTEXT (SNOWFLAKE$ENVIRONMENT namespace)](/sql-reference/functions/sys_context_snowflake_environment),
    [SYS\_CONTEXT (SNOWFLAKE$ORGANIZATION namespace)](/sql-reference/functions/sys_context_snowflake_organization),
    [SYS\_CONTEXT (SNOWFLAKE$ORGANIZATION\_SESSION namespace)](/sql-reference/functions/sys_context_snowflake_organization_session),
    [SYS\_CONTEXT (SNOWFLAKE$SESSION namespace)](/sql-reference/functions/sys_context_snowflake_session),
    [IS\_APPLICATION\_ROLE\_ACTIVATED](/sql-reference/functions/is_application_role_activated)

## Syntax

**Syntax for retrieving properties:**

Copy code

```
SYS_CONTEXT(
  'SNOWFLAKE$APPLICATION' ,
  '<property>'
)
```

**Syntax for calling functions:**

Copy code

```
SYS_CONTEXT(
  'SNOWFLAKE$APPLICATION' ,
  '<function>' , '<argument>' [ , ... ]
)
```

## Arguments

`'SNOWFLAKE$APPLICATION'`
:   Specifies that you want to retrieve a property or call a function to return context information about the application in which
    the function is called.

`'property'`
:   Name of the property that you want to retrieve. You can specify the following properties:

    | Property | Description |
    | --- | --- |
    | `NAME` | Name of the application. |
    | `CURRENT_VERSION` | Current version of the application in which the current SQL statement is executed.  The value of the `CURRENT_VERSION` property can differ from the `INSTALLED_VERSION` property in the following situations:   - The SQL statement is executed in a [setup script](/developer-guide/native-apps/creating-setup-script) that   upgrades the application to a new version.   In this case, `CURRENT_VERSION` is the new version, and `INSTALLED_VERSION` is the currently installed version that is being upgraded.   - A long-running procedure or query started executing before an upgrade completed.   In this case, `CURRENT_VERSION` is the version when the procedure or query started executing, and `INSTALLED_VERSION` is the version after the upgrade completed. |
    | `CURRENT_PATCH` | Current patch number of the application in which the current SQL statement is executed. |
    | `INSTALLED_VERSION` | Installed version of the application in which the current SQL statement is executed. |
    | `INSTALLED_PATCH` | Installed patch number of the application in which the current SQL statement is executed. |
    | `IS_DEV_MODE` | `TRUE` if the application is in [development mode](/developer-guide/native-apps/installing-testing-application#label-native-apps-dev-mode-about); otherwise, `FALSE`.  To compare this value against the BOOLEAN value TRUE or FALSE, [cast](/sql-reference/data-type-conversion#label-data-type-explicit-casting) the value to BOOLEAN. For example:  Copy code  ``` SELECT SYS_CONTEXT('SNOWFLAKE$APPLICATION', 'IS_DEV_MODE')::BOOLEAN = TRUE; ``` |

    Expand

    Show lessSee more

`'function'`
:   Name of the function that you want to call. You can call the following functions:

    - [IS\_APPLICATION\_ROLE\_ACTIVATED](/sql-reference/functions/is_application_role_activated)

`'argument' [ , ... ]`
:   Arguments to pass to the function that you want to call.

## Returns

The function returns a VARCHAR value or NULL:

- The return value depends on
  [the property that you are retrieving](/sql-reference/functions/sys_context_snowflake_application#label-sys-context-snowflake-application-property) or
  [the function that you are calling](/sql-reference/functions/sys_context_snowflake_application#label-sys-context-snowflake-application-function).
- If you call SYS\_CONTEXT with the SNOWFLAKE$APPLICATION namespace outside of
  [any of the supported contexts](/sql-reference/functions/sys_context_snowflake_application#label-sys-context-snowflake-application-contexts), the function returns NULL.

2026\_06 behavior change bundle

When the [2026\_06 behavior change bundle](/release-notes/bcr-bundles/2026_06_bundle) is [enabled in your account](/release-notes/bcr-bundles/managing-behavior-change-releases#label-manage-bcr-check-status), the `CURRENT_PATCH` and `INSTALLED_PATCH` properties return `NUMBER`, and the
`IS_DEV_MODE` property and the `IS_APPLICATION_ROLE_ACTIVATED` and `IS_CONFIGURATION_SET` functions
return `BOOLEAN`. Other properties and functions in this namespace continue to return `VARCHAR`.

Existing casts, such as `::BOOLEAN` or `::NUMBER`, continue to work unchanged.

For the return type of every property and function by namespace, see
[SYS\_CONTEXT return types](/sql-reference/functions/sys_context#label-sys-context-returns).

## Usage notes

- If you are specifying the function call in a double-quoted string in a shell, escape the `$` character with a backslash
  (`\`) so that `$APPLICATION` is not interpreted as a shell variable.

  For example, if you are using Snowflake CLI and you are
  [specifying the SQL statement as a command-line argument](/developer-guide/snowflake-cli/sql/execute-sql) in double
  quotes:

  Copy code

  ```
  snow sql --query "SELECT SYS_CONTEXT('SNOWFLAKE\$APPLICATION', 'NAME');"
  ```

## Examples

The following example returns the current version of the application:

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$APPLICATION', 'CURRENT_VERSION');
```
