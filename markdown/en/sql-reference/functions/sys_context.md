Categories:
:   [Context functions](/sql-reference/functions-context) (General)

# SYS\_CONTEXT

Returns information about the context in which the function is called.

See also:
:   [SYS\_CONTEXT (SNOWFLAKE$APPLICATION namespace)](/sql-reference/functions/sys_context_snowflake_application) ,
    [SYS\_CONTEXT (SNOWFLAKE$CURRENT namespace)](/sql-reference/functions/sys_context_snowflake_current) ,
    [SYS\_CONTEXT (SNOWFLAKE$ENVIRONMENT namespace)](/sql-reference/functions/sys_context_snowflake_environment) ,
    [SYS\_CONTEXT (SNOWFLAKE$ORGANIZATION namespace)](/sql-reference/functions/sys_context_snowflake_organization) ,
    [SYS\_CONTEXT (SNOWFLAKE$ORGANIZATION\_SESSION namespace)](/sql-reference/functions/sys_context_snowflake_organization_session) ,
    [SYS\_CONTEXT (SNOWFLAKE$SESSION namespace)](/sql-reference/functions/sys_context_snowflake_session) ,
    [SYS\_CONTEXT (SNOWFLAKE$SESSION\_ATTRIBUTES namespace)](/sql-reference/functions/sys_context_snowflake_session_attributes)

## Syntax

**Syntax for retrieving properties:**

Copy code

```
SYS_CONTEXT(
  '<namespace>' ,
  '<property>'
)
```

**Syntax for calling functions:**

Copy code

```
SYS_CONTEXT(
  '<namespace>' ,
  '<function>' , '<argument>' [ , ... ]
)
```

## Arguments

`'namespace'`
:   Namespace of the property that you want to retrieve or the function that you want to call. You can specify one of the following
    namespaces:

    | Namespace | Description |
    | --- | --- |
    | [SNOWFLAKE$APPLICATION](/sql-reference/functions/sys_context_snowflake_application) | Properties and functions providing context around the application in which the function is called. |
    | [SNOWFLAKE$CURRENT](/sql-reference/functions/sys_context_snowflake_current) | Properties and functions providing context around the current execution context. The current execution context can differ from the session context inside owner’s rights executables or agent invocations. |
    | [SNOWFLAKE$ENVIRONMENT](/sql-reference/functions/sys_context_snowflake_environment) | Properties providing context around the environment in which the function is called. These properties include information about:   - The client, driver, or library that is used to call the function. - The account associated with the session in which the function is called. - The region of that account. |
    | [SNOWFLAKE$ORGANIZATION](/sql-reference/functions/sys_context_snowflake_organization) | Functions providing context around the current organization. |
    | [SNOWFLAKE$ORGANIZATION\_SESSION](/sql-reference/functions/sys_context_snowflake_organization_session) | Properties providing context around the session in which the function is called, when the current account is in an organization. |
    | [SNOWFLAKE$SESSION](/sql-reference/functions/sys_context_snowflake_session) | Properties and functions providing context around the session in which the function is called. |
    | [SNOWFLAKE$SESSION\_ATTRIBUTES](/sql-reference/functions/sys_context_snowflake_session_attributes) | Custom key-value attributes set for the current session using [SET\_SYS\_CONTEXT](/sql-reference/functions/set_sys_context). |

    Expand

    Show lessSee more

