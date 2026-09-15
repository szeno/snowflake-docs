Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# INTERNAL\_DATA\_TRANSFER\_HISTORY view

Use this view to get a historical view of Snowpark Container Services internal data transfers in your account for the last 365 days.

This view reports the following two types of internal data transfers:

- **SERVICE\_FUNCTION:** When a [service function](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-service-communicating) is invoked, it sends a request to its associated service. Note that the query invoking the service functions executes in a warehouse, while the service runs in a compute pool. There is an internal data transfer cost associated with it. The view captures any data exchanged during the request and response as an internal data transfer of the SERVICE\_FUNCTION type.
- **COMPUTE\_POOL:** Through [service-to-service communication](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-service-communicating-service-to-service), a service can transfer data to another service running in a different compute pool. This incurs internal data transfer costs, which the view reports as data transfer cost with the COMPUTE\_POOL transfer type.

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | The date and beginning of the hour (in the local time zone) in which the data transfer took place. |
| END\_TIME | TIMESTAMP\_LTZ | The date and end of the hour (in the local time zone) in which the data transfer took place. |
| TRANSFER\_TYPE | VARCHAR | It is either `SERVICE_FUNCTION` or `COMPUTE_POOL`. |
| COMPUTE\_POOL\_NAME | VARCHAR | If the transfer type is `SERVICE_FUNCTION`, it represents the name of the compute pool that the service function interacts with. If the transfer type is `COMPUTE_POOL`, it represents the source compute pool that initiated the traffic. |
| BYTES\_TRANSFERRED | NUMBER | Number of bytes transferred during the START\_TIME and END\_TIME window. |

Expand

Show lessSee more

## Usage notes

- Latency for the view can be up to 180 minutes (3 hours).
