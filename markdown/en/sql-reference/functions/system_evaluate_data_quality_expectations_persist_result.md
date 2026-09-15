Categories:
:   [System functions](/sql-reference/functions-system), [Table functions](/sql-reference/functions-table)

# SYSTEM$EVALUATE\_DATA\_QUALITY\_EXPECTATIONS\_PERSIST\_RESULT

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Evaluates data quality [expectations](/user-guide/data-quality-expectations) for associations between data metric functions (DMFs) and a table
and persists the results to the `SNOWFLAKE.LOCAL.DATA_QUALITY_MONITORING_RESULTS_RAW` event table so that ad-hoc quality checks appear in data quality history.

This stored procedure behaves like [SYSTEM$EVALUATE\_DATA\_QUALITY\_EXPECTATIONS](/sql-reference/functions/system_evaluate_data_quality_expectations)
but additionally writes the evaluation results to the `SNOWFLAKE.LOCAL.DATA_QUALITY_MONITORING_RESULTS_RAW` event table.

## Syntax

Copy code

```
CALL SYSTEM$EVALUATE_DATA_QUALITY_EXPECTATIONS_PERSIST_RESULT(
  '<object>'
  [ , <skip_suspended_dmf> ]
)
```

## Arguments

`'object'`
:   Name of the table or view that has at least one DMF with one or more expectations. Must be fully qualified.

`skip_suspended_dmf`
:   A BOOLEAN value that specifies whether to skip suspended DMFs.

    If set to TRUE, the procedure doesn’t return expectations that are defined for associations between the `object` and suspended
    DMFs. A suspended DMF doesn’t run on the object’s specified schedule.

    Default: FALSE

## Returns

Returns a table with the following columns:

| Column | Data type | Description |
| --- | --- | --- |
| `METRIC_DATABASE` | VARCHAR | Name of the database that contains the DMF. |
| `METRIC_SCHEMA` | VARCHAR | Name of the schema that contains the DMF. |
| `METRIC_NAME` | VARCHAR | Name of the DMF. |
| `EXPECTATION_NAME` | VARCHAR | Name that the user assigned the expectation when adding it to the association between the DMF and the table. |
| `EXPECTATION_ID` | VARCHAR | System-generated identifier. |
| `EXPECTATION_EXPRESSION` | VARCHAR | Boolean expression of the expectation. See [Defining what meets the expectation](/user-guide/data-quality-expectations#label-dmf-expectation-expression). |
| `ARGUMENTS` | VARCHAR | Columns with which the DMF is associated. |
| `VALUE` | VARCHAR | The result of the DMF evaluation. |
| `EXPECTATION_VIOLATED` | VARCHAR | If TRUE, the expectation was violated. An expectation is violated when the `EXPECTATION_EXPRESSION` evaluates to FALSE. |

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

Evaluate the expectations for the associations between DMFs and table `t1`, and persist the results to the event table:

Copy code

```
CALL SYSTEM$EVALUATE_DATA_QUALITY_EXPECTATIONS_PERSIST_RESULT('my_db.sch.t1');
```

Evaluate with suspended DMFs skipped:

Copy code

```
CALL SYSTEM$EVALUATE_DATA_QUALITY_EXPECTATIONS_PERSIST_RESULT('my_db.sch.t1', TRUE);
```

## See also

[SYSTEM$EVALUATE\_DATA\_QUALITY\_EXPECTATIONS](/sql-reference/functions/system_evaluate_data_quality_expectations)
