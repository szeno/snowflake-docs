# Running free-form SQL queries on clean room tables

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. Migrate to the
[Collaboration API](/user-guide/cleanrooms/overview) using the
[migration tool](/user-guide/cleanrooms/migration-tool) before the dates below.

- **2026-10-01:** New legacy clean rooms may not be created via the
  [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction).
- **2027-02-01:** The [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction)
  will no longer be accessible, and new legacy clean rooms may not be created via the
  [Provider and Consumer API](/user-guide/cleanrooms/getting-started).
- **2027-06-01:** Legacy [Provider and Consumer clean rooms](/user-guide/cleanrooms/getting-started)
  will no longer be accessible. Use the [Collaboration API](/user-guide/cleanrooms/overview)
  to create and manage clean rooms.

You can enable consumers to run free-form SQL queries on selected datasets in your clean room using either the clean room API or UI.

## Free-form queries using the clean rooms API

You can configure a clean room to allow collaborators to query specific linked datasets from outside the clean room.
Collaborators can run free-form queries on these datasets in any environment where they can access the clean room, including Snowsight or
Snowflake CLI. Free-form datasets behave as standard, read-only views that can be queried using SQL, Python, or other supported
Snowflake languages.

Note

When you grant a consumer permission to run free-form SQL queries in a clean room, that consumer can query the data from that clean
room against any other data that they can access from their account.

### Policies and differential privacy support

When you expose clean room data for free-form queries, all Snowflake policies are respected. Clean room policies (join policies,
column policies) are not enforced in free-form queries.

Clean room differential privacy is not enforced on data exposed to free-form queries. This includes both
[Snowflake differential privacy](/user-guide/diff-privacy/differential-privacy-overview) and
[clean room differential privacy](/user-guide/cleanrooms/differential-privacy).

### Enabling free-form queries

