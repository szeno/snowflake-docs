# Metadata access control

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Metadata access in Horizon Catalog is separate from data access. A role can view or curate metadata
and lineage without being able to query the underlying data, so we recommend managing metadata
access with roles that are separate from your
[data access roles](/user-guide/security-access-control-overview).

## Privileges at a glance

Metadata connectors are schema-level objects. The external objects that a connector ingests, such as
a Power BI dashboard or a Tableau workbook, don’t have grants of their own. Access to them is
inherited from grants on the connector. Every task below therefore also requires `USAGE` (or
`OWNERSHIP`) on the database and schema that contain the connector.

| Task | Privileges required, in addition to `USAGE` on the connector’s database and schema |
| --- | --- |
| [Create a connector](#create-a-connector) | `MANAGE METADATA CONNECTORS` on the account, `CREATE METADATA CONNECTOR` (or `OWNERSHIP`) on the schema, and `USAGE` on a warehouse |
| [Configure, sync, or delete a connector](#manage-a-connector) | `OWNERSHIP` on the connector |
| [View connector metadata and lineage](#view-metadata-and-lineage) | `READ EXTERNAL METADATA` or `USAGE` on the connector |
| [Edit connector metadata](#edit-metadata) | `MODIFY EXTERNAL METADATA` on the connector, plus `READ EXTERNAL METADATA` or `USAGE` on the connector to view it |
| [View Snowflake object metadata](#snowflake-object-metadata) | `USAGE` on databases and schemas, and `REFERENCES` on tables, views, and other table-like objects |
| [Edit Snowflake object metadata](#snowflake-objects) | `APPLY COMMENT` to edit comments and descriptions, `APPLY TAG` to set and unset tags, or `MODIFY` or `OWNERSHIP` on the object |
| [Delegate any of these privileges](#delegate-access) | The privilege granted `WITH GRANT OPTION` |

Expand

Show lessSee more

The examples on this page use the default `CONNECTORS.METADATA` schema, where Snowsight creates
connectors unless you choose another location. If you stored a connector elsewhere, replace
`CONNECTORS` and `METADATA` with its database and schema. To find a connector’s location, run:

Copy code

```
SHOW METADATA CONNECTORS;
```

## Create a connector

The role you select in Snowsight creates the connector and owns it. Snowsight behaves as if
secondary roles are enabled, so privileges from any role you hold apply to most actions. Creating
an object is the exception: the new object is owned by the primary role you select, so that role
alone must have the privileges to create it. Privileges granted to your other roles don’t count,
even when those roles together hold every privilege needed to create the object.

The role must have all of the following:

- **MANAGE METADATA CONNECTORS** on the account. This is the account-level switch for connector
  creation. Without it, a role can’t create connectors anywhere in the account, even in a schema
  it owns.
- **USAGE** or **OWNERSHIP** on the database for the connector.
- **CREATE METADATA CONNECTOR** or **OWNERSHIP** on the schema for the connector.
- **USAGE** on a warehouse. Snowsight runs queries during setup, so the session needs an active
  warehouse. If the role can’t use one, setup fails.

Copy code

```
GRANT MANAGE METADATA CONNECTORS ON ACCOUNT TO ROLE <role_name>;
GRANT USAGE ON DATABASE CONNECTORS TO ROLE <role_name>;
GRANT CREATE METADATA CONNECTOR ON SCHEMA CONNECTORS.METADATA TO ROLE <role_name>;
GRANT USAGE ON WAREHOUSE <warehouse_name> TO ROLE <role_name>;
```

If the selected role creates a new database and schema when it sets up the connector, it owns them,
so it needs only `MANAGE METADATA CONNECTORS`, warehouse `USAGE`, and permission to create the
database.

Note

`MANAGE METADATA CONNECTORS` was previously named `MANAGE METADATA INGESTION`. Both names refer to
the same privilege, and you need only one of them. `SHOW GRANTS` output displays the current name.

### Configure, sync, or delete a connector

Configuring, syncing, and deleting a connector in **Catalog > Connections** requires `OWNERSHIP`
of that connector. `USAGE`, `READ EXTERNAL METADATA`, `MODIFY EXTERNAL METADATA`,
`CREATE METADATA CONNECTOR`, and `MANAGE METADATA CONNECTORS` don’t authorize those actions. The
role selected in Snowsight must own the connector, including when that role is a secondary role.

To give another role those actions, transfer ownership. `COPY CURRENT GRANTS` keeps the grants
already on the connector, and the new role becomes the owner:

Copy code

```
GRANT OWNERSHIP ON METADATA CONNECTOR CONNECTORS.METADATA.<connector_name> TO ROLE <role_name>
  COPY CURRENT GRANTS;
```

Remove a connector from **Catalog > Connections**. There is no `DROP METADATA CONNECTOR`
statement.

## View metadata and lineage

Give end users read-only visibility into connector metadata, Snowflake metadata, and lineage.
Viewing metadata doesn’t require access to the underlying data, so you can grant it to roles that
have no query privileges.

Viewing lineage requires the `VIEW LINEAGE` privilege on the account, plus access to the objects in
the lineage graph. `VIEW LINEAGE` is granted to the `PUBLIC` role by default, so most roles already
have it. If your account has restricted this default grant, re-grant it before following the steps
below. See
[Access control for lineage information](/user-guide/ui-snowsight-lineage#access-control-for-lineage-information).

### Connector metadata and lineage

A connector is owned by the role that created it. Other roles can’t see the connector’s metadata and
lineage until you grant them access. To see a connector’s external objects in lineage graphs and
catalog metadata, the active role must have all of the following:

- **USAGE** on the database that contains the connector
- **USAGE** on the schema that contains the connector
- **READ EXTERNAL METADATA** or **USAGE** on the connector itself, or **OWNERSHIP** of it

`READ EXTERNAL METADATA` and `USAGE` provide the same visibility into a connector’s metadata. Use
`READ EXTERNAL METADATA` when the role only needs to view metadata, because it states that intent
explicitly.

Note

These privileges control the **visibility** of the metadata and lineage that the connector
collects. They don’t expose the connector’s stored credentials, and they don’t grant any access to
the external system itself.

To grant visibility into a single connector:

Copy code

```
GRANT USAGE ON DATABASE CONNECTORS TO ROLE <role_name>;
GRANT USAGE ON SCHEMA CONNECTORS.METADATA TO ROLE <role_name>;
GRANT READ EXTERNAL METADATA ON METADATA CONNECTOR CONNECTORS.METADATA.<connector_name>
  TO ROLE <role_name>;
```

To grant visibility into every connector in the schema, including connectors created later,
combine `ALL` and `FUTURE` grants:

Copy code

```
GRANT READ EXTERNAL METADATA ON ALL METADATA CONNECTORS IN SCHEMA CONNECTORS.METADATA
  TO ROLE <role_name>;
GRANT READ EXTERNAL METADATA ON FUTURE METADATA CONNECTORS IN SCHEMA CONNECTORS.METADATA
  TO ROLE <role_name>;
```

Quote `<connector_name>` when the display name contains a space, a hyphen, or another character
that isn’t valid in an unquoted identifier. Snowsight uses the display name as the identifier. For
a connector named `dbt - zv880`:

Copy code

```
GRANT READ EXTERNAL METADATA ON METADATA CONNECTOR CONNECTORS.METADATA."dbt - zv880"
  TO ROLE <role_name>;
```

Note

If you drop and recreate a connector, the new connector doesn’t inherit grants from the old one.
Re-grant privileges to the roles that need them after recreating a connector, or use a `FUTURE`
grant on the schema so that new connectors receive them automatically.

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

## Edit metadata

Give data stewards the ability to curate the metadata that appears in the catalog without granting
more permissive privileges such as `MODIFY` or `OWNERSHIP`. The privilege depends on where the
metadata comes from.

### Connector metadata

`MODIFY EXTERNAL METADATA` lets a role edit the metadata, such as descriptions, of the external
objects that a connector ingests. Edit them from the catalog in Snowsight. Editing ingested metadata
is a stronger privilege than viewing it, so grant it separately and only to the roles that curate
the catalog.

`MODIFY EXTERNAL METADATA` doesn’t, by itself, grant view access. A role can’t edit metadata that
it can’t see, so it also needs `READ EXTERNAL METADATA` or `USAGE` on the connector, plus `USAGE` on
the connector’s database and schema. For details, see
[Connector metadata and lineage](#connector-metadata-and-lineage).

Grant both privileges on a single connector, or on every connector in the schema:

Copy code

```
-- A single connector
GRANT READ EXTERNAL METADATA ON METADATA CONNECTOR CONNECTORS.METADATA.<connector_name>
  TO ROLE <role_name>;
GRANT MODIFY EXTERNAL METADATA ON METADATA CONNECTOR CONNECTORS.METADATA.<connector_name>
  TO ROLE <role_name>;

-- Every existing and future connector in the schema
GRANT READ EXTERNAL METADATA ON ALL METADATA CONNECTORS IN SCHEMA CONNECTORS.METADATA
  TO ROLE <role_name>;
GRANT READ EXTERNAL METADATA ON FUTURE METADATA CONNECTORS IN SCHEMA CONNECTORS.METADATA
  TO ROLE <role_name>;
GRANT MODIFY EXTERNAL METADATA ON ALL METADATA CONNECTORS IN SCHEMA CONNECTORS.METADATA
  TO ROLE <role_name>;
GRANT MODIFY EXTERNAL METADATA ON FUTURE METADATA CONNECTORS IN SCHEMA CONNECTORS.METADATA
  TO ROLE <role_name>;
```

### Snowflake objects

To curate the descriptions, comments, and tags on Snowflake objects and columns, grant one or both
of the following:

- `APPLY COMMENT`: set and unset comments and descriptions on objects and columns. See
  [APPLY COMMENT](#apply-comment).
- `APPLY TAG`: set and unset tags on objects and columns. You can grant it on the account or on an
  individual tag. For the full tag privileges and grant syntax, see
  [Tag privileges](/user-guide/object-tagging/work#label-object-tags-privileges).

#### APPLY COMMENT

`APPLY COMMENT` lets a role set or unset the comment on an object, including column-level comments
for table-like objects.

Note

Privileges such as `MODIFY` and `OWNERSHIP` continue to authorize comment changes exactly as before. `APPLY COMMENT`
widens who can edit comments. It doesn’t restrict the existing paths.

##### Grant syntax

`APPLY COMMENT` uses the standard [GRANT <privileges>](/sql-reference/sql/grant-privilege)
syntax. You can grant it at three scopes:

Copy code

```
-- Per object
GRANT APPLY COMMENT ON <object_type> <object_name> TO ROLE <role_name>;

-- All existing objects of a type in a schema or database
GRANT APPLY COMMENT ON ALL <object_type_plural> IN { SCHEMA <schema_name> | DATABASE <database_name> }
    TO ROLE <role_name>;

-- Objects of a type created in the future in a schema or database
GRANT APPLY COMMENT ON FUTURE <object_type_plural> IN { SCHEMA <schema_name> | DATABASE <database_name> }
    TO ROLE <role_name>;
```

A role granted `APPLY COMMENT` still needs `USAGE` on the parent database and schema to resolve
the target object. The privilege authorizes the comment change. It doesn’t grant the visibility
needed to navigate to the object.

Copy code

```
-- Examples granting a steward the ability to edit comments on a single table, on every table
-- in a schema, and on every view created in a database going forward:
GRANT APPLY COMMENT ON TABLE finance.gl.journal TO ROLE finance_steward;
GRANT APPLY COMMENT ON ALL TABLES IN SCHEMA finance.gl TO ROLE finance_steward;
GRANT APPLY COMMENT ON FUTURE VIEWS IN DATABASE finance TO ROLE finance_steward;
```

To revoke the privilege, use [REVOKE <privileges>](/sql-reference/sql/revoke-privilege):

Copy code

```
REVOKE APPLY COMMENT ON TABLE finance.gl.journal FROM ROLE finance_steward;
```

##### Supported object types

You can grant `APPLY COMMENT` on the following object types:

- Database
- Schema
- Table
- Dynamic table
- Apache Iceberg™ table
- External table
- Event table
- Interactive table
- View
- Materialized view
- Semantic view
- Function
- Procedure
- Pipe
- Task
- Agent

External objects that a metadata connector ingests aren’t on this list. To edit their
metadata, use [MODIFY EXTERNAL METADATA](#connector-metadata) instead.

##### Statements authorized

With `APPLY COMMENT` on an object, a role can set and unset the object comment and, for table-like
objects, individual column comments. Both the `ALTER … SET COMMENT` and `COMMENT ON` forms are
authorized:

Copy code

```
-- Object comments
ALTER TABLE finance.gl.journal SET COMMENT = 'General ledger journal entries';
ALTER TABLE finance.gl.journal UNSET COMMENT;
COMMENT ON TABLE finance.gl.journal IS 'General ledger journal entries';

-- Column comments
ALTER TABLE finance.gl.journal ALTER COLUMN amount COMMENT 'Signed amount in USD';
ALTER TABLE finance.gl.journal MODIFY COLUMN amount COMMENT 'Signed amount in USD';
ALTER TABLE finance.gl.journal ALTER COLUMN amount UNSET COMMENT;
COMMENT ON COLUMN finance.gl.journal.amount IS 'Signed amount in USD';

-- A statement that changes only comments is authorized, even across multiple columns
ALTER TABLE finance.gl.journal ALTER COLUMN amount COMMENT 'USD', COLUMN currency COMMENT 'ISO code';
```

##### Statements not authorized

`APPLY COMMENT` is comment-only. It doesn’t authorize any other change, and a single statement
that mixes a comment change with any non-comment change is rejected. The role needs `MODIFY` or
`OWNERSHIP` for these statements.

## Delegate access

To let a role grant a privilege to other roles, grant it `WITH GRANT OPTION`. For example, an
account administrator can make a role responsible for metadata access across all connectors in the
default schema, without making it an account administrator:

Copy code

```
-- As ACCOUNTADMIN: let r1 create connectors and pass that ability on.
GRANT MANAGE METADATA CONNECTORS ON ACCOUNT TO ROLE r1 WITH GRANT OPTION;
GRANT CREATE METADATA CONNECTOR ON SCHEMA CONNECTORS.METADATA TO ROLE r1 WITH GRANT OPTION;

-- Let r1 grant view and edit access on every connector in the schema.
GRANT READ EXTERNAL METADATA ON ALL METADATA CONNECTORS IN SCHEMA CONNECTORS.METADATA
  TO ROLE r1 WITH GRANT OPTION;
GRANT READ EXTERNAL METADATA ON FUTURE METADATA CONNECTORS IN SCHEMA CONNECTORS.METADATA
  TO ROLE r1 WITH GRANT OPTION;
GRANT MODIFY EXTERNAL METADATA ON ALL METADATA CONNECTORS IN SCHEMA CONNECTORS.METADATA
  TO ROLE r1 WITH GRANT OPTION;
GRANT MODIFY EXTERNAL METADATA ON FUTURE METADATA CONNECTORS IN SCHEMA CONNECTORS.METADATA
  TO ROLE r1 WITH GRANT OPTION;

-- As r1: give an analyst role read access, and a steward role read and edit access.
GRANT READ EXTERNAL METADATA ON ALL METADATA CONNECTORS IN SCHEMA CONNECTORS.METADATA
  TO ROLE analyst;
GRANT READ EXTERNAL METADATA ON ALL METADATA CONNECTORS IN SCHEMA CONNECTORS.METADATA
  TO ROLE steward;
GRANT MODIFY EXTERNAL METADATA ON ALL METADATA CONNECTORS IN SCHEMA CONNECTORS.METADATA
  TO ROLE steward;
```

The roles that receive these grants still need `USAGE` on the `CONNECTORS` database and the
`CONNECTORS.METADATA` schema.

Revoking `MANAGE METADATA CONNECTORS` immediately stops a role from creating new connectors, even if
it still holds `CREATE METADATA CONNECTOR` on a schema or owns a schema.
