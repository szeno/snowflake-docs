# Monitor the data quality of a schema

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

When a data metric function (DMF) is associated with a table or view, the DMF runs at regular intervals and returns a value that provides
insights into data quality.

You can now use a single SQL statement to configure a schema so that all of the objects in the schema are associated with the same DMF. You
can associate the following system DMFs at the schema level:

- [ROW\_COUNT](/sql-reference/functions/dmf_row_count) — Use to return information about the volume of data in objects within the
  schema.
- [FRESHNESS](/sql-reference/functions/dmf_freshness) — Use to return information about the frequency with which objects in the
  schema are being updated.

When you associate one of these DMFs at the schema level, you can specify that you want Snowflake to determine whether
[anomalies](/user-guide/data-quality-anomaly) exist in the volume or freshness of a table or view over time.

The following example shows how to enable anomaly detection for the association between the ROW\_COUNT DMF and every object in the
`my_schema` schema:

Copy code

```
ALTER SCHEMA my_schema
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.ROW_COUNT ON ()
    ANOMALY_DETECTION = TRUE;
```

Snowflake trains the anomaly detection algorithm and then automatically starts identifying anomalies in the volume of tables and views in
the `my_schema` schema.

## Add a DMF to a schema

When you associate a DMF with a schema, all of the objects within the schema are associated with the DMF.

### Syntax

Use the following syntax to add a DMF to a schema.

Copy code

```
ALTER SCHEMA <name>
  ADD DATA METRIC FUNCTION { SNOWFLAKE.CORE.ROW_COUNT | SNOWFLAKE.CORE.FRESHNESS } ON ()
    [ ANOMALY_DETECTION = { TRUE | FALSE } ]
    [ EXCLUDE_TABLE_TYPES = ( '<object_type>' [ , '<object_type>' ... ] ) ]
```

#### Arguments

`{ SNOWFLAKE.CORE.ROW_COUNT | SNOWFLAKE.CORE.FRESHNESS } ON ()`
:   Associates the system DMF with objects within the schema.

    Possible values are [SNOWFLAKE.CORE.ROW\_COUNT](/sql-reference/functions/dmf_row_count) and
    [SNOWFLAKE.CORE.FRESHNESS](/sql-reference/functions/dmf_freshness).

`ANOMALY_DETECTION = { TRUE | FALSE }`
:   If TRUE, Snowflake uses an algorithm to detect anomalies in the values returned by the DMF. Snowflake detects anomalies in each object,
    not for the entire schema.

    Default: FALSE

