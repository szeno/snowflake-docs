Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# NOTIFICATION\_HISTORY

This table function can be used to query the history of notifications sent through Snowflake. These notifications include:

- [Notifications about errors in tasks](/user-guide/tasks-errors).
- [Notifications about errors in Snowpipe](/user-guide/data-load-snowpipe-errors).
- [Notifications sent by calling SYSTEM$SEND\_EMAIL or SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION](/user-guide/notifications/about-notifications).

The rows returned represent:

- Requests that are being processed.
- Failed attempts at sending notifications.
- Notifications that were sent successfully.

The [STATUS column](#label-notification-history-output) indicates what each row represents. See
[Examples of output from the function](#label-notification-history-example-output).

## Syntax

Copy code

```
NOTIFICATION_HISTORY(
  [ START_TIME => <constant_expr> ]
  [, END_TIME => <constant_expr> ]
  [, INTEGRATION_NAME => '<string>' ]
  [, RESULT_LIMIT => <integer> ] )
```

## Arguments

All the arguments are optional.

`START_TIME=> constant_expr` , `END_TIME=> constant_expr`
:   Time range (in TIMESTAMP\_LTZ format) when the notification is sent out.

    - If START\_TIME is not specified, the range starts 24 hours prior to the END\_TIME.
    - If END\_TIME is not specified, the default is [CURRENT\_TIMESTAMP](/sql-reference/functions/current_timestamp).

    The maximum time range is 14 days.

`INTEGRATION_NAME => 'string'`
:   The fully qualified name of the integration that is tied with the notification. If you omit this argument, the function returns
    all notifications.

    Default: An empty string.

`RESULT_LIMIT => integer`
:   A number specifying the maximum number of rows returned by the function.

    Range: `1` to `10000`

    Default: `100`

## Output

The function returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| CREATED | TIMESTAMP\_LTZ | Timestamp when the notification was created. |
| PROCESSED | TIMESTAMP\_LTZ | Timestamp of the last attempt to send the notification. |
| MESSAGE\_SOURCE | VARCHAR | Type of object or feature that generated the notification. Valid values include:   - `BUDGET` (for [notifications from budgets](/user-guide/budgets#label-budgets-notifications)) - `TASK` (for [notifications from tasks](/user-guide/tasks-errors)) - `SNOWPIPE` (for [notifications from Snowpipe](/user-guide/data-load-snowpipe-errors)) - `STORED_PROCEDURE` (for email notifications sent by   [calling the SYSTEM$SEND\_EMAIL or SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION stored procedure](/user-guide/notifications/about-notifications)) |
| INTEGRATION\_NAME | VARCHAR | Name of the [integration used for this notification](/sql-reference/sql/create-notification-integration). |
| STATUS | VARCHAR | Status of the notification. Valid values are:   - `QUEUED`: The request to send the notification is being processed. - `SUCCESS`: The notification was sent successfully. - `RETRIABLE_FAILURE`: The attempt to send the notification failed, and the system will attempt to send the   notification again. - `FAILURE`: Multiple attempts to send the notification failed, and there will be no more attempts to send the   notification. |
| ERROR\_MESSAGE | VARCHAR | If the notification failed, provides details about why the notification failed.  Note  For webhook notifications, this column contains the body of the HTTP response, which might contain sensitive data. Before using this data, make sure to sanitize it. |
| ID | VARCHAR | Unique ID of a request to send a notification.  If Snowflake fails to send a notification and attempts to send the notification again, the function returns a row for each attempt. Each row for an attempt has the same value in the ID column but a different value in the ATTEMPT column. |
| ATTEMPT | INTEGER | Number of the attempt made to send the notification. |
| MESSAGE\_SOURCE\_INFO | OBJECT | Object containing information about the source of the notification. The fields in this object depend on the type of the source.   - For notifications for budgets, the object contains the following fields:    - `budget_id`: Identifier for the budget.   - `budget_name`: The name of the budget. - For error notifications for tasks, the object contains the following fields:    - `name`: The name of the task   - `graph_run_group_id`: Identifier for the graph run.   - `attempt_number`: Integer representing the number of the attempt to run this task. - For error notifications for Snowpipe, the object contains the `pipe_name` field, which specifies the name of the pipe. - For notifications sent by calling the SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION or SYSTEM$SEND\_EMAIL stored procedure, the   object contains the `query_id` field, which specifies the ID of the statement that called the stored procedure. |

Expand

Show lessSee more

## Usage notes

- Returns results only for the ACCOUNTADMIN role, the integration owner (i.e. the role with the OWNERSHIP privilege on the
  integration) or a role with the USAGE privilege on the integration.
- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema in use or the
  function name must be fully-qualified. For more details, see [Snowflake Information Schema](/sql-reference/info-schema).

## Examples

The following sections contain examples of calling the function and examples of output from the function:

- [Examples of calling the function](#label-notification-history-example-calling)
- [Examples of output from the function](#label-notification-history-example-output)

### Examples of calling the function

The following examples demonstrate how to call this function:

- [Retrieving the most recent notifications](#label-notification-history-example-most-recent)
- [Retrieving notifications by time and integration name](#label-notification-history-example-most-recent-by-name)

#### Retrieving the most recent notifications

Retrieve the most recent notifications that were created in the past 24 hours.

Copy code

```
SELECT * FROM TABLE(INFORMATION_SCHEMA.NOTIFICATION_HISTORY());
```

#### Retrieving notifications by time and integration name

Retrieve the most recent notifications that were created in the past hour and sent using the integration named `my_integration`.

Copy code

```
SELECT * FROM TABLE(INFORMATION_SCHEMA.NOTIFICATION_HISTORY(
  START_TIME=>DATEADD('hour',-1,CURRENT_TIMESTAMP()),
  END_TIME=>CURRENT_TIMESTAMP(),
  RESULT_LIMIT=>100,
  INTEGRATION_NAME=>'my_integration'));
```

### Examples of output from the function

The following examples explain the output returned by this function for notification requests in different states:

- [Example of the output when two attempts fail and a third attempt is in progress](#label-notification-history-example-output-failing-pending)
- [Example of the output when two attempts fail and a third attempt succeeds](#label-notification-history-example-output-succeeded)

#### Example of the output when two attempts fail and a third attempt is in progress

This example selects a subset of the columns in the output:

Copy code

```
SELECT id, attempt, created, processed, status
  FROM TABLE(INFORMATION_SCHEMA.NOTIFICATION_HISTORY());
```

The output includes the rows that represent the attempts to send one notification. In the output:

- The ID column identifies the notification that is being sent.
- The first two attempts to send the notification have failed, but the system can attempt to send the notification again (as
  indicated by the value `RETRIABLE_FAILURE` in the STATUS column).
- A third attempt is being processed, as indicated by the value `QUEUED` in the STATUS column.

```
+-------------------+-------------+-----------------------------------+-----------------------------------+-----------------------+
|   ID              |   ATTEMPT   |   CREATED                         |   PROCESSED                       |   STATUS              |
+-------------------+-------------+-----------------------------------+-----------------------------------+-----------------------+
|   10ae695e-93c3   |   3         |   2023-12-05 15:10:15.194 -0800   |   NULL                            |   QUEUED              |
|   10ae695e-93c3   |   2         |   2023-12-05 15:10:15.194 -0800   |   2023-12-05 15:11:21.443 -0800   |   RETRIABLE_FAILURE   |
|   10ae695e-93c3   |   1         |   2023-12-05 15:10:15.194 -0800   |   2023-12-05 15:10:21.443 -0800   |   RETRIABLE_FAILURE   |
+-------------------+-------------+-----------------------------------+-----------------------------------+-----------------------+
```

#### Example of the output when two attempts fail and a third attempt succeeds

This example selects a subset of the columns in the output:

Copy code

```
SELECT id, attempt, created, processed, status
  FROM TABLE(INFORMATION_SCHEMA.NOTIFICATION_HISTORY());
```

The output includes the rows that represent the attempts to send one notification. In the output:

- The ID column identifies the notification that is being sent.
- The first two attempts to send the notification have failed, but the system can attempt to send the notification again (as
  indicated by the value `RETRIABLE_FAILURE` in the STATUS column).
- A third attempt succeeded, as indicated by the value `SUCCESS` in the STATUS column.

```
+-------------------+-------------+-----------------------------------+-----------------------------------+-----------------------+
|   ID              |   ATTEMPT   |   CREATED                         |   PROCESSED                       |   STATUS              |
+-------------------+-------------+-----------------------------------+-----------------------------------+-----------------------+
|   10ae695e-93c3   |   3         |   2023-12-05 15:10:15.194 -0800   |   2023-12-05 15:12:21.443 -0800   |   SUCCESS             |
|   10ae695e-93c3   |   2         |   2023-12-05 15:10:15.194 -0800   |   2023-12-05 15:11:21.443 -0800   |   RETRIABLE_FAILURE   |
|   10ae695e-93c3   |   1         |   2023-12-05 15:10:15.194 -0800   |   2023-12-05 15:10:21.443 -0800   |   RETRIABLE_FAILURE   |
+-------------------+-------------+-----------------------------------+-----------------------------------+-----------------------+
```
