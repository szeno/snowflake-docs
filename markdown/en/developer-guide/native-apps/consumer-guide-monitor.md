# Monitor and audit a Native App

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

## What visibility do you have?

At any point after installation, you can see exactly what the app has access to, what resources it
is consuming, and what callbacks it has executed. The primary visibility tools are:

- **[Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) app management UI:** the application page shows the app’s status,
  version, and a summary of its access.
- **`SHOW GRANTS`:** a SQL command for querying current privilege grants on the app object.
- **ACCOUNT\_USAGE views:** a set of views in the `SNOWFLAKE` database that give you a programmatic
  audit trail of the app’s access, activity, and usage. Several views specific to Native Apps are
  described in the sections below.
- **Query history:** queries executed by the app appear in your query history, subject to the
  redaction caveat described in
  .

## Checking current access grants

To see what privileges are currently granted to the app, run:

Copy code

```
SHOW GRANTS TO APPLICATION <app_name>;
```

This returns all current grants to the application object: the objects you have granted it access
to.

For a programmatic, historical view of grants, query ACCOUNT\_USAGE:

Copy code

```
SELECT *
FROM SNOWFLAKE.ACCOUNT_USAGE.GRANTS_TO_ROLES
WHERE GRANTEE_NAME = '<app_name>'
  AND GRANTED_TO = 'APPLICATION'
ORDER BY CREATED_ON DESC;
```

This query gives you a time-stamped record of what has been granted to the app, including grants
that have since been revoked (indicated by the `DELETED_ON` timestamp). It is the basis for any
access audit.

## Monitoring app activity and usage

### APPLICATION\_DAILY\_USAGE\_HISTORY

This view provides daily aggregates of the credits and storage consumed by the app. Use it to track
cost trends and catch unexpected spikes in consumption.

Copy code

```
SELECT *
FROM SNOWFLAKE.ACCOUNT_USAGE.APPLICATION_DAILY_USAGE_HISTORY
WHERE APPLICATION_NAME = '<app_name>'
ORDER BY USAGE_DATE DESC;
```

Columns include: `APPLICATION_NAME`, `USAGE_DATE`, `CREDITS_USED`, `CREDITS_USED_BREAKDOWN`,
`STORAGE_BYTES`, `STORAGE_BYTES_BREAKDOWN`.

### APPLICATION\_CALLBACK\_HISTORY

This view records executions of the app’s App Spec callback procedures: the stored
procedures the app runs when its App Specs are approved or revoked. Use
it to see when configuration changes were made and whether they completed successfully.
Configuration, connection, and specification callbacks are captured by this view.
Reference/grant callbacks are currently not covered.

Copy code

```
SELECT *
FROM SNOWFLAKE.ACCOUNT_USAGE.APPLICATION_CALLBACK_HISTORY
WHERE APPLICATION_NAME = '<app_name>'
ORDER BY STARTED_ON DESC;
```

Columns include: `TYPE`, `APPLICATION_NAME`, `STATE`, `STARTED_ON`, `COMPLETED_ON`, `QUERY_ID`,
`ERROR_CODE`, `ERROR_MESSAGE`.

## Event logging and sharing with the provider

The app’s log messages and trace events can be shared with the provider to assist with
troubleshooting. This sharing is not enabled by default: you must actively set up an event table
and opt in to sharing.

**When event sharing is enabled:**

- Log messages and trace events emitted by the app are written to your event table.
- Snowflake shares a subset of those events with the provider’s account.
- The shared events include app-context attributes (the app package name, your account region, and
  similar metadata) but do not include your raw data or the content of your queries.
- Your account name and certain identifiers are hashed before sharing to protect your privacy.

You can enable or disable event sharing at any time. If you do not have an active event table
configured, log and trace data emitted by the app is discarded.

For full instructions, see
[Set up event tracing for an app](/developer-guide/native-apps/ui-consumer-enable-logging).
