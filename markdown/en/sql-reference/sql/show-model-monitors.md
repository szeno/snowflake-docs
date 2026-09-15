# SHOW MODEL MONITORS

Lists all model monitors that you can access in the current or specified schema and displays information about each one. See [ML Observability](/developer-guide/snowflake-ml/model-registry/model-observability) for model version monitors and [Gateway Monitoring & A/B Testing](/developer-guide/snowflake-ml/inference/gateway-monitor-and-ab-testing) for gateway model monitors.

See also:
:   [CREATE MODEL MONITOR](/sql-reference/sql/create-model-monitor),
    [ALTER MODEL MONITOR](/sql-reference/sql/alter-model-monitor),
    [DESCRIBE MODEL MONITOR](/sql-reference/sql/desc-model-monitor),
    [DROP MODEL MONITOR](/sql-reference/sql/drop-model-monitor)

## Syntax

Copy code

```
SHOW MODEL MONITORS
[ LIKE <pattern> ]
[ IN
    {
      ACCOUNT                  |

      DATABASE                 |
      DATABASE <database_name> |

      SCHEMA                   |
      SCHEMA <schema_name>     |
      <schema_name>            |

      GATEWAY <gateway_name>
    }
 ]
```

## Parameters

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`[ IN ... ]`
:   Optionally specifies the scope of the command. Specify one of the following:

    `ACCOUNT`
    :   Returns records for the entire account.

    `DATABASE`, `DATABASE db_name`
    :   Returns records for the current database in use or for a specified database (`db_name`).

        If you specify `DATABASE` without `db_name` and no database is in use, the keyword has no effect on the output.

        Note

        Using SHOW commands without an `IN` clause in a database context can result in fewer than expected results.

        Objects with the same name are only displayed once if no `IN` clause is used. For example, if you have table `t1` in
        `schema1` and table `t1` in `schema2`, and they are both in scope of the database context you’ve specified (that is, the database
        you’ve selected is the parent of `schema1` and `schema2`), then SHOW TABLES only displays one of the `t1` tables.

    `SCHEMA`, `SCHEMA schema_name`
    :   Returns records for the current schema in use or a specified schema (`schema_name`).

        `SCHEMA` is optional if a database is in use or if you specify the fully qualified `schema_name` (for example, `db.schema`).

        If no database is in use, specifying `SCHEMA` has no effect on the output.

    If you omit `IN ...`, the scope of the command depends on whether the session currently has a database in use:

    - If a database is currently in use, the command returns the objects you have privileges to view in the database. This has the
      same effect as specifying `IN DATABASE`.
    - If no database is currently in use, the command returns the objects you have privileges to view in your account. This has the
      same effect as specifying `IN ACCOUNT`.

`IN GATEWAY gateway_name`
:   Lists gateway model monitors associated with the specified Snowflake Gateway. The output columns match those returned by `SHOW MODEL MONITORS` in a schema, but the result includes only monitors of type `GATEWAY_MODEL_MONITOR` for that gateway.

## Output

