Categories:
:   [Context functions](/sql-reference/functions-context) (General)

# IS\_GROUP\_IMPORTED (SYS\_CONTEXT function)

Returns the VARCHAR value `'TRUE'` if the specified group is an [organization user group](/user-guide/organization-users#label-org-users-groups) that
was imported into the current account.

See also:
:   [SYS\_CONTEXT (SNOWFLAKE$ORGANIZATION namespace)](/sql-reference/functions/sys_context_snowflake_organization) ,
    [IS\_GROUP\_ACTIVATED (SYS\_CONTEXT function)](/sql-reference/functions/is_group_activated) ,
    [IS\_USER\_IMPORTED (SYS\_CONTEXT function)](/sql-reference/functions/is_user_imported)

## Syntax

Copy code

```
SYS_CONTEXT(
  'SNOWFLAKE$ORGANIZATION' ,
  'IS_GROUP_IMPORTED' ,
  '<group_name>'
)
```

## Arguments

`'SNOWFLAKE$ORGANIZATION'`
:   Specifies that you want to call a function to return context information about the current organization.

`'IS_GROUP_IMPORTED'`
:   Calls the IS\_GROUP\_IMPORTED function.

`'group_name'`
:   Specifies the name of the organization user group to check.

## Returns

The function returns one of the following VARCHAR values:

- `'TRUE'` if the organization user group was imported into the current account.
- `'FALSE'` if the organization user group was not imported into the current account or is not a valid organization user group.

To compare this return value against the BOOLEAN value TRUE or FALSE, [cast](/sql-reference/data-type-conversion#label-data-type-explicit-casting) the return
value to BOOLEAN. For example:

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$ORGANIZATION', 'IS_GROUP_IMPORTED', 'my_group_name')::BOOLEAN = TRUE;
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

The following example returns `'TRUE'` if the group `my_group_name` is an organization user group that was imported into the
current account:

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$ORGANIZATION', 'IS_GROUP_IMPORTED', 'my_group_name');
```
