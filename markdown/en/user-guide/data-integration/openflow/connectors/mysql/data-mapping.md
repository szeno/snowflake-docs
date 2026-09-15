# Openflow Connector for MySQL: Data mapping

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes MySQL data types are mapped
to Snowflake data types.

## MySQL to Snowflake data type mapping

The following table shows how MySQL data types are mapped to Snowflake data types
when replicating data.

| MySQL type | Snowflake type | Notes |
| --- | --- | --- |
| DECIMAL / NUMERIC | NUMBER | The maximum number of digits in DECIMAL format for MySQL is 65. For Snowflake, the maximum is 38. Precision is lost when exceeded. |
| INT / INTEGER | INT |  |
| TINYINT / BOOL | INT |  |
| SMALLINT | INT |  |
| MEDIUMINT | INT |  |
| BIGINT | INT |  |
| YEAR | INT |  |
| FLOAT | FLOAT |  |
| DOUBLE | FLOAT |  |
| VARCHAR | TEXT |  |
| CHAR | TEXT | Trailing spaces aren’t preserved. |
| TINYTEXT | TEXT |  |
| TEXT | TEXT |  |
| MEDIUMTEXT | TEXT |  |
| LONGTEXT | TEXT | Supported by default up to 16 MB. |
| ENUM | TEXT | Stored as a string value. For example, for `ENUM('one', 'two')` the possible values are `'one'` and `'two'`. |
| SET | TEXT | Stored as a comma-separated string in column declaration order. For example, for `SET('one', 'two')` the possible values are `''`, `'one'`, `'two'`, and `'one,two'`. |
| BIT | TEXT | Represented as a hexadecimal string. For example: `'83060c183060c183'`. |
| DATE | DATE |  |
| DATETIME | TIMESTAMP\_NTZ |  |
| TIMESTAMP | TIMESTAMP\_TZ | Values are stored in UTC. |
| TIME | TIME |  |
| BINARY | BINARY |  |
| VARBINARY | BINARY |  |
| TINYBLOB | BINARY |  |
| BLOB | BINARY |  |
| MEDIUMBLOB | BINARY | Supported by default up to 8 MB. |
| LONGBLOB | BINARY | Supported by default up to 8 MB. |
| JSON | VARIANT | Supported by default up to 16 MB. |

Expand

Show lessSee more

Note

For types with default size limits (8 MB / 16 MB) in this table, it is possible to raise these limits. For details, see [Oversized values](/user-guide/data-integration/openflow/connectors/mysql/about#label-mysql-oversized-values).

Note

Any MySQL data types not listed in this table are mapped to TEXT by default.
