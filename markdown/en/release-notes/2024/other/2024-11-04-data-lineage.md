# November 04, 2024 — Data Lineage — *Preview*

Snowflake is pleased to announce the preview of Data Lineage, a feature that automatically tracks the flow of data
between Snowflake objects in real-time, for example from a table to a view. Relationships among table-like objects,
columns, and stages are supported, as well as between data objects and machine learning objects including datasets,
feature views, and models. You can use lineage information to assist in impact analysis, monitoring, troubleshooting,
and compliance efforts. Lineage can also help you propagate knowledge of sensitive data elements using tags.

Lineage information is available through Snowsight, SQL, and Python. For more information, see:

- [Data Lineage in Snowsight](/user-guide/ui-snowsight-lineage)
- [GET\_LINEAGE SQL function](/sql-reference/functions/get_lineage-snowflake-core)
- [Snowflake ML Lineage API](/developer-guide/snowflake-ml/ml-lineage#label-snowpark-ml-lineage-api)
