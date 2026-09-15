# August 25, 2026: Remote app operations for Snowflake Native Apps (*Preview*)

Remote app operations are now available in public preview for Snowflake Native Apps.
Providers can perform on-demand operations on consumer apps, including running
SQL statements (`run_sql`), retrying a failed upgrade (`retry_upgrade`), and disabling/enabling the app (`disable`/`enable`), all through a new system function `SYSTEM$REMOTE_APP_OPERATION`.

Some remote app operations require consent to be configured by the consumer through the new
`AUTHORIZE_RESTRICTED_PROVIDER_REMOTE_OPERATIONS_UNTIL` app property. By default, restricted operations like `run_sql` are not authorized.

Remote app operation invocations are logged in the
[ACCOUNT\_USAGE.APPLICATION\_REMOTE\_OPERATION\_HISTORY](/sql-reference/account-usage/application_remote_operation_history) view.

For more information, see:

- Provider guide: [Use remote app operations](/developer-guide/native-apps/remote-app-operation)
- Consumer guide: [Manage remote app operations](/developer-guide/native-apps/ui-consumer-remote-app-operation)
- System function reference: [SYSTEM$REMOTE\_APP\_OPERATION](/sql-reference/functions/system_remote_app_operation)
