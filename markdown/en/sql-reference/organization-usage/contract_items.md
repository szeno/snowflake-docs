Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# CONTRACT\_ITEMS view

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

The CONTRACT\_ITEMS view in the ORGANIZATION\_USAGE schema can be used to return the contract information for an organization.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| CONTRACT\_NUMBER | VARCHAR | Snowflake contract number for the organization. |
| START\_DATE | DATE | The start date for the Snowflake contract or the date the CONTRACT\_ITEM goes into effect for the organization. |
| END\_DATE | DATE | The end date for the Snowflake contract or the date the CONTRACT\_ITEM stops being used for the organization. |
| EXPIRATION\_DATE | DATE | The expiration date for the Snowflake contract or the date after which either the Renewal Contract goes into effect if signed within 30 days or the Snowflake relationship is terminated. |
| CONTRACT\_ITEM | VARCHAR | One of capacity, additional capacity, or free usage. |
| CURRENCY | VARCHAR | The currency for the CONTRACT\_ITEM. |
| AMOUNT | NUMBER (38,2) | The amount for the CONTRACT\_ITEM measured in CURRENCY, not credits. |
| CONTRACT\_MODIFIED\_DATE | DATE | The date (in the UTC timezone) the CONTRACT\_ITEM was last modified. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours.
- If multiple organizations draw down from the same capacity contract, only the primary organization can access this view. The primary
  organization is also known as the funding organization.
- This view shows only the active contract for the organization.
- Customers who signed a contract through a Snowflake reseller cannot access data in this view.
- Data is retained indefinitely.
- This view does not include data generated prior to June 2020. To obtain data before this date, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).
