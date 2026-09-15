Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# TRUST\_CENTER\_FINDINGS view

This Account Usage view shows security violations discovered by [Trust Center scanners](/user-guide/trust-center/overview#label-trust-center-scanners).

## Columns

| Column | Data Type | Description |
| --- | --- | --- |
| ID | NUMBER | System identifier of the account that had the finding. |
| PROVIDER\_ID | VARCHAR | System identifier of the provider of the scanner package. |
| SCANNER\_PACKAGE\_ID | VARCHAR | System identifier of the scanner package. |
| SCANNER\_ID | VARCHAR | System identifier of the scanner. |
| SEVERITY | VARCHAR | Severity of the finding, as assigned by the scanner [LOW, MEDIUM, HIGH, CRITICAL]. |
| STATE | VARCHAR | State of the finding [OPEN, RESOLVED, RESOLVED MANUALLY]. |
| CREATED\_ON | TIMESTAMP\_LTZ | The time at which the finding was initially created. |
| UPDATED\_ON | TIMESTAMP\_LTZ | The time at which the finding was last updated. |

Expand

Show lessSee more

## Usage notes

Latency for the view may be up to 60 minutes (1 hour).
