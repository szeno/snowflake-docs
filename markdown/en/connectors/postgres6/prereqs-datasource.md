# Prerequisites for Snowflake Connector for PostgreSQL datasources

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts except government regions.

Important

Thank you for your interest in the Snowflake Connector for PostgreSQL.
Note that we’re now focused on a next-generation solution that will offer a significantly improved experience.
Hence, moving this connector to the general availability status is currently not on our product roadmap.
You may continue to use this connector as a preview feature, but please note that support for future bug
fixes and improvements are not guaranteed. The new solution is available as [Openflow Connector for PostgreSQL](/user-guide/data-integration/openflow/connectors/postgres/about) and
includes better performance, customizability, and enhanced deployment options.

Before installing the Snowflake Connector for PostgreSQL, prepare the associated datasource by performing
the following tasks:

- [Configure associated datasource](#configure-associated-datasource)
- [Create required user](#create-required-user)

## Configure associated datasource

Ensure that you have a PostgreSQL version 11 or higher server that includes data you want to synchronize with Snowflake.
Before installing the Snowflake Connector for PostgreSQL, perform the following in your PostgreSQL environment:

- [Configure wal\_level](#configure-wal-level)
- [Configure publication](#configure-publication)
- [Create replication slot](#create-replication-slot)

### Configure wal\_level

Snowflake Connector for PostgreSQL requires [wal\_level](https://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-WAL-LEVEL) set to `logical`.

Depending on where the PostgreSQL server is hosted, it can be done in different ways.

|  |  |
| --- | --- |
| On premise | Execute the following query with a superuser or a user with `ALTER SYSTEM` privilege:  Copy code  ``` ALTER SYSTEM SET wal_level = logical; ``` |
| RDS | User used by the agent needs to have the `rds_superuser` or `rds_replication` roles assigned.  You also need to set:  - `rds.logical_replication` static parameter to 1. - `max_replication_slots`, `max_connections` and `max_wal_senders` parameters according to your database and replication setup. |
| AWS Aurora | Set the `rds.logical_replication` static parameter to 1. |
| GCP | Set the following flags:  - `cloudsql.logical_decoding=on`. - `cloudsql.enable_pglogical=on`.   For more information, see [Google Cloud documentation](https://cloud.google.com/sql/docs/postgres/replication/configure-logical-replication#set-up-logical-replication-with-pglogical). |
| Azure | Set the replication support to `Logical`. For more information, see [Azure documentation](https://learn.microsoft.com/en-us/azure/postgresql/single-server/concepts-logical#set-up-your-server). |

Expand

Show lessSee more

### Configure publication

Snowflake Connector for PostgreSQL requires [Publication](https://www.postgresql.org/docs/current/logical-replication-publication.html#LOGICAL-REPLICATION-PUBLICATION) to be created and configured.

Log in as a user with `CREATE` privilege in the database and execute the following query:

> Copy code
>
> ```
> CREATE PUBLICATION <publication name>;
> ```

Then define tables that the Snowflake Connector for PostgreSQL agent will be able to see using:

> Copy code
>
> ```
> ALTER PUBLICATION <publication name> ADD TABLE <table name>;
> ```

Attention

**For Postgres v15 and later**

In case of publications created for a subset of table’s columns, add tables for replication
using [ADD\_TABLE\_WITH\_COLUMNS](/connectors/postgres6/configure-replication#label-postgres-connector-add-table-with-columns) procedure, specifying exactly
the same set of columns.

If `ADD_TABLES` is used, the connector will work, but the following non-obvious side effects will occur:

> - in the destination database, columns that are not included in the filter will be suffixed with `_DELETED`. All data replicated during snapshot phase will still be there.
> - in case of adding more columns to the publication, the table will result in a `Permanently Failed` state, requiring restarting the replication.

For more information, see [ALTER PUBLICATION documentation](https://www.postgresql.org/docs/current/sql-alterpublication.html).

### Create replication slot

Snowflake Connector for PostgreSQL will create [Replication Slot](https://www.postgresql.org/docs/current/logicaldecoding-explanation.html#LOGICALDECODING-REPLICATION-SLOTS)
in PostgreSQL server with name having pattern `sf_db_conn_rs_kbmd_<DATASOURCE NAME>`, where `<DATASOURCE NAME>` is
the one specified in [ADD\_DATA\_SOURCE](/connectors/postgres6/configure-replication#label-postgres-connector-add-data-source-6) procedure.

If the connector is not used anymore, Replication Slot must be removed to avoid accumulating data in the PostgreSQL server.

> Copy code
>
> ```
> select pg_drop_replication_slot(<slot_name>)
> ```

## Create required user

Create user for Snowflake Connector for PostgreSQL with the `REPLICATION` attribute. For more information on replication security, see [PostgreSQL documentation](https://www.postgresql.org/docs/current/logical-replication-security.html).

## Next steps

After completing these procedures, follow the steps in [Setting up the Snowflake Connector for PostgreSQL using Snowsight](/connectors/postgres6/install-snowsight).
