# About the Snowflake Connector for PostgreSQL

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts except government regions.

Important

Thank you for your interest in the Snowflake Connector for PostgreSQL.
Note that we’re now focused on a next-generation solution that will offer a significantly improved experience.
Hence, moving this connector to the general availability status is currently not on our product roadmap.
You may continue to use this connector as a preview feature, but please note that support for future bug
fixes and improvements are not guaranteed. The new solution is available as [Openflow Connector for PostgreSQL](/user-guide/data-integration/openflow/connectors/postgres/about) and
includes better performance, customizability, and enhanced deployment options.

The Snowflake Connector for PostgreSQL allows you to:

- Load data into Snowflake from a PostgreSQL database.
- Configure replication so that changes in your PostgreSQL database are replicated to Snowflake.

To handle connections between Snowflake and PostgreSQL, the connector uses an agent. The agent is
distributed as a Docker image. The agent is run within your network and is used to push data into your Snowflake
account.

Note

The Snowflake Connector for PostgreSQL requires exactly one instance of the agent application to be running at
all times.

The ongoing incremental updates use the Change Data Capture (CDC) technique that captures changes performed on the source database.
The changes include INSERT, UPDATE, and DELETE operations, which are automatically replicated on the
destination database in Snowflake.

## Multiple application instances

You can install multiple instances of the Snowflake Connector for PostgreSQL on your Snowflake account.
For more information, see [Optional: Installing multiple instances of Snowflake Connector for PostgreSQL](/connectors/postgres6/install-snowsight#label-postgres-connector-configure-multi-instance).

## Private links

The Snowflake Connector for PostgreSQL supports private links. For more information, see:

- [AWS PrivateLink and Snowflake](/user-guide/admin-security-privatelink)
- [Azure Private Link and Snowflake](/user-guide/privatelink-azure)
- [Google Cloud Private Service Connect and Snowflake](/user-guide/private-service-connect-google)

## Agent and connector application compatibilities

The Snowflake Connector for PostgreSQL is being released against a specific version, described as **x.y.z version** where x is major, y is minor and z is patch. Agents on Docker Hub are also
released with the X.Y.Z version. Each x.y.z version of Snowflake Connector for PostgreSQL supports all agents with the same major version X=x and a minor version no greater than y of the agent. Moreover, each x.0.0 version of the Snowflake Connector for PostgreSQL supports all (x-1).Y.Z versions of the agent for all Y and Z.

## Known limitations

The following sections describe the known limitations for the connector.

### Read replicas are not supported

Because of PostgreSQL limitations, logical replication is not supported on replicas; therefore, the Snowflake Connector for PostgreSQL must be connected to the primary database only.

### Connector availability

When installing the connector, note the following limitations:

- Accounts in government regions are not supported.
- To install and configure the connector, you must be logged in as a user with the ACCOUNTADMIN role. Other roles are not supported at this time.

### Types compatibility

Differences between the source database and Snowflake column types prevent some values from being converted and written into Snowflake because of the maximum column capacity or allowed ranges. For example:

- Snowflake BINARY type has a maximum length of 64 MB (67108864 bytes)
- Snowflake date types, like DATE, DATETIME, and TIMESTAMP, have a maximum year of 9999
- Snowflake VARCHAR type has a maximum length of 128 MB (134217728 bytes)

If such incompatibility happens, the replication of a table is stopped with a failure.

### Source table schema changes

The following table shows different types of changes to the source table schema and whether they are supported, and if so how.

New column names are subject to the same limitations as described in the Identifiers limitations section.

| Type of schema change | Supported? | Notes |
| --- | --- | --- |
| Adding a new column | Yes | The new column will be visible in the destination table just like any other column that existed at the start of the replication.  It is not possible to add a new column with the same name as a previously deleted or renamed column.  For example, if columns `A` and `B` existed initially, but `A` was deleted and `B` was renamed to `B2` - it is not possible to add a column named `A` or `B`. |
| Deleting an existing column | Yes | If a column is deleted in the source table, it will not be deleted in the destination table. Instead, a soft-delete approach is followed and the column will be renamed to `<previous name>__SNOWFLAKE_DELETED` so that historical values can still be queried. All rows replicated after the column is deleted will have a NULL value in this column.  For example, if a column `A` is deleted, it will be renamed to `A__SNOWFLAKE_DELETED` in the destination table and the contents of the column remain unchanged. |
| Renaming a column | Yes | Renaming a column is equal to deleting the column and creating a new one with the new name. The deletion follows the soft-delete approach explained in the previous row.  For example, if column `A` was renamed to `B` - in the destination table `A` was renamed to `A__SNOWFLAKE_DELETED`, and a new column `B` was added. All rows existing before the change keep the column’s values in the `A__SNOWFLAKE_DELETED` column, while new rows added after the change have the values in the `B` column.  It is not possible to rename a column to the same name as a previously deleted or renamed column. For example, if columns `A`, `B` and `C` existed initially, but `A` was deleted and `B` was renamed to `B2` - it is not possible to rename the column `C` to `A` or `B`. |
| Changing the type of column | Partially | Changing the type of source table column is only possible if both the previous and the new type are mapped to the same type in Snowflake.  In any other case, the replication will fail permanently. |
| Changing the precision of a numeric column | No | Changing the precision of a source table column will result in replication failing permanently. |
| Changing the scale of a numeric column | No | Changing the scale of a source table column will result in replication failing permanently. |
| Changing the primary key definition | No | Changing the primary key definition of the source table column will result in replication failing permanently. |

Expand

Show lessSee more

### High-capacity columns

An active agent is continuously reading all events using the logical replication mechanism, even if some events refer to source tables that
were not added for replication. If the logical replication contains very large events, like updates of the TEXT-like columns,
the agent might crash because of the lack of available memory.

### Primary keys

Tables without primary keys are not supported.

### Identifiers limitations

Currently, the connector does not support the `"` character in replicated schema, table or column names.
Additionally, the following keywords are not supported:

For schema names:
:   - `INFORMATION_SCHEMA`

For column names:
:   - `_SNOWFLAKE_INSERTED_AT`
    - `_SNOWFLAKE_UPDATED_AT`
    - `_SNOWFLAKE_DELETED`
    - names with suffix `__SNOWFLAKE_DELETED`
    - Column names marked as `Cannot be used as column name` in [Reserved & limited keywords](/sql-reference/reserved-keywords)

### PostgreSQL version >= 11

Currently, the connector depends on the `wal_level = logical` configuration property that was introduced in PostgreSQL version 11.

### Replica identity setting

The [Replica identity](https://www.postgresql.org/docs/current/sql-altertable.html#SQL-ALTERTABLE-REPLICA-IDENTITY) of replicated tables must be set to `DEFAULT`.

### TOAST values

The replication of tables with TOAST values is not currently supported. This includes adding TOAST-able columns to the source schema when replication is already running.

### Source database authorization

Private key authorization to the source database is not supported. Only authorization via user and password is supported.

### Replica identity

The replica identity of a given table must be the same as the primary key, otherwise the replication will fail.
