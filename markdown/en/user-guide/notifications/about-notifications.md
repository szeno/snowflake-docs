# Notifications in Snowflake

You can configure Snowflake to send notifications to a queue provided by a Cloud service (Amazon SNS, Google Cloud PubSub, or
Azure Event Grid), an email address, or a webhook. For details, see the following sections:

- [Sending notifications to cloud provider queues (Amazon SNS, Google Cloud PubSub, and Azure Event Grid)](/user-guide/notifications/queue-notifications)
- [Sending email notifications](/user-guide/notifications/email-notifications)
- [Sending webhook notifications](/user-guide/notifications/webhook-notifications), for the following external systems:

  - [Slack](https://api.slack.com/messaging/webhooks)
  - [Microsoft Teams](https://support.microsoft.com/en-us/office/create-incoming-webhooks-with-workflows-for-microsoft-teams-8ae491c7-0394-4861-ba59-055e33f75498)
  - [PagerDuty](https://developer.pagerduty.com/docs/ZG9jOjExMDI5NTgw-events-api-v2-overview)
  - [Jira](https://support.atlassian.com/cloud-automation/docs/jira-automation-triggers/#Incoming-webhook)
  - [ServiceNow](https://www.servicenow.com/docs/r/integrate-applications/integration-hub/rest-trigger.html)

## Viewing the history of notifications

To view the history of notifications, call the Information Schema [NOTIFICATION\_HISTORY](/sql-reference/functions/notification_history) table
function.
