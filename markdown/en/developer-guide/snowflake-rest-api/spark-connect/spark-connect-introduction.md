# Manage Spark Connect

Feature — Generally Available

Not available in government regions.

The Snowflake REST [Spark Connect API](/developer-guide/snowflake-rest-api/reference/spark-connect.html) provides the following endpoints to manage Spark Connect:

**Snowflake REST Spark Connect API endpoints**

| Endpoint | Description |
| --- | --- |
| `POST /api/v2/spark-connect/execute-plan` | Executes a request that contains the query and returns a stream of [[ExecutePlanResponse]]. |
| `POST /api/v2/spark-connect/analyze-plan` | Analyzes a query and return a [[AnalyzeResponse]] containing metadata about the query. |
| `POST /api/v2/spark-connect/config` | Updates or fetches the configurations and returns a [[ConfigResponse]] containing the result. |
| `POST /api/v2/spark-connect/add-artifacts` | Add artifacts to the session and returns a [[AddArtifactsResponse]] containing metadata about the added artifacts. |
| `POST /api/v2/spark-connect/push-response` | Pushes Spark response to the GS. |
| `POST /api/v2/spark-connect/pull-request` | Pulls Spark request from the GS. |
| `POST /api/v2/spark-connect/release-execute` | Releases a re-attachable execution, or parts thereof. |
| `POST /api/v2/spark-connect/reattach-execute` | Reattaches to an existing re-attachable execution, or parts thereof. |
| `POST /api/v2/spark-connect/interrupt` | Interrupts running executions. |
| `POST /api/v2/spark-connect/artifact-status` | Check statuses of artifacts in the session and returns them in a [[ArtifactStatusesResponse]]. |

Expand

Show lessSee more

For reference documentation, see [Snowflake Spark Connect API reference](/developer-guide/snowflake-rest-api/reference/spark-connect.html).
