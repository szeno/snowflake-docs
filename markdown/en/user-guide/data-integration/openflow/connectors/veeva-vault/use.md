# Use the Openflow Connector for Veeva Vault

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes tasks you may need to perform after installing and configuring the
Openflow Connector for Veeva Vault.

## Force a full reload

The connector maintains an internal state to track which Direct Data files have already been
processed. In some situations, you may need to force the connector to perform a fresh full
snapshot, for example, after resolving a data issue or after the connector has been stopped for
an extended period.

To force a full reload:

1. Stop all processors in the flow by right-clicking on the connector process group and
   selecting **Stop**.
2. Ensure that no in-flight FlowFiles are being processed. You can verify this by checking
   that all queues in the flow are empty.
3. Right-click on the canvas and select **Disable all controller services**.
4. Go to **Controller services** and locate the controller service named
   **Veeva Vault Client Service**.
5. In the processor **List Veeva Vault Files**, select **View state** and then
   select **Clear state**.
6. Right-click on the canvas and select **Enable all controller services**, then start all
   processors to resume the connector.

The connector treats a cleared state as a fresh start and processes the latest full Direct Data
file on the next execution.

## Monitoring

To track the amount of data being synced from Veeva Vault to Snowflake, query the event table.
The following example query retrieves relevant logs from the last 30 minutes:

Copy code

```
SELECT
  timestamp,
  Deployment_ID,
  Runtime_Key,
  parsed_log:level as log_level,
  parsed_log:loggerName as logger,
  parsed_log:formattedMessage as message,
  parsed_log
FROM (
  SELECT
    timestamp,
    resource_attributes:"openflow.dataplane.id" as Deployment_ID,
    resource_attributes:"k8s.namespace.name" as Runtime_Key,
    TRY_PARSE_JSON(value) as parsed_log
  FROM OPENFLOW.TELEMETRY.EVENTS
  WHERE true
    AND timestamp > dateadd('minutes', -30, sysdate())
    AND record_type = 'LOG'
    AND resource_attributes:"k8s.namespace.name" like 'runtime-%'
  ORDER BY timestamp DESC
)
WHERE true
  AND logger LIKE '%veeva%';
```

For more information about monitoring Openflow flows, see [Monitor Openflow using telemetry data](/user-guide/data-integration/openflow/monitor).

## Troubleshooting

Use the following information to troubleshoot common issues with the connector.

### Direct Data is not enabled

If the connector fails with an error indicating that Direct Data files can’t be retrieved,
verify that Direct Data is enabled on your Vault. Contact your Veeva Vault
administrator to enable this feature in the Vault admin settings.

### Authentication failures

If the connector reports authentication failures:

- Verify that the **Veeva Vault Username** and **Veeva Vault Password** parameters are
  correct.
- Verify that the service account has API access enabled and has the required permissions.
- Check whether the account is locked or disabled in Veeva Vault.

You can verify the credentials by right-clicking on the canvas, selecting
**Controller services**, locating the **Veeva Vault Client Service**, and selecting
**Verify Properties**. This triggers a connectivity and authentication check against the
configured Vault.

### Session expiration during long operations

The connector automatically handles session expiration by re-authenticating when it receives
an `INVALID_SESSION_ID` error from Vault API. No manual intervention is required.
If you see repeated session expiration messages in the event table, verify that no other
process is using the same service account credentials, as concurrent sessions may cause the
previous session to be invalidated.

### No new data appearing in Snowflake

If the connector is running but no new data appears in Snowflake:

- Check that new Direct Data files are being published by Veeva Vault. The connector can
  only process archives that exist.
- Verify that the **Veeva Vault Ingestion Mode** is set correctly. If set to `INCREMENTAL`
  and no incremental archives exist after the configured start time, no data is processed.
- Check the event table for error messages that may indicate failures in the download,
  unpacking, or loading stages.

### Snowflake permission errors

If the connector reports permission errors when creating tables or loading data:

- Verify that the execute-as role configured in the connector has `USAGE` on the destination
  database and schema, `CREATE TABLE` on the schema, and `USAGE` and `OPERATE` on the
  warehouse.
- For Openflow - BYOC Deployments, verify that the service user has the correct role assigned and that the
  RSA public key is configured correctly.
