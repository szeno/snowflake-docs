Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# ANOMALIES\_IN\_CURRENCY\_DAILY view

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view provides insights into whether [cost anomalies](/user-guide/cost-anomalies) occurred in accounts in the
organization.

Each row provides the consumption of an account on a specific day, and whether that consumption was a cost anomaly.

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| DATE | DATE | Day in UTC when the consumption occurred. |
| ANOMALY\_ID | VARCHAR | System-generated identifier. |
| IS\_ANOMALY | BOOLEAN | If true, consumption has been identified as a cost anomaly because it has gone outside the range of the upper and lower bound. |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| ACCOUNT\_NAME | VARCHAR | Name of the account where consumption occurred. |
| ACCOUNT\_LOCATOR | VARCHAR | Account locator of the account where consumption occurred. |
| REGION | VARCHAR | Snowflake region where the account is located. |
| ACTUAL\_VALUE | NUMBER | Amount of consumption measured in CURRENCY. |
| CURRENCY | VARCHAR | Unit of measure for the consumption. |
| UPPER\_BOUND | NUMBER | Predicted highest level of consumption based on the anomaly-detecting algorithm, measured in CURRENCY. Consumption levels above this value are considered an anomaly. |
| LOWER\_BOUND | NUMBER | Predicted lowest level of consumption based on the anomaly-detecting algorithm, measured in CURRENCY. Consumption levels below this value are considered an anomaly. |
| FORECASTED\_VALUE | NUMBER | Predicted consumption based on the anomaly-detecting algorithm, measured in CURRENCY. |

Expand

Show lessSee more

## Usage notes

Latency for the view might be up to 24 hours.