- [Provider steps](#provider-steps)
- [Consumer steps](#consumer-steps)

Important

If a clean room was created before June, 2025 the provider must patch their clean room by running the following code to enable free-form
queries in that clean room:

Copy code

```
USE ROLE SAMOOHA_APP_ROLE;
CALL samooha_by_snowflake_local_db.provider.patch_cleanroom($cleanroom_name,TRUE);
```

#### Provider steps

The provider takes the following steps to make datasets in a clean room available to clean room collaborators using free-form queries:

1. Create the clean room in the standard way.
2. Register and link the datasets into the clean room in the standard way using the API. Note that currently your
   data must be registered using the API; you cannot register views in the clean room UI and use them for free-form queries. You should
   apply any Snowflake aggregation, join, or other policies before sharing your data outside the clean room.
3. Call `provider.enable_workflows_for_consumers` to allow specific users free-form access to the tables that you will specify in the
   next step. **You must name this work flow** `freeform_sql`.
4. Call `provider.enable_datasets_for_workflow` to specify which datasets in the clean room can be queried.
5. Add your collaborators in the standard way by calling `provider.add_consumers`.
6. Publish your clean room.
7. If you want to revoke permission to query these tables, you can do this at the user level by calling
   `provider.disable_consumer_run_analysis` or `provider.remove_consumers`, at the dataset level by calling
   `library.unregister_objects` or `library.unregister_db`, or by deleting the clean room.

If a clean room already exists and data is registered, you can simply call `provider.enable_workflows_for_consumers` and
`provider.enable_datasets_for_workflow` to expose the specified datasets to the specified users.

The following code creates three sample tables and applies Snowflake policies to them, creates a new clean room, links in the tables, and
grants free-form query access to those tables for clean room collaborators via the clean room. The highlighted code shows where you enable
free-form queries in the clean room.

Copy code

```
----------------- Create sample data -----------------
USE ROLE MYROLE;
CREATE DATABASE freeform_db;

-- Create a table with an aggregation constraint.
CREATE OR REPLACE TABLE freeform_db.public.agg_constrained_table
  AS SELECT * FROM SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS;

CREATE AGGREGATION POLICY freeform_db.public.agg_policy AS ()
  RETURNS AGGREGATION_CONSTRAINT ->
  AGGREGATION_CONSTRAINT(MIN_GROUP_SIZE => 5);

ALTER TABLE freeform_db.public.agg_constrained_table
  SET AGGREGATION POLICY freeform_db.public.agg_policy;

-- Create a table with a projection constraint.
CREATE OR REPLACE TABLE freeform_db.public.proj_constrained_table
  AS SELECT * FROM SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS;

CREATE OR REPLACE PROJECTION POLICY freeform_db.public.proj_policy AS ()
  RETURNS PROJECTION_CONSTRAINT ->
  PROJECTION_CONSTRAINT(ALLOW => false);

ALTER TABLE freeform_db.public.proj_constrained_table MODIFY COLUMN hashed_email
  SET PROJECTION POLICY freeform_db.public.proj_policy;

-- Create a table with a masking policy.
CREATE OR REPLACE TABLE freeform_db.public.masked_table
  AS SELECT * FROM SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS;

CREATE OR REPLACE MASKING POLICY freeform_db.public.masking_policy
  AS (val string) RETURNS STRING ->
  CASE
    WHEN current_account() IN ('DCR_PROVIDER_PP6') THEN VAL
    ELSE '*********'
  END;

ALTER TABLE freeform_db.public.masked_table MODIFY COLUMN hashed_email
  SET MASKING POLICY freeform_db.public.masking_policy;

----------------- Create and publish a clean room that supports -----------------
----------------- free-form queries against this data.          -----------------

-- Create the clean room. Nothing new here.
USE ROLE SAMOOHA_APP_ROLE;
SET cleanroom_name = 'freeform queries';
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.provider.cleanroom_init($cleanroom_name, 'INTERNAL');

-- Link in the policy-protected tables from above. Nothing new here.
USE ROLE MYROLE;
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.provider.register_db('freeform_db');
USE ROLE SAMOOHA_APP_ROLE;
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.provider.link_datasets($cleanroom_name,
  ['freeform_db.public.agg_constrained_table',
  'freeform_db.public.proj_constrained_table',
  'freeform_db.public.masked_table']);

-- Grant the following consumer access to the tables specified next.
-- The flow name must be 'freeform_sql'
SET flow_name = 'freeform_sql';
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.provider.enable_workflows_for_consumers($cleanroom_name,
  [$flow_name],
  ['<CONSUMER_LOCATOR>']);

-- Grant the consumer specified above access to the specified tables.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.provider.enable_datasets_for_workflow($cleanroom_name,
  $flow_name,
  ['freeform_db.public.agg_constrained_table',
   'freeform_db.public.proj_constrained_table',
   'freeform_db.public.masked_table']);

-- Add collaborators and publish, in the standard way.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.provider.add_consumers(
  $cleanroom_name, '<CONSUMER_LOCATOR>', '<ORG_NAME>.<CONSUMER_LOCATOR>');
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.provider.set_default_release_directive(
  $cleanroom_name, 'V1_0', '0');
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.provider.create_or_update_cleanroom_listing(
  $cleanroom_name);
```

#### Consumer steps

After the provider has published a clean room with free-form SQL work flows, consumers with access to that clean room can run queries
against the exposed views by following these steps:

1. Install the clean room in the standard way. No need to link in consumer data, as the consumer will access their data in their local
   environment, not in the clean room.
2. Call `consumer.get_provider_freeform_sql_views` to list the free-form SQL views available to the current account and role.
3. Run standard SQL queries against the data.

Copy code

```
-- Install the clean room.
USE ROLE SAMOOHA_APP_ROLE;
SET cleanroom_name = 'freeform queries';

CALL samooha_by_snowflake_local_db.consumer.install_cleanroom($cleanroom_name, '<PROVIDER_LOCATOR>');

-- List free form views available in the clean room.
CALL samooha_by_snowflake_local_db.consumer.GET_PROVIDER_FREEFORM_SQL_VIEWS($cleanroom_name);

-- Run queries on the views
SELECT * FROM <PROJECTION_POLICY_VIEW_NAME>;
SELECT * FROM <MASKING_POLICY_VIEW_NAME>;
SELECT COUNT(hashed_email), age_band
  FROM <AGGREGATION_POLICY_VIEW_NAME> group by age_band;
```

## Free-form queries in the clean rooms UI

The SQL Query template in a clean room lets consumers write free-form SQL to query data in the clean room. When using the SQL
Query template, consumer queries must meet certain requirements to successfully return results. These requirements are determined by how
the data provider protects their tables with data privacy policies.

When creating or updating a clean room in the UI, add the SQL Query template to your clean room and configure it as described below.

### Provider: Create a clean room and set policies

1. Create a clean room or edit an existing clean room, and specify tables or views for your table.
2. Join policies specified during the clean room creation process are ignored when using the SQL Query template, but respected for any
   other templates.
3. In **Configure Analysis & Query** select **Horizontal** » **SQL Query**.
4. In the **SQL Query** settings section, set the following properties:
   1. Under **Tables**, select tables that should be available to clean room collaborators in free-form queries. By default,
      aggregation policies do not need to be applied. To control which columns can be
      projected, and which must be aggregated, you must set column policies in the next section.

      Important

      In free-form queries in the clean rooms UI, you cannot use a table with a name that ends in “LIST” (upper or lower case).
   2. In the **Column Policies** section set the following values to control if or how your columns can be used in a query:

      1. **Aggregation policy columns**: Specify which columns must be aggregated in order to appear in query results. If you apply an
         aggregation policy to a column and one column is used in a query, then the results must be aggregated. Any columns listed here
         will be added to the **Privacy settings** section.
      2. **Projection policy columns**: Columns with a projection policy cannot be projected (that is, included in a SELECT
         statement). However, consumers can filter or join on a column with a projection policy.
      3. **Fully permitted columns**: The consumer can SELECT, filter, or join on these columns without restriction (aggregation or
         otherwise).
   3. The **Privacy settings** section lists all columns with an aggregation policy applied. The **Threshold** value indicates how many
      entities must exist for that value to appear in the results. For example, if you set a threshold of 5 on a FIRST\_NAME column, and the
      name “Erasmus” appears only 4 times in the table, all rows with “Erasmus” will be filtered out before any processing has occurred
      (so, for example, a COUNT(\*) on such a table will omit those 4 rows with the below-threshold group size).

### Consumer: Run a free-form query

1. Join or edit the clean room in the clean rooms UI.
2. In the **Configure Analysis & Query** section, choose your tables that you will use for free-form queries.

   Important

   In free-form queries in the clean rooms UI, you cannot use a table with a name that ends in “LIST” (upper or lower case).
3. Select **Finish** to save your changes.
4. To run a query, select **Run** in the clean room with the SQL Query template and select the SQL Query template.

#### Select join and filtering columns

You can join and filter on any column that has a policy or is fully permitted. To determine if a column can be joined or used in a filter:

1. In the **Query Configurations** section, find the **Tables** tile.
2. Use the drop-down list to select a table. You can join and filter on all of the columns listed.

#### Select projection columns

Queries executed using the SQL Query template have restrictions on which columns can be projected (used in a SELECT statement).

To determine if your query can project a column:

1. In the **Query Configurations** section, find the **Tables** tile.
2. Use the drop-down list to select a table.
3. Look for columns that have a projection policy label, which means you cannot project it. You can project all columns except the ones
   with the projection policy label.

#### Aggregation requirements

If the provider assigned an aggregation policy to a column, all queries executed using the SQL Query template must return aggregated
results.

To determine if your query must aggregate results:

1. In the **Query Configurations** section, find the **Tables** tile.
2. Use the drop-down list to select a table.
3. Look for columns that have an aggregation policy label. If there is at least one aggregation policy label, you must use an aggregate in
   your query.

For guidelines on how to write a successful query against data protected by an aggregation policy, see:

- [Query requirements for aggregation policies](/user-guide/aggregation-policies#label-aggregation-policy-query-reqs). For example, you can use this section to
  determine that the MIN and MAX aggregation functions do not satisfy the query requirements, and cannot be used.
- [Aggregation policy limitations](/user-guide/aggregation-policies#label-aggregation-limitations)

#### Graphing requirements

In order for Snowflake to be able to generate a graph:

- **The results table must include at least one measure (numeric) column and one dimension (category) column.**
- **The measure column name must have the following prefix or suffix (case-insensitive):**
  - Column-name prefixes:

    - COUNT
    - SUM
    - AVG
    - MIN
    - MAX
    - OUTPUT
    - OVERLAP
  - Column-name suffix:

    - \_OVERLAP

Snowflake generates a chart using the first eligible measure column and the first dimension column in a results table.

#### Limitations

- An ORDER BY clause has no effect on how the results of the analysis are displayed.

#### Sample queries

Use this section to better understand what a query can and cannot include when running an analysis with the SQL Query template.

Queries without an aggregation function
:   In some circumstances, you can return values without using an aggregation function.

    | Allowed | Not allowed |
    | --- | --- |
    | Copy code  ``` SELECT gender, regions   FROM TABLE sample_db.demo.customer   GROUP BY gender, region; ``` | Copy code  ``` SELECT gender, regions   FROM TABLE sample_db.demo.customer; ``` |

    Expand

    Show lessSee more

Common table expressions (CTEs)
:   | Allowed | Not allowed |
    | --- | --- |
    | Copy code  ``` WITH audience AS   (SELECT COUNT(DISTINCT t1.hashed_email),     t1.status     FROM provider_db.overlap.customers t1     JOIN consumer_db.overlap.customers t2       ON t1.hashed_email = t2.hashed_email     GROUP BY t1.status);  SELECT * FROM audience; ``` | Copy code  ``` WITH audience AS   (SELECT t1.hashed_email,     t1.status     FROM provider_db.overlap.customers quoted t1     JOIN consumer_db.overlap.customers t2       ON t1.hashed_email = t2.hashed_email     GROUP BY t1.status)  SELECT * FROM audience ``` |

    Expand

    Show lessSee more

CREATE, ALTER, TRUNCATE
:   A query cannot use CREATE, ALTER, or TRUNCATE.

Query with joins
:   | Allowed |
    | --- |
    | Copy code  ``` SELECT p.education_level,   c.status,   AVG(p.days_active),   COUNT(DISTINCT p.age_band)   FROM  samooha_sample_database.demo.customers c   INNER JOIN   samooha_sample_database.demo.customers p     ON  c.hashed_email = p.hashed_email   GROUP BY ALL; ``` |

    Expand

    Show lessSee more

DATE\_TRUNC
:   | Allowed |
    | --- |
    | Copy code  ``` SELECT COUNT(*),   DATE_TRUNC('week', date_joined) AS week   FROM consumer_sample_database.audience_overlap.customers   GROUP BY week; ``` |

    Expand

    Show lessSee more

Quoted identifiers
:   | Allowed |
    | --- |
    | Copy code  ``` SELECT COUNT(DISTINCT t1."hashed_email")   FROM provider_sample_database.audience_overlap."customers quoted" t1   INNER JOIN   consumer_sample_database.audience_overlap.customers t2     ON t1."hashed_email" = t2.hashed_email; ``` |

    Expand

    Show lessSee more
