Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# QUERY\_ATTRIBUTION\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view can be used to determine the compute cost of a given query run on warehouses in your organization.

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
| QUERY\_ID | VARCHAR | Internal/system-generated identifier for the SQL statement. |
| PARENT\_QUERY\_ID | VARCHAR | Query ID of the parent query or NULL if the query does not have a parent. |
| ROOT\_QUERY\_ID | VARCHAR | Query ID of the topmost query in the chain or NULL if the query does not have a parent. |
| WAREHOUSE\_ID | NUMBER | Internal/system-generated identifier for the warehouse that the query was executed on. |
| WAREHOUSE\_NAME | VARCHAR | Name of the warehouse that the query executed on. |
| QUERY\_HASH | VARCHAR | The [hash value](/user-guide/query-hash#label-query-hash) computed based on the canonicalized SQL text. |
| QUERY\_PARAMETERIZED\_HASH | VARCHAR | The [hash value](/user-guide/query-hash#label-query-parameterized-hash) computed based on the parameterized query. |
| QUERY\_TAG | VARCHAR | Query tag set for this statement through the [QUERY\_TAG](/sql-reference/parameters#label-query-tag) session parameter. |
| USER\_NAME | VARCHAR | User who issued the query. |
| START\_TIME | TIMESTAMP\_LTZ | Time when query execution started (in the local time zone). |
| END\_TIME | TIMESTAMP\_LTZ | Time when query execution ended (in the local time zone). |
| CREDITS\_ATTRIBUTED\_COMPUTE | FLOAT | Number of credits attributed to this query. Includes only the credit usage for the query execution and doesn’t include any warehouse idle time. |
| CREDITS\_USED\_QUERY\_ACCELERATION | FLOAT | Number of credits consumed by the [Query Acceleration Service](/user-guide/query-acceleration-service) to accelerate the query. NULL if the query is not accelerated.     The total cost for an accelerated query is the sum of this column and the CREDITS\_ATTRIBUTED\_COMPUTE column. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).
- This view doesn’t include records for jobs executed by [Adaptive Warehouses](/user-guide/warehouses-adaptive).
- The QUERY\_ATTRIBUTE\_HISTORY view in the ACCOUNT\_USAGE schema contains most of the same columns as the QUERY\_ATTRIBUTE\_HISTORY view in the ORGANIZATION\_USAGE schema. For sample queries against the ACCOUNT\_USAGE view, see [Examples](/sql-reference/account-usage/query_attribution_history#label-query-attribution-history-examples). Simply replace SNOWFLAKE.ACCOUNT\_USAGE with SNOWFLAKE.ORGANIZATION\_USAGE in the queries to find organization-level information.
