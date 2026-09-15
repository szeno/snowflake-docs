Feature — Generally Available

Support for this feature is available only to Business Critical Edition (or higher) accounts hosted on AWS.
This feature is not available in Government Regions or in the People’s Republic of China.

Schemas:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# INTERNAL\_STAGE\_NETWORK\_ACCESS\_HISTORY view

This Account Usage view can be used to query any network access attempts to an internal stage within the last 365 days (1 year).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| EVENT\_TIMESTAMP | TIMESTAMP\_LTZ | Cloud service provider event timestamp. |
| EVENT\_ID | VARCHAR | Cloud service provider event ID. |
| EVENT\_NAME | VARCHAR | Cloud service provider event name. |
| EVENT\_TYPE | VARCHAR | Cloud service provider event type. |
| CLOUD\_PROVIDER | VARCHAR | Cloud service provider. |
| USER\_NAME | VARCHAR | User associated with this event. |
| CLIENT\_IP | VARCHAR | Client IP accessing the internal stage. |
| CLIENT\_PRIVATELINK\_ID | VARCHAR | Client private link ID accessing the internal stage: for example, a VPCE ID. |
| BYTES\_IN | NUMBER | Bytes transferred into the stage. |
| BYTES\_OUT | NUMBER | Bytes transferred out of the stage. |
| IS\_SUCCESS | BOOLEAN | Whether the user’s request was successful or not. |
| ERROR\_CODE | VARCHAR | Error code, if the request was not successful. |
| ERROR\_MESSAGE | VARCHAR | Error message returned to the user, if the request was not successful. |
| AUTHENTICATION\_METHOD | VARCHAR | Cloud service provider authentication method, such as `AuthHeader` or `QueryString`. |
| STAGE\_PATH | VARCHAR | Network directory path for the internal stage location. For example, the path appearing after the AWS bucket name in the URL. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 360 minutes (6 hours).
- To enable the view in your account, call the [SYSTEM$OPT\_IN\_INTERNAL\_STAGE\_NETWORK\_LOGS](/sql-reference/functions/system_opt_in_internal_stage_network_logs) function.
- To disable the view in your account, call the [SYSTEM$OPT\_OUT\_INTERNAL\_STAGE\_NETWORK\_LOGS](/sql-reference/functions/system_opt_out_internal_stage_network_logs) function.

- Network access record collection starts at the time you enable the view.
- Network access records are retained for 1 year, starting at the time you enable the view.
