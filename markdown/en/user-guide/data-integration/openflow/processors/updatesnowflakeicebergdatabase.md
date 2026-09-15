# UpdateSnowflakeIcebergDatabase 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-snowflake-processors-nar

## Description

Updates the definition of a Snowflake Iceberg table. A target schema can be inferred from a RecordReader or defined explicitly using the format below: { “columns”: [ { “name”: “<column name>”, “type”: “<iceberg data type>” }, … ] } where <iceberg data type> can be one of: - primitive iceberg type (“string”, “int”, “boolean”,…) - decimal with given precision and scale (“decimal(P,S)”) - {“type”: “list”, “element”: <iceberg data type>} - {“type”: “map”, “key”: <iceberg data type>, “value”: <iceberg data type>} - {“type”: “struct”, “fields”:[<list of struct fields>] }

## Tags

iceberg

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Add Column Strategy | The strategy to use when the incoming schema has a column that is not present in the existing table |
| Alter Column Strategy | The strategy to use when a column has different data type in the incoming schema from the existing table |
| Alter Column Type Strategy | The strategy to use when the existing table has a column with a different type than the incoming schema. |
| Connection Pool | The connection pool to use to connect to Snowflake |
| Desired Schema | The desired schema / table definition |
| Drop Column Strategy | The strategy to use when the existing table has a column that is not present in the incoming schema |
| Max Batch Size | The maximum number of FlowFiles that can be processed in a single execution for a given table. |
| Record Reader | Record Reader to use for obtaining the desired schema |
| Schema Name | The name of the schema to update |
| Table Metadata Cache Expiration Time | The time in seconds after which the cache entry will be removed |
| Table Name | The name of the table to update |
| Table Schema Strategy | Specifies how to obtain the desired schema / table definition |
| Use Table Metadata Cache | Whether to cache table’s metadata instead of reading it directly from Snowflake |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | The incoming FlowFile is routed to this relationship if the table cannot be updated |
| illegal alteration | The incoming FlowFile is routed to this relationship if the update requires an alteration that is configured to fail |
| success | The incoming FlowFile is routed to this relationship after the table has been updated successfully |
| table not found | The incoming FlowFile is routed to this relationship if the specified table does not exist. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| schema.hash | A hexadecimal-encoded SHA-256 hash of the final table schema after all updates have been completed. |

Expand

Show lessSee more
