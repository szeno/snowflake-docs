Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# EXTERNAL\_ACCESS\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

The EXTERNAL\_ACCESS\_HISTORY view in the ORGANIZATION\_USAGE schema can be used to query the history of external access performed by procedure or UDF handler code across accounts in your organization within the last 365 days (1 year).

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
| QUERY\_ID | TEXT | ID of the query or job that called the UDF or procedure performing external access. |
| HOSTNAMES | TEXT | Host names accessed, returned as a JSON array. |
| STATUS | TEXT | Status of the attempt to connect to the external location. One of the following values:   - `SUCCESS` if the connection was successful - `DENY` if the connection was denied |
| IP | TEXT | IP address for the external network location. |
| SOURCE\_CLOUD | TEXT | Name of the cloud provider where the data transfer originated. One of the following:   - `aws` - `gcp` - `azure` |
| SOURCE\_REGION | TEXT | Region where the data transfer originated. |
| TARGET\_CLOUD | TEXT | Name of the cloud provider to which the data was sent. One of the following:   - `aws` - `gcp` - `azure` - `internet` (for regions not on a cloud provider) |
| TARGET\_REGION | TEXT | Region to which the data was sent. `internet` for regions not on a cloud provider. |
| SENT\_BYTES | NUMBER | Number of bytes sent to the external endpoint. |
| RECEIVED\_BYTES | NUMBER | Number of bytes received from the external endpoint. |

Expand

Show lessSee more

## Usage notes

- Each row in the view represents a single IP address that the procedure or UDF accesses. As a result, there might be multiple
  rows with different IP addresses, but with the same query ID. There might also be multiple hostnames mapped to the same IP
  address.
- Latency for the view may be up to 180 minutes (3 hours).
- The data is retained for 365 days (1 year).

## Examples

Retrieve denied external access attempts:

> Copy code
>
> ```
> SELECT account_name, query_id, hostnames, ip, sent_bytes, received_bytes
>   FROM snowflake.organization_usage.external_access_history
>   WHERE status = 'DENY'
>   LIMIT 10;
> ```
