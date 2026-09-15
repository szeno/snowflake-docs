Feature — Generally Available

Not available in government regions.

Schemas:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# INGRESS\_NETWORK\_ACCESS\_HISTORY view

This Account Usage view can be used to query any network access attempts to your Snowflake account within the last 365 days (1 year).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| EVENT\_TIMESTAMP | TIMESTAMP\_LTZ | Time, (in the UTC time zone) of the ingress event occurrence. |
| REQUEST\_ID | VARCHAR | Ingress request ID. |
| REQUEST METHOD | VARCHAR. | Ingress request method, such as GET or POST. |
| REQUEST PATH | VARCHAR | Ingress request path. |
| USER\_NAME | VARCHAR. | User associated with this event. |
| CLIENT\_IP | VARCHAR | Client IP address. This value can be an IPv4 or IPv6 address. |
| CLIENT\_PRIVATELINK\_ID | VARCHAR | Client private link ID. |
| BYTES\_RX | NUMBER | Bytes transferred into Snowflake. |
| BYTES\_TX | NUMBER | Bytes transferred out of Snowflake. |
| IS\_SUCCESS | BOOLEAN | Whether the user’s request was successful or not. |
| ERROR\_CODE | VARCHAR | Error code, if the request was not successful. |
| ERROR\_MESSAGE | VARCHAR | Error message returned to the user, if the request was not successful. |
| JOB\_UUID | VARCHAR | Number automatically assigned to a query job. |
| REQUEST\_AUTHORITY | VARCHAR | The URL that a client used to access a Snowflake ingress location. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 240 minutes (4 hours).

- Although the [INTERNAL\_STAGE\_NETWORK\_ACCESS\_HISTORY view](/sql-reference/account-usage/internal_stage_network_access_history) is user-enabled, the INGRESS\_NETWORK\_ACCESS\_HISTORY view is enabled by default
  in your Snowflake account.
