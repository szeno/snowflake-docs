Categories:
:   [Context functions](/sql-reference/functions-context) (General)

# IS\_GROUP\_ACTIVATED (SYS\_CONTEXT function)

Returns the VARCHAR value `'TRUE'` if the role representing an [organization user group](/user-guide/organization-users#label-org-users-groups) is
activated in a given context.

See also:
:   [SYS\_CONTEXT (SNOWFLAKE$ORGANIZATION namespace)](/sql-reference/functions/sys_context_snowflake_organization) ,
    [IS\_GROUP\_IMPORTED (SYS\_CONTEXT function)](/sql-reference/functions/is_group_imported) ,
    [IS\_USER\_IMPORTED (SYS\_CONTEXT function)](/sql-reference/functions/is_user_imported)

## Syntax

Copy code

```
SYS_CONTEXT(
  'SNOWFLAKE$ORGANIZATION' ,
  'IS_GROUP_ACTIVATED' ,
  '<context>' ,
  '<group_name>'
)
```

## Arguments

`'SNOWFLAKE$ORGANIZATION'`
:   Specifies that you want to call a function to return context information about the current organization.

`'IS_GROUP_ACTIVATED'`
:   Calls the IS\_GROUP\_ACTIVATED function.

`'context'`
:   Specifies the execution context that you want to check. You can specify one of the following values:

    - `SESSION`: Checks if the organization group role is in the role hierarchy of the current session’s primary or secondary
      roles. The function returns `'TRUE'` if the role is in the role hierarchy.
    - `ACTIVE`: Checks if the organization group role is in the role hierarchy in the context of the current call.

      For example, in a call to an owner’s rights stored procedure, the procedure is executed by the owner’s role. The function
      returns `'TRUE'` if the organization group role is in the role hierarchy of the owner’s role.

`'group_name'`
:   Specifies the name of the organization user group to check.

## Returns

The function returns one of the following VARCHAR values:

- `'TRUE'` if the organization user group role is activated in the context specified by `context`.
- `'FALSE'` if the organization user group role is not activated in that context or if the group is not a valid organization
  user group.

To compare this return value against the BOOLEAN value TRUE or FALSE, [cast](/sql-reference/data-type-conversion#label-data-type-explicit-casting) the return
value to BOOLEAN. For example:

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$ORGANIZATION', 'IS_GROUP_ACTIVATED', 'SESSION', 'my_group_name')::BOOLEAN = TRUE;
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

The following example returns `'TRUE'` if the role for the organization user group `my_group_name` is in the role hierarchy
of the session’s primary or secondary roles:

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$ORGANIZATION', 'IS_GROUP_ACTIVATED', 'SESSION', 'my_group_name');
```
