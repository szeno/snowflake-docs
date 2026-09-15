# Openflow connectors for SQL Server: Data mapping

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes how SQL Server data types are mapped to Snowflake data types.
The mapping is the same for the Openflow Connector for SQL Server and the Openflow Connector for SQL Server (CDC).

## SQL Server to Snowflake data type mapping

The following table shows how SQL Server data types are mapped to Snowflake data types
when replicating data.

| SQL Server type | Snowflake type | Notes |
| --- | --- | --- |
| TINYINT | INT |  |
| SMALLINT | INT |  |
| INT | INT |  |
| BIGINT | INT |  |
| DECIMAL | NUMBER | If precision exceeds Snowflake limitations (precision > 38), the value is stored as TEXT. |
| NUMERIC | NUMBER | If precision exceeds Snowflake limitations (precision > 38), the value is stored as TEXT. |
| SMALLMONEY | NUMBER |  |
| MONEY | NUMBER |  |
| REAL | FLOAT |  |
| FLOAT | FLOAT |  |
| BIT | BOOLEAN |  |
| CHAR | TEXT |  |
| VARCHAR | TEXT | Supported by default up to 16 MB. |
| NCHAR | TEXT |  |
| NVARCHAR | TEXT | Supported by default up to 16 MB. |
| TEXT | TEXT | Supported by default up to 16 MB. |
| NTEXT | TEXT | Supported by default up to 16 MB. |
| DATE | DATE |  |
| TIME | TIME |  |
| SMALLDATETIME | TIMESTAMP\_NTZ |  |
| DATETIME | TIMESTAMP\_NTZ |  |
| DATETIME2 | TIMESTAMP\_NTZ |  |
| DATETIMEOFFSET | TIMESTAMP\_TZ |  |
| BINARY | BINARY |  |
| VARBINARY | BINARY | Supported by default up to 8 MB. |
| IMAGE | BINARY | Supported by default up to 8 MB. |
| JSON | VARIANT | Supported by default up to 16 MB. |
| VECTOR | VARIANT | Supported by default up to 16 MB. |
| XML | TEXT | Supported by default up to 16 MB. |
| UNIQUEIDENTIFIER | TEXT |  |
| ROWVERSION / TIMESTAMP | TEXT |  |
| SQL\_VARIANT | TEXT |  |
| GEOGRAPHY | TEXT | Values of this type are inserted as NULL. |
| GEOMETRY | TEXT | Values of this type are inserted as NULL. |

Expand

Show lessSee more

Note

For types with default size limits (8 MB / 16 MB) in this table, it is possible to raise these limits. For details of the Openflow Connector for SQL Server (CDC), see [Oversized values](/user-guide/data-integration/openflow/connectors/sql-server-cdc/about#label-sql-server-cdc-oversized-values) and for Openflow Connector for SQL Server, see [Oversized values](/user-guide/data-integration/openflow/connectors/sql-server/about#label-sql-server-oversized-values).

Note

Any SQL Server data types not listed in this table are mapped to TEXT by default.
