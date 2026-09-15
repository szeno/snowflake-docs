[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# DATA\_CLASSIFICATION\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view displays all historical sensitive data classification results for each table in each account in your organization. Unlike
[DATA\_CLASSIFICATION\_LATEST view](/sql-reference/organization-usage/data_classification_latest), which shows only the most recent classification per table,
this view shows all classification events over time, limited to the last 365 days.

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

| Column name | Data type | Description |
| --- | --- | --- |
| TABLE\_ID | NUMBER | Internal/system-generated identifier for the table that was classified. |
| TABLE\_NAME | VARCHAR | Name of the table. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema that contains the table. |
| SCHEMA\_NAME | VARCHAR | Name of the schema that contains the table. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database that contains the table. |
| DATABASE\_NAME | VARCHAR | Name of the database that contains the table. |
| RESULT | VARIANT | Classification result at the time of classification. For a description of the JSON object, see the output of the [SYSTEM$GET\_CLASSIFICATION\_RESULT](/sql-reference/functions/system_get_classification_result) function. |
| TRIGGER\_TYPE | VARCHAR | Mode of the classification trigger: `MANUAL` or `AUTO CLASSIFICATION`, where `MANUAL` indicates that someone called a system function to initiate the classification process. |
| CLASSIFIED\_ON | TIMESTAMP\_LTZ | Time when the classification was performed. |
| TABLE\_DELETED\_ON | TIMESTAMP\_LTZ | Date and time when the object or parent object was dropped. NULL if the object has not been deleted. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 5 hours.
- Data is retained for 365 days (one year). Rows are removed only when a classification event is older than one year.
- Unlike [DATA\_CLASSIFICATION\_LATEST view](/sql-reference/organization-usage/data_classification_latest), this view retains data for classification events
  even when the associated table, schema, or database is dropped. The `TABLE_NAME`, `SCHEMA_NAME`, and `DATABASE_NAME`
  columns reflect the table and its database/schema location recorded for that classification result, but do not preserve historical
  object names across subsequent rename operations. If a table is later moved to a different schema and reclassified, a new row
  reflects the new location. The `TABLE_DELETED_ON` column is non-null if the table has been dropped.

For more information on how to query this view, see [Query the classification history](/user-guide/classify-results#label-classify-view-history-sql).
