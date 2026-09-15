Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# QUERY\_INSIGHTS view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view displays a row for each [insight produced for a query](/user-guide/query-insights) across the accounts in your organization. It contains the same data as the [QUERY\_INSIGHTS view](/sql-reference/account-usage/query_insights) in the ACCOUNT\_USAGE schema, additionally aggregated at the organization level.

This view is available only in the [organization account](/user-guide/organization-accounts). Users with the GLOBALORGADMIN role, or users granted the SNOWFLAKE.ORGANIZATION\_GOVERNANCE\_VIEWER application role, can access it. For details, see [Accessing the ORGANIZATION\_USAGE schema](/sql-reference/organization-usage#label-org-usage-access-org-account).

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
| START\_TIME | TIMESTAMP\_LTZ | Start time of the query. |
| END\_TIME | TIMESTAMP\_LTZ | End time of the query. |
| TOTAL\_ELAPSED\_TIME | NUMBER | Total elapsed time of the query (in milliseconds). |
| QUERY\_ID | VARCHAR | Internal/system-generated identifier for the SQL statement. |
| QUERY\_HASH | VARCHAR | The [hash value](/user-guide/query-hash#label-query-hash) computed based on the canonicalized SQL text. |
| QUERY\_PARAMETERIZED\_HASH | VARCHAR | The [hash value](/user-guide/query-hash#label-query-parameterized-hash) computed based on the parameterized query. |
| WAREHOUSE\_ID | NUMBER | Internal/system-generated identifier for the warehouse that was used. |
| WAREHOUSE\_NAME | VARCHAR | Warehouse that the query executed on, if any. |
| INSIGHT\_INSTANCE\_ID | NUMBER | Internal/system-generated identifier for the insight. |
| INSIGHT\_TYPE\_ID | VARCHAR | Identifier of the [insight type](/user-guide/query-insights#label-query-insights-types). |
| MESSAGE | VARIANT | Structured information and details about the insight. |
| SUGGESTIONS | ARRAY | Array of strings, each containing a recommended action for the insight. |
| IS\_OPPORTUNITY | BOOLEAN | If `true`, the insight includes suggestions to improve query performance. |
| INSIGHT\_TOPIC | VARCHAR | Label that identifies the type of performance impact detected by this insight. For the list of labels, see [Insight topics](/sql-reference/account-usage/query_insights#insight-topics). |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 210 minutes (3.5 hours).
- The data is retained for 365 days (1 year).

## Examples

For example queries, see the [QUERY\_INSIGHTS view](/sql-reference/account-usage/query_insights#examples) in the ACCOUNT\_USAGE schema. To find organization-level information, replace `SNOWFLAKE.ACCOUNT_USAGE` with `SNOWFLAKE.ORGANIZATION_USAGE` in the queries.
