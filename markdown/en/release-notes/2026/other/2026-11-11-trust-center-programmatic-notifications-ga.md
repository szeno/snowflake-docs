# Nov 11, 2026: Programmatic notifications for Trust Center findings (*General availability*)

Programmatic notifications for Trust Center findings are now generally available and are no longer in [Preview](/release-notes/preview-features).

You can send Trust Center findings to ticketing, alerting, and messaging systems through notification integrations for webhooks,
such as PagerDuty, Slack, Microsoft Teams, Jira, and ServiceNow, and for queues, such as Amazon SNS, Azure Event Grid, and Google
Pub/Sub. Snowflake delivers findings that meet your severity threshold to the endpoint. To verify an integration, send a test
notification with `SNOWFLAKE.TRUST_CENTER.SEND_TEST_NOTIFICATION_INTEGRATION`.

You can configure notification integrations for a scanner package or scanner by using SQL or Snowsight.
In Snowsight, select an existing notification integration, grant the Trust Center access to it, and set the minimum severity level that
triggers a notification.

For more information, see [Programmatic notifications for Trust Center findings](/user-guide/trust-center/notification-integrations).