The command output provides model monitor properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `created_on` | Date and time when the model monitor was created. |
| `name` | Name of the model monitor. |
| `database_name` | Database in which the model monitor is stored. |
| `schema_name` | Schema in which the model monitor is stored. |
| `warehouse_name` | Warehouse used to monitor the model. |
| `refresh_interval` | The refresh interval (target lag) for triggering refresh of the model monitor. |
| `aggregation_window` | The aggregation window for calculating metrics. |
| `model_task` | The task of the model being monitored: `TABULAR_BINARY_CLASSIFICATION`, `TABULAR_REGRESSION`, or `TABULAR_MULTI_CLASSIFICATION`. |
| `type` | The type of monitor, either `MODEL_VERSION_MONITOR` or `GATEWAY_MODEL_MONITOR`. |
| `gateway` | String representation of a JSON object containing information about the Snowflake Gateway associated with gateway model monitors. For model version monitors, the value is empty. See [Gateway JSON object specification](#gateway-json-object-specification). |
| `ground_truth` | String representation of a JSON object detailing the ground truth table for gateway model monitors, if one was specified at creation. Empty otherwise. See [Table JSON object specification](#table-json-object-specification). |
| `monitor_state` | The state of the model monitor:   - ACTIVE: The model monitor is active and operating correctly. - SUSPENDED: Model monitoring is paused. - PARTIALLY\_SUSPENDED: An error condition in which one of the underlying tables has stopped refreshing at the expected interval. See DESCRIBE for more details. - UNKNOWN: An error condition in which the state of the underlying tables cannot be identified. |
| `source` | String representation of a JSON object detailing the source table or view on which aggregations are based for model version monitors. For gateway model monitors, the value is empty. If the table does not exist or is not accessible, the value is an empty string. See [Table JSON object specification](#table-json-object-specification). |
| `baseline` | String representation of a JSON object detailing baseline table being used for monitoring, of which a clone is embedded in the model version monitor object. For gateway model monitors, the value is empty. See [Table JSON object specification](#table-json-object-specification). |
| `model` | String representation of a JSON object containing information specifically about the model being monitored. See [Model JSON object specification](#model-json-object-specification). |
| `comment` | Comment about the model monitor. |

Expand

Show lessSee more

### Table JSON object specification

The following is the format of the JSON representation of a table, as used by the `source`, `baseline`, and `ground_truth` columns in the command output:

| `name` | Name of the source, baseline, or ground truth table or view. |
| --- | --- |
| `database_name` | Database in which the table or view is stored. |
| `schema_name` | Schema in which the table or view is stored. |
| `status` | The status of the table:   - ACTIVE: The table or view is accessible by the user. - MASKED: The current user does not have access to the table or view. Values of other fields appear masked (that is, as a series of asterisks). - DELETED: The table or view has been deleted. - NOT\_SET: The status has not been set. |

Expand

Show lessSee more

### Gateway JSON object specification

The following is the format of the JSON representation of a gateway, as used by the `gateway` column in the command output:

| Field | Description |
| --- | --- |
| `name` | Name of the gateway being monitored by a gateway model monitor. |
| `database_name` | Database in which the gateway is stored. |
| `schema_name` | Schema in which the gateway is stored. |
| `status` | The status of the gateway. Can be `ACTIVE`, `MASKED`, or `DELETED`. `MASKED` indicates that the user does not have access to the gateway; other fields show as a series of asterisks. |

Expand

Show lessSee more

### Model JSON object specification

The following is the format of the JSON representation of a model, as used by the `model` column in the command output:

| Field | Description |
| --- | --- |
| `model_name` | Name of the model being monitored. |
| `version_name` | The name of the model version being monitored. Empty for gateway model monitors because gateway monitors track the model, not a specific version. |
| `function_name` | Name of the specific function being monitored. |
| `database_name` | Database in which the model is stored. |
| `schema_name` | Schema in which the model is stored. |
| `model_status` | The status of the model. Can be ACTIVE, MASKED, or DELETED. MASKED indicates that the user does not have access to the model; other fields show as a series of asterisks. |
| `version_status` | The status of the model version being monitored. Can be ACTIVE or DELETED (MASKED is not a valid status for a model version, because they do not have access control). Empty for gateway model monitors. |

Expand

Show lessSee more

## Access control requirements

| Privilege | Target | Notes |
| --- | --- | --- |
| Any | Model monitor | For `SHOW MODEL MONITORS` in a schema, database, or account |
| USAGE | Gateway | For `SHOW MODEL MONITORS IN GATEWAY` |

Expand

Show lessSee more

## Usage notes

- The command doesn’t require a running warehouse to execute.
- The command only returns objects for which the current user’s current role has been granted at least one access privilege.
- The MANAGE GRANTS access privilege implicitly allows its holder to see every object in the account. By default, only the account
  administrator (users with the ACCOUNTADMIN role) and security administrator (users with the SECURITYADMIN role) have the
  MANAGE GRANTS privilege.

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.
