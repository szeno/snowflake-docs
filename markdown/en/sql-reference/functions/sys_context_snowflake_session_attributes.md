Categories:
:   [Context functions](/sql-reference/functions-context) (General)

# SYS\_CONTEXT (SNOWFLAKE$SESSION\_ATTRIBUTES namespace)

Returns a custom session attribute that was set using [SET\_SYS\_CONTEXT](/sql-reference/functions/set_sys_context) in the
`SNOWFLAKE$SESSION_ATTRIBUTES` namespace.

Custom session attributes are immutable once set and persist for the duration of the session.
They are useful for tracking metadata about a session, such as application context, user
attributes, or audit information.

See also:
:   [SYS\_CONTEXT](/sql-reference/functions/sys_context),
    [SET\_SYS\_CONTEXT](/sql-reference/functions/set_sys_context)

## Syntax

Copy code

```
SYS_CONTEXT(
  'SNOWFLAKE$SESSION_ATTRIBUTES' ,
  '<key>'
)
```

## Arguments

`'SNOWFLAKE$SESSION_ATTRIBUTES'`
:   Specifies that you want to retrieve a custom session attribute.

`'key'`
:   The name of the custom attribute to retrieve. Attribute names are **case-sensitive**.

## Returns

The function returns a VARCHAR value:

- The value of the specified attribute if it has been set in the current session using
  [SET\_SYS\_CONTEXT](/sql-reference/functions/set_sys_context).
- NULL if the attribute has not been set.

2026\_06 behavior change bundle

When the [2026\_06 behavior change bundle](/release-notes/bcr-bundles/2026_06_bundle) is [enabled in your account](/release-notes/bcr-bundles/managing-behavior-change-releases#label-manage-bcr-check-status), custom session
attributes in this namespace continue to return `VARCHAR`.

Existing casts, such as `::BOOLEAN` or `::NUMBER`, continue to work unchanged.

For the return type of every property and function by namespace, see
[SYS\_CONTEXT return types](/sql-reference/functions/sys_context#label-sys-context-returns).

## Access control requirements

No special privileges are required to retrieve custom session attributes. Any user can retrieve
attributes from their own session.

## Usage notes

- Attributes must be set using [SET\_SYS\_CONTEXT](/sql-reference/functions/set_sys_context) before they can be retrieved.
- Attribute names are **case-sensitive**. `app_context` and `APP_CONTEXT` are treated as
  different attributes.
- Attributes are session-scoped and are not visible to other sessions.
- If you are specifying the function call in a double-quoted string in a shell, escape the `$`
  character with a backslash (`\`) so that `$session_attributes` is not interpreted as a
  shell variable.

## Examples

The following example sets a custom attribute and then retrieves it:

Copy code

```
-- Set a custom session attribute
CALL SET_SYS_CONTEXT('SNOWFLAKE$SESSION_ATTRIBUTES', 'app_context', 'production');

-- Retrieve the custom attribute
SELECT SYS_CONTEXT('SNOWFLAKE$SESSION_ATTRIBUTES', 'app_context');
```

```
+---------------------------------------------------------------+
| SYS_CONTEXT('SNOWFLAKE$SESSION_ATTRIBUTES', 'app_context')    |
|---------------------------------------------------------------|
| production                                                    |
+---------------------------------------------------------------+
```

Retrieving an attribute that has not been set returns NULL:

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$SESSION_ATTRIBUTES', 'nonexistent_attr');
```

```
+------------------------------------------------------------------+
| SYS_CONTEXT('SNOWFLAKE$SESSION_ATTRIBUTES', 'nonexistent_attr')  |
|------------------------------------------------------------------|
| NULL                                                             |
+------------------------------------------------------------------+
```

Attribute names are case-sensitive:

Copy code

```
-- Set attributes with different cases
CALL SET_SYS_CONTEXT('SNOWFLAKE$SESSION_ATTRIBUTES', 'mykey', 'lowercase');
CALL SET_SYS_CONTEXT('SNOWFLAKE$SESSION_ATTRIBUTES', 'MyKey', 'mixedcase');
CALL SET_SYS_CONTEXT('SNOWFLAKE$SESSION_ATTRIBUTES', 'MYKEY', 'uppercase');

-- Each is a distinct attribute
SELECT
  SYS_CONTEXT('SNOWFLAKE$SESSION_ATTRIBUTES', 'mykey') AS lower,
  SYS_CONTEXT('SNOWFLAKE$SESSION_ATTRIBUTES', 'MyKey') AS mixed,
  SYS_CONTEXT('SNOWFLAKE$SESSION_ATTRIBUTES', 'MYKEY') AS upper;
```

```
+-----------+-----------+-----------+
| LOWER     | MIXED     | UPPER     |
|-----------+-----------+-----------|
| lowercase | mixedcase | uppercase |
+-----------+-----------+-----------+
```
