# Setting levels for logging, metrics, and tracing

You can set the threshold levels for log messages, log events, trace data, or metrics data captured in an event table.

Each kind of telemetry data supports its own set of levels that are specific to its purpose. You can set these levels by using the
[parameter](/sql-reference/parameters) Snowflake provides for each. You can also set some levels using Snowsight, which
represents the level parameters in a simplified way.

For each kind of telemetry data, you can do the following:

- Set levels specific to that kind of data.
- Set system-wide levels that are in effect unless overridden.
- Override system-wide levels by setting the level for a session or on specific objects (such as procedures and UDFs).

  Levels are represented as both [session parameters](/sql-reference/parameters#label-session-parameters) and [object parameters](/sql-reference/parameters#label-object-parameters).

Note

You can use handler code to override the log level you set with SQL (as described in this topic) when your handler is written in Python.
For more information, see [Overriding log threshold levels with Python](/developer-guide/logging-tracing/logging-python#label-logging-messages-python-overriding-levels).

## Scope

For each type of telemetry data, you can set levels so that they’re in effect at the scope that best suits your requirements. In many
cases, you can override levels set at a larger scope by setting them at a smaller scope, as described in [How Snowflake determines the level in effect](#label-telemetry-level-effective).
For example, you might want to have a set of default levels at the account scope and then set different levels for objects in a particular
database.

You can set each of these in the following scopes:

Account:
:   A level set for the account is in effect everywhere in the account except where overridden by being set at the object or session level.

Object:
:   You can set the telemetry levels on the following kinds of objects:

    - Database or schema containing procedures and functions
    - Stored procedure
    - User-defined function (UDF) or a user-defined table function (UDTF)
    - Externally managed Apache Iceberg™ table with automated refresh configured

    For example, to set the log level for log messages from logging APIs for a specific UDF, use [ALTER FUNCTION](/sql-reference/sql/alter-function) to set
    the LOG\_LEVEL parameter for that UDF. As another example, to set the default log level for all functions and procedures in a database, use
    [ALTER DATABASE](/sql-reference/sql/alter-database) to set the LOG\_LEVEL parameter on that database. As another example, to set the log event level for a
    specific externally managed Iceberg table with automated refresh configured, use [ALTER ICEBERG TABLE](/sql-reference/sql/alter-iceberg-table) to set the
    LOG\_EVENT\_LEVEL parameter on that table. Use [ALTER <object>](/sql-reference/sql/alter) commands to set the LOG\_EVENT\_LEVEL parameter for other
    objects that emit log events (record type EVENT).

    Note

    You can’t set the level on Streamlit objects. Instead, set the level on the database or schema that contains the object.

Session:
:   You can set the telemetry level for calls to functions and procedures made in the current session.

## Levels

You can set the following levels for each kind of telemetry data:

Log messages:
:   When you set a level, only log messages from logging APIs at that level and more severe levels are captured in an event table and visible in
    Snowsight. For example, setting the LOG\_LEVEL parameter to WARN means that log messages at the WARN, ERROR, and FATAL levels are
    captured in the event table.

    Set the [LOG\_LEVEL](/sql-reference/parameters#label-log-level) parameter.

Log events:
:   When you set a level, only log events (record type EVENT) at that level and more severe levels are captured in an event table. Examples
    include events from Snowpipe, tasks, dynamic tables, Snowpark Container Services compute pools, Iceberg tables, and data governance tag
    activity.

    Set the [LOG\_EVENT\_LEVEL](/sql-reference/parameters#label-log-event-level) parameter.

Metrics:
:   You can currently have all metrics data captured or none.

    Set the [METRIC\_LEVEL](/sql-reference/parameters#label-metric-level) parameter.

Tracing:
:   You can specify the following characteristics:

    - Scope of trace event data stored in the event table

      Set the [TRACE\_LEVEL](/sql-reference/parameters#label-trace-level) parameter.
    - Whether to capture SQL text in a traced SQL statement

      This is determined by the [SQL\_TRACE\_QUERY\_TEXT](/sql-reference/parameters#label-sql-trace-query-text) parameter. For more information, see [SQL statement tracing](/developer-guide/logging-tracing/tracing#label-tracing-sql).

## Privileges needed

To set levels on an object, you must use a role that is granted or inherits the privileges described in this section.

For example, the code in the following example grants privileges needed for someone using the `central_log_admin` role to set the
log level for the account:

Copy code

```
GRANT MODIFY LOG LEVEL ON ACCOUNT TO ROLE central_log_admin;
```

For more information about privileges, see [Access control privileges](/user-guide/security-access-control-privileges).

| Level to modify | Parameter to set | Privileges needed |
| --- | --- | --- |
| Log level (log messages) | [LOG\_LEVEL](/sql-reference/parameters#label-log-level) | **Account**   - MODIFY LOG LEVEL on the account   **Object**   - MODIFY LOG LEVEL on the account - MODIFY on the object for which you want to set the level - USAGE on the database or schema containing the procedure or UDF for which you want to set the level   **Session**   - MODIFY SESSION LOG LEVEL |
| Log event level | [LOG\_EVENT\_LEVEL](/sql-reference/parameters#label-log-event-level) | **Account**   - MODIFY LOG EVENT LEVEL on the account   **Object**   - MODIFY LOG EVENT LEVEL on the account - MODIFY on the object for which you want to set the level - USAGE on the database or schema containing the object for which you want to set the level   **Session**   - MODIFY SESSION LOG EVENT LEVEL |
| Metric level | [METRIC\_LEVEL](/sql-reference/parameters#label-metric-level) | **Account**   - MODIFY METRIC LEVEL on the account   **Object**   - MODIFY METRIC LEVEL on the account - MODIFY on the object for which you want to set the level - USAGE on the database or schema containing the procedure or UDF for which you want to set the level   **Session**   - MODIFY SESSION METRIC LEVEL |
| Trace level | [TRACE\_LEVEL](/sql-reference/parameters#label-trace-level) | **Account**   - MODIFY TRACE LEVEL on the account   **Object**   - MODIFY TRACE LEVEL on the account - MODIFY on the object for which you want to set the level - USAGE on the database or schema containing the procedure or UDF for which you want to set the level   **Session**   - MODIFY SESSION TRACE LEVEL |
| SQL text in SQL tracing | [SQL\_TRACE\_QUERY\_TEXT](/sql-reference/parameters#label-sql-trace-query-text) | **Account**   - SQL\_TRACE\_QUERY\_TEXT on the account |

Expand

Show lessSee more

## Setting telemetry levels

You can set telemetry levels using either SQL or, in some cases, Snowsight. In many cases, you can override levels set at a
larger scope by setting them at a smaller scope, as described in [How Snowflake determines the level in effect](#label-telemetry-level-effective).

Before you set levels, verify that you have access to [a role with the privileges](#label-telemetry-level-privileges) needed.

SnowsightSQL

You can use Snowsight to set telemetry levels at the account level.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Monitoring** » **Traces & logs**.
3. On the **Traces & Logs** page, select **Set Event Level**.
4. For **Set logging & tracing for**, select the scope you want from one of the following:

   - **Account**
   - The database and, optionally, the schema
5. Select levels for the telemetry data you want to adjust.

   |  |  |
   | --- | --- |
   | **All Events** | **On** to turn on collection for all kinds of telemetry data; **Off** to turn off collection for all kinds of data. |
   | **Traces** | **On** to set trace data collection to `ALWAYS`; **Off** to set trace data collection to `OFF`. For information about levels, see [TRACE\_LEVEL](/sql-reference/parameters#label-trace-level). |
   | **Logs** | **On** to set log data collection to `INFO`. For information about levels, see [LOG\_LEVEL](/sql-reference/parameters#label-log-level). |
   | **Metrics** | **On** to set trace data collection to `ALL`; **Off** to set trace data collection to `NONE`. For information about levels, see [METRIC\_LEVEL](/sql-reference/parameters#label-metric-level). |

   Expand

   Show lessSee more

You can use SQL to set telemetry levels for the account and for objects such as databases, functions, procedures, and externally managed
Iceberg tables with automated refresh configured.

AccountObjectSession

Use the [ALTER ACCOUNT](/sql-reference/sql/alter-account) command to set the appropriate parameter, based on the telemetry data you want to collect.

The following example sets the log level to ERROR for the account:

Copy code

```
-- Set the log level on the account
ALTER ACCOUNT SET LOG_LEVEL = ERROR;
```

To set the LOG\_LEVEL parameter on the object, use the [ALTER <object>](/sql-reference/sql/alter) command.

The following example sets the log level to ERROR for all functions and procedures in the database `db`. The example
overrides this level to WARN for the UDF `f1(int)`.

Copy code

```
USE ROLE central_log_admin;

-- Set the log levels on a database and UDF.
ALTER DATABASE db1 SET LOG_LEVEL = ERROR;
ALTER FUNCTION f1(int) SET LOG_LEVEL = WARN;

-- Set the log levels on a Snowpark Container Services service.
ALTER SERVICE test_service SET LOG_LEVEL = ERROR;
```

For details on how Snowflake determines the effective log level when the LOG LEVEL is set on different objects, see
[How Snowflake determines the level in effect](#label-telemetry-level-effective).

To set the LOG\_LEVEL parameter for the current session, use the [ALTER SESSION](/sql-reference/sql/alter-session) command.

Copy code

```
USE ROLE developer_debugging;

-- Set the logging level to DEBUG for the current session.
ALTER SESSION SET LOG_LEVEL = DEBUG;
```

If the level parameter is set to different levels for the current session and on the functions and procedures called in that
session, Snowflake determines the effective level to use. See [How Snowflake determines the level in effect](#label-telemetry-level-effective).

## How Snowflake determines the level in effect

You can override the telemetry [level-related parameters](#label-telemetry-levels) (for both [objects](/sql-reference/parameters#label-object-parameters)
and [sessions](/sql-reference/parameters#label-session-parameters)) by using a [hierarchy of levels](/sql-reference/parameters#label-parameter-hierarchy-and-types).

For example, you can set a level to one value for the account, then override it by setting the level for an object, which is lower in the
hierarchy.

The following describes the hierarchy for session and object level parameters.

- For session parameters, the hierarchy is Account » User » Session.

  This means that you can set the parameter for an account, override the account-level parameter for a user, and override the
  user-level parameter for the current session.
- For object parameters, the hierarchy is Account » Database » Schema » Object.

  This means that you can set the parameter for an account, override the account-level parameter for a database or schema, and
  override the database- or schema-level parameter for specific stored procedures and UDFs in that database or schema.

For example, the LOG\_LEVEL for log messages for a function overrides the LOG\_LEVEL for the account that contains the function. If the
LOG\_LEVEL for the account is FATAL and the LOG\_LEVEL for the Java UDF in the account is INFO, the effective LOG\_LEVEL is INFO (the level for
the function, not the account):

Copy code

```
ALTER ACCOUNT SET LOG_LEVEL = FATAL;

ALTER FUNCTION MyJavaUDF SET LOG_LEVEL = INFO;

-- The INFO log level is used because the FUNCTION MYJAVAUDF
-- is lower than the ACCOUNT in the hierarchy.
```

In cases where the level is set in both the session and object parameter hierarchies, the most verbose level is used.

- For LOG\_LEVEL (log messages from logging APIs), the following table lists examples of how parameters set on the session and object affect
  the log level used.

  | Value for the Session | Value for the Object, Schema, Database, or Account | LOG\_LEVEL Used |
  | --- | --- | --- |
  | (unset) | `WARN` | `WARN` |
  | `DEBUG` | (unset) | `DEBUG` |
  | `WARN` | `ERROR` | `WARN` |
  | `INFO` | `DEBUG` | `DEBUG` |
  | (unset) | (unset) | `OFF` |

  Expand

  Show lessSee more

  The same precedence rules apply to LOG\_EVENT\_LEVEL for log events (record type EVENT).
- For metric level — `ALL` overrides `NONE`.
- For trace level — `ALWAYS` overrides `ON_EVENT` and `OFF`; `ON_EVENT` overrides `OFF`.
