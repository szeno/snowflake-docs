Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# DATABASE\_STORAGE\_USAGE\_HISTORY view

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

The DATABASE\_STORAGE\_USAGE\_HISTORY view in the ORGANIZATION\_USAGE schema
can be used to query the average daily storage usage, in bytes, for all the
databases in your organization within a specified date range. The results
include:

- All data stored in tables and materialized views in the database(s).
- All historical data maintained in Fail-safe for the database(s).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization where the usage took place. |
| ACCOUNT\_NAME | VARCHAR | Name of the account where the usage took place. |
| ACCOUNT\_LOCATOR | VARCHAR | Name of the account locator. |
| REGION | VARCHAR | Name of the region where the account is located. |
| USAGE\_DATE | DATE | Date (in the UTC time zone) of this storage usage record. |
| DATABASE\_NAME | VARCHAR | Name of the database. |
| AVERAGE\_DATABASE\_BYTES | FLOAT | Number of bytes of database storage used, including bytes currently in Time Travel. |
| AVERAGE\_FAILSAFE\_BYTES | FLOAT | Number of bytes of Fail-safe storage used. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the database was dropped; NULL for active databases. |
| AVERAGE\_HYBRID\_TABLE\_STORAGE\_BYTES | FLOAT | Number of bytes of hybrid table storage used (data in the row store). |
| AVERAGE\_ARCHIVE\_STORAGE\_COOL\_BYTES | FLOAT | Average number of bytes (including active bytes, time travel bytes, and bytes subject to [minimum storage duration charges](/user-guide/storage-management/storage-lifecycle-policies-billing#label-slp-billing-penalty-bytes)) of table storage used in the COOL storage tier. |
| AVERAGE\_ARCHIVE\_STORAGE\_COLD\_BYTES | FLOAT | Average number of bytes (including active bytes, time travel bytes, and bytes subject to [minimum storage duration charges](/user-guide/storage-management/storage-lifecycle-policies-billing#label-slp-billing-penalty-bytes)) of table storage used in the COLD storage tier. |
| AVERAGE\_COOL\_FAILSAFE\_BYTES | FLOAT | Average number of bytes of Fail-safe storage used in the COOL storage tier. |
| AVERAGE\_COLD\_FAILSAFE\_BYTES | FLOAT | Average number of bytes of Fail-safe storage used in the COLD storage tier. |

Expand

Show lessSee more

## Usage notes

Latency for the view may be up to 24 hours (1 day).

Note

With [BCR-2127](/release-notes/bcr-bundles/2025_07/bcr-2127),
this view includes new columns for storage lifecycle policies.
To view storage lifecycle policy columns, you must enable the 2025\_07 behavior change bundle
in your account.

To [enable this bundle in your account](/release-notes/bcr-bundles/managing-behavior-change-releases#label-manage-bcr-enable-bundle),
execute the following statement:

Copy code

```
SELECT SYSTEM$ENABLE_BEHAVIOR_CHANGE_BUNDLE('2025_07');
```
