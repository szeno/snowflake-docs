Categories:
:   [Context functions](/sql-reference/functions-context) (Session)

# SET\_SYS\_CONTEXT

Sets a value for a specified key in a specified namespace that can be retrieved later using
[SYS\_CONTEXT](/sql-reference/functions/sys_context).

This function has two modes of operation:

- **Immutable session attributes** (`SNOWFLAKE$SESSION_ATTRIBUTES` namespace): Sets custom
  session attributes that are immutable once set and persist for the duration of the session.
  Useful for tracking metadata about a session, such as application context, user attributes, or
  audit information.
- **Session variables** (other namespaces): Behaves like the [SET](/sql-reference/sql/set)
  command, setting session variables that can be updated. Returns the previous value of the
  variable.

See also:
:   [SYS\_CONTEXT](/sql-reference/functions/sys_context) ,
    [SYS\_CONTEXT (SNOWFLAKE$SESSION\_ATTRIBUTES namespace)](/sql-reference/functions/sys_context_snowflake_session_attributes) ,
    [SET](/sql-reference/sql/set)

## Syntax

Copy code

```
CALL SET_SYS_CONTEXT( '<namespace>', '<key>', '<value>' )
```

## Arguments

`'namespace'`
:   The namespace in which to store the key-value pair. Supported namespaces:

    - `SNOWFLAKE$SESSION_ATTRIBUTES` — Stores immutable custom session attributes. Attribute
      names are **case-sensitive**.
    - Any other string (or NULL) — Treats the namespace as a prefix for a session variable name,
      similar to the [SET](/sql-reference/sql/set) command. Namespaces are
      **case-sensitive**.

`'key'`
:   The name of the attribute or variable to set. All key names are **case-sensitive**.

`'value'`
:   The value to assign. The value must be a string or an expression that evaluates to a string.

## Returns

The function returns a VARCHAR value:

- For the `SNOWFLAKE$SESSION_ATTRIBUTES` namespace: Always returns NULL (because immutable
  attributes cannot have a previous value). If the attribute has already been set in the current
  session, the function raises an error instead.
- For other namespaces: Returns the previous value of the session variable, or NULL if the
  variable did not previously exist. This matches the behavior of the
  [SET](/sql-reference/sql/set) command.

2026\_06 behavior change bundle

When the [2026\_06 behavior change bundle](/release-notes/bcr-bundles/2026_06_bundle) is [enabled in your account](/release-notes/bcr-bundles/managing-behavior-change-releases#label-manage-bcr-check-status), it changes the return type
of reads through [SYS\_CONTEXT](/sql-reference/functions/sys_context). The return value of
`SET_SYS_CONTEXT` (the previous value of the attribute or session variable) is unaffected and continues
to be `VARCHAR`.

## Access control requirements

No special privileges are required to set custom session attributes. Any user can set attributes
in their own session.

## Usage notes

**For SNOWFLAKE$SESSION\_ATTRIBUTES namespace (immutable attributes):**

- Attributes are **immutable**. Once an attribute is set, any attempt to set it again (even to
  the same value) will result in an error.
- Attribute names are **case-sensitive**. `app_context`, `App_Context`, and `APP_CONTEXT`
  are treated as three different attributes.
- Attributes are **session-scoped**. They persist for the duration of the session and are not
  visible to other sessions.
- To retrieve attribute values, use [SYS\_CONTEXT (SNOWFLAKE$SESSION\_ATTRIBUTES namespace)](/sql-reference/functions/sys_context_snowflake_session_attributes):
  `SYS_CONTEXT('SNOWFLAKE$SESSION_ATTRIBUTES', '<key>')`.

**For other namespaces (session variables):**

- Variable names are **case-sensitive**. `user_id` and `USER_ID` are treated as different
  variables.
- Variables can be **updated**. Setting a variable that already exists returns the previous value
  and updates it with the new value.
- The namespace (if provided) is used as a prefix: `SET_SYS_CONTEXT('myns', 'mykey', 'val')`
  creates a variable named `myns.mykey`.
- Variables can be retrieved using `SYS_CONTEXT('<namespace>', '<key>')` with the exact case
  used when setting the variable.

**General notes:**

- If you are specifying the function call in a double-quoted string in a shell, escape the `$`
  character with a backslash (`\`) so that `$session_attributes` is not interpreted as a
  shell variable.

## Examples

**Example 1: Immutable session attributes (SNOWFLAKE$SESSION\_ATTRIBUTES namespace)**

Set a custom attribute to track the application context:

Copy code

```
CALL SET_SYS_CONTEXT('SNOWFLAKE$SESSION_ATTRIBUTES', 'app_context', 'production');
```

Retrieve the attribute value (note: attribute names are case-sensitive):

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$SESSION_ATTRIBUTES', 'app_context');
```

```
+---------------------------------------------------------------+
| SYS_CONTEXT('SNOWFLAKE$SESSION_ATTRIBUTES', 'app_context')   |
|---------------------------------------------------------------|
| production                                                    |
+---------------------------------------------------------------+
```

Once an attribute is set, attempting to change it results in an error:

Copy code

```
-- This will fail because the attribute is immutable
CALL SET_SYS_CONTEXT('SNOWFLAKE$SESSION_ATTRIBUTES', 'app_context', 'development');
```

```
SQL compilation error: Cannot overwrite context value: app_context
```

Attribute names are case-sensitive:

Copy code

```
-- This succeeds because it's a different attribute name (different case)
CALL SET_SYS_CONTEXT('SNOWFLAKE$SESSION_ATTRIBUTES', 'APP_CONTEXT', 'staging');

SELECT SYS_CONTEXT('SNOWFLAKE$SESSION_ATTRIBUTES', 'app_context') AS lower_case,
       SYS_CONTEXT('SNOWFLAKE$SESSION_ATTRIBUTES', 'APP_CONTEXT') AS upper_case;
```

```
+------------+------------+
| LOWER_CASE | UPPER_CASE |
|------------+------------|
| production | staging    |
+------------+------------+
```

**Example 2: Session variables (other namespaces)**

Set a session variable with a namespace prefix:

Copy code

```
CALL SET_SYS_CONTEXT('myapp', 'user_id', '12345');
```

```
+---------------------------------------------------+
| SET_SYS_CONTEXT('myapp', 'user_id', '12345')     |
|---------------------------------------------------|
| NULL                                              |
+---------------------------------------------------+
```

The variable is stored with the exact case provided: `myapp.user_id`. Retrieve it:

Copy code

```
SELECT SYS_CONTEXT('myapp', 'user_id');
```

```
+----------------------------------+
| SYS_CONTEXT('myapp', 'user_id')  |
|----------------------------------|
| 12345                            |
+----------------------------------+
```

Update the variable (returns the previous value):

Copy code

```
CALL SET_SYS_CONTEXT('myapp', 'user_id', '67890');
```

```
+---------------------------------------------------+
| SET_SYS_CONTEXT('myapp', 'user_id', '67890')     |
|---------------------------------------------------|
| 12345                                             |
+---------------------------------------------------+
```
