# Free-form SQL queries

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

A data provider can allow their data to be exposed to an analysis runner via a template or free-form queries. When a data provider enables
free-form queries on a dataset, any analysis runners with access to the data offering can run SQL queries in their environment against that
dataset.

Analysis runners and data providers must both have joined the collaboration before the data becomes available.

## Overview

Here are the steps to run free-form queries against data in a clean room:

**Data provider**

1. Register a data offering that contains one or more datasets where `allowed_analyses: template_and_freeform_sql` is specified.

   If the data provider wants to apply Snowflake policies to columns in the dataset, they must create those policies before registering the
   data, and associate the policies with the columns in the data offering specification.
2. Link the data offering into the collaboration in the standard way.

**Analysis runner**

After the collaboration is installed on their account, the analysis runner calls VIEW\_DATA\_OFFERINGS. If there is a value in the
`freeform_sql_view_name` column, the dataset can be queried directly against the view named in that column.

Any policies listed in `freeform_sql_column_policies` are applied to the data by the collaboration. Any policies applied directly to the
source data by the data provider are enforced, but won’t be shown in that column.

Details about the data provider and analysis steps are given in the following sections.

## Registering a free-form query dataset (Data Provider)

The following steps show how to enable free-form queries during data offering registration:

1. Specify `allowed_analyses: template_and_freeform_sql` in the collaboration specification. This enables the dataset to be queried
   using either a template or free-form query.

   Copy code

   ```
   ...
   datasets:
   - alias: customers_view
     data_object_fqn: PROVIDER_DB.DATA_SCH.CUSTOMERS
     object_class: custom
     allowed_analyses: template_and_freeform_sql
     schema_and_template_policies:
       HASHED_EMAIL:
         category: join_standard
         column_type: hashed_email_b64_encoded
   ...
   ```

   Only the columns listed under `schema_and_template_policies` are available for querying via templates or free-form queries.
