# DESCRIBE APPLICATION

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

Displays information about a Snowflake Native App.

DESCRIBE can be abbreviated to DESC.

See also:
:   [ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package), [CREATE APPLICATION PACKAGE](/sql-reference/sql/create-application-package), [DROP APPLICATION PACKAGE](/sql-reference/sql/drop-application-package),
    [SHOW APPLICATION PACKAGES](/sql-reference/sql/show-application-packages),

## Syntax

Copy code

```
DESC[RIBE] APPLICATION <name>
```

## Parameters

`name`
:   Specifies the [identifier](/sql-reference/identifiers) of the app to
    describe.

## Output

The command displays properties of an app in the following columns:

| Column | Description |
| --- | --- |
| `property` | The name of the property of the app. This column can include the properties listed in the following table. |
| `value` | The value assigned to the property of the app. |

Expand

Show lessSee more

The `property` column can include the following properties of an app:

| Property | Description |
| --- | --- |
| `name` | The name of the app. |
| `source_organization` | The name of the organization of the account containing the application package used to create the app. |
| `source_account` | The account of the application package used to create the app. |
| `source_type` | The source used to create the app. Valid values are `APP_PACKAGE` and `LISTING`. |
| `source` | The name of the application package or listing used to create the app. |
| `version` | The version identifier of the app. |
| `version_label` | The version label of the app. This label is visible to consumer when they install a Snowflake Native App. |
| `patch` | The patch number of the app. |
| `created_on` | The timestamp when the app was created. |
| `last_upgraded_on` | The timestamp of the last upgrade of the app. |
| `restricted_callers_rights` | Indicates that restricted caller’s rights have been enabled for the app. See [Grant restricted caller’s rights to an executable in an app](/developer-guide/native-apps/ui-consumer-restricted-callers-rights) for more information. |
| `share_events_with_provider` | Indicates whether [logging and event sharing](/developer-guide/native-apps/event-about) is enabled for the app. |
| `authorize_telemetry_event_sharing` | The status of the `AUTHORIZE_TELEMETRY_EVENT_SHARING` flag. |
| `log_level` | The log level defined by the provider in the manifest file. |
| `log_event_level` | The log event level defined by the provider in the manifest file. |
| `trace_level` | The trace level defined by the provider in the manifest file. |
| `metric_level` | The metric level defined by the provider in the manifest file. |
| `auditlog_level` | The audit log level defined by the provider in the manifest file. |
| `effective_log_level` | The log level enabled for the app. |
| `effective_log_event_level` | The log event level enabled for the app. |
| `effective_trace_level` | The current trace level configured for the app. |
| `effective_metric_level` | The current metric level configured for the app. |
| `effective_auditlog_level` | The current audit log level configured for the app. |
| `debug_mode` | Indicates whether the app was created using debug mode. |
| `disable_application_redaction` | Indicates if redaction of provider data has been disabled. |
| `upgrade_state` | The current state of the background installation or upgrade of the app. Valid values are:  - `INSTALLING`: The application object is in the process of being created. - `INSTALL_FAILED`: The creation of the application object failed. The application object   remains in the `INSTALL_FAILED` state until it is dropped. See the `UPGRADE_FAILURE_REASON`   column of the [DESCRIBE APPLICATION](/sql-reference/sql/desc-application) command for information about why the   installation or upgrade failed. - `COMPLETE`: The setup script successfully completed and the application object was created   or upgraded. - `QUEUED`: The application object is queued for upgrade. - `UPGRADING`: The application object is in the process of being upgraded. - `FAILED`: All upgrade attempts failed. The reason for the failure is listed in the   `UPGRADE_FAILURE_REASON` column, if present. The instance remains in the `FAILED` state until   a release directive is updated to point to a different version than the one that the upgrade was   targeting, as defined in the `TARGET_UPGRADE_VERSION` column. - `QUEUED_DELAYED`: The application object is queued for an upgrade that is scheduled for a future time. - `QUEUED_RETRY`: The instance failed one or more upgrade attempts. The reason for the failure   is indicated in `UPGRADE_FAILURE_REASON`: The instance is queued to perform another upgrade attempt. - `DISABLED`: The application object and its upgrades were disabled. In this state the instance will be   inaccessible for consumers, it will not be considered for upgrades and will not block application package   version drop. The reason for the failure is listed in the `UPGRADE_FAILURE_REASON` column, if present. |
| `upgrade_target_version` | The version identifier to which the app is being upgraded. |
| `upgrade_target_patch` | The patch to which the app is being upgraded. |
| `upgrade_attempt` | Indicates whether an upgrade was attempted for the app. |
| `upgrade_task_id` | The internal task identifier for the upgrade attempt. |
| `upgrade_started_on` | The timestamp when the upgrade was initiated. |
| `upgrade_attempted_on` | The timestamp for the last app installation or retry attempt. |
| `upgrade_failure_type` | The reason for an upgrade failure. Possible values are:   - `VERSION_SETUP`: indicates that an error occurred when running the setup script   for the app. This can occur if the setup script contains a syntax error, is empty, etc.   When this error occurs, an email notification is sent to the provider. - `INTERNAL`: indicates an internal Snowflake error, for example, if a required   object does not respond or cannot be found. |
| `upgrade_failure_reason` | The reason the upgrade failed, if applicable. |
| `upgrade_after` | Indicates that the provider has scheduled an upgrade to begin at this time. However, the app may be upgraded before this date and time. For more information, see . |
| `upgrade_in_maintenance_window` | If `TRUE` indicates that the provider has scheduled the app to be upgraded during a Snowpark Container Services maintenance window.  This feature is currently in Preview. |
| `previous_version` | The identifier of the previous version of the app. |
| `previous_patch` | The number of the previous patch of the installed app. |
| `previous_version_state` | The state of the previous version of the app. |
| `comment` | Text that provides information about the app. |
| `disablement_reasons` | An array containing the reasons why the app was disabled. For more information, see [Reasons an app can become disabled](/sql-reference/data-sharing-usage/application-state-view#label-app-state-view-disablement-reasons). |
| `release_channel_name` | The type of release channel. Valid values are `QA`, `ALPHA`, `DEFAULT`. For more information, see [Publish an app using release channels](/developer-guide/native-apps/release-channels). |
| `authorize_restricted_provider_remote_operations_until` | The timestamp until which the consumer has authorized the provider to perform [restricted remote app operations](/developer-guide/native-apps/ui-consumer-remote-app-operation). If authorized indefinitely, the value is `INDEFINITE`. If consent has not been granted, the value is `NEVER`. |

Expand

Show lessSee more

## Usage notes

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

## Examples

Describe the properties of an app:

Copy code

```
DESC APPLICATION hello_snowflake_app;
```

```
+------------------------------------+-------------------------------+
| property                           | value                         |
|------------------------------------+-------------------------------|
| name                               | hello_snowflake_app           |
| source_organization                | my_organization               |
| source_account                     | provider_account              |
| source_type                        | APPLICATION PACKAGE           |
| source                             | hello_snowflake_package       |
| version                            | v1_0                          |
| version_label                      | NULL                          |
| patch                              | 0                             |
| created_on                         | 2024-05-25 08:30:41.520 -0700 |
| last_upgraded_on                   |                               |
| share_events_with_provider         | FALSE                         |
| authorize_telemetry_event_sharing  | FALSE                         |
| log_level                          | OFF                           |
| log_event_level                    | OFF                           |
| trace_level                        | OFF                           |
| debug_mode                         | FALSE                         |
| upgrade_state                      | COMPLETE                      |
| upgrade_target_version             | NULL                          |
| upgrade_target_patch               | 0                             |
| upgrade_attempt                    | NULL                          |
| upgrade_task_id                    | NULL                          |
| upgrade_started_on                 |                               |
| upgrade_attempted_on               |                               |
| upgrade_failure_type               | NULL                          |
| upgrade_failure_reason             | NULL                          |
| previous_version                   | NULL                          |
| previous_patch                     | 0                             |
| previous_version_state             | COMPLETE                      |
| comment                            |                               |
+------------------------------------+-------------------------------+
```
