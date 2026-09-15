# Managing access with inherited grants

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

## What are inherited grants?

An inherited grant is a single grant created on a container object (`ACCOUNT`, `DATABASE`, or `SCHEMA`) that
automatically applies to every current and future object of a specified type within that container. Inherited grants
are created with the `INHERITED` keyword in the standard `GRANT` statement, and creating one requires `MANAGE GRANTS`
on the container or a higher container; owning the container alone doesn’t authorize it.

## Why use inherited grants

For access requirements that apply uniformly to all current and future objects of a type, Snowflake recommends using
inherited grants instead of maintaining equivalent combinations of bulk, future, or repeated object-level grants. A
single inherited grant describes the requirement directly: the privilege, object type, scope, and grantee are defined
once, and access stays consistent as the container’s contents evolve.

If your requirement is instead to delegate the ability to decide which roles receive which privileges, use
[container-level `MANAGE GRANTS`](/user-guide/container-manage-grants-intro).

- **Ease of use:** Express container-wide intent with one statement. A single
  `GRANT INHERITED <privilege> ON ALL <object_type_plural> IN <container>` replaces multiple grants for existing and new
  objects. Adding a new object to a container, such as a new table in a database, requires no follow-up grant
  administration.
- **Reduce grant proliferation and simplify role hierarchy:** One inherited grant takes the place of many individual
  records. Inherited grants allow access to be managed at the container level instead of using object-specific roles.
  This simplifies the grant catalog and the role hierarchy complexity, making role-based access easier to reason about
  during reviews.
- **Consistent authorization profile:** Because the privilege is defined once at the container level, every object of
  the specified type receives identical access. This eliminates drift between objects that may otherwise accumulate
  when grants are issued one object at a time.
- **Small compile-time improvement for complex queries:** Because a container’s access is defined once instead of once
  per object, Snowflake evaluates fewer grant records when compiling a query that references many objects. For
  complex queries that touch a large number of tables or views, this can modestly reduce query compilation time.
- **Application access at scale:** Snowflake Native Apps can be granted broad read access to a container with one
  inherited grant per object type.
- **Auditability:** Inherited grants are recorded at the container level, which makes container-wide access reviewable
  from a single row. New columns on `SHOW GRANTS` and the `GRANTS_TO_ROLES` view (`IS_INHERITED`, `INHERITED_FROM`,
  `INHERITED_FROM_DATABASE`, `INHERITED_FROM_SCHEMA`) let auditors trace any per-object access back to the inherited
  grant that authorized it.

## How inherited grants work

An inherited grant is indicated by the keyword `INHERITED` and has four parts:

| Part | Description |
| --- | --- |
| Privilege | The action allowed, such as `SELECT`, `INSERT`, `USAGE`, or `MODIFY`. |
| Object type | The specific type of object the grant applies to, such as `TABLES`, `EVENT TABLES`, or `HYBRID TABLES`. |
| Container | The account, database, or schema on which the grant is created. |
| Grantee | The entity that receives the privilege. Account roles, database roles, users, and applications can be used as grantees for inherited grants. |

Expand

Show lessSee more

Example:

Copy code

```
GRANT INHERITED SELECT ON ALL TABLES
  IN SCHEMA prod.analytics
  TO ROLE analyst_role;
```

This statement creates an inherited grant for tables in the `prod.analytics` schema.

Snowflake applies the inherited grant to matching existing tables in the schema. Snowflake also applies the same
privilege to matching tables created later in the schema.

## When to use inherited grants

Inherited grants are designed for the standard case where a role should have a uniform privilege across every current
and future object of a given type in a container. They are not the right choice for every scenario.

### Use inherited grants when

- **You want a role to have a uniform privilege across all objects of a type in a container.** For example, an analyst
  role that should be able to `SELECT` from every table in a database. This is the canonical use case.
- **You want new objects to be automatically covered without administrative action.** Inherited grants eliminate the
  need to maintain future grants or to backfill grants when a new object is created.
