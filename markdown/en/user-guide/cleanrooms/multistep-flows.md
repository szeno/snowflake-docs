# Using internal tables for multistep workflows

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

## Overview

Many clean room use cases involve running a single SQL query against one or more tables in a clean room and displaying the results in the response.
However, there are use cases where you might require creating an internal table that can be used within subsequent templates to
support a multistep workflow. For example, a machine learning flow, where the model is trained once against a dataset and then run multiple times
against varying input data, either singly or in batches.

## Creating internal tables

You can create internal tables inside a clean room to store intermediary results, or as persistent storage for usage downstream (for example, to save training data that is used for multiple runs). See properties and guidance of internal tables below:

- You can create internal tables by using a clean room template that executes CREATE TABLE, or by running a UDF/UDTF that uses
  Python to create a table.
- Internal tables can be created in the `cleanroom` schema, which is available by default. If a custom schema is preferred, the schema must be created first before creating the table.
- By default, internal tables are only accessible by approved templates in the clean room. If access needs to be provided outside of templates, then the CLEANROOM\_PUBLIC\_ROLE application role of the clean room needs to be granted corresponding privileges. For example, the following grant can be given: `GRANT SELECT ON TABLE CLEANROOM.MY_TABLE TO APPLICATION ROLE CLEANROOM_PUBLIC_ROLE;`
- If you have proper access, you can list the internal tables in your collaboration. Internal tables can be found at
  `SFDCR_collaboration_name.cleanroom`, and can be listed by running the following SQL code:
  `SHOW TABLES IN SCHEMA SFDCR_collaboration_name.CLEANROOM;`.
- Internal tables are deleted when the collaboration is removed. However, if an internal table is designed to have a shorter lifetime than
  the collaboration, consider deleting the table when it’s no longer needed.

Here are some examples of creating an internal table:

TemplateUDF

A JinjaSQL template can create an internal table, which is done in some types of [activation](/user-guide/cleanrooms/activation).

This example template creates the table and returns the table name, so that the name can be passed in as a parameter to other templates.

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.REGISTER_TEMPLATE(
  $$
  api_version: 2.0.0
  spec_type: template
  name: my_test_template
  version: V1
  type: sql_analysis
  description: Simple join example. Saves to table analysis_results
  template:
    BEGIN
    CREATE OR REPLACE TABLE cleanroom.analysis_results AS
      SELECT count(*) AS ITEM_COUNT, p1.status, p1.age_band
      FROM IDENTIFIER({{ source_table[0] }}) AS p1
      JOIN IDENTIFIER({{ source_table[1] }}) AS p2
      ON IDENTIFIER({{ join_col_1 | join_policy }}) = IDENTIFIER({{ join_col_2 | join_policy }})
      GROUP BY p1.status, p1.age_band;
    RETURN 'analysis_results';
    END;
  $$
  );
```

A UDF can create an internal table. This is typically done by executing SQL in Python.

Copy code

```
# Snippet of Python UDF to save results to an internal table.
table_name = f'cleanroom.results'

session.sql(f"""
CREATE OR REPLACE TABLE {table_name} AS (
  WITH joint_data AS (
    SELECT
        date,
        p.hashed_email AS hem,
        impression_id
    FROM {source_table} p
  )
  SELECT
    date,
    COUNT(DISTINCT hem) AS reach,
    COUNT(DISTINCT impression_id) AS num_impressions
  FROM joint_data
  GROUP BY date
  ORDER BY date
);
""").collect()
```