`'property'`
:   Name of the property that you want to retrieve. The properties that you can specify depend on the namespace. See the
    [documentation for a namespace](/sql-reference/functions/sys_context#label-sys-context-namespace-list) for the list of properties that you can specify.

`'function'`
:   Name of the function that you want to call. The functions that you can call depend on the namespace. See the
    [documentation for a namespace](/sql-reference/functions/sys_context#label-sys-context-namespace-list) for the list of functions that you can call.

`'argument' [ , ... ]`
:   Arguments to pass to the function that you want to call.

## Returns

The function returns a value whose data type depends on the property that you are retrieving or the
function that you are calling. Most properties and functions return a VARCHAR value or NULL.

2026\_06 behavior change bundle

When the [2026\_06 behavior change bundle](/release-notes/bcr-bundles/2026_06_bundle) is [enabled in your account](/release-notes/bcr-bundles/managing-behavior-change-releases#label-manage-bcr-check-status), `SYS_CONTEXT`
returns a value typed to match the property or function that you access instead of always returning
`VARCHAR`. The following properties and functions return a typed value:

| Namespace | Property or function | Return type |
| --- | --- | --- |
| SNOWFLAKE$SESSION | `ID` | NUMBER |
| SNOWFLAKE$SESSION | `IS_ROLE_ACTIVATED` | BOOLEAN |
| SNOWFLAKE$CURRENT | `IS_ROLE_ACTIVATED` | BOOLEAN |
| SNOWFLAKE$CURRENT | `IS_AGENT_ACTIVATED` | BOOLEAN |
| SNOWFLAKE$APPLICATION | `CURRENT_PATCH` | NUMBER |
| SNOWFLAKE$APPLICATION | `INSTALLED_PATCH` | NUMBER |
| SNOWFLAKE$APPLICATION | `IS_DEV_MODE` | BOOLEAN |
| SNOWFLAKE$APPLICATION | `IS_APPLICATION_ROLE_ACTIVATED` | BOOLEAN |
| SNOWFLAKE$APPLICATION | `IS_CONFIGURATION_SET` | BOOLEAN |
| SNOWFLAKE$ORGANIZATION | `IS_USER_IMPORTED` | BOOLEAN |
| SNOWFLAKE$ORGANIZATION | `IS_GROUP_IMPORTED` | BOOLEAN |
| SNOWFLAKE$ORGANIZATION | `IS_GROUP_ACTIVATED` | BOOLEAN |

Expand

Show lessSee more

All other properties and functions continue to return `VARCHAR`. Existing casts, such as `::BOOLEAN`
or `::NUMBER`, continue to work unchanged.

- The return value depends on the property that you are retrieving or the function that you are calling.

  See the [documentation for each namespace](/sql-reference/functions/sys_context#label-sys-context-namespace-list) for information about the properties and
  return values of functions in that namespace.
- The function returns NULL if:

  - The namespace is not accessible from within the context of the function call. For example, attempting to access properties in
    the SNOWFLAKE$APPLICATION namespace returns NULL if you are calling the function outside of application code.
  - The value of the property or the return value of the function call is NULL or non-existent.

When `SYS_CONTEXT` returns `VARCHAR` (see the preceding note), Boolean-valued properties and functions return the string
`TRUE` or `FALSE`. To compare this return value against the BOOLEAN value TRUE or FALSE,
[cast](/sql-reference/data-type-conversion#label-data-type-explicit-casting) the return value to BOOLEAN. For example:

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$SESSION', 'IS_ROLE_ACTIVATED', 'MY_CUSTOM_ROLE')::BOOLEAN = TRUE;
```

```
+-----------------------------------------------------------------------------------------+
| SYS_CONTEXT('SNOWFLAKE$SESSION', 'IS_ROLE_ACTIVATED', 'MY_CUSTOM_ROLE')::BOOLEAN = TRUE |
|-----------------------------------------------------------------------------------------|
| True                                                                                    |
+-----------------------------------------------------------------------------------------+
```

## Access control requirements

See the [documentation for each namespace](/sql-reference/functions/sys_context#label-sys-context-namespace-list) for information about the access control
requirements for the properties and functions in that namespace.

## Usage notes

See the [documentation for each namespace](/sql-reference/functions/sys_context#label-sys-context-namespace-list) for usage notes for the properties and
functions in that namespace.

## Examples

See the [documentation for each namespace](/sql-reference/functions/sys_context#label-sys-context-namespace-list) for examples of retrieving the properties and
calling the functions in that namespace.
