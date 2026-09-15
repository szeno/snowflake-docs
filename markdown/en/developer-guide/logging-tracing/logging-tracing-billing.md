# Costs of telemetry data collection

When you log messages from a function or procedure, Snowflake collects the messages in batches and ingests the batches into the event table.

To perform this work, Snowflake uses Snowflake-managed resources, also referred to as the serverless compute model. As is the case with
[other serverless features](/user-guide/cost-understanding-compute#label-serverless-credit-usage), Snowflake bills your account for the compute resource and cloud
services usage needed to ingest the logged messages. These costs appear on your bill as separate line items.

To determine the credit usage for logging over time, use the following views:

- [METERING\_HISTORY view](/sql-reference/account-usage/metering_history).
- [METERING\_DAILY\_HISTORY view](/sql-reference/account-usage/metering_daily_history) (Account Usage).
- [METERING\_DAILY\_HISTORY view](/sql-reference/organization-usage/metering_daily_history) (Organization Usage).

To reduce the cost of logging:

- Avoid logging frequently over a long period of time.
- [Set the level of messages ingested](/developer-guide/logging-tracing/telemetry-levels) on specific objects. For example, set the
  log level for specific functions or procedures in a session, instead of setting the log level for all functions or procedures.

If you do not want to collect telemetry data, you can do any one of the following:

- Disable or change telemetry levels appropriately. For more information, see [Set telemetry levels](/developer-guide/logging-tracing/logging-tracing-overview#label-logging-event-table-level).

  This option is not applicable for [Native Apps](/developer-guide/native-apps/native-apps-about).
- Uninstall the applications or connectors emitting telemetry data, or drop the unnecessary objects.
- If you do not want any logging and tracing events to be collected at all in the account, execute the following command to deactivate
  the event table:

  Copy code

  ```
  ALTER ACCOUNT SET EVENT_TABLE = NONE
  ```
