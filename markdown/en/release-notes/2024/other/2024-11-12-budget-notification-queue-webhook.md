# November 12, 2024 — Budgets: Support for cloud provider queue and webhook notifications

You can now configure your account budget and custom budgets so that notifications are sent to the following:

- A queue provided by a cloud service (Amazon SNS, Azure Event Grid, or Google Cloud PubSub).
- A webhook for Slack, Microsoft Teams, or PagerDuty.

To do this, you create a [notification integration for a queue](/user-guide/notifications/queue-notifications) or a
[webhook](/user-guide/notifications/webhook-notifications), and you call a method to associate the integration with the
budget. The BUDGET class now supports the following new methods:

| Method | Description |
| --- | --- |
| [<budget\_name>!ADD\_NOTIFICATION\_INTEGRATION](/sql-reference/classes/budget/methods/add_notification_integration) | Adds a queue or webhook notification integration to a custom budget or the account budget. |
| [<budget\_name>!GET\_NOTIFICATION\_INTEGRATIONS](/sql-reference/classes/budget/methods/get_notification_integrations) | Returns information about the queue and webhook notification integrations associated with a custom budget or the account budget. |
| [<budget\_name>!REMOVE\_NOTIFICATION\_INTEGRATION](/sql-reference/classes/budget/methods/remove_notification_integration) | Removes a queue or webhook notification integration from a custom budget or the account budget. |

Expand

Show lessSee more

For information, see [Notifications for budgets](/user-guide/budgets/notifications).
