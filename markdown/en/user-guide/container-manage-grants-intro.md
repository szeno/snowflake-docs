# Delegating grant management with container-level MANAGE GRANTS

This topic provides an introduction to container-level `MANAGE GRANTS` for databases and schemas.

Opt in to inherited grants and container-level MANAGE GRANTS

One account parameter enables both features. Use the [ALTER ACCOUNT](/sql-reference/sql/alter-account) command to opt in. For
example:

Copy code

```
ALTER ACCOUNT SET FEATURE_RBAC_INHERITED_GRANTS = 'ENABLED';
```

To turn both features back off for the account:

Copy code

```
ALTER ACCOUNT SET FEATURE_RBAC_INHERITED_GRANTS = 'DISABLED';
```

## What are container-level MANAGE GRANTS?

The `MANAGE GRANTS` privilege allows a role to manage access on securable objects using direct grants and inherited
grants. A role with account-level `MANAGE GRANTS` can manage privileges broadly across the account.

`MANAGE GRANTS` on databases and schemas are container-level `MANAGE GRANTS` that provide a more scoped way to delegate
grant management. The role that holds `MANAGE GRANTS` on a container can manage direct and inherited grants on objects
inside that container (including the container itself) and only that container, without involving `SECURITYADMIN` or
`ACCOUNTADMIN`.

Container-level `MANAGE GRANTS` provides a narrower administrative boundary than account-level `MANAGE GRANTS`.
However, the role is still trusted to make broad authorization decisions within the specified database or schema.

## Why use container-level MANAGE GRANTS

Container-level `MANAGE GRANTS` delegates the authority to decide who receives access, unlike inherited grants, which
only grant the access itself. Letting the delegated role define both direct and inherited grants on objects within
the container lets database and schema administrators manage grants on the containers they administer, without
involving `SECURITYADMIN` or `ACCOUNTADMIN` for every change.

## When to use container-level MANAGE GRANTS

Use container-level `MANAGE GRANTS` when a trusted administrator needs to independently decide which roles receive
which grants within a database or schema.

For example, use container-level `MANAGE GRANTS` when:

- A database administrator is responsible for defining and changing access for a data domain.
- Different schema administrators independently administer access within their own schemas.
- You need to delegate grant administration without granting account-wide `MANAGE GRANTS`.

