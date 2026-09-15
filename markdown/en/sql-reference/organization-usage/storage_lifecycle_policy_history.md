Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# STORAGE\_LIFECYCLE\_POLICY\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view displays the aggregated execution history of
[storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies).
This view shows historical data from the past 12 months and only includes policy executions
that have completed successfully or with failures. The view doesn’t include queued, currently executing, or cancelled
policy executions.

Each row in this view corresponds to a different storage lifecycle policy execution.

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
| POLICY\_DB | VARCHAR | The name of the database that contains the storage lifecycle policy. |
| POLICY\_SCHEMA | VARCHAR | The name of the schema that contains the storage lifecycle policy. |
| POLICY\_NAME | VARCHAR | The name of the storage lifecycle policy. |
| REF\_ENTITY\_DB | VARCHAR | The name of the database that contains the object that the storage lifecycle policy is attached to. |
| REF\_ENTITY\_SCHEMA | VARCHAR | The name of the schema that contains the object that the storage lifecycle policy is attached to. |
| REF\_ENTITY\_NAME | VARCHAR | The name of the object that the storage lifecycle policy is attached to. |
| REF\_ENTITY\_DOMAIN | VARCHAR | The domain (type) of the object that the storage lifecycle policy is attached to; for example, Table. |
| STATE | VARCHAR | The aggregated state of the storage lifecycle policy execution: SUCCEEDED or FAILED (completed executions only). |
| START\_TIME | TIMESTAMP\_LTZ | Earliest timestamp of when any task in the storage lifecycle policy execution started. |
| END\_TIME | TIMESTAMP\_LTZ | Latest timestamp of when any task in the storage lifecycle policy execution completed. |
| EXECUTION\_RESULT | VARIANT | JSON object containing detailed results for each task type in the storage lifecycle policy execution. The object can be of type EXPIRE, ARCHIVE, or EXPIRE\_ARCHIVE ARCHIVE. Each nested object contains: start\_time, end\_time, state, and error details. |
| POLICY\_BODY | VARCHAR | The body of the storage lifecycle policy. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).

- The view contains historical data for the past 12 months (one year).
- The view only shows completed policy executions. It doesn’t include queued, currently executing, or cancelled policy executions.
