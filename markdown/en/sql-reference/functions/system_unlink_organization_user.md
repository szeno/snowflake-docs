Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$UNLINK\_ORGANIZATION\_USER

Unlinks a user object from an [organization user](/user-guide/organization-users) so it can be managed as a local user going forward.

## Syntax

Copy code

```
SYSTEM$UNLINK_ORGANIZATION_USER( '<user_name>' )
```

## Arguments

`'user_name'`
:   Name of a user object that was imported from an organization user.

## Examples

Copy code

```
SELECT SYSTEM$UNLINK_ORGANIZATION_USER('jloeb');
```
