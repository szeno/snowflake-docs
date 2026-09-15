Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# DATA\_MOVEMENT\_RULE\_REFERENCES view

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Account Usage view displays a row for each rule-to-policy mapping in your account, showing which rules are assigned to which policies and whether each rule is in the enforce or alert list.

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| `POLICY_ID` | NUMBER | Internal/system-generated identifier for the data movement policy. |
| `POLICY_NAME` | VARCHAR | Name of the data movement policy. |
| `POLICY_DATABASE` | VARCHAR | Database of the data movement policy. |
| `POLICY_SCHEMA` | VARCHAR | Schema of the data movement policy. |
| `RULE_ID` | NUMBER | Internal/system-generated identifier for the data movement rule. |
| `RULE_NAME` | VARCHAR | Name of the data movement rule. |
| `RULE_DATABASE` | VARCHAR | Database of the data movement rule. |
| `RULE_SCHEMA` | VARCHAR | Schema of the data movement rule. |
| `RULE_MOVEMENT_TYPE` | VARCHAR | Movement type of the rule: `COPY_INTO_EXTERNAL_STAGE`, `COPY_INTO_INTERNAL_STAGE`, `AGENT_ACCESS`, `SNOWSIGHT_UI`, `UI_DOWNLOAD`, `PROGRAMMATIC_FETCH`, or `UNKNOWN`. |
| `RULE_CATEGORY` | VARCHAR | Whether the rule is in the enforce or alert list: `ENFORCE` or `ALERT`. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 3 hours.
- The view only displays objects for which the current role for the session has been granted access privileges.
- Only active rule-to-policy mappings are included. Mappings removed by `ALTER DATA MOVEMENT POLICY ... REMOVE ENFORCE_RULES` or `REMOVE ALERT_RULES` are excluded.

These views are also available in the ORGANIZATION\_USAGE schema. Organization usage must be enabled for the account.
