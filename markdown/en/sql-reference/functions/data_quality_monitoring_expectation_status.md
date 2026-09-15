Categories:
:   [LOCAL schema](/sql-reference/local) , [Table functions](/sql-reference/functions-table)

# DATA\_QUALITY\_MONITORING\_EXPECTATION\_STATUS

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

For a specified object, returns a row for every time a data metric function (DMF) with an
[expectation](/user-guide/data-quality-expectations) was run. You can obtain the status of the expectation in each row.

See also:
:   [DATA\_QUALITY\_MONITORING\_EXPECTATION\_STATUS view](/sql-reference/local/data_quality_monitoring_expectation_status) (LOCAL view)

## Syntax

Copy code

```
DATA_QUALITY_MONITORING_EXPECTATION_STATUS(
  REF_ENTITY_NAME => '<string>' ,
  REF_ENTITY_DOMAIN => '<string>'
  )
```

## Arguments

`REF_ENTITY_NAME => 'string'`
:   The name of the table object on which the data metric function with an expectation is set. The name must be fully qualified.

    - The entire object name must be enclosed in single quotes.
    - If the object name is case-sensitive or includes any special characters or spaces, double quotes are required to process the
      case/characters. The double quotes must be enclosed within the single quotes, such as `'"table_name"'`.

`REF_ENTITY_DOMAIN => 'string'`
:   The object type on which the data metric function with an expectation is set.

    If the object is a kind of table, use `'TABLE'` as the argument value.

    If the object is a view or materialized view, use `'VIEW'` as the argument value.

    For a list of supported object types on which a data metric function can be set, see [Supported table kinds](/user-guide/data-quality-intro#label-data-quality-supported-tables).

## Output

The function returns rows with the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| `scheduled_time` | TIMESTAMP\_LTZ | The time the DMF is scheduled to run based on the schedule that you set for the table or view. |
| `change_commit_time` | TIMESTAMP\_LTZ | The time the DMF trigger operation occurred, or NULL if the DMF is not scheduled to run by a trigger operation.  For information about the trigger operation, see [Adjust the schedule for DMFs](/user-guide/data-quality-working#label-data-quality-schedule). |
| `measurement_time` | TIMESTAMP\_LTZ | The time at which the metric was evaluated. |
| `table_id` | NUMBER | Internal/system-generated identifier of the table that is associated with the DMF. |
| `table_name` | VARCHAR | Name of the table that is associated with the DMF. |
| `table_schema` | VARCHAR | Name of the schema that contains the table that is associated with the DMF. |
| `table_database` | VARCHAR | Name of the database that contains the table that is associated with the DMF. |
| `metric_id` | NUMBER | Internal/system-generated identifier of the DMF. |
| `metric_name` | VARCHAR | Name of the DMF. |
| `metric_schema` | VARCHAR | Name of the schema that contains the DMF. |
| `metric_database` | VARCHAR | Name of the database that contains the DMF. |
| `metric_return_type` | VARCHAR | Return type of the DMF. |
| `argument_ids` | ARRAY | Array of the identifiers of the DMF arguments. Array elements are in the same order as the arguments. |
| `argument_types` | ARRAY | Array of the domain/type of each argument. Array elements are in the same order as the arguments.  Currently only supports COLUMN type arguments. |
| `argument_names` | ARRAY | Array of the names of the DMF arguments. For column arguments, each element is the name of a column. Array elements are in the same order as the arguments. |
| `reference_id` | VARCHAR | The ID to uniquely identify the metric entity reference, known as the association ID. |
| `value` | VARIANT | The result of the DMF evaluation. |
| `expectation_name` | VARCHAR | Name that was given to the expectation when it was added to the association between the DMF and the object. |
| `expectation_id` | VARCHAR | System-generated identifier. |
| `expectation_expression` | VARCHAR | Boolean expression of the expectation. See [Defining what meets the expectation](/user-guide/data-quality-expectations#label-dmf-expectation-expression). |
| `expectation_violated` | BOOLEAN | If TRUE, the expectation was violated. An expectation is violated when the `expectation_expression` evaluates to FALSE.  A NULL value indicates the evaluation of the expectation failed. |

Expand

Show lessSee more

## Access control requirements

To access this function, the role in use must have the SNOWFLAKE.DATA\_QUALITY\_MONITORING\_LOOKUP application role, at a minimum. For other
application role options, see [Viewing data quality results](/user-guide/data-quality-access-control#label-data-quality-access-control-view). Use the [GRANT APPLICATION ROLE](/sql-reference/sql/grant-application-role)
command to grant the application role to a role.

To view results, the role in use must also have the following privileges:

- The SELECT or OWNERSHIP privileges on the object (table or view) to which the data metric function is assigned.
- The USAGE or OWNERSHIP privileges on the data metric function.

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

## Usage notes

Errors occur if the specified object name does not exist or if the query operator is not authorized to view any data metric function on
the object. Unsupported object types specified in the REF\_ENTITY\_DOMAIN argument, such as `'STREAM'`, also return errors.

## Examples

Return a row for each data metric function with an expectation that is assigned to the table named `my_table`:

Copy code

```
SELECT *
  FROM TABLE(SNOWFLAKE.LOCAL.DATA_QUALITY_MONITORING_EXPECTATION_STATUS(
    REF_ENTITY_NAME => 'my_db.sch1.my_table',
    REF_ENTITY_DOMAIN => 'TABLE'));
```
