# Snowflake Connector for MySQL characteristics

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts except government regions.

Important

Thank you for your interest in the Snowflake Connector for MySQL.
We’re now focused on a next-generation solution that will offer a significantly
improved experience; therefore, moving this connector to the general availability
status is currently not on our product roadmap.
You may continue to use this connector as preview feature, but please note that support for future bug
fixes and improvements are not guaranteed. The new solution is available as [Openflow Connector for MySQL](/user-guide/data-integration/openflow/connectors/mysql/about) and
includes better performance, customizability, and enhanced deployment options.

## Version support

Our general policy is that the Snowflake Connector for MySQL supports any officially supported MySQL Long-Term Support (LTS) version. We will be phasing out support for older versions as our users move onto newer ones, and will be announcing support for new versions as they get released.

While the connector supports a number of MySQL cloud flavors, some of them require additional settings. See [Prerequisites for Snowflake Connector for MySQL datasources](/connectors/mysql6/prereqs-datasource).

The following table lists tested and officially supported versions.

**List of officially supported PostgreSQL versions**

|  | 8.0 | 8.4 |
| --- | --- | --- |
| [Standard](https://www.mysql.com/) | Yes | Yes |
| [AWS RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_MySQL.html) | Yes |  |
| [Amazon Aurora](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraMySQLReleaseNotes/Welcome.html) | Yes, as Version 3 |  |
| [GCP Cloud SQL](https://cloud.google.com/sql/mysql?hl=en) | Yes | Yes |
| [Azure Database](https://azure.microsoft.com/en-us/products/mysql/) | No |  |

Expand

Show lessSee more

## Server settings

For the connector to work correctly, review and adjust the following settings on your MySQL server.

|  |  |
| --- | --- |
| `log_bin` | Set to `on`.  This enables the binary log that records structural and data changes. |
| `binlog_format` | Set to `row`.  The connector supports only row-based replication. MySQL 8.x versions may be the last ones to support this setting, and future versions will only support row-based replication.  Not applicable in GCP Cloud SQL, where it is fixed at the right value. |
| `binlog_row_metadata` | Set to `full`.  The connector requires all row metadata to operate, most importantly, column names and primary key information. |
| `binlog_row_image` | Set to `full`.  The connector requires that all columns be written into the binary log.  Not applicable in Amazon Aurora, where it is fixed at the right value. |
| `binlog_row_value_options` | Leave empty.  This option only affects JSON columns, where it can be set to include only the modified parts of JSON documents for `UPDATE` statements. The connector requires that full documents are written into the binary log. |
| `binlog_expire_logs_seconds` | Set to *at least* a few hours, or longer to ensure that the database agent can continue incremental replication after extended pauses or downtime.  If you’re using scheduled replication, the value needs to be longer than the configured schedule. |

Expand

Show lessSee more

## The binary log

MySQL’s binary log, once enabled, collects changes from *all* tables in a given instance. There is no way to exclude tables or columns. The connector will therefore receive changes from all tables in the database, and he database agent will process changes from tables that you configure for replication, but discard changes to all other tables.

Every change needs to be first loaded by the database agent, and for some **particularly large changes**, like updates to `BLOB` columns, even if they’re made on tables not configured for replication, these may exhaust the database agent’s memory and cause it to crash. If you store particularly large values anywhere in your database, make sure to configure sufficient memory for the database agent and its container.

**Transaction size** is limited by [MySQL’s replication limits](https://dev.mysql.com/doc/refman/8.4/en/group-replication-limitations.html#group-replication-limitations-transaction-size) to under 4 GB. Transactions crossing the limit will cause replication for the affected table to fail permanently.

## Agent authentication

The only authentication method currently supported is username and password. Every data source entry in the database agent’s configuration includes its own set of credentials, and these can be different for each data source.

The database agent’s users must have the following grants:

- `REPLICATION SLAVE` on all schemas and tables
- `REPLICATION CLIENT` on all schemas and tables
- `SELECT` on all schemas and on all tables

For instructions on how to create a user for the database agent, see [Create required user](/connectors/mysql6/prereqs-datasource#label-mysql-connector-create-agent-user).
