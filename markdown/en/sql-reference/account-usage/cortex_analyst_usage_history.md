Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# CORTEX\_ANALYST\_USAGE\_HISTORY view

The CORTEX\_ANALYST\_USAGE\_HISTORY view can be used to query the usage history of [Cortex Analyst](/user-guide/snowflake-cortex/cortex-analyst).

The information in the view includes the number of credits consumed each time Cortex Analyst is called, aggregated in one-hour increments.
The view also includes relevant metadata, such as the start and end times of the messages and the number of messages sent.

Tip

In [Cortex Code](/user-guide/cortex-code/cortex-code), including the [CLI](/user-guide/cortex-code/cortex-code-cli), [Desktop](/user-guide/cortex-code/cortex-code-desktop), and [Snowsight](/user-guide/cortex-code/cortex-code-snowsight) interfaces, you can use the [`cost-intelligence`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-cost-intelligence) bundled skill to answer questions about the usage data in this view. Invoke the skill with `/cost-intelligence`, or describe your question in plain language and Cortex Code selects the skill automatically.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | Start of the specified time range in which the Cortex Analyst message request was received. |
| END\_TIME | TIMESTAMP\_LTZ | End of the specified time range in which the Cortex Analyst message response was sent. |
| REQUEST\_COUNT | NUMBER | The number of messages sent to Cortex Analyst. |
| CREDITS | NUMBER | The number of credits billed for a set of messages sent to Cortex Analyst. |
| USERNAME | TEXT | The username of the user who sent the Cortex Analyst message request. The username is included with the session.  For more information about authenticating, see [Authenticating to the server](/developer-guide/sql-api/authenticating). |

Expand

Show lessSee more

## Usage notes

- The view provides up-to-date credit usage for an account within the last 365 days (1 year).
- Credit rate usage is based on the number of messages processed, as outlined in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).
