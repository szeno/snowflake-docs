# Using inherited grants

This topic describes how to issue, revoke, migrate, audit, and troubleshoot
[inherited grants](/user-guide/inherited-grants-intro).

## Get started

Use inherited grants for privileges that should apply uniformly to all current and future objects of a type in a
container.

Before creating an inherited grant, determine whether:

- The same privilege should apply to every matching existing object.
- The same privilege should automatically apply to every matching object created in the future.
- No matching object in the scope needs to be excluded from the privilege.
- The chosen container represents the intended access-requirement boundary.

An object-level revoke does not override an inherited grant. If some objects must not receive the privilege, use a
narrower inherited-grant scope or direct grants instead.

You can combine inherited grants with row access policies or masking policies when the role should have access to the
objects but requires different row-level or column-level protection. For example, inherited `SELECT` can provide
access to all tables in a schema while masking policies protect sensitive columns.

However, if a role must not be able to query a particular table at all, don’t use an inherited `SELECT` grant whose
scope includes that table.

## Syntax

Copy code

```
GRANT  INHERITED <privilege> [ , <privilege> ... ]
  ON   ALL <object_type_plural> IN { ACCOUNT | DATABASE <name> | SCHEMA <name> }
  TO   { ROLE <role_name> | DATABASE ROLE <db_role_name> | USER <user_name> | APPLICATION <name> }

REVOKE INHERITED <privilege> ON ALL <object_type_plural>
  IN   { ACCOUNT | DATABASE <name> | SCHEMA <name> }
  FROM { ROLE <role_name> | DATABASE ROLE <db_role_name> | USER <user_name> | APPLICATION <name> }
```

## Required container privileges

Inherited object privileges do not replace required container privileges. For a role to access an object in a schema,
the role typically also needs `USAGE` on the database and schema.

For example, to allow `analyst_role` to query tables in `prod.analytics`:

Copy code

```
GRANT USAGE ON DATABASE prod TO ROLE analyst_role;
GRANT USAGE ON SCHEMA prod.analytics TO ROLE analyst_role;

GRANT INHERITED SELECT ON ALL TABLES
  IN SCHEMA prod.analytics
  TO ROLE analyst_role;
```

The inherited `SELECT` grant controls access to the tables. The `USAGE` grants allow the role to resolve the database
and schema.

## Examples

### Set up a consistent authorization profile

Copy code

```
USE ROLE SECURITYADMIN;
GRANT INHERITED USAGE  ON ALL SCHEMAS IN DATABASE sales_db TO ROLE analyst;
GRANT INHERITED SELECT ON ALL TABLES  IN DATABASE sales_db TO ROLE analyst;
```

**Outcome:** `analyst` can `SELECT` from every existing and future table in `sales_db`, with one grant record per
privilege rather than one per table.

The role that creates an inherited grant must have sufficient grant-management authority. Don’t grant a new role
container-level `MANAGE GRANTS` solely so that it can create a single inherited grant. Use
[container-level `MANAGE GRANTS`](/user-guide/container-manage-grants-using) when that role must independently
administer access over time.

### New objects are covered automatically

Continuing from the example above:

Copy code

```
USE ROLE sales_db_owner; -- any role with CREATE TABLE on the schema
CREATE TABLE sales_db.us_west.new_orders (id INT);

USE ROLE analyst;
SELECT * FROM sales_db.us_west.new_orders;   -- succeeds, no additional grant required
```

### Cover multiple object types

Inherited grants apply to a specific object type. To extend a privilege across multiple types, issue one statement per
type (`TABLES`, `DYNAMIC TABLES`, `ICEBERG TABLES`, `VIEWS`, etc.):

Copy code

```
USE ROLE SECURITYADMIN;
GRANT INHERITED SELECT ON ALL TABLES         IN DATABASE sales_db TO ROLE analyst;
GRANT INHERITED SELECT ON ALL DYNAMIC TABLES IN DATABASE sales_db TO ROLE analyst;
GRANT INHERITED SELECT ON ALL ICEBERG TABLES IN DATABASE sales_db TO ROLE analyst;
GRANT INHERITED SELECT ON ALL VIEWS          IN DATABASE sales_db TO ROLE analyst;
```

**Outcome:** `analyst` can `SELECT` from every existing and future table, dynamic table, Iceberg table, and view in
`sales_db`. Object types not listed (such as materialized views or external tables) are not covered and require their
own `GRANT INHERITED` statement.

Note

For applications that depend on complete visibility into a container, for example, a compliance scanner cataloging
every accessible object, a missing object type is invisible: the grants that do exist work correctly, but nothing
signals the coverage gap. Add a new `GRANT INHERITED` statement whenever the workload starts using an object type
that isn’t already covered.

