# Cortex Analyst administrator monitoring

Transition to Cortex Agents

Snowflake recommends transitioning to [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents), which supports every Cortex Analyst capability with higher answer quality.

To improve the quality of answers provided by Cortex Analyst, you must continue to refine the semantic model or view.
To help you refine the model or view, Cortex Analyst logs requests to an event table in the Snowflake database.

The logs include the following:

- The user who asked the question
- The question asked
- Generated SQL
- Errors and/or warnings
- Request and response bodies
- Other metadata

There is a small lag, on the order of 1-2 minutes, between a request being made and it being visible in the view.

## Accessing logs

You can view these logs in the **Monitoring** tab of the Semantic View within Snowsight.
In order to view the logs, users must have the SELECT privilege on referenced tables, in
addition to:

- MONITOR or OWNERSHIP on the semantic view (when using semantic views)
- WRITE privilege on the stage (for semantic models stored in a file on a stage)

Alternatively, you can query the logs directly from the Snowflake database using SQL,
depending on your privileges.

## Querying logs with SQL

Call the SNOWFLAKE.LOCAL.CORTEX\_ANALYST\_REQUESTS table function to retrieve logs for a specific semantic model or view. This
table function performs access control checks to ensure that the caller has required privileges to access the request data.

The following is an example of how to call the function:

Copy code

```
SELECT * FROM TABLE(
  SNOWFLAKE.LOCAL.CORTEX_ANALYST_REQUESTS(
    '<semantic_model_or_view_type>',
    '<semantic_model_or_view_name>'
  )
);
```

When calling this function, pass in the following arguments:

- `semantic_model_or_view_type`: Specify the type of semantic model or view used in the requests:

  - For a semantic model defined in a file on a stage, specify `'FILE_ON_STAGE'`.
  - For a semantic view, specify `'SEMANTIC_VIEW'`.
- `semantic_model_or_view_name`: Specify the location where the semantic model or view is defined:

  - For a semantic view defined in a file on a stage, specify the fully qualified path to the semantic view specification file
    (for example, `@my_db.my_schema.my_stage/path/to/file.yaml`).
  - For a semantic view, specify the fully qualified name of the semantic view.

Returns: A table with all API requests for the specified semantic model or view.

If a query was made using inline YAML (instead of a semantic view or a file on stage), the request will not be accessible via
the table function, but will be visible in the view and event table detailed below.

If you are using a role that has been granted the SNOWFLAKE.CORTEX\_ANALYST\_REQUESTS\_ADMIN or SNOWFLAKE.CORTEX\_ANALYST\_REQUESTS\_VIEWER application role, you can query the
[SNOWFLAKE.LOCAL.CORTEX\_ANALYST\_REQUESTS\_V](/sql-reference/local/cortex_analyst_requests_v) view. This view includes all requests
to Cortex Analyst across all semantic models and views.

You can also query the raw event data in the SNOWFLAKE.LOCAL.CORTEX\_ANALYST\_REQUESTS\_RAW event table. The responses are in the
[OpenTelemetry format](https://opentelemetry.io/docs/specs/otel/). The SNOWFLAKE.LOCAL.CORTEX\_ANALYST\_REQUESTS\_V view contains the same data, formatted and processed for human readability.