`EXCLUDE_TABLE_TYPES = ( 'object_type', 'object_type' ... )`
:   Excludes all objects of the specified type; Snowflake doesn’t create associations between the DMF and those objects. The following are
    the possible values:

    - `'DYNAMIC_TABLE'`
    - `'EVENT_TABLE'`
    - `'EXTERNAL_TABLE'`
    - `'ICEBERG_TABLE'`
    - `'MATERIALIZED_VIEW'`
    - `'TABLE'`
    - `'VIEW'`

    To exclude a specific object, not all objects of a certain type, you can
    [override the DMF association at the object level](#label-dmf-bulk-override).

### Examples

Associate the FRESHNESS DMF with all objects in a schema:

Copy code

```
ALTER SCHEMA my_schema
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.FRESHNESS ON ();
```

Associate the ROW\_COUNT DMF with all objects in a schema and enable anomaly detection for those associations:

Copy code

```
ALTER SCHEMA my_schema
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.ROW_COUNT ON ()
    ANOMALY_DETECTION = TRUE;
```

Associate the ROW\_COUNT DMF with tables within a schema, but don’t associate it with views and materialized views:

Copy code

```
ALTER SCHEMA my_schema
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.ROW_COUNT ON ()
    EXCLUDE_TABLE_TYPES=('VIEW', 'MATERIALIZED_VIEW');
```

## Overriding settings at the object level

When you add a DMF at the schema level, Snowflake creates an object-level association between every object in the schema and the DMF. You
can override this association at the object level if you want to change how the DMF runs on the object.

Suppose that you enabled anomaly detection when you added the ROW\_COUNT DMF to `my_schema`. If you don’t want Snowflake to detect
anomalies in the table `my_schema.employees`, then run the following command:

Copy code

```
ALTER TABLE employees
  MODIFY DATA METRIC FUNCTION SNOWFLAKE.CORE.ROW_COUNT ON ()
    SET ANOMALY_DETECTION = FALSE;
```

You can also remove the association from a specific object if you want to stop running the DMF. For example, if you wanted to stop the
ROW\_COUNT DMF from running on the `my_schema.employees` table, run the following command:

Copy code

```
ALTER TABLE employees
  DROP DATA METRIC FUNCTION SNOWFLAKE.CORE.ROW_COUNT ON ();
```

You can also override the schema-level schedule to change how often a DMF runs for a particular object. For information about setting the
schedule at the object level, see [Adjust the schedule for DMFs](/user-guide/data-quality-working#label-data-quality-schedule).

## Adjusting the run schedule

By default, the data metric schedule for a schema is 60 minutes; the DMF runs on each object in the schema every hour. You can change this
default at the schema level or you can override it at the object level.

Use the following command to control how often DMFs run on objects in a schema:

Copy code

```
ALTER SCHEMA <name> SET DATA_METRIC_SCHEDULE = '<schedule>';
```

The possible values for `schedule` are the same at the schema level as they are at the object level. To view the possible values,
see [ALTER TABLE … SET DATA\_METRIC\_SCHEDULE](/sql-reference/sql/alter-table#label-alter-table-data-metric-function-action).

The schedule you set at the schema level controls how often the DMF runs on every object unless you override it for specific tables or
views. For information about setting the schedule at the object level, see [Adjust the schedule for DMFs](/user-guide/data-quality-working#label-data-quality-schedule).

## Suspending DMFs

The syntax for suspending and resuming a DMF associated at the schema level is the same as the syntax for table-level associations. For
example, to suspend the ROW\_COUNT DMF that is associated with schema `my_schema`, run the following command:

Copy code

```
ALTER SCHEMA my_schema
  MODIFY DATA METRIC FUNCTION SNOWFLAKE.CORE.ROW_COUNT ON ()
    SUSPEND;
```

## Determining which associations were set at the schema level

You can use the following view and function to determine which objects are associated with a DMF:

- [DATA\_QUALITY\_MONITORING\_RESULTS](/sql-reference/local/data_quality_monitoring_results) view in the ACCOUNT\_USAGE schema.
- [DATA\_QUALITY\_MONITORING\_RESULTS](/sql-reference/functions/data_quality_monitoring_results) table function.

The view and the output of the function contain a column `level`, which has the following possible values:

- `TABLE` — Someone associated the DMF with the object directly.
- `SCHEMA` — Someone added the DMF to the schema, which created the association between the object and the DMF.

## Tracking schema-level associations

You can call the [DATA\_METRIC\_FUNCTION\_REFERENCES](/sql-reference/functions/data_metric_function_references) function to determine which DMFs were added to a
schema. For example, to see which DMFs were added to the `db1.my_schema` schema, run the following command:

Copy code

```
SELECT *
  FROM TABLE(
    INFORMATION_SCHEMA.DATA_METRIC_FUNCTION_REFERENCES(
      REF_ENTITY_NAME => 'db1.my_schema',
      REF_ENTITY_DOMAIN => 'schema'
    )
  );
```

## Access control requirements

To add a DMF to a schema, you must have the following access control privileges and roles:

- OWNERSHIP on the schema.
- MANAGE DATA QUALITY on the account.
- EXECUTE DATA METRIC FUNCTION on the account.
- SNOWFLAKE.DATA\_METRIC\_USER database role.

Snowflake won’t run the DMF unless the schema owner continues to have the MANAGE DATA QUALITY privilege on the account.

To successfully run the DMF on an object in the schema, the object owner must have the same privileges that are needed to associate the DMF
with the object. For a list of these privileges, see [Access control requirements](/user-guide/data-quality-access-control#label-data-quality-access-control-common-tasks).

## Considerations and limitations

- The FRESHNESS DMF requires a column argument for views and external tables. As a result, if you add the FRESHNESS DMF to a schema,
  Snowflake skips views and external tables when associating the DMF with objects in the schema.
- You can’t set a trigger-based schedule at the schema level.
