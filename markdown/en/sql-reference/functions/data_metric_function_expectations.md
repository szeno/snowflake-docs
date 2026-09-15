Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# DATA\_METRIC\_FUNCTION\_EXPECTATIONS

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns information about the [expectations](/user-guide/data-quality-expectations) that exist in the account.

## Syntax

Copy code

```
DATA_METRIC_FUNCTION_EXPECTATIONS(
  [ METRIC_NAME => '<string>' ]
  [, REF_ENTITY_NAME => '<string>' ]
  [, REF_ENTITY_DOMAIN => '<string>' ]
)
```

## Arguments

`METRIC_NAME => 'string'`
:   Specifies the name of a system or custom data metric function (DMF). This function returns expectations that were added to the
    associations between objects and the specified DMF.

`REF_ENTITY_NAME => 'string'`
:   Specifies the name of an object with which DMFs are associated. Returns expectations that were added to DMF associations with the object.
    If specified, you must also specify `REF_ENTITY_DOMAIN`.

    The entire object name must be enclosed in single quotes.

    If the object name is case-sensitive or includes any special characters or spaces, double quotes are required to process the
    case/characters. The double quotes must be enclosed within the single quotes, such as `'"table_name"'`.

`REF_ENTITY_DOMAIN => 'string'`
:   The object type of `REF_ENTITY_NAME`.

    - If the object is any type of table, use `table` as the argument value.
    - If the object is a view or materialized view, use `view` as the argument value.

## Output

The function returns the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| `metric_database_name` | VARCHAR | Database where the DMF exists. |
| `metric_schema_name` | VARCHAR | Schema where the DMF exists. |
| `metric_name` | VARCHAR | Name of the DMF. |
| `metric_signature` | VARCHAR | Signature of the DMF. |
| `metric_data_type` | VARCHAR | Data type returned by the DMF. |
| `ref_entity_database_name` | VARCHAR | Database of the object associated with the DMF. |
| `ref_entity_schema_name` | VARCHAR | Schema of the object associated with the DMF. |
| `ref_entity_name` | VARCHAR | Name of the object associated with the DMF. |
| `ref_entity_domain` | VARCHAR | Type of object associated with the DMF. |
| `ref_arguments` | ARRAY | Arguments passed to the DMF. |
| `ref_id` | VARCHAR | System-generated identifier. |
| `expectation_id` | VARCHAR | System-generated identifier of the expectation. |
| `expectation_name` | VARCHAR | Name given to the expectation by the user when it was added to the DMF association. |
| `expectation_expression` | VARCHAR | Boolean expression of the expectation. See [Defining what meets the expectation](/user-guide/data-quality-expectations#label-dmf-expectation-expression). |

Expand

Show lessSee more

## Examples

Return expectations that exist for a specific object.

Copy code

```
SELECT *
  FROM TABLE(
    INFORMATION_SCHEMA.DATA_METRIC_FUNCTION_EXPECTATIONS(
      REF_ENTITY_NAME => 'my_table',
      REF_ENTITY_DOMAIN => 'table'));
```

Return expectations that exist for a specific DMF.

Copy code

```
SELECT *
  FROM TABLE(
    INFORMATION_SCHEMA.DATA_METRIC_FUNCTION_EXPECTATIONS(
      METRIC_NAME => 'SNOWFLAKE.CORE.NULL_COUNT'));
```

Return expectations that exist for a specific association between an object and a DMF.

Copy code

```
SELECT *
  FROM TABLE(
    INFORMATION_SCHEMA.DATA_METRIC_FUNCTION_EXPECTATIONS(
      METRIC_NAME => 'SNOWFLAKE.CORE.NULL_COUNT',
      REF_ENTITY_NAME => 'my_table',
      REF_ENTITY_DOMAIN => 'table'));
```
