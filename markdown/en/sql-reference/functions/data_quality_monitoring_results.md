Categories:
:   [LOCAL schema](/sql-reference/local) , [Table functions](/sql-reference/functions-table)

# DATA\_QUALITY\_MONITORING\_RESULTS

Returns a row for each data metric function assigned to the specified object, which includes the evaluation result and other metadata of
the data metric function on the object.

See also:
:   [DATA\_QUALITY\_MONITORING\_RESULTS view](/sql-reference/local/data_quality_monitoring_results) (LOCAL view)

## Syntax

Copy code

```
DATA_QUALITY_MONITORING_RESULTS(
  REF_ENTITY_NAME => '<string>' ,
  REF_ENTITY_DOMAIN => '<string>'
  )
```

## Arguments

`REF_ENTITY_NAME => 'string'`
:   The name of the table object on which the data metric function is set.

    - The entire object name must be enclosed in single quotes.
    - If the object name is case-sensitive or includes any special characters or spaces, double quotes are required to process the
      case/characters. The double quotes must be enclosed within the single quotes, such as `'"<table_name>"'`.

`REF_ENTITY_DOMAIN => 'string'`
:   The object type on which the data metric function is set.

    If the object is a kind of table, use `'TABLE'` as the argument value.

    If the object is a view or materialized view, use `'VIEW'` as the argument value.

    For a list of supported object types on which a data metric function can be set, see [Supported table kinds](/user-guide/data-quality-intro#label-data-quality-supported-tables).

## Returns

The function returns the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| `scheduled_time` | TIMESTAMP\_LTZ | The time the DMF is scheduled to run based on the schedule that you set for the table or view. |
| `change_commit_time` | TIMESTAMP\_LTZ | The time the DMF trigger operation occurred, or `NULL` if the DMF is not scheduled to run by a trigger operation.  For information about the trigger operation, see [Adjust the schedule for DMFs](/user-guide/data-quality-working#label-data-quality-schedule). |
| `measurement_time` | TIMESTAMP\_LTZ | The time at which the metric was evaluated. |
| `table_id` | NUMBER | Internal/system-generated identifier of the table that the DMF is associated with. |
| `table_name` | VARCHAR | Name of the table that the DMF is associated with. |
| `table_schema` | VARCHAR | Name of the schema that contains the table that the DMF is associated with. |
| `table_database` | VARCHAR | Name of the database that contains the table that the DMF is associated with. |
| `metric_id` | NUMBER | Internal/system-generated identifier of the DMF. |
| `metric_name` | VARCHAR | Name of the DMF. |
| `metric_schema` | VARCHAR | Name of the schema that contains the DMF. |
| `metric_database` | VARCHAR | Name of the database that contains the DMF. |
| `metric_return_type` | VARCHAR | Return type of the DMF. |
| `argument_ids` | ARRAY | Array of the identifiers of the DMF arguments. Array elements are in the same order as the arguments. |
| `argument_types` | ARRAY | Array of the domain/type of each DMF argument. Array elements are in the same order as the arguments.  Currently only supports COLUMN type arguments. |
| `argument_names` | ARRAY | Array of the names of the DMF arguments. For column arguments, each element is the name of a column. Array elements are in the same order as the arguments. |
| `reference_id` | VARCHAR | The ID to uniquely identify the metric entity reference, known as the association ID. |
| `value` | VARIANT | The result of the DMF evaluation. |

Expand

Show lessSee more

## Access control requirements

To determine which privileges and roles you need to call this function, see [Viewing data quality results](/user-guide/data-quality-access-control#label-data-quality-access-control-view).

## Usage notes

Errors occur if the specified object name does not exist or if the query operator is not authorized to view any data metric function on
the object. Unsupported object types listed as the REF\_ENTITY\_DOMAIN, such as `'stream'`, also return errors.

## Examples

Return a row for each data metric function assigned to the table named `my_table`:

> Copy code
>
> ```
> USE DATABASE SNOWFLAKE;
> USE SCHEMA LOCAL;
> SELECT *
>   FROM TABLE(SNOWFLAKE.LOCAL.DATA_QUALITY_MONITORING_RESULTS(
>     REF_ENTITY_NAME => 'my_db.my_schema.my_table',
>     REF_ENTITY_DOMAIN => 'table'));
> ```
