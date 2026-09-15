Categories:
:   [Context functions](/sql-reference/functions-context) (General)

# IS\_APPLICATION\_ROLE\_ACTIVATED (SYS\_CONTEXT function)

Returns the VARCHAR value `'TRUE'` if an application role is activated in the specified context.

See also:
:   [SYS\_CONTEXT (SNOWFLAKE$APPLICATION namespace)](/sql-reference/functions/sys_context_snowflake_application)

## Syntax

Copy code

```
SYS_CONTEXT(
  'SNOWFLAKE$APPLICATION' ,
  'IS_APPLICATION_ROLE_ACTIVATED' ,
  '<context>' ,
  '<app_role>'
)
```

## Arguments

`'SNOWFLAKE$APPLICATION'`
:   Specifies that you want to call a function to return context information about the application in which the function is called.

`'IS_APPLICATION_ROLE_ACTIVATED'`
:   Calls the IS\_APPLICATION\_ROLE\_ACTIVATED function.

`'context'`
:   Specifies the execution context that you want to check. You can specify one of the following values:

    - `SESSION`: Checks if the application role is in the role hierarchy of the current session’s primary or secondary roles.
      The function returns `'TRUE'` if the role is in the role hierarchy.
    - `ACTIVE`: Checks if the application role is in the role hierarchy in the context of the current call.

      For example, in a call to an owner’s rights stored procedure, the procedure is executed by the owner’s role. The function
      returns `'TRUE'` if the application role is in the role hierarchy of the owner’s role.

`'app_role'`
:   Specifies the application role to check.

    Do not qualify the role name with the name of the application. The function automatically determines the application name from
    the context in which the function is called.

## Returns

The function returns one of the following VARCHAR values:

- `'TRUE'` if the application role is activated in the context specified by `context`.
- `'FALSE'` if the application role is not activated in that context or if the application role is not valid.

To compare this return value against the BOOLEAN value TRUE or FALSE, [cast](/sql-reference/data-type-conversion#label-data-type-explicit-casting) the return
value to BOOLEAN. For example:

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$APPLICATION', 'IS_APPLICATION_ROLE_ACTIVATED', 'SESSION', 'my_app_role')::BOOLEAN = TRUE;
```

2026\_06 behavior change bundle

When the [2026\_06 behavior change bundle](/release-notes/bcr-bundles/2026_06_bundle) is [enabled in your account](/release-notes/bcr-bundles/managing-behavior-change-releases#label-manage-bcr-check-status), when you call this
function through `SYS_CONTEXT`, it returns `BOOLEAN` instead of the `VARCHAR`
string `'TRUE'` or `'FALSE'`.

Existing casts, such as `::BOOLEAN` or `::NUMBER`, continue to work unchanged.

For the return type of every property and function by namespace, see
[SYS\_CONTEXT return types](/sql-reference/functions/sys_context#label-sys-context-returns).

## Usage notes

## Examples

The following example returns `TRUE` if the application role `my_app_role` is in the role hierarchy of the session’s primary
or secondary roles:

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$APPLICATION', 'IS_APPLICATION_ROLE_ACTIVATED', 'SESSION', 'my_app_role');
```