- **You manage grants at the container level rather than the object level.** If your access model is “this role gets
  read access to this database,” inherited grants express that intent in a single statement.
- **You are granting access to a Snowflake-managed application** (for example, a governance scanner) that needs to see
  every current and future object in a container.
- **You are operating at scale.** Customers with large numbers of grants benefit from the reduction in grant records,
  which improves authorization performance.

### Use direct grants when

- **Some objects must not receive the privilege.** An inherited grant applies uniformly to every matching object in
  its scope and does not provide an object-level deny or exclusion. If a role must not have `SELECT` on particular
  tables, use direct grants for the objects the role should access, or use a narrower inherited-grant scope that
  excludes the sensitive objects. If the role may access the object but certain rows or columns require additional
  protection, use [row access policies](/user-guide/security-row-intro) or
  [masking policies](/user-guide/security-column-intro) as appropriate.
- **Different objects in the container need different privileges.** If some tables should be `SELECT`-only and others
  should be `INSERT`-able, model the difference with direct grants on the appropriate objects rather than
  overgranting via inheritance.
- **The privilege should not extend to future objects.** Inherited grants always cover future objects of the specified
  type. If you want to grant a privilege on the objects that exist *today* and explicitly require a review step before
  new objects are added, use `GRANT ... ON ALL <object_type_plural> IN <container>` (the existing one-time bulk grant).
