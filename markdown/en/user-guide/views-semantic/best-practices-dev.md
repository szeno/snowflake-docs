# Best practices for developing and deploying semantic views

This section describes best practices for the development of data pipelines and data products that incorporate
[semantic views](/user-guide/views-semantic/overview). These recommendations are primarily intended for data engineering and data science
professionals who need assistance with the following development processes:

- [Ownership and data access](#ownership-and-data-access)
- [Options for creating, updating, and querying semantic views](#options-for-creating-updating-and-querying-semantic-views)
- [Conversion of YAML semantic models to native semantic views](#conversion-of-yaml-semantic-models-to-native-semantic-views)
- [Automated deployment of semantic views](#automated-deployment-of-semantic-views)
- [Integration with dbt projects](#integration-with-dbt-projects)
- [Integration with BI tools](#integration-with-bi-tools)

Note

This section does not address best practices for *modeling* semantic views (design, descriptions, metrics, relationships,
and accuracy). For that guidance, see [Best practices for modeling semantic views](/user-guide/views-semantic/best-practices-modeling). The information in this section
assumes that Snowflake semantic views are being iteratively designed and need to be managed as part of a data engineering
pipeline or data product.

## Ownership and data access

Semantic views facilitate access to information that exists in multiple canonical data sources. The semantic
layer enables a shift from thinking about how to query a specific data source to focusing on use cases and
business questions supported by a unified view of the available data. With this overall goal in mind, data
engineering and business teams must work together closely. The business teams have expertise in the business cases,
while the data engineering teams understand how to access the data from tables and views. Both teams need to share
ownership of the semantic model.

To secure the semantic layer in a way that serves the needs of both teams, use role-based access control (RBAC)
to grant appropriate privileges to semantic views and their dependent objects. If you’re starting from scratch,
you can use the sequence of GRANT statements in the next section as a working template. However, if your team
members already have permissions set up in a certain way for development, test, and production environments,
you might need to make some changes or direct them to use different roles as needed.

### Grant privileges on semantic view objects

Four key types of objects require the appropriate grants:

- Semantic views themselves
- Tables used in semantic view definitions
- Views used in semantic view definitions
- Cortex Search Service objects (generally applied on categorical data within views and tables)

To simplify privileges for a given domain, Snowflake recommends creating objects within the same database schema. Then you can
use a specific custom role to grant access to end users on that universe of objects. For example, for a “Sales Analysis” Cortex
Agent, you might create a `sales_analysis` schema within the `sales` database and create a role specifically for granting access to
semantic views and other data necessary for the agent (for example, `snowflake_intelligence_sales_analysis_role`). With the schema
and role in place, you should grant privileges on future objects to this role.

The following commands demonstrate this approach:

Copy code

```
-- Set variables for the specified role, database, and schema
SET my_role = 'snowflake_intelligence_sales_analysis_role';
SET my_db = 'sales';
SET my_schema = 'sales_analysis';
SET my_full_schema = $my_db || '.' || $my_schema;

-- Grant usage on the database and schema that will contain the tables and views
GRANT USAGE ON DATABASE IDENTIFIER($my_db) TO ROLE IDENTIFIER($my_role);
GRANT USAGE ON SCHEMA IDENTIFIER($my_full_schema) TO ROLE IDENTIFIER($my_role);

-- Grant privileges on future objects within the schema
-- For tables and views, SELECT is the typical "usage" grant for read access
GRANT SELECT ON FUTURE TABLES IN SCHEMA IDENTIFIER($my_full_schema) TO ROLE IDENTIFIER($my_role);
GRANT SELECT ON FUTURE VIEWS IN SCHEMA IDENTIFIER($my_full_schema) TO ROLE IDENTIFIER($my_role);
GRANT SELECT ON FUTURE SEMANTIC VIEWS IN SCHEMA IDENTIFIER($my_full_schema) TO ROLE IDENTIFIER($my_role);

-- For other object types, USAGE is the correct privilege
GRANT USAGE ON FUTURE FUNCTIONS IN SCHEMA IDENTIFIER($my_full_schema) TO ROLE IDENTIFIER($my_role);
GRANT USAGE ON FUTURE PROCEDURES IN SCHEMA IDENTIFIER($my_full_schema) TO ROLE IDENTIFIER($my_role);
GRANT USAGE ON FUTURE STAGES IN SCHEMA IDENTIFIER($my_full_schema) TO ROLE IDENTIFIER($my_role);
GRANT USAGE ON FUTURE CORTEX SEARCH SERVICES IN SCHEMA IDENTIFIER($my_full_schema) TO ROLE IDENTIFIER($my_role);
```

The example includes grants on future tables and views to support scenarios where users might need direct access to the underlying
data objects in addition to the semantic views. While querying a semantic view only requires SELECT privilege on the semantic view itself,
granting access to tables and views ensures flexibility for users who might need to query or analyze the base data directly, outside of the
semantic layer. If you want to restrict users strictly to semantic views, you can omit the grants on tables and views and only grant privileges
on the semantic view objects. However, note that Cortex Agents that use semantic views require the role
that is executing queries to have SELECT privilege on both the semantic view and its underlying tables.

While you’re in the process of setting up grants, keep the following additional points in mind:

- If your end data is already correctly shared with end users, you can proceed as is. However, if your Snowflake data has
  generally been shared via service accounts or at the BI layer, you need to take extra steps to share the underlying data with end users.
- The semantic view is a new object type in Snowflake; therefore, most role types don’t have default or inherited read/write access privileges on these views.
  Regardless of your underlying data sharing, work with your core Snowflake admin team to provision access to this new object type.
- For the benefit of Snowflake CoWork (and the potential of expanding the functionality of agents there), it’s worth granting the USAGE
  privilege on stages, procedures, and functions (as shown in the example). You can use these objects to create custom tools within
  Snowflake CoWork.
- CREATE SEMANTIC VIEW is a required schema-level privilege for any user who creates a semantic view or edits a semantic view in
  Snowsight.

### Limit access with masking policies and row access policies

Semantic views use *owner’s rights*, meaning that a user with access to a semantic view does not require separate access to its underlying tables;
the view’s owner (role) controls access. As long as a user has SELECT privilege on the semantic view object itself, privileges to see the base data
are not required. This behavior is consistent with the privileges [required to query standard views](/user-guide/views-introduction#label-views-privileges).

Depending on the underlying data in your semantic views and Cortex Agents, you might not want all end users to have unlimited access to all
of that data, even though they have been granted privileges through your custom role. You can use
[Dynamic Data Masking policies](/user-guide/security-column-ddm-intro) and [row access policies](/user-guide/security-row-intro)
to control access to the underlying data at the row level. These policies can’t be set directly on semantic view attributes, but
if they are set on underlying tables and columns, they propagate to semantic views and are enforced. This is a security benefit for
applications that work with sensitive data. However, note that sample values, which are stored as metadata, are not masked. See
[Sample values are not masked](#label-semantic-views-sample-values-not-masked).

For example, you can create a row access policy and a masking policy and apply them both to an `accounts` table that underlies a semantic view
named `account_semantic_view`. In this example, rows are only visible when the user querying the semantic view has an email that matches an
authorized account. Secondly, the sensitive column (`sensitive_col`) is dynamically masked for unauthorized roles, even via semantic views.

Copy code

```
-- Row access policy (restricts rows by user email)
CREATE OR REPLACE ROW ACCESS POLICY my_schema.account_row_policy AS (user_email STRING)
  RETURNS BOOLEAN ->
    EXISTS (
      SELECT 1
      FROM my_schema.account_access_list
      WHERE email = user_email()
    );

-- Masking policy (masks "sensitive_col" for users without a privileged role)
CREATE OR REPLACE MASKING POLICY my_schema.sensitive_col_masking_policy AS (val STRING)
RETURNS STRING ->
  CASE
    WHEN current_role() IN ('SENSITIVE_DATA_ACCESS_ROLE') THEN val
    ELSE 'MASKED'
  END;

-- Attach row access policy to the user_email column in the accounts table
ALTER TABLE my_schema.accounts
  ADD ROW ACCESS POLICY account_row_policy ON (user_email);

-- Attach masking policy to the sensitive_col column
ALTER TABLE my_schema.accounts
  MODIFY COLUMN sensitive_col
  SET MASKING POLICY sensitive_col_masking_policy;

-- Create the semantic view on the "accounts" table
CREATE OR REPLACE SEMANTIC VIEW my_schema.account_semantic_view
  TABLES (
    accounts AS my_schema.accounts
    PRIMARY KEY (account_id)
  )
  FACTS (
    account_id AS accounts.account_id,
    account_name AS accounts.account_name
  )
  DIMENSIONS (
    user_email AS accounts.user_email,
    sensitive_col AS accounts.sensitive_col
);
```

If you are using dbt, you can apply these policies in a
[post-hook](https://docs.getdbt.com/reference/resource-configs/pre-hook-post-hook). For example:

Copy code

```
models:
- name: accounts
  description: "Table of accounts for semantic analytics."
  columns:
    - name: account_id
      description: "Unique identifier for the account."
    - name: account_name
      description: "Name of the account."
    - name: user_email
      description: "Email address linked to each account row."
    - name: sensitive_col
      description: "Sensitive information to be masked for non-privileged users."
  post-hook:
    - >
      ALTER TABLE {{ this }}
        ADD ROW ACCESS POLICY account_row_policy ON (user_email);
  ...
```

The code `ALTER TABLE {{ this }}` uses the dbt runtime variable for the fully qualified table name. Every time dbt builds or updates
the `accounts` table, the policy is applied.

### Sample values are not masked

Although users who can query semantic views that have masking policies applied can’t see the actual data values in query results, sample
values that were defined in Snowsight aren’t masked because the masking policy is not applied to metadata.
A user who runs the [GET\_DDL](/sql-reference/functions/get_ddl) function on a semantic view that has sample values defined for dimensions
will see those exact values. For example, look at the values in the WITH EXTENSION clause in the following DDL:

Copy code

```
SELECT GET_DDL('SEMANTIC_VIEW','TEST_SAMPLE_VALUES');
```

```
create or replace semantic view TEST_SAMPLE_VALUES
tables (MARCH_TEMPS
  ...)
facts (MARCH_TEMPS.TEMPERATURE as TEMPERATURE
  ...)
dimensions (MARCH_TEMPS.CITY as CITY,
MARCH_TEMPS.COUNTY as COUNTY,
MARCH_TEMPS.OBSERVED as OBSERVED)
  ...
with extension (CA='{"tables":[{"name":"MARCH_TEMPS","dimensions":[{"name":"CITY","sample_values":["South Lake Tahoe","Big Bear City"]},{"name":"COUNTY","sample_values":["San Bernardino","El Dorado"]}],"facts":[{"name":"TEMPERATURE","sample_values":["44","46","52"]}],"time_dimensions":[{"name":"OBSERVED","sample_values":["2025-03-15T09:50:00.000+0000","2025-03-15T09:55:00.000+0000","2025-03-15T10:10:00.000+0000"]}]}
...);
```

If necessary, you can provide representative, non-sensitive sample values, rather than use real values, when you create the semantic view. Cortex Agents can use any value that’s representative of a real value to determine the contents of the column.

## Options for creating, updating, and querying semantic views

You can author semantic views in Snowflake by writing a YAML file, using Snowflake DDL syntax, or using
the UI in Snowsight. Snowflake provides convenient functions for both importing YAML models and exporting semantic views to YAML models.
For details, see [Conversion of YAML semantic models to native semantic views](#label-semantic-views-yaml-conversion).

Generally, it’s best to start by creating semantic views (rather than semantic models), which are Snowflake metadata objects that benefit from
RBAC, usage statistics, and direct integration with other Snowflake features, including Cortex Agents and Snowflake CoWork.

To create a semantic view, you have three main options:

- Create a semantic view in Snowsight:

  - You can use the wizard, or you can upload a YAML specification.
  - The wizard approach is recommended for initial setup, and includes automatic creation of synonyms, sample values, and column descriptions.
    For instructions, see [Semantic View Autopilot](/user-guide/views-semantic/autopilot).
- Create a semantic view via a SQL CREATE OR REPLACE SEMANTIC VIEW statement, using any interface that supports SQL. For instructions, see
  [Using SQL commands to create and manage semantic views](/user-guide/views-semantic/sql).

  Programmatic creation and querying is possible through interfaces such as JDBC and ODBC drivers or the
  [SQL API](/developer-guide/sql-api/index). However, you can’t use the
  [Snowflake REST APIs](/developer-guide/snowflake-rest-api/snowflake-rest-api).
- Create a semantic view from a YAML specification in SQL by calling the SYSTEM$CREATE\_SEMANTIC\_VIEW\_FROM\_YAML stored procedure.
  See [Conversion of YAML semantic models to native semantic views](#label-semantic-views-yaml-conversion).

In addition, if you are using dbt, you can configure the creation of semantic views in Snowflake by installing the `dbt_semantic_view` package.
For more information, see [Integration with dbt projects](#label-semantic-views-dbt-integration).

Keep in mind that the setup of roles and privileges for your team members might have an impact on their ability to create semantic views.
For example, if your production environment requires you to run as a SERVICE user, you can’t sign in to Snowsight in that
environment; you have to use SQL commands to create and manage semantic views.

When semantic views have been created in a Snowflake database, administrators can manage them by using standard SHOW
and DESCRIBE commands, and users can access them downstream via [SQL SELECT statements](/user-guide/views-semantic/querying)
and in the following ways:

- Through [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents) (semantic views must be added to a new or existing
  [agent](/user-guide/snowflake-cortex/cortex-agents-manage#label-snowflake-agents-modify-agents))
- Through [Streamlit](/developer-guide/streamlit/about-streamlit) or other custom applications that use
  the [Cortex Agents REST API](/user-guide/snowflake-cortex/cortex-agents-rest-api) or
  [generate SELECT FROM SEMANTIC\_VIEW statements](/user-guide/views-semantic/querying)

Except for comments, you can’t add or alter tables, columns, or metadata within existing semantic views, so you must recreate them
(with [CREATE OR REPLACE](/sql-reference/sql/create-semantic-view) commands) to incorporate any changes. Also note that updating a
semantic view via a SQL command overwrites any manual edits that you have made in an active Snowsight session. Preserving both sets of
changes is not supported.

## Conversion of YAML semantic models to native semantic views

You can convert existing stage-based semantic model YAML files to native semantic views using the
[SYSTEM$CREATE\_SEMANTIC\_VIEW\_FROM\_YAML](/sql-reference/stored-procedures/system_create_semantic_view_from_yaml) stored procedure. To export a semantic view
back to YAML, use the [SYSTEM$READ\_YAML\_FROM\_SEMANTIC\_VIEW](/sql-reference/functions/system_read_yaml_from_semantic_view) function.

If you’re migrating from the legacy stage-based YAML approach, see
[Migrating from the legacy stage API](/user-guide/views-semantic/semantic-models-vs-views). For guidance
on choosing between YAML and DDL as an authoring format, see
[YAML vs DDL authoring](/user-guide/views-semantic/yaml-vs-ddl).

Note

Snowflake doesn’t support bulk conversion of semantic models. You must convert YAML files to semantic views
one at a time. If you need bulk conversion or CI/CD integration, script the conversions in a series.

## Automated deployment of semantic views

Where possible, leverage CI/CD pipelines and programmatic interfaces to create, modify, and manage semantic views. Ideally,
set up your workflow so that semantic view updates are synchronized automatically with your Git repository. This approach reduces manual errors
that might be caused by copying and pasting or pushing changes to Git.

- Store the semantic view YAML (or SQL DDL) in a Git repository; this approach supports version control, peer review, history, and rollback.
- If you are using Snowsight, export or download the YAML model regularly and commit it to Git.
- Trigger CI/CD pipelines on changes to Git (to run tests and accuracy checks, then deploy only if these tests pass).
- If necessary, roll back by redeploying the previous known-good YAML or DDL from Git.

To promote models from dev to test or production environments, you can incorporate automated deployment scripts for that purpose, or you
can use [schema-level cloning](/sql-reference/sql/create-clone). Semantic views are cloned when schemas that contain them are cloned.
Cloning is a good option for promoting semantic views across databases and environments that use the same Snowflake account. To promote
semantic views across accounts, you can use [account replication](/user-guide/account-replication-intro).

Semantic views can be shared directly via the [Snowflake Marketplace](/collaboration/collaboration-marketplace-about) and
[data sharing](/guides-overview-sharing). You can create [secure views](/user-guide/views-secure) based on semantic views, and sharing
these nested views is supported. However, some resharing scenarios have limitations (such as when a consumer of a share wishes to further share a
view built on a semantic view).

To support materializing and maintaining semantic views as part of a Snowflake data pipeline, you can use a dbt project;
see [Integration with dbt projects](#label-semantic-views-dbt-integration). Support for a similar process using the [Snowflake Terraform provider](/user-guide/terraform) is planned.

Ultimately, your goal should be to enable a workflow that is similar to the following dbt example:

- Work on dbt project changes in an IDE, such as VS Code.
- Add a new semantic view definition to the dbt code.
- Push the changes to Git.
- Set up triggers that do a `dbt run` operation as part of the data pipeline.

As a result, the semantic view would be materialized in the Snowflake account.

## Integration with dbt projects

You can integrate semantic views into your dbt workflow by installing the `dbt_semantic_view` package that is available
from Snowflake Labs: <https://hub.getdbt.com/Snowflake-Labs/dbt_semantic_view/latest/>.

This package works natively with [dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake) or any dbt installation that has
access to a Snowflake account. You can use this package to materialize semantic views via dbt and reference them from downstream models.

Note

The code samples in Snowflake Labs are intended for reference, testing, and educational purposes. These code samples aren’t covered by any
Service-Level Agreement.

The following instructions assume that you are familiar with dbt and already have dbt installed in an environment that can connect to Snowflake.

To install and use the `dbt_semantic_view` package:

1. Add the following code to your `packages.yml` file:

   Copy code

   ```
   packages:
     - package: Snowflake-Labs/dbt_semantic_view
    version: 1.0.3
   ```

   Specify the version number. To find the current version, see the [dbt\_semantic\_view package page](https://hub.getdbt.com/Snowflake-Labs/dbt_semantic_view/latest/).

   Note

   The `dbt_semantic_view` package is a direct passthrough to Snowflake’s SQL layer.
   You don’t need to update the package version to access new Snowflake semantic view
   features. When Snowflake adds new SQL capabilities (for example, AI\_VERIFIED\_QUERIES),
   they will be available immediately via the package without any package update.
2. Run the `dbt deps` command to install the package.
3. In the dbt `models` directory, create a model that uses the semantic view materialization code:

   Copy code

   ```
   {{ config(materialized='semantic_view') }}

   TABLES(
   {{ source('<source_name>', '<table_name>') }},
   {{ ref('<another_model>') }}
   )
   [ RELATIONSHIPS ( relationshipDef [ , ... ] ) ]
   [ FACTS ( factExpression [ , ... ] ) ]
   [ DIMENSIONS ( dimensionExpression [ , ... ] ) ]
   [ METRICS ( metricExpression [ , ... ] ) ]
   [ COMMENT = '<comment>' ]
   [ COPY GRANTS ]
   ```

   For example, you can materialize a simple semantic view as follows:

   Copy code

   ```
   {{ config(materialized='semantic_view') }}

   TABLES(t1 AS {{ ref('base_table') }}, t2 as {{ source('seed_sources', 'base_table2') }})
   DIMENSIONS(t1.count as value, t2.volume as value)
   METRICS(t1.total_rows AS SUM(t1.count), t2.max_volume as max(t2.volume))
   COMMENT='test semantic view'
   ```
4. Configure your connection to Snowflake in dbt, specifying the connection details in your dbt
   `profiles.yml` file. For more information, see the
   [dbt documentation](https://docs.getdbt.com/docs/core/connect-data-platform/profiles.yml). For example:

   Copy code

   ```
   semantic_project:
     target: snowflake
     outputs:
    snowflake:
    type: "snowflake"
    account: "{{ env_var('SNOWFLAKE_ACCOUNT') }}"
    user: "{{ env_var('SNOWFLAKE_USER') }}"
    password: "{{ env_var('SNOWFLAKE_PASSWORD') }}"
    authenticator: "{{ env_var('SNOWFLAKE_AUTHENTICATOR') }}"
    role: "{{ env_var('SNOWFLAKE_ROLE') }}"
    database: "{{ env_var('SNOWFLAKE_DATABASE') }}"
    warehouse: "{{ env_var('SNOWFLAKE_WAREHOUSE') }}"
    schema: "{{ env_var('SNOWFLAKE_SCHEMA') }}"
    threads: 4
   ```
5. Given this profile, you could authenticate with the following environment variables:

   Copy code

   ```
   $ export SNOWFLAKE_ACCOUNT=snowflake_acct1
   $ export SNOWFLAKE_USER=sem_user1
   $ export SNOWFLAKE_PASSWORD=**************
   $ export SNOWFLAKE_AUTHENTICATOR=externalbrowser
   $ export SNOWFLAKE_ROLE=semantic_role
   $ export SNOWFLAKE_DATABASE=sem_db
   $ export SNOWFLAKE_WAREHOUSE=sem_wh
   $ export SNOWFLAKE_SCHEMA=sem_schema
   ```
6. Run the `dbt build` command to connect to your Snowflake account and create the model. The following
   example builds a specific model defined as `models/semantic_view_basic`. Note that another model,
   `table_refer_to_semantic_view`, depends on this model, so the command requires the `+` sign at the end.

   Copy code

   ```
   $ dbt build --target snowflake --select semantic_view_basic+
   23:43:16  Running with dbt=1.11.0-b3
   23:43:17  Registered adapter: snowflake=1.10.2
   23:43:17  Found 9 models, 8 data tests, 1 seed, 2 operations, 2 sources, 500 macros
   23:43:17
   23:43:17  Concurrency: 4 threads (target='snowflake')
   23:43:17
   23:43:32  1 of 2 START hook: dbt_semantic_view_integration_tests.on-run-start.0 .......... [RUN]
   23:43:32  1 of 2 OK hook: dbt_semantic_view_integration_tests.on-run-start.0 ............. [OK in 0.90s]
   23:43:33  2 of 2 START hook: dbt_semantic_view_integration_tests.on-run-start.1 .......... [RUN]
   23:43:33  2 of 2 OK hook: dbt_semantic_view_integration_tests.on-run-start.1 ............. [OK in 0.38s]
   23:43:33
   23:43:33  1 of 6 START sql semantic_view model sem_schema.semantic_view_basic ............ [RUN]
   23:43:33  1 of 6 OK created sql semantic_view model sem_schema.semantic_view_basic ....... [SUCCESS 1 in 0.26s]
   23:43:33  3 of 6 START test semantic_view_basic_has_no_copy_grants ....................... [RUN]
   23:43:33  2 of 6 START test semantic_view_basic_has_comment .............................. [RUN]
   23:43:33  4 of 6 START test semantic_view_sum_matches_base_table ......................... [RUN]
   23:43:33  2 of 6 PASS semantic_view_basic_has_comment .................................... [PASS in 0.23s]
   23:43:34  3 of 6 PASS semantic_view_basic_has_no_copy_grants ............................. [PASS in 0.75s]
   23:43:34  4 of 6 PASS semantic_view_sum_matches_base_table ............................... [PASS in 1.05s]
   23:43:34  5 of 6 START sql table model sem_schema.table_refer_to_semantic_view ........... [RUN]
   23:43:35  5 of 6 OK created sql table model sem_schema.table_refer_to_semantic_view ...... [SUCCESS 1 in 1.22s]
   23:43:35  6 of 6 START test table_refer_semantic_view_matches_semantic_view .............. [RUN]
   23:43:36  6 of 6 PASS table_refer_semantic_view_matches_semantic_view .................... [PASS in 0.26s]
   23:43:36
   23:43:36  Finished running 2 project hooks, 1 semantic view model, 1 table model, 4 data tests in 0 hours 0 minutes and 19.34 seconds (19.34s).
   23:43:36
   23:43:36  Completed successfully
   23:43:36
   23:43:36  Done. PASS=8 WARN=0 ERROR=0 SKIP=0 NO-OP=0 TOTAL=8
   ```

For more information about the `dbt_semantic_view` package, which includes pre-built models and tests that you can run,
see the `README.md` file. Go to <https://hub.getdbt.com/Snowflake-Labs/dbt_semantic_view/latest/> and select **View on GitHub**.

See also <https://www.snowflake.com/en/engineering-blog/dbt-semantic-view-package/>.

## Integration with BI tools

A number of BI tool vendors offer integrations with Snowflake semantic views. To learn more about these integrations, please contact
your BI tool account teams and follow these links:

- Sigma: <https://www.sigmacomputing.com/blog/snowflake-semantic-views-launch>
- Omni: <https://omni.co/snowflake>
- Honeydew: <https://honeydew.ai/blog/honeydew-and-snowflake-semantic-views/>
- Hex: <https://hex.tech/blog/introducing-snowflake-semantic-sync-aisql/>
- ThoughtSpot: <https://www.thoughtspot.com/blog/snowflake-semantic-views-thoughtspot-one-ai-context-layer>
