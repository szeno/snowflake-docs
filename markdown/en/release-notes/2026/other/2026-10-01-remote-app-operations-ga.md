# Oct 1, 2026: Remote app operations for Snowflake Native Apps (*General availability*)

Remote app operations for Snowflake Native Apps are now generally available.

Providers can perform on-demand operations on consumer apps by calling the
[SYSTEM$REMOTE\_APP\_OPERATION](/sql-reference/functions/system_remote_app_operation) system function,
including running SQL statements (`run_sql`), retrying a failed upgrade (`retry_upgrade`),
and disabling or enabling the app (`disable`/`enable`).

Restricted operations such as `run_sql` require consumer consent, which consumers can configure
through the `AUTHORIZE_RESTRICTED_PROVIDER_REMOTE_OPERATIONS_UNTIL` property on
[ALTER APPLICATION](/sql-reference/sql/alter-application) or
[CREATE APPLICATION](/sql-reference/sql/create-application).
Providers can check consent status through the
[APPLICATION\_STATE](/sql-reference/data-sharing-usage/application-state-view) view.

For more information, see:

- [Use remote app operations](/developer-guide/native-apps/remote-app-operation) (provider guide)
- [Manage remote app operations](/developer-guide/native-apps/ui-consumer-remote-app-operation) (consumer guide)
- [SYSTEM$REMOTE\_APP\_OPERATION](/sql-reference/functions/system_remote_app_operation) (function reference)
