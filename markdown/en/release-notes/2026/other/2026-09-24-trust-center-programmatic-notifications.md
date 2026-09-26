# Sep 24, 2026: Programmatic notifications for Trust Center findings (*Preview*)

You can send Trust Center findings to enterprise ticketing and monitoring systems without waiting in Snowsight or email. Configure a notification integration for a webhook or queue, such as PagerDuty, Slack, Microsoft Teams, Amazon SNS, Azure Event Grid, or Google Pub/Sub, and Snowflake delivers findings that meet your severity threshold to that endpoint.

You can now send a test notification as soon as the integration is configured. This capability launched in Snowflake version 10.33.100, which was deployed the week of September 13-16, 2026. Call `SNOWFLAKE.TRUST_CENTER.SEND_TEST_NOTIFICATION_INTEGRATION` to push a mock finding to a single integration at the scanner-package or scanner level. You don’t have to wait for a scanner to produce a real finding before you confirm that tickets or alerts show up in your system.

For more information, see [Programmatic notifications for Trust Center findings](/user-guide/trust-center/notification-integrations) and
[Send a test notification](/user-guide/trust-center/notification-integrations#label-trust-center-webhook-test).
