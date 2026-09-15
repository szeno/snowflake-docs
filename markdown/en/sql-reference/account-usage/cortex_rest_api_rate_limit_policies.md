Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# CORTEX\_REST\_API\_RATE\_LIMIT\_POLICIES view

Query the CORTEX\_REST\_API\_RATE\_LIMIT\_POLICIES view to see the per-model rate limit policies
for Cortex REST API endpoints in your account. The view shows the requests-per-minute (RPM) and
tokens-per-minute (TPM) limits for each model.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| MODEL\_NAME | TEXT | Name of the model for which the rate limit policy applies. |
| RPM | NUMBER | The requests-per-minute limit for the model. A NULL value means no RPM limit is enforced. |
| TPM | NUMBER | The tokens-per-minute limit for the model. A NULL value means no TPM limit is enforced. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 360 minutes (6 hours).
- The view is scoped to the account that runs the query.
