Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$LINK\_ORGANIZATION\_USER

Links an [organization user](/user-guide/organization-users) with a user that already exists in the regular account.

When an account administrator adds an organization user group to a regular account, a conflict arises when an organization user in the
group corresponds to a person or service that already has a user object in the account. This function resolves the conflict and allows the
user to be managed as an organization user going forward.

## Syntax

Copy code

```
SYSTEM$LINK_ORGANIZATION_USER( '<local_user>', '<org_user>' )
```

## Arguments

`'local_user'`
:   Name of a user object that exists in the regular account.

`'org_user'`
:   Name of the organization user that corresponds to the same person or service as `local_user`.

## Usage notes

Linking an organization user to a local user object replaces the EMAIL property of the local user with the EMAIL property of the
organization user.

The `TYPE` property of the local user must be compatible with the `TYPE` property of the organization user. Snowflake treats a user whose
`TYPE` property is `NULL` as a `PERSON` user, so the types are compatible in the following cases:

| Organization user type | Compatible local user types |
| --- | --- |
| `PERSON` | `PERSON`, `NULL` |
| `SERVICE` | `SERVICE` |

Expand

Show lessSee more

If the types aren’t compatible, the function returns an error and the local user isn’t linked. For example, you can’t link a `SERVICE`
local user to a `PERSON` organization user. Because the type of an organization user can’t be changed, resolve this kind of conflict by
creating the organization user with the type you need, or by using [ALTER USER](/sql-reference/sql/alter-user) to change the type of the local user
before you link it. After a local user is linked, its `TYPE` property can no longer be changed in the regular account. For more
information about organization user types, see [Organization user types](/user-guide/organization-users#label-org-users-types).

## Examples

Link the local user `jloeb` with the organization user of the same name:

Copy code

```
SELECT SYSTEM$LINK_ORGANIZATION_USER('jloeb', 'jloeb');
```

Link a local service user with a `SERVICE` organization user. Both users are `SERVICE` users, so the types are compatible:

Copy code

```
SELECT SYSTEM$LINK_ORGANIZATION_USER('etl_pipeline', 'etl_pipeline');
```
