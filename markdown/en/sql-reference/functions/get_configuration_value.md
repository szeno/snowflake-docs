Categories:
:   [Context functions](/sql-reference/functions-context) (General)

# GET\_CONFIGURATION\_VALUE (SYS\_CONTEXT function)

Returns the current value for the specified configuration.

See also:
:   [SYS\_CONTEXT (SNOWFLAKE$APPLICATION namespace)](/sql-reference/functions/sys_context_snowflake_application)

## Syntax

Copy code

```
SYS_CONTEXT(
  'SNOWFLAKE$APPLICATION' ,
  'GET_CONFIGURATION_VALUE' ,
  '<config_name>' ,
)
```

## Arguments

`'SNOWFLAKE$APPLICATION'`
:   Specifies that you want to call a function to return context information about the application in which the function is called.

`'GET_CONFIGURATION_VALUE'`
:   Calls the GET\_CONFIGURATION\_VALUE function.

`'config_name'`
:   Specifies the name of the configuration to get the value for.

## Returns

The function returns the current value of the configuration.

2026\_06 behavior change bundle

When the [2026\_06 behavior change bundle](/release-notes/bcr-bundles/2026_06_bundle) is [enabled in your account](/release-notes/bcr-bundles/managing-behavior-change-releases#label-manage-bcr-check-status), this function
continues to return `VARCHAR`.

Existing casts, such as `::BOOLEAN` or `::NUMBER`, continue to work unchanged.

For the return type of every property and function by namespace, see
[SYS\_CONTEXT return types](/sql-reference/functions/sys_context#label-sys-context-returns).

## Usage notes

- This function can only be used by an app.
- For a configuration definition of type `APPLICATION_NAME`, the value returned is the current
  name of the application stored in the specified configuration.
