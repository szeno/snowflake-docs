Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# CORTEX\_PROVISIONED\_THROUGHPUT\_USAGE\_HISTORY view

This Account Usage view lets you retrieve billing data for provisioned throughputs.

Tip

In [Cortex Code](/user-guide/cortex-code/cortex-code), including the [CLI](/user-guide/cortex-code/cortex-code-cli), [Desktop](/user-guide/cortex-code/cortex-code-desktop), and [Snowsight](/user-guide/cortex-code/cortex-code-snowsight) interfaces, you can use the [`cost-intelligence`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-cost-intelligence) bundled skill to answer questions about the usage data in this view. Invoke the skill with `/cost-intelligence`, or describe your question in plain language and Cortex Code selects the skill automatically.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| PROVISIONED\_THROUGHPUT\_ID | VARCHAR | UUID identifying the provisioned throughput. |
| INTERVAL\_START\_TIME | TIMESTAMP\_TZ | Start of the measurement interval for the billing period. |
| INTERVAL\_END\_TIME | TIMESTAMP\_TZ | End of the measurement interval for the billing period. |
| CLOUD\_SERVICE\_PROVIDER | VARCHAR | Host cloud provider. |
| MODEL\_NAME | VARCHAR | Configured model name. |
| TERM\_START\_DATE | DATE | Start of the provisioned throughput’s term. |
| TERM\_END\_DATE | DATE | End of the provisioned throughput’s term. |
| PTU\_COUNT | NUMBER | Number of PTUs active. |
| PTU\_CREDITS | NUMBER(38,9) | Number of credits billed during this interval. |

Expand

Show lessSee more

## Usage notes

- The view provides up-to-date credit usage for an account within the last 365 days (1 year).
