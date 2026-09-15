# Viewing MySQL data in Snowflake

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

The connector replicates data to the destination database, which was defined while setting up the connector and calling `PUBLIC.ADD_DATA_SOURCE('data_source_name', 'dest_db')`.

Data tables contain the replicated data and are available under identifier `dest_db.schema_name.table_name` where:

- `dest_db` is the name of the destination database.
- `schema_name` is the schema name in which the original MySQL table resides.
- `table_name` is the name of the original MySQL table.

Note

`dest_db`, `schema_name` and `table_name` needs to be double quoted in case their names are mixed-case.

The replicated tables contain the additional metadata columns:

| Column name | Data type | Description |
| --- | --- | --- |
| `_SNOWFLAKE_INSERTED_AT` | TIMESTAMP\_NTZ | Timestamp of when the row was inserted into the destination table, in UTC. |
| `_SNOWFLAKE_UPDATED_AT` | TIMESTAMP\_NTZ | Timestamp of when the row was last updated in the destination table, in UTC. |
| `_SNOWFLAKE_DELETED` | BOOLEAN | Value is `true` if the row has been deleted from the source table. |

Expand

Show lessSee more

The replicated data types are mapped to match the Snowflake types. For more information, see [MySQL to Snowflake data type mapping](#label-mysql-connector-types-mappings-6).

## Replicated data access control

To control access to replicated data use `DATA_READER` application role. More on connector application roles: [Application roles in the Snowflake Connector for MySQL](/connectors/mysql6/roles)
For more granular control over specific destination objects, use `ACCOUNTADMIN` role to grant proper privileges or create database roles.

## MySQL to Snowflake data type mapping

In Snowflake, column names of replicated tables are capitalized and types are mapped to match the Snowflake types.

The following table shows how connector data types are mapped to Snowflake types.

| MySQL Type | Snowflake Type | Notes |
| --- | --- | --- |
| DECIMAL / NUMERIC | NUMBER | The maximum number of digits in DECIMAL format for MySQL is 65. For Snowflake, the maximum is 38.  Supported up to the maximum allowed digits in Snowflake. When exceeded, precision is lost. For more information, see [Numeric data types](/sql-reference/data-types-numeric). |
| INT / INTEGER | INT |  |
| TINYINT / BOOL | INT |  |
| SMALLINT | INT |  |
| MEDIUMINT | INT |  |
| BIGINT | INT |  |
| YEAR | INT |  |
| FLOAT | FLOAT |  |
| DOUBLE | FLOAT |  |
| VARCHAR | VARCHAR |  |
| TINYTEXT | VARCHAR |  |
| TEXT | VARCHAR |  |
| ENUM | VARCHAR | Stored as a string. For example, for ENUM(‘one’, ‘two’) the possible values are: ‘one’, ‘two’. |
| SET | VARCHAR | Stored as a comma-joined string in column declaration order. For example, for SET(‘one’, ‘two’) the possible values are: ‘ ‘, ‘one’, ‘two’, ‘one,two’. |
| MEDIUMTEXT | VARCHAR | Supported up to the maximum entry size in Snowflake (16MB). |
| LONGTEXT | VARCHAR | Supported up to the maximum entry size in Snowflake (16MB). |
| CHAR | VARCHAR | Sent to Snowflake without the trailing spaces. |
| BIT | VARCHAR | Represented in hexadecimal, for example: ’83060c183060c183’. |
| DATE | DATE | Stored in target tables as strings, for example ’1971-01-31’. In flattened views, date is converted to DATE. |
| DATETIME | DATETIME / TIMESTAMP\_NTZ |  |
| TIMESTAMP | TIMESTAMP\_TZ | Stored in target tables as strings in UTC, for example ’2000-12-30 23:59:59.001009+00:00’. In flattened views, timestamps are converted to TIMESTAMP\_TZ. |
| TIME | TIME | Stored in target tables as strings, for example ’23:59:59’. In flattened views, time values are converted to TIME. |
| BINARY | BINARY |  |
| MEDIUMBLOB | BINARY | Supported up to the maximum entry size in Snowflake, which is 16MB. |
| LONGBLOB | BINARY | Supported up to the maximum entry size in Snowflake, which is 16MB. |
| BLOB | BINARY |  |
| VARBINARY | BINARY |  |
| TINYBLOB | BINARY |  |
| JSON | VARIANT | JSON can be stored in the MySQL BinLog as a complete document or as a partial update. By default, it is stored as a complete document. Partial updates are currently not supported.  JSONs are sent to Snowflake as strings, but Snowpipe Streaming converts them to a VARIANT data type and stores them internally as ARRAY, OBJECT, etc.  Supported up to the maximum entry size in Snowflake, which is 16MB. |

Expand

Show lessSee more

## Resuming snapshot load after failures

If the connection between the database agent and the connector is lost during snapshot load, because of time and cost optimisation,
the connector will continue to load the snapshot from the point where it was stopped before. This happens regardless of whether the agent was
restarted or if there was an issue with the connections between the source database and the database agent, and the database agent and the connector.

This feature works for primary key columns of the following types:

- TINYINT
- SMALLINT
- MEDIUMINT
- INT
- BIGINT
- ENUM
- CHAR
- TINYTEXT
- VARCHAR
- TEXT

If the primary key is of any other type, the snapshot load after the connection failure for a particular column will start from the beginning.

## Viewing data from deleted columns

If a column is deleted in the source table, it will not be deleted in the destination table.
Instead, a soft-delete approach is followed, and the column will be renamed to `<previous name>__SNOWFLAKE_DELETED` so that historical values can still be queried.

For example, if a column `A` is deleted, it will be renamed to `A__SNOWFLAKE_DELETED` in the destination table and can be queried as

Copy code

```
SELECT A__SNOWFLAKE_DELETED FROM <TABLE_NAME>;
```

## Viewing data from renamed columns

Renaming a column is equal to deleting the column and creating a new one with the new name.
The deletion follows the soft-delete approach explained in the previous section.

For example, if column `A` was renamed to `B` - in the destination table `A` was renamed to `A__SNOWFLAKE_DELETED` and a new column `B` is added.
All rows existing before the change keep the values of the column in the `A__SNOWFLAKE_DELETED` column while new rows added after the change have the values in the `B` column.
Values from the renamed column can be viewed as a single column with a simple query:

Copy code

```
SELECT
     CASE WHEN B IS NULL THEN A__SNOWFLAKE_DELETED ELSE B END AS A_RENAMED_TO_B
FROM <TABLE_WITH_RENAMED_COLUMN>;
```

A view can be created to simplify the usage after a column is renamed.

## Next steps

After completing these procedures, review the processes in [Snowflake Connector for MySQL ongoing tasks](/connectors/mysql6/ongoing)