Don’t grant `MANAGE GRANTS` solely to give a role access to objects. If the required access can be expressed
directly, prefer the mechanism that describes that access without delegating grant-management authority. See
[When to use inherited grants](/user-guide/inherited-grants-intro#label-inherited-grants-intro-when) for guidance on
choosing between inherited and direct grants.

| Requirement | Recommended mechanism |
| --- | --- |
| An administrator must decide which roles receive which grants within a database or schema | Container-level `MANAGE GRANTS` |
| An administrator must manage grants across the entire account | Account-level `MANAGE GRANTS` |

Expand

Show lessSee more

Container-level `MANAGE GRANTS` reduces the scope of delegated authority compared with account-level `MANAGE GRANTS`,
but it remains a powerful administrative privilege.

## How container-level MANAGE GRANTS works

A role that holds container-level `MANAGE GRANTS` is a role granted `MANAGE GRANTS` on a specific container. The
privilege must be granted explicitly, because owning a database or schema doesn’t confer it. Within that container, the
role can do everything a holder of `MANAGE GRANTS ON ACCOUNT` can do today, but it cannot affect grants on objects
outside the container. Specifically, a role that holds container-level `MANAGE GRANTS` can:

- Resolve any securable inside the container in a grant-management call such as `SHOW`, `GRANT`, or `DESCRIBE`. For
  example, `SHOW TABLES` returns every table inside the container.
- Grant or revoke direct and inherited grants on objects inside the container.
- Grant `MANAGE GRANTS` on lower-level containers inside the container, such as on schemas inside its database, if the
  role holds `MANAGE GRANTS WITH GRANT OPTION`.

A role that holds container-level `MANAGE GRANTS` cannot delegate `MANAGE GRANTS` on the *same* container, or on
container object types inside the same container, to another role unless it holds
`MANAGE GRANTS WITH GRANT OPTION` on that container.

### Comparison with account-level MANAGE GRANTS

| Aspect | `MANAGE GRANTS ON ACCOUNT` | `MANAGE GRANTS ON DATABASE` / `SCHEMA` |
| --- | --- | --- |
| Typical holder | `SECURITYADMIN` | A delegated role (for example, `sales_admin`) |
| Scope of authority | All objects in the account | Only objects in the specified container |
| Can transfer ownership | Yes | No |
| Trust assumption | Holder is fully trusted at the account level | Holder must be trusted at the container level |

Expand

Show lessSee more

## Security considerations

`MANAGE GRANTS` is a powerful privilege. Grant it only to roles that are trusted to administer access within the
specified scope of authority.

### Treat MANAGE GRANTS as an administrative trust boundary

Granting `MANAGE GRANTS` on a database or schema means you trust the role to make authorization decisions about
securable objects throughout that container.

Within its scope of authority, the administrator can grant privileges that expose data or allow object execution, and
can revoke privileges required by users and workloads. As a result, misuse or compromise of a role
that holds `MANAGE GRANTS` can affect both:

- **Confidentiality**, by granting unintended access.
- **Availability**, by revoking access required by legitimate workloads.

Container-level `MANAGE GRANTS` limits the blast radius compared with account-level `MANAGE GRANTS`. It does not
eliminate the need to trust the administrator within that boundary.

### Use the narrowest practical scope of authority

Prefer schema-level `MANAGE GRANTS` when access administration should be limited to one schema.

Copy code

```
GRANT MANAGE GRANTS ON SCHEMA prod.finance
  TO ROLE finance_access_admin;
```

Use database-level `MANAGE GRANTS` only when the role should manage grants across the database.

Copy code

```
GRANT MANAGE GRANTS ON DATABASE prod
  TO ROLE prod_access_admin;
```

Use account-level `MANAGE GRANTS` only when account-wide grant management is required.

Choose a container whose contents are expected to share the same grant-administration trust boundary.

Granting `MANAGE GRANTS` on a database also gives the administrator grant-management authority over schemas added to
that database later. For example, the database-level grant above also gives `prod_access_admin` authority over any
schema created in `prod` after the grant is made.

Before using database-level `MANAGE GRANTS`, consider whether schemas that exist now or might be created later need a
different administrative trust boundary. If they do, prefer schema-level `MANAGE GRANTS` for those schemas instead.

Container boundaries should align with administrative security boundaries, not only organizational convenience.

### Container-level MANAGE GRANTS can expand access

A role with container-level `MANAGE GRANTS` can grant privileges to other roles within its scope of authority.

For example, a role with `MANAGE GRANTS ON SCHEMA prod.finance` can grant access to supported objects in
`prod.finance`. Depending on the privileges granted, this can expose data, allow object execution, or grant access
more broadly than intended.

Treat container-level `MANAGE GRANTS` as delegated access administration, not as a low-risk privilege.

### Use caution with executable objects

Container-level `MANAGE GRANTS` can allow an administrator to grant execution privileges, such as `USAGE` or
`EXECUTE`, on supported executable objects in the container. Because some objects execute with the privileges of the
object owner, the security impact can be greater than granting access to ordinary data objects. See
[Use caution with executable objects](/user-guide/inherited-grants-intro#label-inherited-grants-intro-executable-objects)
for the object types involved and how owner-executed objects can expose privileges.

Before delegating `MANAGE GRANTS` on a container, verify that the administrator is trusted to decide who can invoke
every supported executable object in it. When possible, separate containers that hold highly privileged executable
objects from containers where grant administration is delegated more broadly.

### MANAGE GRANTS does not grant object access by itself

`MANAGE GRANTS` does not by itself allow a role to query data, create objects, modify objects, execute objects, or
use warehouses.

However, a role that holds `MANAGE GRANTS` can grant and revoke supported privileges within its scope of authority.
Evaluate the security impact of `MANAGE GRANTS` based on the authorization decisions the holder can make, not only on
the object access the holder receives directly. See
[When to use container-level MANAGE GRANTS](#label-container-manage-grants-intro-when) for guidance on granting object
access directly instead.

### Audit container-level MANAGE GRANTS regularly

Regularly review roles that have `MANAGE GRANTS` at the account, database, and schema levels.

Pay particular attention to:

- `MANAGE GRANTS` on sensitive databases and schemas.
- Roles that hold `MANAGE GRANTS WITH GRANT OPTION`.
- Lower-level `MANAGE GRANTS` delegations created by other delegated administrators.
- Containers that contain owner-executed objects.
- Changes to the contents of containers with delegated grant administration.

Don’t review only which roles currently hold `MANAGE GRANTS`. Also review the direct and inherited grants that
delegated administrators have created within their scope.

When reviewing a role that receives privileges from delegated administrators, consider the role hierarchy through
which those privileges can become available to other roles.

Copy code

```
SHOW GRANTS TO ROLE finance_access_admin;
SHOW GRANTS ON DATABASE prod;
SHOW GRANTS ON SCHEMA prod.finance;
```

For historical review, use the `GRANTS_TO_ROLES` view in `ACCOUNT_USAGE`.

### Revoking MANAGE GRANTS does not undo previous grant changes

Revoking `MANAGE GRANTS` prevents a role from performing future grant-management operations that require that
privilege. It does not automatically revoke other direct or inherited grants that the administrator previously
created.

For example, suppose `sales_admin` uses its delegated authority to grant `SELECT` to another role. Revoking
`MANAGE GRANTS` from `sales_admin` does not automatically revoke that `SELECT` privilege.

`CASCADE` doesn’t change this. Revoking with `CASCADE` removes dependent `MANAGE GRANTS` privileges that the
administrator delegated to other roles, but not the direct or inherited grants that the administrator or any of those
roles created.

If you revoke `MANAGE GRANTS` because an administrator is no longer trusted, because the privilege was granted too
broadly, or as part of an incident response:

1. Remove the grant-management authority.
2. Review grants in the affected scope.
3. Identify access created or changed through the delegated administration model.
4. Revoke privileges that are no longer intended.
5. Verify the resulting effective access.

Don’t assume that revoking `MANAGE GRANTS` restores the authorization state that existed before the privilege was
granted.

## Limitations

- **No ownership transfer:** Container-level `MANAGE GRANTS` doesn’t authorize `GRANT OWNERSHIP`. Transferring
  ownership requires the `OWNERSHIP` privilege on the object or account-level `MANAGE GRANTS`. Stricter rules apply to
  owner-executed objects; see
  [Stricter authorization for ownership transfer of owner-executed objects](/user-guide/inherited-grants-intro#label-inherited-grants-intro-ownership-transfer).
- **Not supported on imported databases:** `MANAGE GRANTS` can’t be granted on an imported (consumer-side) database or
  on a schema inside one.

**Next Topics:**

- [Using container-level MANAGE GRANTS](/user-guide/container-manage-grants-using)
