# Viewing PostgreSQL data in Snowflake

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts except government regions.

Important

Thank you for your interest in the Snowflake Connector for PostgreSQL.
Note that we’re now focused on a next-generation solution that will offer a significantly improved experience.
Hence, moving this connector to the general availability status is currently not on our product roadmap.
You may continue to use this connector as a preview feature, but please note that support for future bug
fixes and improvements are not guaranteed. The new solution is available as [Openflow Connector for PostgreSQL](/user-guide/data-integration/openflow/connectors/postgres/about) and
includes better performance, customizability, and enhanced deployment options.

The connector replicates data to the destination database, which was defined while setting up the connector and calling `PUBLIC.ADD_DATA_SOURCE('data_source_name', 'dest_db')`.

Data tables contain the replicated data and are available under identifier `dest_db.schema_name.table_name` where:

- `dest_db` is the name of the destination database.
- `schema_name` is the schema name in which the original PostgreSQL table resides.
- `table_name` is the name of the original PostgreSQL table.

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

The replicated data types are mapped to match the Snowflake types. For more information, see [PostgreSQL to Snowflake data type mapping](#label-postgres-connector-types-mappings-6).

## Replicated data access control

To control access to replicated data use `DATA_READER` application role. More on connector application roles: [Application roles in the Snowflake Connector for PostgreSQL](/connectors/postgres6/roles)
For more granular control over specific destination objects, use `ACCOUNTADMIN` role to grant proper privileges or create database roles.

## PostgreSQL to Snowflake data type mapping

In Snowflake, column names of replicated tables are capitalized and types are mapped to match the Snowflake types.

The following table shows the PostgreSQL to Snowflake types mapping.

| PostgreSQL Type | Snowflake Type | Notes |
| --- | --- | --- |
| BIGINT / INT8 | INT |  |
| BIGSERIAL / SERIAL8 | INT |  |
| BIT [(N)] | VARCHAR |  |
| BIT VARYING [(N)] / VARBIT [(n)] | VARCHAR |  |
| BOOLEAN / BOOL | BOOLEAN |  |
| BOX | VARCHAR |  |
| BYTEA | BINARY(N) | Supported up to the max datapoint size in Snowflake (16MB). Max length 1 GB. |
| CHARACTER [(N)] / CHAR [(N)] | VARCHAR [N] | Max length 10485760 ~= 10 MB |
| CHARACTER VARYING [(N)] / VARCHAR [(N)] | VARCHAR [N] | Max length 10485760 ~= 10 MB |
| CIDR | VARCHAR |  |
| CIRCLE | VARCHAR |  |
| DATE | DATE |  |
| DOUBLE PRECISION / FLOAT8 | FLOAT |  |
| INET | VARCHAR |  |
| INTEGER / INT / INT4 | INT |  |
| INTERVAL [FIELDS][(P)] | VARCHAR |  |
| JSON | VARIANT | Supported up to the max datapoint size in Snowflake (16MB). |
| JSONB | VARIANT | Supported up to the max datapoint size in Snowflake (16MB). |
| LINE | VARCHAR |  |
| LSEG | VARCHAR |  |
| MACADDR | VARCHAR |  |
| MACADDR8 | VARCHAR |  |
| MONEY | VARIANT |  |
| NUMERIC [(P, S)] / DECIMAL [(P, S)] | DECIMAL(P, S) | Scale and precision are also recreated on the Snowflake side preserving Snowflake limitations. |
| PATH | VARCHAR |  |
| PG\_LNS | VARCHAR |  |
| POINT | VARCHAR |  |
| POLYGON | VARCHAR |  |
| REAL / FLOAT4 | FLOAT |  |
| SMALLINT / INT2 | INT |  |
| SMALLSERIAL / SERIAL2 | INT |  |
| SERIAL / SERIAL4 | INT |  |
| TEXT | VARCHAR |  |
| TIME [(P)] [ without time zone ] | TIME |  |
| TIME [(P)] with time zone | TIME |  |
| TIMESTAMP [(P)] [ without time zone ] | DATETIME / TIMESTAMP\_NTZ |  |
| TIMESTAMP [(P)] with time zone | TIMESTAMP\_TZ |  |
| TSQUERY | VARCHAR |  |
| TSVECTOR | VARCHAR |  |
| UUID | VARCHAR |  |
| XML | VARCHAR |  |

Expand

Show lessSee more

All other types, including arrays, ENUMs, custom types and ranges are mapped to VARCHAR values in Snowflake.
The following table illustrates how types not explicitly mentioned in the table above are handled.

| PostgreSQL Type | Data in PostgreSQL | Column in Snowflake |
| --- | --- | --- |
| ENUM | monday | “monday” |
| array of INTEGER | {1,2,3,5} | “{1,2,3,5}” |
| intrange | [6,31) | “[6,31)” |
| custom type (2 fields, INT4 and TEXT) | (text value,5432) | “(text value,5432)” |

Expand

Show lessSee more

## Resuming snapshot load after failures

If the connection between the database agent and the connector is lost during snapshot load, because of time and cost optimisation,
the connector will continue to load the snapshot from the point where it was stopped before. This happens regardless of whether the agent was
restarted or if there was an issue with the connections between the source database and the database agent, and the database agent and the connector.

This feature works for primary key columns of the following types:

- SMALLINT/INT2
- INTEGER/INT/INT4
- BIGINT/INT8
- UUID
- NUMERIC
- TEXT
- VARCHAR
- BOOL

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

After completing these procedures, review the processes in [Snowflake Connector for PostgreSQL ongoing tasks](/connectors/postgres6/ongoing)
