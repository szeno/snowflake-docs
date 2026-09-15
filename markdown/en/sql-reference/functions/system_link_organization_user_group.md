Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$LINK\_ORGANIZATION\_USER\_GROUP

Links an [organization user group](/user-guide/organization-users#label-org-users-groups) with an access control role that already exists in the regular account.

When an account administrator adds an organization user group to a regular account, a conflict arises if there is an existing role with the
same name as the group. This function resolves the conflict and allows the role to be managed as an organization user group going forward.

## Syntax

Copy code

```
SYSTEM$LINK_ORGANIZATION_USER_GROUP( <name> )
```

## Arguments

`name`
:   Name of an organization user group. This matches the name of an existing access control role.

## Usage notes

You can’t link an organization user group to a role that is granted to other roles.

## Examples

Copy code

```
SELECT SYSTEM$LINK_ORGANIZATION_USER_GROUP('marketing_team');
```
