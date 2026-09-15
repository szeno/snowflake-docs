Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# DATA\_MOVEMENT\_VIOLATIONS view

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Account Usage view displays a row for each query that violated a data movement policy in your account. Each row consolidates all triggered policies across potentially many tables into a single entry keyed by query ID.

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| `QUERY_ID` | VARCHAR | ID of the query that violated a data movement policy. |
| `ENFORCED_POLICY` | VARCHAR | Fully qualified name (FQN) of the enforced rule and corresponding policy triggered by the query. NULL if no enforce rule was triggered. |
| `MOVEMENT_TYPE` | VARCHAR | Movement type of the statement that triggered the violation. Possible values: `COPY_INTO_EXTERNAL_STAGE`, `COPY_INTO_INTERNAL_STAGE`, `SNOWSIGHT_UI`, `AGENT_ACCESS`, `PROGRAMMATIC_FETCH`. `UI_DOWNLOAD` violations aren’t included in this view. |
| `ALERTED_POLICIES` | VARCHAR | FQNs of alert rules and corresponding policies triggered by the query. |
| `USER_NAME` | VARCHAR | Name of the user that ran the query. |
| `DATA_ENTITIES` | ARRAY | FQNs of the tables involved in the query. |
| `TIMESTAMP` | TIMESTAMP\_LTZ | Timestamp of the query. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 3 hours.
- Data is retained for one year.
- The view only displays objects for which the current role for the session has been granted access privileges.
- `UI_DOWNLOAD` violations aren’t included in this view.

These views are also available in the ORGANIZATION\_USAGE schema. Organization usage must be enabled for the account.
