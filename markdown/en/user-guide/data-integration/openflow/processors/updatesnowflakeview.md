# UpdateSnowflakeView 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-snowflake-processors-nar

## Description

Creates or replaces Snowflake views based on column mappings provided in the incoming FlowFile. The processor checks if the view exists and only recreates it if the definition has changed. The FlowFile content should contain JSON with column mappings, optional join configuration, and optional flatten configuration: { “columns”: [ { “source\_field”: “customer\_data:id”, “destination\_column”: “customer\_id”, “type”: “VARCHAR” }, { “source\_field”: “f.value:order\_amount”, “destination\_column”: “order\_amount”, “type”: “NUMBER” }, { “expression”: “SUM(f.value:order\_amount::NUMBER)”, “destination\_column”: “total\_amount” }, { “expression”: “COUNT(*)”, “destination\_column”: “order\_count” } ], “from”: { “table”: “raw\_data”, “alias”: “rd”, “joins”: [ { “type”: “INNER”, “table”: “customers”, “alias”: “c”, “on”: “customer\_data:id::VARCHAR = c.customer\_id” } ] }, “flatten”: [ { “input”: “rd.orders”, “alias”: “f”, “path”: null } ], “where”: “active = true AND status =’VALID’”, “group\_by”: [“customer\_id”, “region”], “order\_by”: [“order\_amount DESC”, “customer\_id ASC”] } Column configuration supports: - source\_field: Simple field/column reference (supports JSON notation like “data:field” or table aliases like “t.column”) - expression: Complex SQL expression (e.g., “SUM(amount)”, “COUNT(*)”) - destination\_column: The output column name in the view (optional - auto-generated if not provided) - type: Snowflake data type for automatic type casting (VARCHAR, NUMBER, BOOLEAN, DATE, TIMESTAMP, etc.) Use either source\_field OR expression, not both. When type is specified, automatic type casting is applied. When type is omitted, the expression is used as-is without casting. Flatten configuration supports: - input: The nested field/column to flatten (required) - alias: Alias for the flattened data (required) - path: Optional path within the nested structure The “from” section is required and specifies the source table and optional joins. Optional SQL clauses can be included: - where: WHERE clause condition (e.g., “active = true AND status =’VALID’”) - group\_by: GROUP BY clause as an array of column names (e.g., [“customer\_id”, “region”]) - order\_by: ORDER BY clause as an array of column/expression with direction (e.g., [“order\_amount DESC”, “customer\_id ASC”])

## Tags

flatten, view

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Connection Pool | The connection pool to use to connect to Snowflake |
| Schema Name | The name of the schema where the view will be created |
| Secure | Whether to create a secure view. Secure views hide the view definition from unauthorized users. |
| View Name | The name of the view to create or update |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles that failed to be processed |
| success | FlowFiles that were successfully processed |
| unchanged | FlowFiles where the view already exists and hasn’t changed |

Expand

Show lessSee more
