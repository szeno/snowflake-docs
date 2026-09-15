Categories:
:   [Table functions](/sql-reference/functions-table) (Snowpark Container Services)

# <service\_name>!SPCS\_GET\_METRICS

Returns the metrics that Snowflake collected for the specified service. For more information, see [Access platform metrics](/developer-guide/snowpark-container-services/monitoring-services#label-monitoring-services-platform-metrics).

See also:
:   [Monitoring Services](/developer-guide/snowpark-container-services/monitoring-services)

## Syntax

Copy code

```
<service_name>!SPCS_GET_METRICS(
    [ START_TIME => <constant_expr> ],
    [ END_TIME => <constant_expr> ] )
```

## Arguments

`START_TIME => constant_expr`
:   Start time (in TIMESTAMP\_LTZ format) for the time range from which to retrieve metrics. For available functions to construct data, time, and timestamp data, see [Date & time functions](/sql-reference/functions-date-time).

    If the `START_TIME` isn’t specified, it defaults to one day ago.

`END_TIME => constant_expr`
:   End time (in TIMESTAMP\_LTZ format) for the time range from which to retrieve metrics.

    If END\_TIME isn’t specified, it defaults to the current timestamp.

## Output

The function returns the following columns:

| Column | Data Type | Description |
| --- | --- | --- |
| `TIMESTAMP` | TIMESTAMP\_NTZ | Universal Coordinated Time (UTC) timestamp when Snowflake collected the metric. |
| `METRIC_NAME` | VARCHAR | Name of the metric. |
| `VALUE` | VARCHAR | Value of the metric. |
| `UNIT` | VARCHAR | Unit of the metric returned. |
| `INSTANCE_ID` | NUMBER | Name of the service instance if the metric is related to the service instance. |
| `CONTAINER_NAME` | VARCHAR | Name of the container if the metric is related to the container. For example, a volume metric won’t have container name. |
| `RESOURCE` | VARCHAR | Hardware — for example, GPU — the metrics is about. This column isn’t populated. |
| `RECORD` | OBJECT | Key-value pairs that provide metric information. |
| `RECORD_ATTRIBUTES` | OBJECT | Key-value pairs that provide additional information about the metric. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| MONITOR | Service |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- It can take a few minutes before metrics appear in the output.

## Examples

Retrieve the metrics that Snowflake collected for the `my_test_job` job over the past day, the default.

Copy code

```
SELECT * FROM TABLE(mydb.myschema.my_test_job!SPCS_GET_METRICS());
```

Retrieve the metrics that Snowflake collected for the `my_test_job` job over the past three days.

Copy code

```
SELECT * from TABLE(mydb.myschema.my_test_job!SPCS_GET_METRICS(start_time => DATEADD('day', -3, CURRENT_TIMESTAMP())));
```

Retrieve metrics from the past day for the `spcs_get_metrics` job instance `0` in the container named `main`.

Copy code

```
SELECT * FROM TABLE(mydb.myschema.my_test_job!SPCS_GET_METRICS())
 WHERE instance_id = 0 AND container_name = 'main';
```