2. If you want to apply Snowflake policies in free-form queries without applying them to your source data, take the following steps:

   1. Create your Snowflake policies in the standard way. Don’t apply them to your table.

      Copy code

      ```
      CREATE OR REPLACE AGGREGATION POLICY PROVIDER_DB.DATA_SCH.MIN_GROUP_SIZE_POLICY
        AS () RETURNS AGGREGATION_CONSTRAINT ->
          AGGREGATION_CONSTRAINT(MIN_GROUP_SIZE => 5);
      ```

      The role that creates the collaboration must have the USAGE privilege on the database, schema, and policy object.

      These policies are linked dynamically; any changes that you make to these policies immediately affect any datasets that use those
      policies, even if the data offering is already registered and linked.
   2. Assign your policies in the data offering specification under the `freeform_sql_policies` field. Important: All column
      names used under `freeform_sql_policies` must use the [auto-generated column name](/user-guide/cleanrooms/resources-data-offerings#label-dcr-source-column-renaming) if the
      column has been renamed. Renaming affects only join-standard category columns.

      These policies aren’t applied directly to the source table, only to the view registered by the collaboration.

      Copy code

      ```
      schema_and_template_policies:
        HASHED_EMAIL:                                  # Source column name.
          category: join_standard
          column_type: hashed_email_b64_encoded        # Column is renamed to the column_type value.
        STATUS:
          category: passthrough
        AGE_BAND:
          category: passthrough
        DAYS_ACTIVE:
          category: passthrough
        INCOME_BRACKET:
          category: passthrough
      freeform_sql_policies:          # Apply agg, join, and masking policies created by the data owner to these columns.
        aggregation_policy:
          name: PROVIDER_DB.DATA_SCH.MIN_GROUP_SIZE_POLICY
          entity_keys:
            - HASHED_EMAIL_B64_ENCODED
        join_policy:
          name: PROVIDER_DB.DATA_SCH.EMAIL_JOIN_POLICY
          columns:
            - HASHED_EMAIL_B64_ENCODED    # This is the renamed column.
        masking_policies:
          - name: PROVIDER_DB.DATA_SCH.MASK_INCOME_POLICY
            columns:
              - INCOME_BRACKET
      ```
3. Register the data offering in the standard way by calling REGISTER\_DATA\_OFFERING.

## Running free-form queries (Analysis Runner)

When an analysis runner calls VIEW\_DATA\_OFFERINGS, if a value appears in the `freeform_sql_view_name` column, the free-form SQL view
can be queried directly, without using a template. All Snowflake policies applied to the source table or defined in the
[data offering’s](/user-guide/cleanrooms/spec-data-offering#label-dcr-collaboration-data-yaml) `freeform_sql_policies` section are enforced in the queries.

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.VIEW_DATA_OFFERINGS($collaboration_name);
```

| Column | Value |
| --- | --- |
| TEMPLATE\_VIEW\_NAME | `data_provider.provider_customers_V1.customers` |
| TEMPLATE\_JOIN\_COLUMNS | `hashed_email_b64_encoded` |
| ANALYSIS\_ALLOWED\_COLUMNS | `STATUS, AGE_BAND, DAYS_ACTIVE, INCOME_BRACKET` |
| ACTIVATION\_ALLOWED\_COLUMNS |  |
| **FREEFORM\_SQL\_VIEW\_NAME** | `SFDCR_FREEFORM_SQL_DEMO.FREEFORM_SQL.DATA_PROVIDER_PROVIDER_CUSTOMERS_V1_CUSTOMERS` |
| FREEFORM\_SQL\_COLUMN\_POLICIES | Copy code  ``` {   "aggregation_policy": {"entity_keys": ["HASHED_EMAIL_B64_ENCODED"]},   "masking_policy": {"columns": ["INCOME_BRACKET"]},   "join_policy": {"columns": ["HASHED_EMAIL_B64_ENCODED"]},   "no_policy": {"columns": ["DAYS_ACTIVE", "AGE_BAND", "STATUS"]} } ``` |
| SHARED\_BY | `data_provider` |
| SHARED\_WITH | `["data_consumer"]` |
| DATA\_OFFERING\_ID | `provider_customers_V1` |

Expand

Show lessSee more

You must use the value from `freeform_sql_view_name`, not the value from `template_view_name`.

Copy code

```
SELECT status, COUNT(*) AS customer_count
  FROM SFDCR_FREEFORM_SQL_DEMO.FREEFORM_SQL.DATA_PROVIDER_PROVIDER_CUSTOMERS_V1_CUSTOMERS AS t
  GROUP BY status
  ORDER BY customer_count DESC;
```

## Example: Two-party collaboration

The following example demonstrates a two-party collaboration, where one party (the “provider”) is the collaboration owner and a data
provider for the consumer. The other party (the “consumer”) is an analysis runner who can run the template and use the data provided by the
provider, and also run free-form SQL queries on the data, subject to the policies defined in the data provider’s specification.

To run this example, you must have two separate accounts with Snowflake Data Clean Rooms installed.

You can either download the files and upload them to your Snowflake account, or copy and paste the example code into worksheets in two
separate accounts by using Snowsight.

File downloadsProvider codeConsumer code

Download the source SQL files, and then upload them into two separate accounts that have Snowflake Data Clean Rooms installed:

- [Collaboration owner and data provider worksheet](/static/samples/clean-rooms/collab-hub-freeform-sql-provider.sql)
- [Collaboration query runner worksheet](/static/samples/clean-rooms/collab-hub-freeform-sql-consumer.sql)

Copy code

```
-- ============================================================================
-- Free-form SQL Collaboration Demo: Data Provider
-- ============================================================================
-- This example demonstrates a Snowflake Data Clean Rooms collaboration using
-- freeform SQL policies. The data provider creates a sample dataset with
-- Snowflake aggregation, join, and masking policies, registers a data offering
-- that permits freeform SQL queries, creates a template, and initializes a
-- collaboration with one other collaborator (data_consumer).
--
-- For more information, see:
--   docs.snowflake.com/user-guide/cleanrooms/free-form-sql.rst
--   docs.snowflake.com/user-guide/cleanrooms/spec-reference
-- ============================================================================

-- ============================================================================
-- SETUP: Create sample database, schema, table, and policies.
-- ============================================================================

USE ROLE SAMOOHA_APP_ROLE;
USE WAREHOUSE APP_WH;

-- You can't use secondary roles with most collaboration procedures.
USE SECONDARY ROLES NONE;

CREATE DATABASE IF NOT EXISTS PROVIDER_DB;
CREATE SCHEMA IF NOT EXISTS PROVIDER_DB.DATA_SCH;

-- Create a table with 300 rows from the sample CUSTOMERS table.
CREATE OR REPLACE TABLE PROVIDER_DB.DATA_SCH.CUSTOMERS AS
  SELECT HASHED_EMAIL, STATUS, AGE_BAND, REGION_CODE, DAYS_ACTIVE, INCOME_BRACKET
  FROM SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS
  LIMIT 300;

-- Create an aggregation policy that requires a minimum group size of 5.
CREATE OR REPLACE AGGREGATION POLICY PROVIDER_DB.DATA_SCH.MIN_GROUP_SIZE_POLICY
  AS () RETURNS AGGREGATION_CONSTRAINT ->
    AGGREGATION_CONSTRAINT(MIN_GROUP_SIZE => 5);

-- Create an inactive join policy. You will modify this later.
CREATE OR REPLACE JOIN POLICY PROVIDER_DB.DATA_SCH.EMAIL_JOIN_POLICY
  AS () RETURNS JOIN_CONSTRAINT ->
    JOIN_CONSTRAINT(JOIN_REQUIRED => FALSE);

-- Create a masking policy that replaces the original value with a fixed string.
CREATE OR REPLACE MASKING POLICY PROVIDER_DB.DATA_SCH.MASK_INCOME_POLICY
  AS (val STRING) RETURNS STRING ->
    '***MASKED***';

-- ============================================================================
-- Register a data offering with freeform SQL policies.
-- ============================================================================

-- The data offering enables freeform SQL queries (template_and_freeform_sql)
-- and attaches three Snowflake policies to protect data in freeform queries:
--   * Aggregation policy on hashed_email: enforces a minimum group size of 5.
--   * Join policy on hashed_email: requires joins to include this column.
--   * Masking policy on income_bracket: masks the column value in query results.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.REGISTER_DATA_OFFERING(
  $$
  api_version: 2.0.0
  spec_type: data_offering
  version: V1
  name: provider_customers
  description: Customer dataset with freeform SQL policies.
  datasets:
    - alias: customers
      data_object_fqn: PROVIDER_DB.DATA_SCH.CUSTOMERS
      object_class: custom
      allowed_analyses: template_and_freeform_sql
      schema_and_template_policies:
        HASHED_EMAIL:
          category: join_standard
          column_type: hashed_email_b64_encoded
        STATUS:
          category: passthrough
        AGE_BAND:
          category: passthrough
        DAYS_ACTIVE:
          category: passthrough
        INCOME_BRACKET:
          category: passthrough
      freeform_sql_policies:
        aggregation_policy:
          name: PROVIDER_DB.DATA_SCH.MIN_GROUP_SIZE_POLICY
          entity_keys:
            - HASHED_EMAIL_B64_ENCODED
        join_policy:
          name: PROVIDER_DB.DATA_SCH.EMAIL_JOIN_POLICY
          columns:
            - HASHED_EMAIL_B64_ENCODED
        masking_policies:
          - name: PROVIDER_DB.DATA_SCH.MASK_INCOME_POLICY
            columns:
              - INCOME_BRACKET
  $$
);

-- Save the data offering ID returned by the registration call.
SET data_offering_id = '<data_offering_id>';

CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.VIEW_REGISTERED_DATA_OFFERINGS();

-- ============================================================================
-- Register a template with a simple one-table query.
-- ============================================================================

CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.REGISTER_TEMPLATE(
  $$
  api_version: 2.0.0
  spec_type: template
  name: status_summary
  version: V1
  type: sql_analysis
  description: Returns a count of customers grouped by status.
  template:
    SELECT status, COUNT(*) AS customer_count
      FROM IDENTIFIER({{ source_table[0] }})
      GROUP BY status
      ORDER BY customer_count DESC;
  $$
);

-- Save the template ID returned by the registration call.
SET template_id = '<template_id>';

CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.VIEW_REGISTERED_TEMPLATES();

-- ============================================================================
-- Create the collaboration.
-- ============================================================================

-- Replace the <...> placeholders with the appropriate values.
-- Get your account data sharing ID with:
--   SELECT CURRENT_ORGANIZATION_NAME() || '.' || CURRENT_ACCOUNT_NAME();
-- In this collaboration, the consumer can run templated and free-form queries
-- against the provider's data. The provider/owner isn't an analysis runner.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.INITIALIZE(
  $$
  api_version: 2.0.0
  spec_type: collaboration
  name: freeform_sql_demo
  owner: data_provider
  collaborator_identifier_aliases:
    data_provider: <provider_account_data_sharing_id>
    data_consumer: <consumer_account_data_sharing_id>
  analysis_runners:
    data_consumer:
      data_providers:
        data_provider:
          data_offerings:
            - id: <data_offering_id>
      templates:
        - id: <template_id>
  $$,
  'APP_WH'
);

SET collaboration_name = 'freeform_sql_demo';

-- INITIALIZE automatically joins the owner. Repeat until status is JOINED.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.GET_STATUS($collaboration_name);

-- Verify that the collaboration is visible.
-- Collaboration spec is in COLLABORATION_SPEC column.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.VIEW_COLLABORATIONS() ->>
  SELECT * FROM $1 WHERE "SOURCE_NAME" = $collaboration_name;

-- SWITCH TO data_consumer account to join and run analyses.

-- Update the join policy associated with HASHED_EMAIL_B64_ENCODED.
-- All queries on that data offering now require joins on HASHED_EMAIL_B64_ENCODED.
-- Re-run any of the previously successful free-form queries and they will fail.
ALTER JOIN POLICY PROVIDER_DB.DATA_SCH.EMAIL_JOIN_POLICY SET BODY ->
  JOIN_CONSTRAINT(JOIN_REQUIRED => TRUE);

-- ============================================================================
-- CLEANUP: Delete the collaboration, registered resources, and sample data.
-- ============================================================================

-- Teardown is a multi-step process. Call TEARDOWN, then wait for GET_STATUS
-- to report LOCAL_DROP_PENDING, then call TEARDOWN again.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.TEARDOWN($collaboration_name);
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.GET_STATUS($collaboration_name);

-- When GET_STATUS reports LOCAL_DROP_PENDING, call TEARDOWN again to complete.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.TEARDOWN($collaboration_name);
```

Copy code

```
-- ============================================================================
-- Free-form SQL Collaboration Demo: Data Consumer
-- ============================================================================
-- This example demonstrates joining a Snowflake Data Clean Rooms collaboration
-- as an analysis runner. The data consumer joins a collaboration created by
-- the data provider, views available templates and data offerings, runs an
-- analysis using the provider's template, and then runs several free-form SQL
-- queries directly against the data-offering views.
--
-- The data offering in this collaboration has three free-form SQL policies:
--   * Aggregation policy (hashed_email): minimum group size of 5.
--   * Join policy (hashed_email): joins must include this column. Currently inactive.
--   * Masking policy (income_bracket): values are replaced with '***MASKED***'.
--
-- For more information, see:
--   docs.snowflake.com/user-guide/cleanrooms/free-form-sql.rst
--   docs.snowflake.com/user-guide/cleanrooms/spec-reference
-- ============================================================================

-- ============================================================================
-- Join the collaboration
-- ============================================================================

USE ROLE SAMOOHA_APP_ROLE;
USE WAREHOUSE APP_WH;

-- You can't use secondary roles with most collaboration procedures.
USE SECONDARY ROLES NONE;

-- View available collaborations. Look for the collaboration created by the data provider.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.VIEW_COLLABORATIONS();

-- Use the SOURCE_NAME column value from the response to VIEW_COLLABORATIONS().
SET collaboration_name = 'freeform_sql_demo';

-- Use the OWNER_ACCOUNT column value from the response to VIEW_COLLABORATIONS().
SET collaborator_data_sharing_id = '<provider_data_sharing_id>';

-- Review the collaboration spec before joining.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.REVIEW($collaboration_name, $collaborator_data_sharing_id);

-- Join the collaboration. Joining is asynchronous; call GET_STATUS until JOINED.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.JOIN($collaboration_name);
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.GET_STATUS($collaboration_name);

-- ============================================================================
-- View available templates and data offerings
-- ============================================================================

-- View data offerings shared with you in this collaboration.
-- Set a variable to use in future queries.
-- Note that the view name used by templates != the view name used for free-form SQL queries.
-- Templates use the TEMPLATE_VIEW_NAME value.
-- Free-form queries use the FREEFORM_SQL_VIEW_NAME value.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.VIEW_DATA_OFFERINGS($collaboration_name);
SET template_view_name = '<template_view_name>';
SET freeform_view_name = '<freeform_view_name>';

-- View templates available to you in this collaboration.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.VIEW_TEMPLATES($collaboration_name);

-- ============================================================================
-- Run an analysis using the provider's template
-- ============================================================================

-- Replace the placeholders with the template name/version from VIEW_TEMPLATES
-- and the view name from VIEW_DATA_OFFERINGS.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.RUN(
  $collaboration_name,
  $$
  api_version: 2.0.0
  spec_type: analysis
  description: Count customers grouped by status.
  template: '<status_summary_template_name_and_version>'
  template_configuration:
    view_mappings:
      source_tables:
        - '<template_view_name>'
  $$
);

-- ============================================================================
-- Free-form SQL queries: Queries that SUCCEED
-- ============================================================================

-- The following queries run directly against the data-offering view.

-- Query 1: Count customers grouped by status.
-- Succeeds because the aggregation produces groups larger than 5.
SELECT status, COUNT(*) AS customer_count
  FROM IDENTIFIER( $freeform_view_name ) AS t
  GROUP BY status
  ORDER BY customer_count DESC;

-- Query 2: Count customers grouped by age_band.
-- Succeeds because the aggregation produces groups larger than 5.
SELECT age_band, COUNT(*) AS customer_count
  FROM IDENTIFIER( $freeform_view_name ) AS t
  GROUP BY age_band
  ORDER BY age_band;

-- Query 3: Select income_bracket to demonstrate the masking policy.
-- The query succeeds, but income_bracket values are replaced with '***MASKED***'
-- because the masking policy is applied to this column.
SELECT income_bracket, COUNT(*) AS customer_count
  FROM IDENTIFIER( $freeform_view_name ) AS t
  GROUP BY income_bracket;

-- Query 4: Combine masked and unmasked columns.
-- income_bracket is masked; status and age_band are not.
SELECT status, age_band, income_bracket, COUNT(*) AS customer_count
  FROM IDENTIFIER( $freeform_view_name ) AS t
  GROUP BY status, age_band, income_bracket
  ORDER BY customer_count DESC;

-- Query 5: Group by a high-cardinality column.
-- Succeeds, but shows no values for hashed_email_b64_encoded because
-- grouping by hashed_email_b64_encoded produces groups of 1.
SELECT hashed_email_b64_encoded, COUNT(*) AS row_count
  FROM IDENTIFIER( $freeform_view_name ) AS t
  GROUP BY hashed_email_b64_encoded;

-- ============================================================================
-- Free-form SQL queries: Queries that FAIL
-- ============================================================================

-- Query 6: Select individual rows without aggregation.
-- FAILS because the aggregation policy requires a minimum group size of 5.
SELECT hashed_email_b64_encoded, status, age_band
  FROM IDENTIFIER( $freeform_view_name ) AS t
  LIMIT 10;

-- Query 8: Select a column not listed in the data offering.
-- FAILS because region_code is not included in schema_and_template_policies,
-- so it is not exposed in the data-offering view, although it is present in the source data.
SELECT region_code, COUNT(*) AS customer_count
  FROM IDENTIFIER( $freeform_view_name ) AS t
  GROUP BY region_code;

-- SWITCH TO provider account, update the JOIN policy, and re-run the successful
-- queries, which will now fail.
```
