# Metadata access control

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Metadata access in Horizon Catalog is separate from data access. A role can view or curate metadata
and lineage without being able to query the underlying data, so we recommend managing metadata
access with roles that are separate from your
[data access roles](/user-guide/security-access-control-overview).

This page covers three needs:

- [Create a connector](#create-a-connector): for the role that sets up a metadata connector.
- [View metadata and lineage](#view-metadata-and-lineage): for end users and analysts who explore
  the catalog and lineage (read-only).
- [Edit metadata](#edit-metadata): for data stewards who curate the descriptions and comments that
  appear in the catalog.

## Create a connector

The role you select in Snowsight creates the connector and owns it. Snowsight behaves as if
secondary roles are enabled, so privileges from any role you hold apply to most actions. Creating
an object is the exception: the new object is owned by the primary role you select, so that role
alone must have the privileges to create it. Privileges granted to your other roles don’t count,
even when those roles together hold every privilege needed to create the object.

The role must have all of the following:

- **MANAGE METADATA CONNECTORS** on the account
- **USAGE** or **OWNERSHIP** on the database for the connector
- **CREATE METADATA CONNECTOR** or **OWNERSHIP** on the schema for the connector

If the selected role creates a new database and schema when it sets up the connector, it owns them
and needs only `MANAGE METADATA CONNECTORS`, plus permission to create the database. Otherwise,
grant the privileges for the default `CONNECTORS.METADATA` location:

Copy code

```
GRANT MANAGE METADATA CONNECTORS ON ACCOUNT TO ROLE <role_name>;
GRANT USAGE ON DATABASE CONNECTORS TO ROLE <role_name>;
GRANT CREATE METADATA CONNECTOR ON SCHEMA CONNECTORS.METADATA TO ROLE <role_name>;
```

## View metadata and lineage

Give end users read-only visibility into Snowflake metadata, connector metadata, and lineage.
Viewing metadata doesn’t require access to the underlying data, so you can grant it to roles that
have no query privileges.

Viewing lineage requires the `VIEW LINEAGE` privilege on the account, plus access to the objects in
the lineage graph. `VIEW LINEAGE` is granted to the `PUBLIC` role by default, so most roles already
have it. If your account has restricted this default grant, re-grant it before following the steps
below. See
[Access control for lineage information](/user-guide/ui-snowsight-lineage#access-control-for-lineage-information).

### Snowflake object metadata

To control visibility of Snowflake objects (databases, schemas, tables, views, and similar) in
Horizon Catalog, grant `USAGE` and `REFERENCES` privileges using a combination of `ALL` and
`FUTURE` grants:

- `ALL` grants apply the grant to every matching object that exists when you run the statement.
- `FUTURE` grants create a standing rule that applies the grant to objects created later.

Using `ALL` and `FUTURE` grants together gives a role visibility into both the objects that exist
today and anything created in the future, which is the same effect as an inherited grant. For more
information, see [GRANT <privileges>](/sql-reference/sql/grant-privilege).

Copy code

```
-- Visibility of databases can be granted via USAGE.
GRANT USAGE ON DATABASE db TO ROLE r1;

-- Visibility of schemas can be granted via USAGE. Grant to all existing
-- schemas, and add a FUTURE grant for schemas created later.
GRANT USAGE ON ALL SCHEMAS IN DATABASE db TO ROLE r1;
GRANT USAGE ON FUTURE SCHEMAS IN DATABASE db TO ROLE r1;

-- Visibility of table-like objects beneath a schema can be granted via the
-- REFERENCES privilege. Use the same ALL and FUTURE combination so the role
-- has visibility into everything.
GRANT REFERENCES ON ALL TABLES IN DATABASE db TO ROLE r1;
GRANT REFERENCES ON FUTURE TABLES IN DATABASE db TO ROLE r1;

-- Enumerate each object type you want the role to see (views, and so on).
GRANT REFERENCES ON ALL VIEWS IN DATABASE db TO ROLE r1;
GRANT REFERENCES ON FUTURE VIEWS IN DATABASE db TO ROLE r1;
```

### Connector metadata and lineage

A connector is created by the role that sets it up in **Catalog > Connections**, and that
role owns it. Other roles can’t see the connector’s metadata and lineage until you grant them
access. To see a connector’s external objects in lineage graphs and catalog metadata, the active
role must have all of the following:

- **USAGE** on the database that contains the connector
- **USAGE** on the schema that contains the connector
- **USAGE** on the connector itself, or **OWNERSHIP** of it

Note

Granting `USAGE` on a connector controls the **visibility** of the metadata and lineage that
the connector collects. It doesn’t expose the connector’s stored credentials, and it doesn’t
grant any access to the external system itself.

All metadata connectors are created under the `CONNECTORS.METADATA` schema by default. Grant `USAGE` to
each role that needs to view the connector’s metadata and lineage:

Copy code

```
GRANT USAGE ON DATABASE CONNECTORS TO ROLE <role_name>;
GRANT USAGE ON SCHEMA CONNECTORS.METADATA TO ROLE <role_name>;
GRANT USAGE ON METADATA CONNECTOR CONNECTORS.METADATA.<connector_name> TO ROLE <role_name>;
```

Quote `<connector_name>` when the display name contains a space, a hyphen, or another character
that isn’t valid in an unquoted identifier. Snowsight uses the display name as the identifier. For
a connector named `dbt - zv880`:

Copy code

```
GRANT USAGE ON METADATA CONNECTOR CONNECTORS.METADATA."dbt - zv880" TO ROLE <role_name>;
```

If you stored your connector in a different database or schema, replace `CONNECTORS` and `METADATA`
with the actual database and schema names. To find the connector’s location, run:

Copy code

```
SHOW METADATA CONNECTORS;
```

Note

If you drop and recreate a connector, the new connector does not inherit grants from the old
one. Re-grant `USAGE` to the roles that need it after recreating a connector.

Configuring, syncing, and deleting a connector in **Catalog > Connections** requires `OWNERSHIP`
of that connector. `USAGE`, `CREATE METADATA CONNECTOR`, and `MANAGE METADATA CONNECTORS` do not
authorize those actions. The role selected in Snowsight must own the connector, including when
that role is a secondary role. To give another role those actions, transfer ownership.
`COPY CURRENT GRANTS` keeps the grants already on the connector, and the new role becomes the owner:

Copy code

```
GRANT OWNERSHIP ON METADATA CONNECTOR CONNECTORS.METADATA.<connector_name> TO ROLE <role_name>
  COPY CURRENT GRANTS;
```

Quote `<connector_name>` when the display name contains a space or a hyphen. Remove a connector
from **Catalog > Connections**. There is no `DROP METADATA CONNECTOR` statement.

## Edit metadata

Give data stewards the ability to curate the tags that appear in the catalog without granting more
permissive privileges such as `MODIFY` or `OWNERSHIP`. The `APPLY TAG` privilege lets a role set and
unset tags on objects and columns. You can grant it on the account or on an individual tag. For the
full tag privileges and grant syntax, see
[Tag privileges](/user-guide/object-tagging/work#label-object-tags-privileges).
