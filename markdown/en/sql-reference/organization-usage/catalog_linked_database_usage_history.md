[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# CATALOG\_LINKED\_DATABASE\_USAGE\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

Use this Organization Usage view to view the credit usage for
[catalog-linked databases](/user-guide/tables-iceberg-catalog-linked-database)
across accounts in your organization within the last 12 months.

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

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | The date and beginning of the hour (in the local time zone) in which the catalog-linked database operation took place. |
| END\_TIME | TIMESTAMP\_LTZ | The date and end of the hour (in the local time zone) in which the catalog-linked database operation took place. |
| DATABASE\_ID | NUMBER | Internal identifier for the catalog-linked database that consumed credits. |
| DATABASE\_NAME | VARCHAR | Name of the catalog-linked database that consumed credits. |
| CREDITS\_USED\_COMPUTE | NUMBER(38,9) | Number of credits used by the catalog-linked database for table creation operations between the START\_TIME and END\_TIME. The cost for this usage is described in Table 5 of the [Snowflake service consumption table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf) on the Snowflake website. See the Snowflake-managed compute column for the Automated Refresh and Data Registration row. |
| CREDITS\_USED\_CLOUD\_SERVICES | NUMBER(38,9) | Number of credits used by the catalog-linked database for automatic table discovery, schema creation or deletion, and table deletion between the START\_TIME and END\_TIME. Usage for cloud services is charged only if the daily consumption of cloud services exceeds 10% of the daily usage of virtual warehouses. For more information, see [Understanding billing for cloud services usage](/user-guide/cost-understanding-compute#label-understanding-billing-for-cloud-services-usage). |
| CREDITS\_USED | NUMBER(38,9) | Number of credits billed for this catalog-linked database between the START\_TIME and END\_TIME. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 5 hours.
