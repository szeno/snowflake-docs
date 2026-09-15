Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# ANOMALIES\_DAILY view

This Account Usage view provides insights into whether [cost anomalies](/user-guide/cost-anomalies) occurred in the account.

Each row provides the consumption on a specific day, and whether that consumption was a cost anomaly.

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| DATE | DATE | Day in UTC when the consumption occurred. |
| ANOMALY\_ID | VARCHAR | System-generated identifier. |
| IS\_ANOMALY | BOOLEAN | If true, consumption has been identified as a cost anomaly because it has gone outside the range of the upper and lower bound. |
| ACTUAL\_VALUE | NUMBER | Amount of consumption measured in credits. |
| UPPER\_BOUND | NUMBER | Predicted highest level of consumption based on the anomaly-detecting algorithm, measured in credits. Consumption levels above this value are considered an anomaly. |
| LOWER\_BOUND | NUMBER | Predicted lowest level of consumption based on the anomaly-detecting algorithm, measured in credits. Consumption levels below this value are considered an anomaly. |
| FORECASTED\_VALUE | NUMBER | Predicted consumption based on the anomaly-detecting algorithm, measured in credits. |

Expand

Show lessSee more

## Usage notes

Latency for the view might be up to 8 hours.
