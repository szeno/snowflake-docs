Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# EXTERNAL\_ACCESS\_HISTORY view

This Account Usage view can be used to query the history of external access performed by procedure or UDF handler code within the last
365 days (1 year).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| QUERY\_ID | TEXT | ID of the query or job that called the UDF or procedure performing external access. |
| HOSTNAMES | TEXT | Name of the hosts accessed. |
| STATUS | TEXT | Status of the attempt to connect to the external location. One of the following values:   - `Success` if the connection was successful - `Deny` if the connection was denied |
| IP | VARCHAR | IP address for the external network location. |
| SOURCE\_CLOUD | TEXT | Name of the cloud provider where the data transfer originated. One of the following:   - `aws` - `gcp` - `azure` |
| SOURCE\_REGION | TEXT | Region where the data transfer originated. |
| TARGET\_CLOUD | TEXT | Name of the cloud provider to which the data was sent. One of the following:   - `aws` - `gcp` - `azure` - `internet` (for regions not on a cloud provider) |
| TARGET\_REGION | TEXT | Region to which the data was sent. `internet` for regions not on a cloud provider. |
| SENT\_BYTES | VARIANT | Number of bytes sent to the external endpoint. |
| RECEIVED\_BYTES | VARIANT | Number of bytes received from the external endpoint. |

Expand

Show lessSee more

## Usage notes

General notes:

- Each row in the view represents a single IP address that the procedure or UDF accesses. As a result, there might be multiple
  rows with different IP addresses, but with the same query ID. There might also be multiple hostnames mapped to the same IP
  address.
- Latency for the view might be up to 180 minutes (3 hours).
