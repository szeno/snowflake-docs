Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# OUTBOUND\_PRIVATELINK\_ENDPOINTS view

This Account Usage view displays one row for each private endpoint that has been created for
[outbound private connectivity](/user-guide/private-connectivity-outbound).

## Columns

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
- Users with the SECURITY\_VIEWER database role can access this view.
- Data for deleted endpoints is retained for 1 year.
- For endpoints created during the preview of the outbound private connectivity feature (before November 2024), values in the
  LAST\_ALTERED\_ON column might be the time at which the data became available in the OUTBOUND\_PRIVATELINK\_ENDPOINTS view, not the creation
  times of the endpoints.
