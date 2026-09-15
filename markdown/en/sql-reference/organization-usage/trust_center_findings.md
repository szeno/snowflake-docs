Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# TRUST\_CENTER\_FINDINGS view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view shows security violations discovered by [Trust Center scanners](/user-guide/trust-center/overview#label-trust-center-scanners).

## Columns

**Organization-level columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| ACCOUNT\_LOCATOR | VARCHAR | System-generated identifier for the account. |
| ACCOUNT\_NAME | VARCHAR | User-defined identifier for the account. |

Expand

Show lessSee more

**Additional columns**

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

- Latency for the view may be up to 180 minutes (3 hours).
