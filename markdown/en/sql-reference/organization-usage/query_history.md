Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# QUERY\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view can be used to query Snowflake query history by various dimensions (time range, session, user, warehouse, etc.) within the last 365 days (1 year).

The view is available in both the ORGANIZATION\_USAGE and READER\_ACCOUNT\_USAGE schemas with the following differences:

- The following columns are available *only* in the reader account view:
  - READER\_ACCOUNT\_NAME
  - READER\_ACCOUNT\_DELETED\_ON

Alternatively, you can call the Information Schema table function, also named QUERY\_HISTORY. See the
[description of the QUERY\_HISTORY function](/sql-reference/functions/query_history).

See also:

> [QUERY\_HISTORY , QUERY\_HISTORY\_BY\_\*](/sql-reference/functions/query_history) (Information Schema table function),
> [Monitor query activity with Query History](/user-guide/ui-snowsight-activity) (Snowsight dashboard),
> [Use the Grouped Query History view in Snowsight](/user-guide/ui-snowsight-activity#label-snowsight-grouped-query-history)

## Columns

**Organization-level columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| `organization_name` | VARCHAR | Name of the organization. |
| `account_locator` | VARCHAR | System-generated identifier for the account. |
| `account_name` | VARCHAR | User-defined identifier for the account. |

Expand

Show lessSee more

**Additional columns**

The *Available only in reader account usage views* column in the following table indicates whether the QUERY\_HISTORY column is available in the
[READER\_ACCOUNT\_USAGE](/sql-reference/account-usage) schema.

| Column Name | Data Type | Description | Available only in reader account usage views |
| --- | --- | --- | --- |
| `reader_account_name` | VARCHAR | Name of the reader account in which the SQL statement was executed. | ✔ |
| `query_id` | VARCHAR | Internal/system-generated identifier for the SQL statement. | ✔ |
| `query_text` | VARCHAR | Text of the SQL statement. The limit is 100K characters. Longer SQL statements are truncated. |  |
| `database_id` | NUMBER | Internal/system-generated identifier for the database that was in use. | ✔ |
| `database_name` | VARCHAR | Database that was specified in the context of the query at compilation. | ✔ |
| `schema_id` | NUMBER | Internal/system-generated identifier for the schema that was in use. | ✔ |
| `schema_name` | VARCHAR | Schema that was specified in the context of the query at compilation. | ✔ |
| `query_type` | VARCHAR | DML, query, etc. If the query failed, then the query type may be UNKNOWN. |  |
| `session_id` | NUMBER | Session that executed the statement. | ✔ |
| `authn_event_id` | NUMBER | ID for the event for the authentication of the user for this query. This ID corresponds to the value in the `event_id` column in the [LOGIN\_HISTORY](/sql-reference/account-usage/login_history) view. |  |
| `user_name` | VARCHAR | User who issued the query. |  |
| `role_name` | VARCHAR | Role that was active in the session at the time of the query. | ✔ |
| `warehouse_id` | NUMBER | Internal/system-generated identifier for the warehouse that was used. | ✔ |
| `warehouse_name` | VARCHAR | Warehouse that the query executed on, if any. | ✔ |
| `warehouse_size` | VARCHAR | Size of the warehouse when this statement executed. | ✔ |
| `warehouse_type` | VARCHAR | Type of the warehouse when this statement executed. | ✔ |
| `cluster_number` | NUMBER | The cluster (in a multi-cluster warehouse) that this statement executed on. | ✔ |
| `query_tag` | VARCHAR | Query tag set for this statement through the QUERY\_TAG session parameter. | ✔ |
| `execution_status` | VARCHAR | Execution status for the query. Valid values: `success`, `fail`, `incident`. | ✔ |
| `error_code` | NUMBER | Error code, if the query returned an error. | ✔ |
| `error_message` | VARCHAR | Error message, if the query returned an error. The limit is 5K characters. Longer error messages are truncated. | ✔ |
| `start_time` | TIMESTAMP\_LTZ | Statement start time (in the local time zone). | ✔ |
| `end_time` | TIMESTAMP\_LTZ | Statement end time (in the local time zone). | ✔ |
| `total_elapsed_time` | NUMBER | Elapsed time (in milliseconds). | ✔ |
| `bytes_scanned` | NUMBER | Number of bytes scanned by this statement. | ✔ |
| `percentage_scanned_from_cache` | FLOAT | Percentage of data scanned from the local disk cache. The value ranges from 0.0 to 1.0. Multiply by 100 to get a true percentage. |  |
| `bytes_written` | NUMBER | Number of bytes written (for example, when loading into a table). |  |
| `bytes_written_to_result` | NUMBER | Number of bytes written to a result object. For example, `SELECT * FROM ...` would produce a set of results in tabular format representing each field in the selection.     In general, the results object represents whatever is produced as a result of the query, and `bytes_written_to_result` represents the size of the returned result. |  |
| `bytes_read_from_result` | NUMBER | Number of bytes read from a result object. |  |
| `rows_produced` | NUMBER | The number of rows produced by this statement. The `rows_produced` column will be deprecated in a future release. The value in the `rows_produced` column doesn’t always reflect the logical number of rows affected by a query. Snowflake recommends using the `rows_inserted`, `rows_updated`, `rows_written_to_result`, or `rows_deleted` columns instead. | ✔ |
| `rows_inserted` | NUMBER | Number of rows inserted by the query. |  |
| `rows_updated` | NUMBER | Number of rows updated by the query. |  |
| `rows_deleted` | NUMBER | Number of rows deleted by the query. |  |
| `rows_unloaded` | NUMBER | Number of rows unloaded during data export. |  |
| `bytes_deleted` | NUMBER | Number of bytes deleted by the query. |  |
| `partitions_scanned` | NUMBER | Number of micro-partitions scanned. |  |
| `partitions_total` | NUMBER | Total micro-partitions of all tables included in this query. |  |
| `bytes_spilled_to_local_storage` | NUMBER | Volume of data spilled to local disk. |  |
| `bytes_spilled_to_remote_storage` | NUMBER | Volume of data spilled to remote disk. |  |
| `bytes_sent_over_the_network` | NUMBER | Volume of data sent over the network. |  |
| `compilation_time` | NUMBER | Compilation time (in milliseconds). | ✔ |
| `execution_time` | NUMBER | Execution time (in milliseconds). | ✔ |
| `queued_provisioning_time` | NUMBER | Time (in milliseconds) spent in the warehouse queue, waiting for the warehouse compute resources to provision, due to warehouse creation, resume, or resize. | ✔ |
| `queued_repair_time` | NUMBER | Time (in milliseconds) spent in the warehouse queue, waiting for compute resources in the warehouse to be repaired. | ✔ |
| `queued_overload_time` | NUMBER | Time (in milliseconds) spent in the warehouse queue, due to the warehouse being overloaded by the current query workload. | ✔ |
| `transaction_blocked_time` | NUMBER | Time (in milliseconds) spent blocked by a concurrent DML. | ✔ |
| `outbound_data_transfer_cloud` | VARCHAR | Target cloud provider for statements that unload data to another region and/or cloud. | ✔ |
| `outbound_data_transfer_region` | VARCHAR | Target region for statements that unload data to another region and/or cloud. | ✔ |
| `outbound_data_transfer_bytes` | NUMBER | Number of bytes transferred in statements that unload data from Snowflake tables. | ✔ |
| `inbound_data_transfer_cloud` | VARCHAR | Source cloud provider for statements that load data from another region and/or cloud. | ✔ |
| `inbound_data_transfer_region` | VARCHAR | Source region for statements that load data from another region and/or cloud. | ✔ |
| `inbound_data_transfer_bytes` | NUMBER | Number of bytes transferred in a replication operation from another account. The source account could be in the same region or a different region than the current account. | ✔ |
| `list_external_files_time` | NUMBER | Time (in milliseconds) spent listing external files. |  |
| `credits_used_cloud_services` | NUMBER | Number of credits used for cloud services. This value does not take into account the [adjustment for cloud services](/user-guide/cost-understanding-compute#label-understanding-billing-for-cloud-services-usage), and may therefore be greater than the credits that are billed. To determine how many credits were actually billed, run queries against the [metering daily history](/sql-reference/organization-usage/metering_daily_history). | ✔ |
| `reader_account_deleted_on` | TIMESTAMP\_LTZ | Time and date (in the UTC time zone) when the reader account is deleted. | ✔ |
| `release_version` | VARCHAR | Release version in the format of `major_release.minor_release.patch_release`. |  |
| `external_function_total_invocations` | NUMBER | The aggregate number of times that this query called remote services. For important details, see the Usage Notes. |  |
| `external_function_total_sent_rows` | NUMBER | The total number of rows that this query sent in all calls to all remote services. |  |
| `external_function_total_received_rows` | NUMBER | The total number of rows that this query received from all calls to all remote services. |  |
| `external_function_total_sent_bytes` | NUMBER | The total number of bytes that this query sent in all calls to all remote services. |  |
| `external_function_total_received_bytes` | NUMBER | The total number of bytes that this query received from all calls to all remote services. |  |
| `query_load_percent` | NUMBER | The approximate percentage of active compute resources in the warehouse for this query execution. |  |
| `is_client_generated_statement` | BOOLEAN | Indicates whether the query was client-generated. |  |
| `query_acceleration_bytes_scanned` | NUMBER | Number of bytes scanned by the [query acceleration service](/user-guide/query-acceleration-service). |  |
| `query_acceleration_partitions_scanned` | NUMBER | Number of partitions scanned by the query acceleration service. |  |
| `query_acceleration_upper_limit_scale_factor` | NUMBER | Upper limit [scale factor](/user-guide/query-acceleration-service#label-query-acceleration-scale-factor) that a [query would have benefited from](/user-guide/query-acceleration-service). |  |
| `transaction_id` | NUMBER | [ID of the transaction](/sql-reference/transactions#label-transaction-id) that contains the statement or 0 if the statement is not executed within a transaction. |  |
| `child_queries_wait_time` | NUMBER | Time (in milliseconds) to complete the cached lookup when calling a [memoizable function](/developer-guide/udf/sql/udf-sql-scalar-functions#label-udf-sql-scalar-memoizable). |  |
| `role_type` | VARCHAR | Specifies whether an APPLICATION, DATABASE\_ROLE, or ROLE executed the query. |  |
| `query_hash` | VARCHAR | The [hash value](/user-guide/query-hash#label-query-hash) computed based on the canonicalized SQL text. |  |
| `query_hash_version` | NUMBER | The [version of the logic](/user-guide/query-hash#label-query-hash-version) used to compute `QUERY_HASH`. |  |
| `query_parameterized_hash` | VARCHAR | The [hash value](/user-guide/query-hash#label-query-parameterized-hash) computed based on the parameterized query. |  |
| `query_parameterized_hash_version` | NUMBER | The [version of the logic](/user-guide/query-hash#label-query-hash-version) used to compute `QUERY_PARAMETERIZED_HASH`. |  |
| `secondary_role_stats` | VARCHAR | A JSON-formatted string that contains three fields regarding secondary roles that were evaluated in the query: a list of secondary roles or `ALL` depending on the session, a count of the number of secondary roles, and the internal/system-generated ID for each secondary role. The count and number of IDs have a maximum of 50. |  |
| `rows_written_to_result` | NUMBER | Number of rows written to a result object. For CREATE TABLE AS SELECT (CTAS) and all DML operations, this result is `1`. |  |
| `query_retry_time` | NUMBER | Total execution time (in milliseconds) for query retries caused by actionable errors. For more information, see [Query retry columns](#query-retry-columns). |  |
| `query_retry_cause` | VARCHAR | Error that caused the query to retry. If there is no query retry, the field is NULL. For more information, see [Query retry columns](#query-retry-columns). |  |
| `fault_handling_time` | NUMBER | Total execution time (in milliseconds) for query retries caused by errors that are *not* actionable. For more information, see [Query retry columns](#query-retry-columns). |  |
| `user_type` | VARCHAR | The type of the user executing the query. It’s the same as the `type` column in the [users](/sql-reference/organization-usage/users). If a Snowpark Container Services service executes the query, the user type is SNOWFLAKE\_SERVICE. |  |
| `user_database_name` | VARCHAR | When the value in the `user_type` column is SNOWFLAKE\_SERVICE, it specifies the service’s database name; otherwise, it’s NULL. |  |
| `user_database_id` | VARCHAR | When the value in the `user_type` column is SNOWFLAKE\_SERVICE, it specifies the internal, Snowflake-generated identifier for the service’s database; otherwise, it’s NULL. |  |
| `user_schema_name` | VARCHAR | When the value in the `user_type` column is SNOWFLAKE\_SERVICE, it specifies the service’s schema name; otherwise, it’s NULL. |  |
| `user_schema_id` | VARCHAR | When the value in the `user_type` column is SNOWFLAKE\_SERVICE, it specifies the internal, Snowflake-generated identifier for the service’s schema; otherwise, it’s NULL. |  |
| `bind_values` | ARRAY | Bind values in serialized form. If the query contains no bind values, then this column contains an empty array. If the array is too large or the [ALLOW\_BIND\_VALUES\_ACCESS](/sql-reference/parameters#label-allow-bind-values-access) parameter is set to `FALSE`, this column contains NULL. For more information, see [Retrieve bind variable values](/sql-reference/bind-variables#label-bind-variables-retrieving-values). |  |
| `agent_type` | VARCHAR | The type of agent that directly invoked the query. Possible values: `CORTEX_AGENT` (persistent, named [Cortex Agent](/user-guide/snowflake-cortex/cortex-agents)), `CORTEX_LITE_AGENT` (stateless, on-demand agent via the [REST API](/developer-guide/snowflake-rest-api/cortex-lite-agent/cortex-lite-agent-introduction) or Snowflake CoCo client), `EXTERNAL_AGENT` (external agent using a [SERVICE\_AGENT](/user-guide/admin-user-management#label-user-management-types) user type or a [custom OAuth integration](/user-guide/oauth-custom#configuring-agent-sessions) configured with `IS_AGENTIC = TRUE`). NULL if not invoked by an agent. |  |

Expand

Show lessSee more

## Usage notes

### General

- Latency for the view may be up to 180 minutes (3 hours).

- The values for the columns
  `external_function_total_invocations`, `external_function_total_sent_rows`,
  `external_function_total_received_rows`, `external_function_total_sent_bytes`, and `external_function_total_received_bytes`
  are affected by many factors, including:

  - The number of external functions in the SQL statement.
  - The number of rows per batch sent to each remote service.
  - The number of retries due to transient errors (for example, because a response was not received within the expected time).
- If you want to filter on client-generated query statements, use
  [QUERY\_HISTORY](/sql-reference/functions/query_history) (an Information Schema table function).
- Canceled queries are identified by their `error_message` text (`SQL execution canceled`), not by their `execution_status` value.

# Query retry columns

A query might need to be retried one or more times in order to successfully complete. There can be multiple causes that result in a query
retry. Some of these causes are *actionable*, that is, a user can make changes to reduce or eliminate query retries for a specific query.
For example, if a query is retried due to an out of memory error, modifying warehouse settings might resolve the issue.

Some query retries are caused by a fault that is not actionable. That is, there is no change a user can make to prevent the
query retry. For example, a network outage might result in a query retry. In this case, there is no change to the query or to the
warehouse that executes it that can prevent the query retry.

The QUERY\_RETRY\_TIME, QUERY\_RETRY\_CAUSE, and FAULT\_HANDLING\_TIME columns can help you optimize queries that are retried and better
understand fluctuations in query performance.

## Query history for hybrid tables

The following notes explain when records are logged in the QUERY\_HISTORY view for queries against hybrid tables:

- Short-running queries that operate exclusively against hybrid tables do not generate a record in this
  view or [QUERY\_HISTORY](/sql-reference/functions/query_history) (Information
  Schema table function). To monitor such queries, use the
  [AGGREGATE\_QUERY\_HISTORY](/sql-reference/account-usage/aggregate_query_history) view.
  This view allows you to more easily monitor high-throughput operational
  workloads for trends and issues.
- Short-running queries that operate exclusively against hybrid tables do not provide a query profile
  that you can inspect in Snowsight.
- Queries against hybrid tables do generate both a record in the QUERY\_HISTORY view and a query profile if any of the
  following conditions are met:
  - A query is executed against any table type other than the hybrid table type. This
    condition ensures that there is no behavior change for any existing
    non-Unistore workloads.
  - A query fails with an EXECUTION\_STATUS of `failed_with_incident` (see
    [QUERY\_HISTORY](/sql-reference/functions/query_history)). This
    condition ensures that you can investigate and report the specific failed
    query to receive assistance.
  - A query is running longer than approximately 500 milliseconds. This
    condition ensures that you can investigate performance issues for slow queries.
  - Query result size is too large.
  - A query is associated with a Snowflake transaction.
  - A query contains a system function with side effects.
  - A query is not one of the following statement types: SELECT, INSERT,
    DELETE, UPDATE, MERGE.
  - A query is executed from SnowSQL, Snowsight, or Classic Console. This
    condition ensures that you can manually generate a full query profile to
    investigate performance issues for any specific query even if it is not
    categorized as long-running.
  - Even if a query does not meet any of these criteria, queries can be
    periodically sampled to generate a record in the QUERY\_HISTORY view and a
    query profile to help your investigation.

## PUT and GET commands

For the [PUT](/sql-reference/sql/put) and [GET](/sql-reference/sql/get) commands,
an EXECUTION\_STATUS of `success` in the [QUERY\_HISTORY](/sql-reference/account-usage/query_history)
does \_not\_ mean that data files were successfully uploaded or downloaded.
Instead, the status indicates that Snowflake received authorization to proceed with the file transfer.
