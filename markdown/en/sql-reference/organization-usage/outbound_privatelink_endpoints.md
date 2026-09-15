Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# OUTBOUND\_PRIVATELINK\_ENDPOINTS view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view displays one row for each private endpoint that has
been created for
[outbound private connectivity](/user-guide/private-connectivity-outbound)
in an account.

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
| PROVIDER\_RESOURCE\_ID | VARCHAR | Identifier of the AWS service or the Microsoft Azure resource that the endpoint connects to. |
| HOSTNAME | VARCHAR | Hostname of the AWS service or Microsoft Azure resource that the endpoint connects to. |
| SUBRESOURCE | VARCHAR | Subresource of the Microsoft Azure resource that the endpoint connects to. Endpoints for AWS do not have a subresource. |
| SNOWFLAKE\_RESOURCE\_ID | VARCHAR | Identifier of the private endpoint that connects to the AWS service or Microsoft Azure resource. For AWS, this is the VPCE\_ID of the endpoint. For Microsoft Azure, this is the resource ID of the endpoint. |
| ENDPOINT\_STATE | VARCHAR | Current state of the endpoint. One of the following:   - `PENDING_CREATION`: The endpoint is still being created. - `CREATED`: The endpoint is created and ready to use. This state indicates that Snowflake received a response from the cloud provider   about the endpoint being successfully created. - `FAILED`: The endpoint is in an unexpected state on the cloud provider, and cannot be used. - `PENDING_DELETION`: The endpoint is on the deletion queue, but can be restored. - `DELETING`: The endpoint is being deleted on the cloud provider and cannot be restored. |
| CREATED\_ON | TIMESTAMP\_LTZ | Date and time when the endpoint was created. |
| LAST\_ALTERED\_ON | TIMESTAMP\_LTZ | Date and time when the endpoint state last changed. |
| DELETED\_ON | TIMESTAMP\_LTZ | Date and time when the endpoint was deleted. NULL if an endpoint has not been deleted, including deprovisioned endpoints that haven’t been deleted yet. |

Expand

Show lessSee more

## Usage notes

- Latency for this view might be up to 2 hours.
- Data for deleted endpoints is retained for 1 year.
- For endpoints created during the preview of outbound private connectivity
  (before November 2024), values in the LAST\_ALTERED\_ON column might be the
  time at which the data became available in the OUTBOUND\_PRIVATELINK\_ENDPOINTS
  view, not the creation times of the endpoints.
