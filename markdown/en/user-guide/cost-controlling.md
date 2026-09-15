# Controlling cost

You can use budgets to control credit usage for compute costs, including those incurred by serverless features. If you are only concerned
with controlling the costs of warehouses, you can also use resource monitors to monitor and suspend warehouses. In addition, Snowflake
provides cost controls you can configure to help avoid unexpected costs.

## Use budgets to control credit usage

A *budget* allows you to set a monthly spending limit and monitor the credit usage of all
[supported objects](/user-guide/budgets/custom-budget#label-budgets-supported-objects) and serverless features in your account. In addition to your account budget,
you can create custom budgets to monitor credit usage of groups of specified objects and the serverless features used by those objects.
For example, you can create a custom budget for each department in your organization. Each budget sends a notification if the
credit usage is expected to exceed its spending limit for the month. You can configure the budget to send this notification to a
list of email addresses, a queue provided by a cloud service (Amazon SNS, Azure Event Grid, or Google Cloud PubSub), or a webhook
for a third-party system (for example, Slack, Microsoft Teams, or PagerDuty).

For information about budgets, see [Monitor credit usage with budgets](/user-guide/budgets).

## Use resource monitors to control credit usage

A *resource monitor* lets you monitor credit usage by user-managed virtual warehouses. You can set a spending limit that resets on a
monthly basis or on a custom schedule. A resource monitor can
send an email notification when your credit usage reaches a percentage (threshold) of the spending limit. You can customize up to five
notification thresholds. To help avoid unexpected credit usage, you can optionally suspend a warehouse when its credit usage reaches
a threshold.

For background information about how virtual warehouses incur costs, see [Understanding compute cost](/user-guide/cost-understanding-compute).

For information about resource monitors, see [Working with resource monitors](/user-guide/resource-monitors).

## Cost controls for warehouses

For a set of best practices that act as cost controls for virtual warehouses, see [Cost controls for warehouses](/user-guide/cost-controlling-controls).
