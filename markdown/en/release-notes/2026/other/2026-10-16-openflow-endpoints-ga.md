# Oct 16, 2026: Openflow Endpoints (*General availability*)

With this release, Openflow endpoints are now generally available for Snowflake deployments and Bring Your Own Cloud (BYOC) deployments. You can create stable HTTPS URLs that route external HTTP requests to Listen processors in your Openflow runtimes.

With Openflow endpoints, you can do the following:

- Expose a stable endpoint URL for a custom flow that uses a compatible HTTP Listen processor, such as ListenHTTP or ListenOTLP.
- Send data from an external HTTP client into an Openflow runtime without reconfiguring the client when the target runtime or processor changes inside the deployment.
- Authenticate requests with a Snowflake service user programmatic access token (PAT).
- Manage endpoint creation, attachment, and deletion from the Openflow control plane UI.

Openflow endpoints require the following minimum Openflow deployment versions:

- Snowflake Deployments (SPCS): 1.53
- BYOC deployments: 1.70.0

For more information, see [Openflow Endpoints](/user-guide/data-integration/openflow/openflow-endpoints).
