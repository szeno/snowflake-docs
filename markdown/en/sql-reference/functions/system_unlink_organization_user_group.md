Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$UNLINK\_ORGANIZATION\_USER\_GROUP

Unlinks an access control role from an [organization user group](/user-guide/organization-users#label-org-users-groups) so it can be managed as a local role going
forward.

## Syntax

Copy code

```
SYSTEM$UNLINK_ORGANIZATION_USER_GROUP( '<role>' )
```

## Arguments

`'role'`
:   Name of an access control role that is linked to an organization user group.

## Usage notes

When you unlink an organization user group, user objects that were added to the regular account when the group was imported are also
unlinked.

## Examples

Copy code

```
SELECT SYSTEM$UNLINK_ORGANIZATION_USER_GROUP('marketing_team');
```
