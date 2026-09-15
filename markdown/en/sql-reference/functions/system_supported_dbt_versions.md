Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$SUPPORTED\_DBT\_VERSIONS

Returns a JSON array containing the versions that Snowflake supports for dbt Projects on Snowflake.

For more information, see [Supported dbt versions for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-dbt-core-versions).

## Syntax

Copy code

```
SYSTEM$SUPPORTED_DBT_VERSIONS()
```

## Arguments

None.

## Returns

Returns a JSON array containing the versions that Snowflake supports for dbt Projects on Snowflake.

## Examples

To view supported dbt versions, run the following SQL command:

Copy code

```
SELECT SYSTEM$SUPPORTED_DBT_VERSIONS();
```

```
[{"dbt_version":"1.9.4","type":"dbt Core"},{"dbt_version":"1.10.15","type":"dbt Core"},{"dbt_version":"1.11.11","type":"dbt Core"},{"dbt_version":"2.0.0-preview","type":"dbt Fusion"},{"dbt_version":"2.0.0-preview.175","type":"dbt Fusion"},{"dbt_version":"2.0.0-preview.186","type":"dbt Fusion"}]
```
