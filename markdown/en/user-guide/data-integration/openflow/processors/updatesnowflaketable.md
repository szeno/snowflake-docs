# UpdateSnowflakeTable 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-snowflake-processors-nar

## Description

Updates the definition of a Snowflake table based on the schema provided in the incoming FlowFile. The schema is expected to be in JSON with the following format, regardless of whether it is provided via FlowFile content or specified as a property: { “columns”: [ { “name”: “<column name>”, “type”: “<column type>”, “nullable”: <true/false>, “precision”: <only for numeric type>, “scale”: <only for numeric type> }, … ], “primaryKeys”: [“<name of first primary key column>”, “<name of second primary key column>”, …] } This processor supports table-only operations: creating, altering, and dropping tables.

## Tags

alter, columns, create, ddl, drop, preview, snowflake, table, update

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Add Column Strategy | The strategy to use when the incoming schema has a column that is not present in the existing table |
| Add Not Null Strategy | The strategy to use when the incoming schema has a not-null constraint that is not present in the existing table |
| Alter Column Type Strategy | The strategy to use when the existing table has a column with a different type than the incoming schema. |
| Column Name Transformation | An optional transformation that can be applied to the names of columns defined in the schema. This transformation is applied to the column names before they are compared to the existing columns in the table. This property can reference the following variables via Expression Language, in addition to attributes: *column.name*, *column.type*, *column.nullable*, *column.precision*, *column.scale*, *column.primaryKey*.The result of applying transformations based on this property will be treated according to the setting of *Object Name Handling* property. |
| Column Removal Strategy | The strategy to use when the existing table has a column that is not present in the incoming schema |
| Connection Pool | The connection pool to use to connect to Snowflake |
| Creation Parameters | Additional parameters to include in the CREATE TABLE statement. For example, ‘CLUSTER BY (column\_name)’ |
| Desired Schema | The desired schema / table definition |
| Drop Column Strategy | The strategy to use when the existing table has a column that is not present in the incoming schema |
| Drop Not Null Strategy | The strategy to use when the existing table has a not-null constraint that is not present in the incoming schema |
| Include Default Values | Whether or not to include DEFAULT values in CREATE TABLE or ALTER TABLE ADD COLUMN statements |
| Include Not Null Constraints | Whether or not to include NOT NULL constraints in CREATE TABLE or ALTER TABLE ADD COLUMN statements |
| Include Primary Key Constraints | Whether or not to include primary key constraints in the creation statement |
| Max Batch Size | The maximum number of FlowFiles that can be processed in a single execution for a given table. |
| Modify Primary Key Strategy | The strategy to use when the incoming schema has a primary key that differs from the existing primary key. Modifying the Primary Key requires dropping the existing one, if any, and adding a new one. |
| Object Identifier Resolution | Controls how source object identifiers (schemas, tables, columns) are stored and queried in Snowflake. This setting determines whether you will need to use double quotes in your SQL queries. |
| Record Reader | Record Reader to use for obtaining the desired schema |
| Removed Column Name Suffix | The suffix to append to a column that was removed. For example, to rename column ‘foo’ to ‘foo\_\_deleted’, the property can be set to \_\_*deleted*. This property value will behave differently depending on the value of *Object Name Handling* property, i.e. If *Object Name Handling* is set to *Case Sensitive Name*, then the suffix will be appended as-is. If *Object Name Handling* is set to *SQL Identifier*, then the suffix and must consist of only letters, numbers, dollar sign ($), and underscore (\_) characters, additionally it will be appended as case-insensitive or case-sensitive depending on the column name it is being appended to is case-insensitive (not double-quoted) or case-sensitive (double-quoted) respectively. |
| Schema Name | The name of the schema containing the table |
| Table Metadata Cache Expiration Time | The time in seconds after which the cache entry will be removed |
| Table Name | The name of the table to update |
| Table Schema Strategy | Specifies how to obtain the desired schema / table definition |
| Update Type | The type of table update to perform |
| Use Table Metadata Cache | Whether to cache table’s metadata instead of reading it directly from Snowflake. Applies to [Create Table If Not Exists, Alter Table] |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | The incoming FlowFile is routed to this relationship if the table cannot be updated |
| success | The incoming FlowFile is routed to this relationship after the table has been updated successfully |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| schema.hash | A SHA-256 hash of the final table schema after all updates have been completed. Can be used for change detection and caching purposes. |

Expand

Show lessSee more
