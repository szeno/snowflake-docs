Categories:
:   [Context functions](/sql-reference/functions-context) (General)

# IS\_DATABASE\_ROLE\_ACTIVATED (SYS\_CONTEXT function)

Returns the VARCHAR value `'TRUE'` if a database role is activated. You can check activation in the session context or in the
current execution context.

See also:
:   [IS\_ROLE\_ACTIVATED (SYS\_CONTEXT function)](/sql-reference/functions/is_role_activated) ,
    [SYS\_CONTEXT (SNOWFLAKE$CURRENT namespace)](/sql-reference/functions/sys_context_snowflake_current) ,
    [SYS\_CONTEXT (SNOWFLAKE$SESSION namespace)](/sql-reference/functions/sys_context_snowflake_session)

## Syntax

**Check database role activation in the session:**

Copy code

```
SYS_CONTEXT(
  'SNOWFLAKE$SESSION' ,
  'IS_DATABASE_ROLE_ACTIVATED' ,
  '<database_role>'
)
```

**Check database role activation in the current execution context:**

Copy code

```
SYS_CONTEXT(
  'SNOWFLAKE$CURRENT' ,
  'IS_DATABASE_ROLE_ACTIVATED' ,
  '<database_role>'
)
```

## Arguments

`'SNOWFLAKE$SESSION'`
:   Specifies that you want to check database role activation in the session context.

`'SNOWFLAKE$CURRENT'`
:   Specifies that you want to check database role activation in the current execution context. The current execution context can
    differ from the session context inside an owner’s rights executable or during an agent invocation. For more information, see
    [SYS\_CONTEXT (SNOWFLAKE$CURRENT namespace)](/sql-reference/functions/sys_context_snowflake_current).

`'IS_DATABASE_ROLE_ACTIVATED'`
:   Calls the IS\_DATABASE\_ROLE\_ACTIVATED function.

`'database_role'`
:   Specifies the database role to check. The name can be fully qualified or relative.

## Returns

The function returns one of the following VARCHAR values:

- `'TRUE'` if the specified database role is in the active role hierarchy of the specified context.
- `'FALSE'` if the specified database role isn’t in the active role hierarchy, or if the database role doesn’t exist.

To compare this return value against the BOOLEAN value TRUE or FALSE, [cast](/sql-reference/data-type-conversion#label-data-type-explicit-casting) the return
value to BOOLEAN. For example:

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$SESSION', 'IS_DATABASE_ROLE_ACTIVATED', 'my_db_role')::BOOLEAN = TRUE;
```

2026\_06 behavior change bundle

When the [2026\_06 behavior change bundle](/release-notes/bcr-bundles/2026_06_bundle) is [enabled in your account](/release-notes/bcr-bundles/managing-behavior-change-releases#label-manage-bcr-check-status), this function
continues to return `VARCHAR` (the string `'TRUE'` or `'FALSE'`) rather than `BOOLEAN`.

Existing casts, such as `::BOOLEAN` or `::NUMBER`, continue to work unchanged.

For the return type of every property and function by namespace, see
[SYS\_CONTEXT return types](/sql-reference/functions/sys_context#label-sys-context-returns).

## Usage notes

- When you use the SNOWFLAKE$SESSION namespace, the function checks whether the database role is in the role hierarchy of the
  session’s primary or secondary roles.
- When you use the SNOWFLAKE$CURRENT namespace, the function checks the innermost execution context. Inside an owner’s rights
  stored procedure, for example, this reflects the owner’s activated roles, not the caller’s.
- This function isn’t supported in governance policies (such as masking policies, row access policies, or projection policies)
  applied to shared tables. Shared objects can’t access consumer session state.
- If you don’t specify a fully qualified name, the function resolves the database context of the database role as follows:

  - **Queries:** Session database (the database currently in use).
  - **Body of a data protection policy:** Database containing the protected table or view.
  - **Sharing:** Database in the consumer account.
- This function can’t be used in materialized view definitions because the function isn’t deterministic.
- To simulate the result of this function in a policy, use the `SNOWFLAKE$SESSION_ACTIVATED_DATABASE_ROLES` or
  `SNOWFLAKE$CURRENT_ACTIVATED_DATABASE_ROLES` [list argument](/sql-reference/functions/policy_context#label-policy-context-sys-context-list-args)
  with the [POLICY\_CONTEXT](/sql-reference/functions/policy_context) function.

## Examples

Check a database role in the current database using a relative name:

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$SESSION', 'IS_DATABASE_ROLE_ACTIVATED', 'ANALYST_ROLE');
```

```
+-------------------------------------------------------------------------+
| SYS_CONTEXT('SNOWFLAKE$SESSION', 'IS_DATABASE_ROLE_ACTIVATED', 'ANA...  |
+-------------------------------------------------------------------------+
| TRUE                                                                    |
+-------------------------------------------------------------------------+
```

Check a database role in a different database using a fully qualified name:

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$SESSION', 'IS_DATABASE_ROLE_ACTIVATED', 'DB2.READER_ROLE');
```

```
+-------------------------------------------------------------------------+
| SYS_CONTEXT('SNOWFLAKE$SESSION', 'IS_DATABASE_ROLE_ACTIVATED', 'DB ...  |
+-------------------------------------------------------------------------+
| TRUE                                                                    |
+-------------------------------------------------------------------------+
```

Check a database role in the current execution context (which may differ from the session context inside an owner’s rights
executable):

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$CURRENT', 'IS_DATABASE_ROLE_ACTIVATED', 'ANALYST_ROLE');
```
