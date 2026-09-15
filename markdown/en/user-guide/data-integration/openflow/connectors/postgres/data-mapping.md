# Openflow Connector for PostgreSQL: Data mapping

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes how PostgreSQL data types are mapped
to Snowflake data types.

## PostgreSQL to Snowflake data type mapping

The following table shows how PostgreSQL data types are mapped to Snowflake data types
when replicating data.

| PostgreSQL type | Snowflake type | Notes |
| --- | --- | --- |
| SMALLINT / INT2 | INT |  |
| INTEGER / INT / INT4 | INT |  |
| BIGINT / INT8 | INT |  |
| SMALLSERIAL / SERIAL2 | INT |  |
| SERIAL / SERIAL4 | INT |  |
| BIGSERIAL / SERIAL8 | INT |  |
| NUMERIC / DECIMAL | NUMBER | Scale and precision are preserved within Snowflake limitations. Negative scale is converted to scale 0 with adjusted precision. |
| REAL / FLOAT4 | FLOAT |  |
| DOUBLE PRECISION / FLOAT8 | FLOAT |  |
| MONEY | FLOAT |  |
| BOOLEAN / BOOL | BOOLEAN |  |
| CHARACTER / CHAR / BPCHAR | TEXT |  |
| CHARACTER VARYING / VARCHAR | TEXT | Supported by default up to 16 MB. |
| TEXT | TEXT | Supported by default up to 16 MB. |
| BYTEA | BINARY | Supported by default up to 8 MB. |
| DATE | DATE |  |
| TIME / TIME WITHOUT TIME ZONE | TIME |  |
| TIME WITH TIME ZONE / TIMETZ | TIMESTAMP\_TZ |  |
| TIMESTAMP / TIMESTAMP WITHOUT TIME ZONE | TIMESTAMP\_NTZ |  |
| TIMESTAMP WITH TIME ZONE / TIMESTAMPTZ | TIMESTAMP\_LTZ |  |
| INTERVAL | TEXT |  |
| JSON | VARIANT | Supported by default up to 16 MB. |
| JSONB | VARIANT | Supported by default up to 16 MB. |
| UUID | TEXT |  |
| XML | TEXT | Supported by default up to 16 MB. |
| BIT | TEXT |  |
| BIT VARYING / VARBIT | TEXT |  |
| POINT | TEXT |  |
| LINE | TEXT |  |
| LSEG | TEXT |  |
| BOX | TEXT |  |
| PATH | TEXT |  |
| POLYGON | TEXT |  |
| CIRCLE | TEXT |  |
| CIDR | TEXT |  |
| INET | TEXT |  |
| MACADDR | TEXT |  |
| MACADDR8 | TEXT |  |
| TSVECTOR | TEXT |  |
| TSQUERY | TEXT |  |
| PG\_LSN | TEXT |  |

Expand

Show lessSee more

Note

For types with default size limits (8 MB / 16 MB) in this table, it is possible to raise these limits. For details, see [Oversized values](/user-guide/data-integration/openflow/connectors/postgres/about#label-postgres-oversized-values).

Note

Any PostgreSQL data types not listed in this table are mapped to TEXT by default.
