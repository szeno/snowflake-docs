Categories:
:   [Context functions](/sql-reference/functions-context) (General)

# IS\_ROLE\_ACTIVATED (SYS\_CONTEXT function)

Returns the VARCHAR value `'TRUE'` if an account role is activated. You can check one role or several roles in a single call,
and you can check activation in the session context or in the current execution context.

See also:
:   [IS\_DATABASE\_ROLE\_ACTIVATED (SYS\_CONTEXT function)](/sql-reference/functions/is_database_role_activated) ,
    [SYS\_CONTEXT (SNOWFLAKE$CURRENT namespace)](/sql-reference/functions/sys_context_snowflake_current) ,
    [SYS\_CONTEXT (SNOWFLAKE$SESSION namespace)](/sql-reference/functions/sys_context_snowflake_session)

## Syntax

**Check role activation in the session:**

Copy code

```
SYS_CONTEXT(
  'SNOWFLAKE$SESSION' ,
  'IS_ROLE_ACTIVATED' ,
  '<role>' [ , '<role>' ... ]
)
```

**Check role activation in the current execution context:**

Copy code

```
SYS_CONTEXT(
  'SNOWFLAKE$CURRENT' ,
  'IS_ROLE_ACTIVATED' ,
  '<role>' [ , '<role>' ... ]
)
```

## Arguments

`'SNOWFLAKE$SESSION'`
:   Specifies that you want to check role activation in the session context.

`'SNOWFLAKE$CURRENT'`
:   Specifies that you want to check role activation in the current execution context. The current execution context can differ
    from the session context inside an owner’s rights executable or during an agent invocation. For more information, see
    [SYS\_CONTEXT (SNOWFLAKE$CURRENT namespace)](/sql-reference/functions/sys_context_snowflake_current).

`'IS_ROLE_ACTIVATED'`
:   Calls the IS\_ROLE\_ACTIVATED function.

`'role' [ , 'role' ... ]`
:   Specifies the account role or roles to check. You can pass one role or several roles as separate arguments. The function returns
    `'TRUE'` if any of the specified roles is activated. Multiple roles must be constant values (see the usage notes).

## Returns

The function returns one of the following VARCHAR values:

- `'TRUE'` if any of the specified account roles is activated in the specified context.
- `'FALSE'` if none of the specified account roles is activated, or if none of the specified roles exists.

To compare this return value against the BOOLEAN value TRUE or FALSE, [cast](/sql-reference/data-type-conversion#label-data-type-explicit-casting) the return
value to BOOLEAN. For example:

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$SESSION', 'IS_ROLE_ACTIVATED', 'my_role')::BOOLEAN = TRUE;
```

2026\_06 behavior change bundle

When the [2026\_06 behavior change bundle](/release-notes/bcr-bundles/2026_06_bundle) is [enabled in your account](/release-notes/bcr-bundles/managing-behavior-change-releases#label-manage-bcr-check-status), when you call this
function through `SYS_CONTEXT`, it returns `BOOLEAN` instead of the `VARCHAR`
string `'TRUE'` or `'FALSE'`.

Existing casts, such as `::BOOLEAN` or `::NUMBER`, continue to work unchanged.

For the return type of every property and function by namespace, see
[SYS\_CONTEXT return types](/sql-reference/functions/sys_context#label-sys-context-returns).

## Usage notes

- When you use the SNOWFLAKE$SESSION namespace, the function checks whether the role is in the role hierarchy of the session’s
  primary or secondary roles.
- When you use the SNOWFLAKE$CURRENT namespace, the function checks the innermost execution context. Inside an owner’s rights
  stored procedure, for example, this reflects the owner’s activated roles, not the caller’s.
- When you specify more than one role, the function returns `'TRUE'` if any of the roles is activated. Snowflake ignores
  duplicate role names.
- You can specify multiple roles only when each role is a constant value, such as a string literal. When the role is an
  expression that isn’t a constant, such as a column reference in a row access policy, you can specify only a single role.
- To simulate the result of this function in a policy, use the `SNOWFLAKE$SESSION_ACTIVATED_ROLES` or
  `SNOWFLAKE$CURRENT_ACTIVATED_ROLES` [list argument](/sql-reference/functions/policy_context#label-policy-context-sys-context-list-args)
  with the [POLICY\_CONTEXT](/sql-reference/functions/policy_context) function.

## Examples

The following example returns `'TRUE'` if the role `my_role` is in the role hierarchy of the session’s primary or secondary
roles:

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$SESSION', 'IS_ROLE_ACTIVATED', 'my_role');
```

The following example checks whether the role `analyst` is activated in the current execution context:

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$CURRENT', 'IS_ROLE_ACTIVATED', 'analyst');
```

The following example checks several roles in a single call. It returns `'TRUE'` if any of the roles `analyst`, `auditor`, or
`reviewer` is activated in the session:

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$SESSION', 'IS_ROLE_ACTIVATED', 'analyst', 'auditor', 'reviewer');
```
