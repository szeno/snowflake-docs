# Sep 24, 2026: Code Bundles (*Preview*)

Code Bundles let you package non-SQL code, like Python, and run it directly on Snowflake compute with a single command, without wrapping it in a stored procedure. This release expands Code Bundles with three new ways to run, in [preview](/release-notes/preview-features):

- **Warehouse execution:** run Python Code Bundles directly on warehouse compute by setting `compute_type: warehouse`, in addition to compute pools.
- **Spark jobs:** submit Spark applications (Scala, Java, or Python) as batch jobs on Snowflake compute by setting `type: spark`. Spark support is built on Snowpark Connect, so you can run existing Spark code on Snowflake without re-platforming it.
- **ML Jobs:** run a workload as a Snowflake ML Job on compute pool compute by setting `type: ml`. The job runs in the Snowflake Container Runtime, the same execution environment as the `snowflake-ml-python` job APIs, but the job definition is versioned in Snowflake and submitted with SQL.

Scheduling notebooks on compute pools (Snowpark Container Services), the capability previously delivered as Notebook Projects, is generally available. Other new capabilities in preview include inline specification overrides and the REST API, Python API, and Snowflake CLI clients.

For more information, see [Snowflake Code Bundles](/developer-guide/code-bundles/code-bundles), [Submit Spark jobs on Snowflake](/developer-guide/snowpark-connect/snowpark-connect-submit-code-bundle), and [Run ML Jobs with Code Bundles](/developer-guide/code-bundles/ml-code-bundles).
