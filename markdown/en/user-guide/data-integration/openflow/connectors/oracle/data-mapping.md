# Openflow Connector for Oracle: Data mapping

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

Note

The Openflow Connector for Oracle is also subject to additional terms of service beyond the standard
connector terms of service. For more information, see the
[Openflow Connector for Oracle Addendum](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/openflow-oracle-terms/).

This topic describes how Oracle data types are mapped to Snowflake data types when replicating data.

## Oracle to Snowflake data type mapping

The following table shows how Oracle data types are mapped to Snowflake data types
when replicating data.

| Oracle type | Snowflake type | Notes |
| --- | --- | --- |
| NUMBER | NUMBER | If precision is undefined, mapped to NUMBER(38, 19). If precision or scale exceeds Snowflake limitations (precision > 38 or scale > 37), the value is stored as TEXT. |
| FLOAT | FLOAT |  |
| BINARY\_FLOAT | FLOAT |  |
| BINARY\_DOUBLE | FLOAT |  |
| CHAR | TEXT |  |
| VARCHAR2 | TEXT |  |
| NCHAR | TEXT |  |
| NVARCHAR2 | TEXT |  |
| CLOB | TEXT | Supported by default up to 16 MB. |
| NCLOB | TEXT | Supported by default up to 16 MB. |
| LONG | TEXT | Supported by default up to 16 MB. |
| DATE | TIMESTAMP\_NTZ |  |
| TIMESTAMP | TIMESTAMP\_NTZ |  |
| TIMESTAMP WITH TIME ZONE | TIMESTAMP\_TZ |  |
| TIMESTAMP WITH LOCAL TIME ZONE | TIMESTAMP\_LTZ |  |
| INTERVAL | TEXT |  |
| INTERVAL YEAR TO MONTH | TEXT |  |
| INTERVAL DAY TO SECOND | TEXT |  |
| RAW | BINARY |  |
| LONG RAW | BINARY | Supported by default up to 8 MB. |
| BLOB | BINARY | Supported by default up to 8 MB. |
| BOOLEAN | BOOLEAN |  |
| JSON | VARIANT | Supported by default up to 16 MB. |
| XMLTYPE | TEXT | Supported by default up to 16 MB. |

Expand

Show lessSee more

Note

For types with default size limits (8 MB / 16 MB) in this table, it is possible to raise these limits. For details, see [Oversized values](/user-guide/data-integration/openflow/connectors/oracle/about#label-oracle-oversized-values).

Note

Any Oracle data types not listed in this table are mapped to TEXT by default.

## Next steps

Review [Set up tasks for the Openflow Connector for Oracle](/user-guide/data-integration/openflow/connectors/oracle/setup-tasks) to set up the connector.
