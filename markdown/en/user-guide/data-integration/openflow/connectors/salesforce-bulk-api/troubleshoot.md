# Troubleshooting the Openflow Connector for Salesforce Bulk API

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes how to troubleshoot the Openflow Connector for Salesforce Bulk API.

Use the following information to troubleshoot issues with the connector.

## Authentication and OAuth errors

The connector uses the OAuth 2.0 JWT Bearer Flow to authenticate with Salesforce. Authentication errors typically occur during initial setup and can be diagnosed using the [Verification feature](#salesforce-verify-connection) on the controller service before starting the connector.

### `invalid_grant` error

The `invalid_grant` error indicates that Salesforce rejected the OAuth token request. Common causes include:

- **Wrong OAuth flow type.** The external client app in Salesforce does not have the **Enable JWT Bearer Flow** checkbox selected. The connector requires this specific flow. Other OAuth flows (such as Authorization Code Flow) are not supported. See .
- **Mismatched private key and certificate.** The private key configured in the connector (the **Connected App Key** parameter) does not match the public certificate uploaded to the external client app in Salesforce.
- **Wrong Consumer Key.** The **OAuth2 Client ID** parameter does not match the **Consumer Key** of the external client app where the certificate was uploaded.
- **Mixed credentials from multiple apps.** If you have created multiple external client apps or experimented with different configurations, the Client ID, certificate, and private key might belong to different apps. All three must come from the same external client app.
- **Deprecated Connected App.** Salesforce has deprecated Connected Apps in favor of External Client Apps. If you are using a Connected App, Snowflake recommends creating a new external client app instead.
- **Incorrect token endpoint URL.** The **OAuth2 Token Endpoint URL** parameter must point to the correct Salesforce instance. For example: `https://myCompany.my.salesforce.com/services/oauth2/token`.
- **Incorrect audience.** The **OAuth2 Audience** parameter must be set to `https://login.salesforce.com` for production environments or `https://test.salesforce.com` for sandboxes and test environments.

### Permission errors

If the JWT token is successfully generated but the user lacks permissions, you see a permission or authorization error. This means the JWT Bearer Flow is working, but the Salesforce user (the OAuth2 Subject) is not authorized to use the external client app.

To resolve this issue:

1. In Salesforce, go to the **Policies** tab of the external client app.
2. Verify that **Permitted Users** is set to **Admin approved users are pre-authorized**.
3. Verify that the profiles or permission sets assigned in the **App Policies** section include the user specified in the **OAuth2 Subject** parameter of the connector.

For more details, see .

## Check the connector state

You can examine the connector state to ensure that data is being replicated as expected. The connector maintains a state of current and past operations to ensure no Salesforce changes are missed and to retry bulk job queries if failures occur.

To view the state:

1. Right-click on the canvas and select **Controller services**.
2. Locate the controller service named **Salesforce Bulk Jobs State**.
3. In the **Salesforce Bulk Jobs State** menu, click **View state**.

The state is a set of key/value pairs where the key is the Salesforce Object type. For
example, the state for the `Account` object might look like the following example:

Copy code

```
{"previousLast":"2025-09-30T09:41:23.484406926Z","currentLast":"2025-09-30T09:41:23.484406926Z","status":"COMPLETED"}
```

The `status` can be one of the following:

- `IN_PROGRESS`
- `COMPLETED`
- `FAILED`
- `ABORTED`

If the status is `IN_PROGRESS`, a FlowFile is still being processed for that object type.

Caution

Do not delete FlowFiles manually. This can cause a job to remain in the `IN_PROGRESS` status indefinitely because the state cannot be manually updated.

If this occurs, you must perform a full reload for that object type.

## Force a full load for a given object type

To force the connector to perform a full refresh for one or more object types:

1. Stop all processors in the flow.
2. Ensure that no in-flight FlowFiles are being processed.
3. Right-click on the canvas and select **Disable all controller services**.
4. Go to **Controller services** and open the state of the controller service named
   **Salesforce Bulk Jobs State**.
5. Perform one of the following actions:

   - Select **Clear state** to clear the entire state. This forces a full load for
     **all** configured Object types fetched by the connector.
   - Select the trash icon next to a specific Object type to clear the state for a
     specific object type only. This forces a full load of that specific object type
     during the next execution of the connector.
6. In the canvas, right-click, select **Enable all controller services**, and then start all processors.

## If an object type remains in status IN\_PROGRESS

If the state for a given object type is stuck in `IN_PROGRESS` and there are no in-flight FlowFiles for that object type, a FlowFile may have been manually deleted before it could update the status.

In this case, you must perform a full load for that object type to ensure the connector
captures all events.

If the state is stuck in `IN_PROGRESS` but no FlowFiles were manually deleted, contact
[Snowflake Support](/user-guide/contacting-support).