- **You are granting on object types not supported by inherited grants** (see
  [Limitations](#label-inherited-grants-intro-limitations) in this topic).

The following table summarizes the guidance on when to use inherited vs. direct grants:

| Scenario | Use |
| --- | --- |
| Role needs the same privilege on all current and future objects of a type | **Inherited grant** |
| Role must not have the privilege on some objects in the container | **Direct grants**, or an inherited grant at a narrower scope |
| Role can access all objects, but sensitive rows or columns require different protection | **Inherited grant** + row access or masking policies |
| Different objects require different object privileges | **Direct grants** |
| Role needs the same access to objects that exist today, with explicit review before new objects receive access | **`GRANT ... ON ALL`** or direct grants |
| Application needs access to every current and future object of supported types in a container | **Inherited grant** for each required object type |
| A trusted administrator needs to independently decide who receives which privileges | **Container-level `MANAGE GRANTS`** |

Expand

Show lessSee more

## Security considerations

### Inherited grants do not provide object-level exceptions

An inherited grant applies the specified privilege to every matching object in its scope, and you cannot revoke the
privilege from one individual object to create an exception.

The failure mode is silent. Given the following grant:

Copy code

```
GRANT INHERITED SELECT ON ALL TABLES
  IN DATABASE sales_db
  TO ROLE analyst;
```

revoking `SELECT` on one table appears to succeed, but `analyst` retains `SELECT` on that table through the inherited
grant. No error indicates that the exception wasn’t created.

Use inherited grants only when the privilege is intended to apply uniformly throughout the selected scope. See
[Use direct grants when](#label-inherited-grants-intro-when) for the alternatives.

### Container membership can change effective access

An inherited grant applies to every matching current and future object in its scope. This includes objects created in
the container and objects that become members of the container through supported move or clone operations.

Important

Creating, moving, or cloning an object into a container can change who can access that object even though no new
`GRANT` statement is issued.

Treat a container with inherited grants as an access-requirement boundary. Before creating, moving, or cloning a
sensitive object into a container, review the inherited grants that apply to the target container.

Cross-container schema clone or move requires particular care because matching child objects can become subject to
inherited grants in the target container.

### Use caution with executable objects

Some Snowflake objects can execute with the privileges of the object owner rather than only the privileges of the
caller. For example, owner’s-rights stored procedures run with the privileges of the procedure owner.

Inherited grants do not change object ownership. However, an inherited grant can grant a privilege such as `USAGE` or
`EXECUTE` on current and future executable objects. This can allow a role to invoke objects that run with the owner’s
privileges.

Review inherited grants carefully for executable object types, such as procedures, functions, tasks, alerts, services,
and Streamlit in Snowflake apps.

Before granting inherited execution access, verify that:

- The role should be allowed to invoke every matching current and future object in the scope.
- The object type’s execution model is understood.
- Owner-executed objects do not expose privileges beyond the intended operation.

### Align container scope with the access requirement

Use the narrowest practical scope for inherited grants.

Choose a container where all matching objects are expected to share the same access requirement, including objects
that might be added in the future.

For example, if all tables in `prod.finance` should be readable by `finance_reader`, a schema-level inherited grant
accurately represents that requirement:

Copy code

```
GRANT INHERITED SELECT ON ALL TABLES
  IN SCHEMA prod.finance
  TO ROLE finance_reader;
```

Don’t use a broader database-level inherited grant merely to reduce the number of grant statements if the database
contains schemas with different security requirements.

Also consider the role hierarchy of the grantee. An inherited privilege granted to a role can become available
through roles that inherit from that role. When reviewing the scope of an inherited grant, review both the container
boundary and the role hierarchy.

### Account scope reaches every database, including personal databases

`ACCOUNT` is the broadest scope available to an inherited grant. An account-scope grant covers every matching object in
every database in the account, including databases created later and objects inside
[personal databases](/user-guide/personal-databases).

Personal databases are private workspaces that each user owns. An account-scope inherited grant reaches into them
without any grant being issued on the individual database, so a statement such as:

Copy code

```
GRANT INHERITED SELECT ON ALL TABLES
  IN ACCOUNT
  TO ROLE analyst;
```

gives `analyst` read access to tables in every user’s personal database, and to every personal database created
afterward.

Before using `ACCOUNT` scope, confirm that the grantee should have the privilege on objects in every current and future
database. If the requirement applies to a known set of databases, issue a database-level or schema-level inherited
grant for each one instead.

### Validate access-review and entitlement tooling

See [Information Schema visibility](#label-inherited-grants-intro-information-schema) in Limitations for how
Information Schema views handle inherited-grant access. Before adopting inherited grants, validate access-review,
entitlement-management, and security-audit tooling that relies on Information Schema, unless you have already opted
in to the 2026\_07 behavior change bundle.

To review inherited access, use inherited-grant-aware sources such as:

Copy code

```
SHOW INHERITED GRANTS IN DATABASE sales_db;
SHOW GRANTS ON TABLE sales_db.us_west.orders;
```

or `SNOWFLAKE.ACCOUNT_USAGE.GRANTS_TO_ROLES`.

When reviewing the grantee, also review its role hierarchy to determine which additional roles can exercise the
privilege.

### Stricter authorization for ownership transfer of owner-executed objects

`GRANT OWNERSHIP` on an owner-executed object to a role outside your active role hierarchy now fails with an
authorization error. Previously the statement succeeded. The change prevents privilege escalation: with inherited
grants, a role can retain `USAGE` on an object it has transferred away, which would let it execute the object’s body
under the new owner’s privileges.

The change only applies to ownership transfers of **owner-executed objects**, that is, objects whose body or schedule
runs with the new owner’s privileges:

| Category | Object types |
| --- | --- |
| Queryable Objects | `VIEW`, `MATERIALIZED VIEW`, `DYNAMIC TABLE`, `SEMANTIC VIEW`, `EXTERNAL TABLE`, `DIRECTORY TABLE`, `EVENT TABLE` |
| Procedures and DMFs | `PROCEDURE`, `FUNCTION`, `DATA METRIC FUNCTION` |
| Schedulers and triggers | `TASK`, `ALERT` |
| Ingest | `PIPE` |
| Function-based policies | `MASKING POLICY`, `ROW ACCESS POLICY`, `AGGREGATION POLICY`, `PROJECTION POLICY`, `JOIN POLICY`, `TOKENIZATION POLICY`, `PRIVACY POLICY`, `STORAGE LIFECYCLE POLICY` |
| File-based code | `STREAMLIT`, `DCM PROJECT` |
| Container services | `SNOWSERVICE INSTANCE` |
| Composites | `CORTEX SEARCH SERVICE` |

Expand

Show lessSee more

The following remain unchanged:

- `GRANT OWNERSHIP` on objects that are not owner-executed (tables, schemas, databases, sequences, stages, and so on).
- `GRANT OWNERSHIP ... COPY CURRENT GRANTS`, which has always required account-level `MANAGE GRANTS` or that the
  receiver role be in the caller’s role hierarchy.
- Account-level `MANAGE GRANTS` (held by `SECURITYADMIN`) continues to authorize ownership transfer to any role.

To transfer ownership of an owner-executed object, the caller must either:

- Have the receiver role in their active role hierarchy (that is, the receiver role has been granted, directly or
  transitively, to the role they are using), or
- Hold account-level `MANAGE GRANTS`.

Container-level `MANAGE GRANTS` (held on a database or schema) does not authorize the transfer.

## Limitations

### Privileges that cannot be granted as inherited grants

The following privileges are not eligible for inheritance:

- `OWNERSHIP`.
- Privileges whose only target is the account (for example, `CREATE WAREHOUSE`, `MANAGE WAREHOUSES`, `MONITOR USAGE`).
  Inherited grants flow from a container to objects inside the container, so privileges that have no enclosing
  container cannot be inherited.
- `USAGE` on `ROLE` and `USAGE` on `USER`.
- `USAGE` on `STREAMLIT`.
- `USAGE` on `XMLA_ENDPOINT`.

### Object types that cannot be targets of an inherited grant

`GRANT INHERITED <privilege> ON <type> IN <container>` is rejected when `<type>` is one of:

- `ORGANIZATION`
- `APPLICATION` (consumer-side installed app)
- `APPLICATION PACKAGE`
- `SHARE`
- `INTEGRATION`

### Account scope excludes native apps and bundles

`GRANT INHERITED <privilege> ON ALL <object_type_plural> IN ACCOUNT` does not flow into objects that live inside an `APPLICATION`
(consumer-side) or `APPLICATION PACKAGE` (provider-side) container.

### Data sharing and the Native App Framework

Inherited grants are not compatible with cross-account sharing boundaries. The following are rejected:

- Granting inherited privileges on an **imported (shared) database** or any schema or object inside one.
- Granting inherited privileges on objects that belong to a foreign account.
- Granting inherited privileges **to a database role from an imported database**, or to a database role that has
  already been shared with a consumer.
- Granting a database role that holds inherited grants **to a share**.
- Granting inherited privileges **to an `APPLICATION ROLE`**.
- Granting inherited privileges on an `APPLICATION PACKAGE` or on a consumer-side `APPLICATION` object (covered by the
  unsupported object types list above).

### Restricted clauses

Inherited grants cannot be combined with `WITH GRANT OPTION`, `CASCADE`, or `RESTRICT`.

### Information Schema visibility

2026\_07 behavior change bundle

When the [2026\_07 behavior change bundle](/release-notes/bcr-bundles/2026_07_bundle) is
[enabled in your account](/release-notes/bcr-bundles/managing-behavior-change-releases#label-manage-bcr-check-status),
Information Schema views evaluate inherited grants (along with `MANAGE GRANTS` and caller grants) when determining
object visibility, and return the same objects as an equivalent `SHOW` command. See
[Information Schema views: Now honor MANAGE GRANTS privilege, caller grants, and inherited grants (Pending)](/release-notes/bcr-bundles/2026_07/bcr-2416).

Before you opt in to the 2026\_07 behavior change bundle, Information Schema views do not consider inherited grants
when determining whether an object is visible to the current role. As a result, an object for which the current role
has access only through an inherited grant does not appear in Information Schema query results, even though the role
can access the object.

To identify inherited grants regardless of bundle status, use the SHOW GRANTS command or the
SNOWFLAKE.ACCOUNT\_USAGE.GRANTS\_TO\_ROLES view.

See [Validate access-review and entitlement tooling](#label-inherited-grants-intro-validate-tooling) for the security
implications of this limitation.

**Next Topics:**

- [Using inherited grants](/user-guide/inherited-grants-using)