### Account-scope grant

Copy code

```
USE ROLE SECURITYADMIN;
GRANT INHERITED USAGE ON ALL WAREHOUSES IN ACCOUNT TO ROLE analyst;
```

**Outcome:** `analyst` can use any current or future warehouse in the account.

`ACCOUNT` is the broadest available scope. Before using it for object types that live inside databases, review
[Account scope reaches every database, including personal databases](/user-guide/inherited-grants-intro#label-inherited-grants-intro-account-scope).

### Grant inherited access to an application

Copy code

```
USE ROLE SECURITYADMIN;
GRANT INHERITED USAGE  ON ALL SCHEMAS IN DATABASE sales_db TO APPLICATION trust_center;
GRANT INHERITED SELECT ON ALL TABLES  IN DATABASE sales_db TO APPLICATION trust_center;
```

**Outcome:** The `trust_center` application can read every existing and future table in `sales_db` without requiring
additional grants as new schemas or tables are added.

## Revoke inherited grants

To remove an inherited grant, add the `INHERITED` keyword to `REVOKE`. The container and object type must match those
of the original grant.

Copy code

```
USE ROLE SECURITYADMIN;
REVOKE INHERITED SELECT ON ALL TABLES IN DATABASE sales_db FROM ROLE analyst;
```

**Outcome:** `analyst` loses `SELECT` on every table in `sales_db` it received through this inherited grant, including
tables created after the grant was issued.

Any role holding `MANAGE GRANTS` on the container or a higher container can revoke an inherited grant, regardless of
which role created it.

Before revoking, consider the following:

- **One revoke affects every covered object.** Confirm that no user, application, or workload depends on the access.
- **Other authorization paths survive.** Direct grants, a different inherited grant, or the role hierarchy can still
  provide the privilege, so access might continue to succeed after the revoke.
- **Lower-level inherited grants are independent.** Revoking a database-level inherited grant doesn’t remove inherited
  grants defined on schemas in that database. Revoke those separately.
- **`RESTRICT` and `CASCADE` aren’t supported.** See
  [Restricted clauses](/user-guide/inherited-grants-intro#label-inherited-grants-intro-limitations) in Limitations.

To confirm, verify that the grant is gone and the privilege is no longer reported on a covered object:

Copy code

```
SHOW INHERITED GRANTS IN DATABASE sales_db;
SHOW GRANTS ON TABLE sales_db.us_west.orders;
```

## Representative patterns

The patterns below show end-to-end role hierarchies built on inherited grants. Each pattern is a target end-state;
adapt the role names and container choices to your environment.

### Pattern 1: Centrally managed database access

Use this pattern when a database has a consistent authorization profile and no domain administrator needs to
independently make grant decisions.

Copy code

```
USE ROLE SECURITYADMIN;

CREATE ROLE sales_db_reader;
CREATE ROLE sales_db_writer;

GRANT ROLE sales_db_reader TO ROLE sales_db_writer;

GRANT USAGE ON DATABASE sales_db TO ROLE sales_db_reader;

GRANT INHERITED USAGE ON ALL SCHEMAS
  IN DATABASE sales_db
  TO ROLE sales_db_reader;

GRANT INHERITED SELECT ON ALL TABLES
  IN DATABASE sales_db
  TO ROLE sales_db_reader;

GRANT INHERITED SELECT ON ALL VIEWS
  IN DATABASE sales_db
  TO ROLE sales_db_reader;

GRANT INHERITED INSERT, UPDATE, DELETE ON ALL TABLES
  IN DATABASE sales_db
  TO ROLE sales_db_writer;

GRANT ROLE sales_db_reader TO USER alice;
GRANT ROLE sales_db_writer TO USER bob;
```

**Outcome:** The reader and writer roles receive consistent access across matching current and future objects without
delegating grant-management authority to another role. Use this as the default inherited-grant pattern when the
authorization profile is centrally managed.

### Pattern 2: Per-domain pattern (schemas as domains)

Use this pattern when a single database holds multiple domains (each represented by a schema) that need independent
grant administration.

This pattern intentionally uses container-level `MANAGE GRANTS` because each domain lead is trusted to make
independent authorization decisions for its schema. Don’t use this pattern merely because inherited grants are being
created. If a central administrator defines the entire authorization profile, Pattern 1 (Centrally managed database
access) avoids unnecessary delegation of grant-management authority.

Copy code

```
USE ROLE SECURITYADMIN;

-- One database admin who can delegate further
CREATE ROLE sales_db_admin;
GRANT MANAGE GRANTS ON DATABASE sales_db TO ROLE sales_db_admin WITH GRANT OPTION;

-- Per-domain roles
CREATE ROLE us_west_reader;
CREATE ROLE us_west_lead;
CREATE ROLE eu_reader;
CREATE ROLE eu_lead;

USE ROLE sales_db_admin;

-- Each domain lead is the role that holds MANAGE GRANTS for its schema
GRANT MANAGE GRANTS ON SCHEMA sales_db.us_west TO ROLE us_west_lead;
GRANT MANAGE GRANTS ON SCHEMA sales_db.eu      TO ROLE eu_lead;

-- Database-level USAGE is outside each lead's schema-scoped authority, so pass it down with GRANT OPTION
GRANT USAGE ON DATABASE sales_db TO ROLE us_west_lead WITH GRANT OPTION;
GRANT USAGE ON DATABASE sales_db TO ROLE eu_lead      WITH GRANT OPTION;

-- Each domain lead defines its own grants, including the database USAGE its readers need
USE ROLE us_west_lead;
GRANT USAGE ON DATABASE sales_db TO ROLE us_west_reader;
GRANT USAGE ON SCHEMA sales_db.us_west TO ROLE us_west_reader;
GRANT INHERITED SELECT ON ALL TABLES IN SCHEMA sales_db.us_west TO ROLE us_west_reader;

USE ROLE eu_lead;
GRANT USAGE ON DATABASE sales_db TO ROLE eu_reader;
GRANT USAGE ON SCHEMA sales_db.eu TO ROLE eu_reader;
GRANT INHERITED SELECT ON ALL TABLES IN SCHEMA sales_db.eu TO ROLE eu_reader;
```

**Outcome:** Each domain (US West, EU) has its own lead role holding `MANAGE GRANTS` on its schema, plus its own reader
role. Domain leads operate independently without involving the database admin or `SECURITYADMIN` for routine grant
management, including when they add reader roles later.

Reading a table requires `USAGE` on the database as well as the schema. See
[Required container privileges](#label-inherited-grants-using-container-privileges). Because each lead’s
`MANAGE GRANTS` is scoped to its own schema, it can’t grant database-level `USAGE` on its own authority. Granting each
lead `USAGE ON DATABASE sales_db WITH GRANT OPTION` lets it extend that privilege to its own reader roles, so a new
reader doesn’t require the database admin.

Each schema acts as both an access-requirement boundary for inherited grants and an administrative trust boundary for
`MANAGE GRANTS`. The database admin uses database-level `MANAGE GRANTS WITH GRANT OPTION` only because it must create
the lower-level schema grant administrators, not to manage schema-level grants directly.

### Pattern 3: Application access pattern

Use this pattern when a Snowflake-managed application (for example, a governance scanner or data-quality service)
needs to read every current and future object in a container.

Copy code

```
USE ROLE SECURITYADMIN;
GRANT INHERITED USAGE  ON ALL SCHEMAS IN DATABASE sales_db TO APPLICATION trust_center;
GRANT INHERITED SELECT ON ALL TABLES  IN DATABASE sales_db TO APPLICATION trust_center;
GRANT INHERITED SELECT ON ALL VIEWS   IN DATABASE sales_db TO APPLICATION trust_center;
```

**Outcome:** The application can scan every current and future schema, table, and view in `sales_db` without
future-grant proliferation. New objects are covered automatically.

Grant only the privileges and object types the application requires. An inherited grant on one object type doesn’t
provide visibility into other object types. If an application is expected to provide complete inventory, security,
governance, or data-quality coverage, verify that all required supported object types are included.

Also consider future objects: granting inherited access to an application means that matching objects created later
automatically become accessible to that application. For sensitive databases, review whether the application should
automatically receive access to every future matching object before using a database-wide inherited grant.

## Migrate from future grants and `GRANT <privileges> ON ALL`

If you use matching bulk and future grants to maintain a consistent authorization profile, you can often replace them
with a single inherited grant. Migrate only when the inherited grant represents the same intended authorization
profile.

Because inherited grants apply to both existing and future matching objects, a migration can broaden access if the
previous configuration didn’t already provide access to all existing objects. Use the following sequence to avoid
access gaps and unintended access expansion.

### Step 1: Inventory the current authorization state

Identify the existing grants you intend to replace.

For each candidate pattern, record:

- Privilege.
- Grantee.
- Object type.
- Container.
- Access to existing objects.
- Future-grant behavior.
- Known object-level exceptions.

For example:

Copy code

```
-- Future grants on a database
SHOW FUTURE GRANTS IN DATABASE sales_db;

-- Future grants on a schema
SHOW FUTURE GRANTS IN SCHEMA sales_db.us_west;

-- Existing grants held by the role you are migrating
SHOW GRANTS TO ROLE analyst;
```

Look for repeated patterns such as a bulk `SELECT` grant on all existing tables plus a matching future `SELECT` grant
for the same role and container. Also identify any direct object grants or narrower-scope grants that might cause
effective access to differ from the apparent bulk/future pattern.

### Step 2: Identify patterns that can be represented by an inherited grant

A grant pattern is a good candidate for an inherited grant when:

- The privilege is the same for existing and future matching objects.
- The grantee is the same.
- The object type is the same.
- The container is the same.
- The grantee should receive the privilege on every matching current object.
- The grantee should automatically receive the privilege on every matching future object.
- No matching object in the scope needs to be excluded from the privilege.

If some objects must not receive the privilege, don’t use an inherited grant whose scope includes those objects. Use
direct grants or a narrower inherited-grant scope instead. See
[Get started](#label-inherited-grants-using-get-started) for how row access and masking policies fit alongside an
inherited grant.

Important

Creating an inherited grant can immediately expand access. An inherited grant applies to both existing and future
matching objects. Before issuing the inherited grant, verify that the grantee should receive the privilege on
existing objects as well as future objects.

For example, a future-only grant:

Copy code

```
GRANT SELECT ON FUTURE TABLES
  IN DATABASE sales_db
  TO ROLE analyst;
```

doesn’t by itself grant `SELECT` on tables that already exist. Replacing it with:

Copy code

```
GRANT INHERITED SELECT ON ALL TABLES
  IN DATABASE sales_db
  TO ROLE analyst;
```

provides the privilege on matching existing tables as well as future tables. Don’t perform this migration unless
that expansion is intended.

### Step 3: Create the inherited grant

After confirming that the inherited grant represents the intended authorization profile, create it before removing
the old grants.

Copy code

```
USE ROLE sales_admin; -- role with MANAGE GRANTS on sales_db
GRANT INHERITED SELECT ON ALL TABLES IN DATABASE sales_db TO ROLE analyst;
```

Creating the inherited grant before removing the previous grants avoids an access gap during the migration. At this
stage, the old and new authorization paths can coexist temporarily.

### Step 4: Verify the inherited grant

Before revoking the previous grants, verify that the inherited grant itself represents the intended authorization
profile. Because the previous grants still exist during this step, successfully accessing an object does not by
itself prove that the inherited grant is providing the access.

First, verify that the expected inherited grant exists:

Copy code

```
SHOW INHERITED GRANTS IN DATABASE sales_db;
```

Then inspect an existing object, and, when practical, a newly created object:

Copy code

```
SHOW GRANTS ON TABLE sales_db.us_west.orders;
SHOW GRANTS ON TABLE sales_db.us_west.recently_added;
```

Confirm `IS_INHERITED` is `TRUE` for the expected privilege, and that `INHERITED_FROM` (with `INHERITED_FROM_DATABASE`
or `INHERITED_FROM_SCHEMA`, if applicable) identifies the intended source container.

Don’t rely solely on a successful `SELECT`, `EXECUTE`, or other object operation while the previous grants remain in
place. Multiple authorization paths might allow the operation to succeed.

### Step 5: Revoke the original future and bulk grants

Once parity is confirmed, revoke the original grants to complete the migration.

Copy code

```
USE ROLE sales_admin; -- role with sufficient authority to revoke the previous grants
REVOKE SELECT ON ALL TABLES    IN DATABASE sales_db FROM ROLE analyst;
REVOKE SELECT ON FUTURE TABLES IN DATABASE sales_db FROM ROLE analyst;
```

Important

Run Step 5 only after verifying parity in Step 4. If the inherited grant is missing or incorrect, revoking the original
grants will cause an access gap.

After removing the previous grants, repeat the verification from Step 4. At this point, verify both:

- The previous grant sources no longer exist.
- The intended access still succeeds through the inherited grant.

This final verification confirms that the migrated authorization profile doesn’t depend on one of the grants that was
removed.

After migration, if the delegated administrator’s remaining work is fully represented by inherited grants, see
[Reduce delegated grant-management authority](/user-guide/container-manage-grants-using#label-container-manage-grants-using-examples)
to evaluate revoking `MANAGE GRANTS`.

The following table summarizes when to consider migrating to inherited grants:

| Pattern | Recommended migration |
| --- | --- |
| Matching `ON ALL` + `ON FUTURE` privilege for the same role, type, and container | Migrate to an inherited grant if every existing and future matching object should receive the privilege. |
| Future grant only | Migrate only if providing the same privilege to existing objects is also intended. |
| Object-level grants with exceptions | Keep direct grants, or reorganize the container boundary. |
| Same object privilege, but different row/column visibility is required | Consider an inherited grant plus row access or masking policies. |
| Different object privileges within the same container | Keep direct grants. |
| Small, stable set of objects | Keep direct grants unless inherited grants provide a clear administrative benefit. |
| Repeated uniform grants maintained by a delegated administrator | Migrate to inherited grants and evaluate whether the administrator still requires `MANAGE GRANTS`. |

Expand

Show lessSee more

## Audit inherited grants

Snowflake supports the following approaches to facilitate inherited-grant auditing.

- Use `SHOW INHERITED GRANTS IN <container>` to enumerate every inherited grant defined in a database or schema. This
  is the most direct way to see what container-level grants are in effect.
- Use the `GRANTS_TO_ROLES` view in `ACCOUNT_USAGE` with `IS_INHERITED = TRUE` to find all inherited grants
  account-wide, and to reconstruct the history of inherited-grant creation and revocation (including revoked grants,
  which appear with a non-null `DELETED_ON` value).
- For per-object access reviews, use `SHOW GRANTS ON <object>`. The response includes both direct and inherited grants
  applicable to the object, with the source container identified in the `INHERITED_FROM` column.

Three `SHOW` commands return inherited grant information, each populating four new columns.

| Command | Description |
| --- | --- |
| `SHOW GRANTS ON <object>` | Regular and inherited grants on the target object, including grants inherited from upstream containers. `MANAGE GRANTS` from upstream are excluded from the rollup. |
| `SHOW GRANTS TO ROLE <role>` | Regular and inherited grants directly granted to the role. Individual securables are not enumerated for performance; the `NAME` column is empty for inherited grant rows. |
| `SHOW INHERITED GRANTS IN <container>` | Inherited grants defined in the specified container. |

Expand

Show lessSee more

| Column | Description |
| --- | --- |
| `IS_INHERITED` | `TRUE` if the row is an inherited grant; `FALSE` otherwise. |
| `INHERITED_FROM` | Container type the grant is inherited from: `ACCOUNT`, `DATABASE`, or `SCHEMA`. Empty for regular grants. |
| `INHERITED_FROM_DATABASE` | Database name when `INHERITED_FROM` is `DATABASE` or `SCHEMA`. |
| `INHERITED_FROM_SCHEMA` | Schema name when `INHERITED_FROM` is `SCHEMA`. |

Expand

Show lessSee more

The same four columns appear in the `GRANTS_TO_ROLES` view in `ACCOUNT_USAGE` and the `INFORMATION_SCHEMA`.

## Troubleshoot inherited grants

| Behavior | Likely cause | Action |
| --- | --- | --- |
| `SELECT` query fails with “Object does not exist or not authorized” even though `GRANT INHERITED SELECT ON ALL TABLES ...` was issued | Missing `USAGE` on the parent schema or database; name resolution fails before the `SELECT` privilege is checked | Issue `GRANT INHERITED USAGE ON ALL SCHEMAS IN DATABASE <name>` and ensure the role has `USAGE` on the database itself. |
| `GRANT INHERITED ...` fails with “Insufficient privileges” | Executing role lacks `MANAGE GRANTS` on the container or a regrantable privilege | Grant `MANAGE GRANTS` on the container (or higher) to the executing role, or use a role that already holds it. |
| `SHOW GRANTS TO ROLE <role>` returns inherited rows with an empty `NAME` column | Expected behavior: inherited grants apply to a class of securables, not a specific object | Use `SHOW INHERITED GRANTS IN <container>` to see container-level grants, or `SHOW GRANTS ON <object>` to see the inherited grant in the context of a specific object. |
| New table created in a covered container is not accessible to the grantee | The new table is of an object type not covered by the inherited grant (for example, an `ICEBERG TABLE` when only `TABLES` was granted) | Issue an additional `GRANT INHERITED` statement for the new object type. |
| `GRANT INHERITED USAGE ON ALL STREAMLITS ...` fails | `USAGE` on `STREAMLIT` is not eligible for inheritance | Grant direct `USAGE` grants on individual Streamlit apps instead. |
| Inherited grant on a shared database fails | Inherited grants are not supported on imported (consumer-side) databases or shared schemas in this release | Use direct grants for shared-database flows. |

Expand

Show lessSee more
