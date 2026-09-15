# Snowflake Connector for PostgreSQL characteristics

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts except government regions.

Important

Thank you for your interest in the Snowflake Connector for PostgreSQL.
Note that we’re now focused on a next-generation solution that will offer a significantly improved experience.
Hence, moving this connector to the general availability status is currently not on our product roadmap.
You may continue to use this connector as a preview feature, but please note that support for future bug
fixes and improvements are not guaranteed. The new solution is available as [Openflow Connector for PostgreSQL](/user-guide/data-integration/openflow/connectors/postgres/about) and
includes better performance, customizability, and enhanced deployment options.

## Version support

The Snowflake Connector for PostgreSQL supports any officially supported PostgreSQL version. Snowflake drops support for older versions as customers move to newer versions. Snowflake announces support for new versions as they are released.

While the connector supports a number of PostgreSQL cloud versions, some require additional settings. See [Prerequisites for Snowflake Connector for PostgreSQL datasources](/connectors/postgres6/prereqs-datasource) for more information.

The following are the supported PostgresSQL versions.

**Supported PostgreSQL versions**

|  | 11 | 12 | 13 | 14 | 15 | 16 | 17 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [Standard](https://www.postgresql.org/) | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| [AWS RDS](https://docs.aws.amazon.com/AmazonRDS/latest/PostgreSQLReleaseNotes/Welcome.html) | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| [Amazon Aurora](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraPostgreSQLReleaseNotes/Welcome.html) | Yes | Yes | Yes | Yes | Yes | Yes |  |
| [GCP Cloud SQL](https://cloud.google.com/sql/docs/postgres/) | Yes | Yes | Yes | Yes | Yes | Yes |  |
| [Azure Database](https://learn.microsoft.com/en-us/azure/postgresql/) | Yes | Yes | Yes | Yes | Yes | Yes |  |

Expand

Show lessSee more

## Server settings

Review and adjust the following settings on your PostgreSQL server as required:

|  |  |
| --- | --- |
| `wal_level` | Set to `logical`.  The connector relies on primary keys to merge changes into destination tables. The following settings ensure that Write-Ahead Log (WAL) records include primary key information: |
| `max_replication_slots` | Add 1 for every data source configuration entry for this database in the database agent. |
| `max_connections` | Add 1 for every data source configuration entry for this database in the database agent. |
| `max_wal_senders` | Add 1 for every data source configuration entry for this database in the database agent. |

Expand

Show lessSee more

## Publications

The connector requires a [PostgreSQL publication](https://www.postgresql.org/docs/current/logical-replication-publication.html) to access tables for replication.

- The database agent supports exactly one publication per data source. If you need to use multiple publications in a single PostgreSQL server, you can configure that server multiple times as separate data sources, each one with its own publication.
- The publication should include all changes made to data, including `INSERT`, `UPDATE`, `DELETE`, and `TRUNCATE`.
- The publication can be set up for `ALL TABLES` or a subset of tables, but for optimal performance, only add those tables that should be replicated. The connector will only receive changes from the tables included in the publication.
- Tables can be added to the publication with all their columns, or a subset of columns. When adding with a subset of columns, use the [ADD\_TABLE\_WITH\_COLUMNS procedure](/connectors/postgres6/configure-replication#label-postgres-connector-add-table-with-columns).

Warning

When a table is added to a publication with a subset of columns, but then enabled for replication using the [ADD\_TABLES](/connectors/postgres6/configure-replication#label-postgres-connector-add-source-table) procedure, columns missing from the publication will be marked in the destination table as deleted. Adding any additional columns to the publication later will result in the table being marked as permanently failed.

For more information on publication configuration, see [Configure publication](/connectors/postgres6/prereqs-datasource#label-postgres-connector-configure-publication).

## Replication slots

To replicate data and schema changes, the connector creates a [replication slot](https://www.postgresql.org/docs/current/logicaldecoding-explanation.html#LOGICALDECODING-REPLICATION-SLOTS). The slot is created when the first table in a given data source is added to replication, and used for all tables from that data source.

The slot’s name is structured as `sf_db_conn_rs_kbmd_<data-source-name>`, where `<data-source-name>` is the identifier of the data source in the database agent’s configuration.

- If you configure the database agent to connect to the same database multiple times, by adding several data sources, the connector will create *multiple* replication slots.
- If you configure multiple database agents to connect to the same PostgreSQL server, you must provide unique data source names to each database agent.

Caution

The database agent *does not remove* unused replication slots. If you disconnect the database agent from a PostgreSQL instance or remove all of its tables from replication, then you *must* also manually drop the replication slot to prevent it from holding up WAL trimming.

### WAL growth and replication slot position

Once created, a replication slot will cause PostgreSQL to retain the WAL data from the position held by the replication slot, until the connector confirms and advances that position. The connector periodically confirms the position after records have been stored in its journal tables, even if they were not yet merged into destination tables.

- In **continuous mode**, the connector confirms the position every minute.
- In **scheduled mode**, the connector confirms the position based on the configured schedule. Keep in mind that longer schedules *will cause the WAL to grow larger*.

You must ensure there is enough disk space on your PostgreSQL server for the WAL. If you detect the WAL growing continuously, check the following:

- Is the database agent connected, and the connector actively replicating data? If not, the replication slot is not being advanced, and blocks WAL trimming.
- Is the replication keeping up with the data changes in replicated tables? If not, meaning that the lag between a data change in the source and its appearance in the Snowflake destination table keeps growing, then the replication slot is being advanced too slowly. You need to remove some tables from replication, or increase the compute warehouse size.

The `max_wal_size` setting in PostgreSQL will have no effect on WAL growth when it is caused by a replication slot not advancing.

Tip

In critical situations, you can manually drop the replication slot used by the connector. This will break any replication running in the connector, but enable PostgreSQL to trim the WAL and reclaim disk space.

## Primary keys and table replica identity

The connector relies on primary keys to merge changes into the destination tables. As a result:

- Every table enabled for replication must have a primary key. The key can be a single column or composite.
- Tables must also have their [REPLICA IDENTITY](https://www.postgresql.org/docs/current/sql-altertable.html#SQL-ALTERTABLE-REPLICA-IDENTITY) set to `DEFAULT`. This ensures primary keys are represented in the WAL, and the connector can read them.

## Agent authentication

The only authentication method currently supported is username and password. Every data source entry in the database agent’s configuration includes its own set of credentials, and these can vary between data sources.

The database agent’s users must have a role with the `REPLICATION` attribute, or `SUPERUSER` if the former cannot be applied.

For instructions on how to create a user for the database agent, see [Create required user](/connectors/postgres6/prereqs-datasource#label-postgres-connector-create-agent-user).

For more information on securing the database agent’s access to the source databases, see [PostgreSQL documentation](https://www.postgresql.org/docs/current/logical-replication-security.html).
