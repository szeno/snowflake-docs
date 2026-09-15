Categories:
:   [Context functions](/sql-reference/functions-context) (General)

# IS\_CONFIGURATION\_SET (SYS\_CONTEXT function)

Returns the VARCHAR value `'TRUE'` if the specified configuration has a value set,
that is, the configuration’s status is `DONE`. Returns `FALSE` if the
configuration does not have a value set, that is, the configuration’s status is `PENDING`.

See also:
:   [SYS\_CONTEXT (SNOWFLAKE$APPLICATION namespace)](/sql-reference/functions/sys_context_snowflake_application)

## Syntax

Copy code

```
SYS_CONTEXT(
  'SNOWFLAKE$APPLICATION' ,
  'IS_CONFIGURATION_SET' ,
  '<config_name>' ,
)
```

## Arguments

`'SNOWFLAKE$APPLICATION'`
:   Specifies that you want to call a function to return context information about the app in which the function is called.

`'IS_CONFIGURATION_SET'`
:   Calls the IS\_CONFIGURATION\_SET function.

`'config_name'`
:   Specifies the name of the configuration to check.

## Returns

The function returns one of the following VARCHAR values:

- `'TRUE'` if the configuration has a value set.
- `'FALSE'` if the configuration does not have a value set.

To compare this return value against the BOOLEAN value TRUE or FALSE, [cast](/sql-reference/data-type-conversion#label-data-type-explicit-casting) the return
value to BOOLEAN. For example:

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$APPLICATION', 'IS_CONFIGURATION_SET', 'my_config_name')::BOOLEAN = TRUE;
```

2026\_06 behavior change bundle

When the [2026\_06 behavior change bundle](/release-notes/bcr-bundles/2026_06_bundle) is [enabled in your account](/release-notes/bcr-bundles/managing-behavior-change-releases#label-manage-bcr-check-status), when you call this
function through `SYS_CONTEXT`, it returns `BOOLEAN` instead of the `VARCHAR`
string `'TRUE'` or `'FALSE'`.

Existing casts, such as `::BOOLEAN` or `::NUMBER`, continue to work unchanged.

For the return type of every property and function by namespace, see
[SYS\_CONTEXT return types](/sql-reference/functions/sys_context#label-sys-context-returns).

## Usage notes

- This function can only be used by an app.
