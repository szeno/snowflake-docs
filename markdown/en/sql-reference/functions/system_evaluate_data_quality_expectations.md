Categories:
:   [System functions](/sql-reference/functions-system), [Table functions](/sql-reference/functions-table)

# SYSTEM$EVALUATE\_DATA\_QUALITY\_EXPECTATIONS

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the [expectations](/user-guide/data-quality-expectations) for associations between data metric functions (DMFs) and a table,
including whether an expectation is currently violated.

## Syntax

Copy code

```
SYSTEM$EVALUATE_DATA_QUALITY_EXPECTATIONS(
  REF_ENTITY_NAME  => '<object>'
  [ , SKIP_SUSPENDED_DMF => { TRUE | FALSE } ]
)
```

## Arguments

`REF_ENTITY_NAME => 'object'`
:   Name of the table or view that has at least one DMF with one or more expectations. Must be fully qualified.

`SKIP_SUSPENDED_DMF => { TRUE | FALSE }`
:   If set to TRUE, the function doesn’t return expectations that are defined for associations between the `object` and suspended
    DMFs. A suspended DMF doesn’t run on the object’s specified schedule.

    Default: TRUE

## Returns

Returns a table with the following columns:

| Column | Data type | Description |
| --- | --- | --- |
| `metric_database` | VARCHAR | Name of the database that contains the DMF. |
| `metric_schema` | VARCHAR | Name of the schema that contains the DMF. |
| `metric_name` | VARCHAR | Name of the DMF. |
| `expectation_name` | VARCHAR | Name that the user assigned the expectation when adding it to the association between the DMF and the table. |
| `expectation_id` | NUMBER | System-generated identifier. |
| `expectation_expression` | VARCHAR | Boolean expression of the expectation. See [Defining what meets the expectation](/user-guide/data-quality-expectations#label-dmf-expectation-expression). |
| `arguments` | ARRAY | Columns with which the DMF is associated. |
| `value` | VARIANT | The result of the DMF evaluation. |
| `expectation_violated` | BOOLEAN | If TRUE, the expectation was violated. An expectation is violated when the `expectation_expression` evaluates to FALSE. |
| `group_by_values` | VARIANT | For an expectation defined on an association created with a WITHIN GROUP clause, a JSON object that identifies the group this row corresponds to. Each key is a grouping column name and each value is that column’s value for the group, for example `{"REGION": "US", "COUNTRY": "CA"}`. NULL for non-grouped associations.  For more information, see [Apply data quality checks by group](/user-guide/data-quality-group-by). |

Expand

Show lessSee more

## Access control privileges

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| SELECT | Table or view |  |
| USAGE | Data metric function (DMF) |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Example

Return the expectations for the associations between DMFs and table `t1`. The DMFs are executed to determine if the expectations are
currently violated.

Copy code

```
SELECT *
  FROM TABLE(SYSTEM$EVALUATE_DATA_QUALITY_EXPECTATIONS(
      REF_ENTITY_NAME => 'my_db.sch.t1'));
```

## See also

For expectations defined on an association created with a WITHIN GROUP clause, this function evaluates every group and returns one row per distinct group, with each group identified in the `group_by_values` output column. To retrieve the underlying rows for a specific group value, use
[SYSTEM$DATA\_METRIC\_SCAN](/sql-reference/functions/system_data_metric_scan), which accepts a `WITHIN_GROUP_VALUES` argument. For more information, see [Apply data quality checks by group](/user-guide/data-quality-group-by).

To evaluate expectations and persist the results to the `SNOWFLAKE.LOCAL.DATA_QUALITY_MONITORING_RESULTS_RAW` event table so that they appear in data quality history, use
[SYSTEM$EVALUATE\_DATA\_QUALITY\_EXPECTATIONS\_PERSIST\_RESULT](/sql-reference/functions/system_evaluate_data_quality_expectations_persist_result).
