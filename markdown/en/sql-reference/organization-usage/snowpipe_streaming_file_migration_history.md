[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# SNOWPIPE\_STREAMING\_FILE\_MIGRATION\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view can be used to query the history of data migrated into Snowflake tables using [Snowpipe Streaming](/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview) within the last 365 days (1 year). The view displays the number of rows and bytes migrated and credits used for migration billed for accounts in your organization.

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
| START\_TIME | TIMESTAMP\_LTZ | Start of the time (in the local time zone) range in which data migration took place. |
| END\_TIME | TIMESTAMP\_LTZ | End of the time (in the local time zone) range in which data migration took place. |
| CREDITS\_USED | FLOAT | Number of credits billed for Snowpipe Streaming data migration during the START\_TIME and END\_TIME window. |
| NUM\_BYTES\_MIGRATED | NUMBER | Number of bytes migrated during the START\_TIME and END\_TIME window. |
| NUM\_ROWS\_MIGRATED | NUMBER | Number of rows migrated during the START\_TIME and END\_TIME window. |
| TABLE\_ID | NUMBER | Internal/system-generated identifier for the target table that the Snowpipe Streaming client loads data into. |
| TABLE\_NAME | VARCHAR | The name of the target table that the Snowpipe Streaming client loads data into. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema that the target table belongs to. |
| SCHEMA\_NAME | VARCHAR | The name of the schema that the target table belongs to. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database that the target table belongs to. |
| DATABASE\_NAME | VARCHAR | The name of the database that the target table belongs to. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 14 hours.

- Note that file migration sometimes may be pre-empted by clustering or other DML operations. Migration may not always occur and therefore the migration history will be empty even after 12 hours.
- The NUM\_BYTES\_MIGRATED and NUM\_ROWS\_MIGRATED columns only show the number of bytes and rows processed during the migration process. These numbers may not equal the actual numbers of rows and bytes inserted by Snowpipe Streaming to the table because some rows and bytes are processed outside of the migration process due to clustering or other DML operations.

  For example, Snowpipe Streaming inserts 1M rows and the table has 1M rows, but the NUM\_ROWS\_MIGRATED column in the migration history view only shows 800K rows. This is because the other 200K rows are processed outside of the migration process.
