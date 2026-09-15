[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# DATA\_CLASSIFICATION\_LATEST view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view displays one row for the most recent result of a classified table for each classified table. Each row corresponds
to a different table.

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
| TABLE\_ID | NUMBER | Internal/system-generated identifier for the table that was classified. |
| TABLE\_NAME | VARCHAR | Name of the table. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema that contains the table. |
| SCHEMA\_NAME | VARCHAR | Name of the schema that contains the table. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database that contains the table. |
| DATABASE\_NAME | VARCHAR | Name of the database that contains the table. |
| RESULT | VARIANT | Latest classification result. For a description of the JSON object, see the output of the [SYSTEM$GET\_CLASSIFICATION\_RESULT](/sql-reference/functions/system_get_classification_result) function. |
| STATUS | VARCHAR | One of the following: `CLASSIFIED` or `REVIEWED`. |
| TRIGGER\_TYPE | VARCHAR | Mode of the classification trigger: `MANUAL` or `AUTO CLASSIFICATION`, where `MANUAL` indicates that someone called a system function to initiate the classification process. |
| LAST\_CLASSIFIED\_ON | TIMESTAMP\_LTZ | Time when the table was last successfully classified. |
| LAST\_CLASSIFICATION\_ATTEMPT | TIMESTAMP\_LTZ | Timestamp of the last sensitive data classification attempt. If the value is greater than `LAST_CLASSIFIED_ON`, it indicates that the last sensitive data classification attempt resulted in a failure. |
| ERROR\_MESSAGE | VARCHAR | Error message from the last sensitive data classification attempt, if it resulted in a failure. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 5 hours.
- This view retains data for as long as the table exists.
- A row in the view is removed when the following occur:
  - A table is dropped or renamed.
  - The table is reclassified.
