# Tutorial: Get started with collaboration clean rooms (API)

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

## Introduction

This tutorial is aimed at developers who want to create and use collaboration clean rooms using the Snowflake Data Clean Rooms API.
You will work through a two-account scenario where two collaborators share data, register templates, and run analyses.

### What you will learn

This tutorial shows you how to:

- Register data offerings and templates in the clean rooms registry.
- Create a collaboration using a YAML collaboration specification.
- Join a collaboration from a second account.
- Link templates and data offerings to an existing collaboration.
- Run analyses as different collaborators with different permissions.

### Requirements to run this tutorial

- Two Snowflake accounts, Enterprise Edition or higher, each with the Snowflake Data Clean Rooms environment installed.
  If clean rooms isn’t installed, see [Installing the Snowflake Data Clean Rooms environment](/user-guide/cleanrooms/installing-dcr).
- The SAMOOHA\_APP\_ROLE must be granted to the user in each account.

Note

This tutorial requires **two separate Snowflake accounts**. You will run Alice’s steps in one account and Bob’s steps in the other.
Each section heading indicates which account to use.

The tutorial includes code snippets with `<placeholders>` that you should replace with the appropriate values.

## Collaboration basics

A collaboration clean room allows multiple parties to share and analyze data securely without exposing raw data to each other.
Collaborations are defined by a YAML specification that lists the collaborators, their data, and what each party can do.

Key concepts used in this tutorial:

- **Collaboration specification**: A YAML document that defines the collaborators, their aliases, roles, data offerings, and templates.
- **Collaboration roles**: Each collaborator is assigned one or more roles:

  - **Owner**: Creates and manages the collaboration. There is exactly one owner per collaboration.
  - **Data provider**: Contributes data offerings that other collaborators can use in analyses.
  - **Analysis runner**: Runs templates against the shared data. Each analysis runner has a list of data providers and templates
    available to use.

    In this tutorial:

    - **Alice** is the collaboration **owner**, a **data provider**, and an **analysis runner**.
    - **Bob** is a **data provider** and an **analysis runner**.
- **Data offering**: A table linked into the collaboration by a data provider.
- **Template**: A registered JinjaSQL query that analysis runners execute against a data offering.

In this tutorial, Alice and Bob each contribute one data offering. Alice registers a template that only Alice can run.
Bob registers a template that both Alice and Bob can run. Both templates join the two collaborators’ data on a shared column.

## Alice: Register resources

Run the following steps in **Alice’s account** to set up the session environment and create sample data:

Copy code

```
USE WAREHOUSE APP_WH;
USE ROLE SAMOOHA_APP_ROLE;

-- Secondary roles must be disabled to call link_data_offerings.
USE SECONDARY ROLES NONE;

-- Create sample data for Alice.
CREATE DATABASE IF NOT EXISTS ALICE_DB;
CREATE SCHEMA IF NOT EXISTS ALICE_DB.ALICE_SCH;
CREATE OR REPLACE TABLE ALICE_DB.ALICE_SCH.ALICE_DATA AS
  SELECT * FROM SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS LIMIT 100;
```

Note

In real-world usage, we recommend [assigning more fine-grained privileges](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-access-management-api) to your
users instead of using the top-level SAMOOHA\_APP\_ROLE role.

Next, you will register a data offering and a template to use in the collaboration.

### Register a data offering

A data offering is a registered dataset with column-level policies that control how collaborators can use the data.
You will create a data offering from the sample data you created.

Register Alice’s data offering so that it can be included in the collaboration specification. Data offerings are defined by a YAML data
offering specification.

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.REGISTER_DATA_OFFERING(
    $$
    api_version: 2.0.0
    spec_type: data_offering
    version: v1
    name: alice_customer_data
    datasets:
     - alias: customer_list
       data_object_fqn: ALICE_DB.ALICE_SCH.ALICE_DATA
       object_class: custom
       allowed_analyses: template_only
       schema_and_template_policies:
         hashed_email:
           category: join_standard
           column_type: hashed_email_b64_encoded
         status:
           category: passthrough
    $$
    );
```

The data-offering specification defines the following properties:

- `datasets`: A list of tables or views to share.
- `alias`: A short name used to reference this dataset within this spec and by templates.
- `allowed_analyses`: Restricts usage to templates only (no free-form SQL).
- `schema_and_template_policies`: Defines the format, naming, and availability of columns from this data source.
  The data offering exposes only two columns from your source table: `hashed_email` (which must be used as a join column) and `status`.

Save the data offering ID from the response. You will need it when creating the collaboration specification.

Copy code

```
-- Save the ID.
SET alice_data_offering_id = '<alice_data_offering_id>';

-- View your registered data offerings.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.VIEW_REGISTERED_DATA_OFFERINGS();
```

### Register a template

A template is a JinjaSQL query that analysis runners execute in the collaboration. Register a template that joins two tables
on the hashed email column and counts matches grouped by status:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.REGISTER_TEMPLATE(
$$
api_version: 2.0.0
spec_type: template
name: alice_only_template
version: v1
type: sql_analysis
description: Joins two tables on hashed email and counts matches grouped by status.
template:
  SELECT T.status, COUNT(*)
    FROM IDENTIFIER( {{ source_table[0] }} ) AS T
      JOIN IDENTIFIER( {{ source_table[1] }} ) AS T1
      ON T.hashed_email_b64_encoded = T1.hashed_email_b64_encoded
    GROUP BY T.status;
$$);
```

The template uses two tables `source_table[0]` and `source_table[1]`. These are data offerings present in the collaboration. The analysis runner passes in the names of the tables to use when they run the analysis.

Note

This tutorial uses `T` and `T1` as table aliases for simplicity. In production templates, you should use the
[standard aliases](/user-guide/cleanrooms/custom-templates#label-dcr-required-template-table-aliases) `p`, `p1`, `p2`, and so on, which are required for
Snowflake Data Clean Room policy enforcement.

Save the template ID from the response:

Copy code

```
-- Save the ID.
SET alice_template_id = '<alice_only_template_id>';

-- View all registered templates.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.VIEW_REGISTERED_TEMPLATES();
```

## Alice: Create the collaboration

Continue in **Alice’s account**.

Now that the resources are registered, Alice creates the collaboration. The collaboration is defined by a YAML specification
that lists the collaborators, their roles, data offerings, and templates.

Call INITIALIZE with the collaboration specification. Review the YAML carefully before running it:

Copy code

```
-- Replace the <...> placeholders with the appropriate values.
-- Get your account data sharing ID:
--   SELECT CURRENT_ORGANIZATION_NAME() || '.' || CURRENT_ACCOUNT_NAME();

CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.INITIALIZE(
$$
api_version: 2.0.0
spec_type: collaboration
name: api_tutorial_collaboration
owner: alice
collaborator_identifier_aliases:
  alice: <alice_account_data_sharing_id>
  bob: <bob_account_data_sharing_id>
analysis_runners:
  alice:
    data_providers:
      alice:
        data_offerings:
        - id: <alice_data_offering_id>
      bob:
        data_offerings: []
    templates:
    - id: <alice_only_template_id>
  bob:
    data_providers:
      alice:
        data_offerings:
        - id: <alice_data_offering_id>
      bob:
        data_offerings: []
$$,
'APP_WH'
);
```

### Understanding the collaboration specification

The collaboration specification uses the aliases defined in the `collaborator_identifier_aliases` section to refer to all collaborators.

The collaboration defines the following roles and relationships:

- `analysis_runners` lists the collaborators that can run analyses in this collaboration. Only collaborators listed at the top level here
  can run analyses.
- Each analysis runner entry has the following elements:

  - `data_providers`: Only these data providers can supply data to this analysis runner.
  - `data_offerings`: Only these data offerings from the listed data providers can supply data to this analysis runner.
- Only the templates listed for an analysis runner can be used. Notice that this collaboration currently shares the `alice_only_template`
  with Alice.

After the collaboration is created, the owner can request to add or remove collaborators, change collaborator roles, and change the data
providers, data offerings, and templates shared with each analysis runner by calling
[EDIT](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-edit-reference) (a
[preview feature](/release-notes/preview-features)); such changes require approval from the affected collaborators.

### Wait for the collaboration to be created and joined

INITIALIZE creates and joins the owner to the collaboration. This process is asynchronous.
Call GET\_STATUS until Alice’s status is `JOINED`:

Copy code

```
SET collaboration_name = '<collaboration_name>';

-- Check status. Repeat until the status is JOINED.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.GET_STATUS($collaboration_name);

-- Verify the collaboration is visible.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.VIEW_COLLABORATIONS();
```

### Enable template auto-approval

Whenever a collaborator asks to share a template with you in a collaboration, all designated recipients must approve the request before the
template is shared. This tutorial doesn’t cover the approval flow, so run the following code to automatically approve all requests:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.SET_CONFIGURATION(
  $collaboration_name,
  'TEMPLATE_AUTO_APPROVAL',
  'true'
);
```

## Bob: Join the collaboration

Switch to **Bob’s account** and run the following steps.

Set up the session environment:

Copy code

```
USE WAREHOUSE APP_WH;
USE ROLE SAMOOHA_APP_ROLE;

-- Secondary roles must be disabled to call join or link_data_offering.
USE SECONDARY ROLES NONE;
```

View the collaboration invitation, then join it:

Copy code

```
-- See which collaborations you are invited to, or have joined.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.VIEW_COLLABORATIONS();

-- Add the SOURCE_NAME and OWNER_ACCOUNT values from the response.
SET collaboration_name = '<collaboration_name>';
SET collaborator_data_sharing_id = '<alice_account_data_sharing_id>';

-- Review and join the collaboration.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.REVIEW(
  $collaboration_name,
  $collaborator_data_sharing_id
);
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.JOIN($collaboration_name);
```

Joining is asynchronous. Call GET\_STATUS until Bob’s status is `JOINED`:

Copy code

```
-- Check status. Repeat until the status is JOINED.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.GET_STATUS($collaboration_name);
```

## Bob: Link a template

Continue in **Bob’s account**.

Bob creates and registers a template. This template joins two tables on the hashed email column,
and returns a cross-tabulation of statuses from both tables. Templates are written in JinjaSQL; a template specification is written in
YAML, which contains the embedded JinjaSQL template.

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.REGISTER_TEMPLATE(
    $$
    api_version: 2.0.0
    spec_type: template
    name: bob_shared_template
    version: v1
    type: sql_analysis
    description: Cross-tabulates statuses from two tables joined on hashed email.
    template:
      SELECT T.status AS status_1, T1.status AS status_2, COUNT(*) AS match_count
        FROM IDENTIFIER({{ source_table[0] }}) AS T
          JOIN IDENTIFIER({{ source_table[1] }}) AS T1
          ON T.hashed_email_b64_encoded = T1.hashed_email_b64_encoded
        GROUP BY T.status, T1.status
        ORDER BY match_count DESC;
    $$
);
SET bob_template_id = '<bob_shared_template_id>';
```

Now request to link the template to the collaboration, and share it with both Alice and Bob. (Notice how you must explicitly request to
share a template with yourself; templates are not automatically shared with the account that registered them.)

Because Alice enabled template auto-approval, Alice automatically approves the request:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.ADD_TEMPLATE_REQUEST(
  $collaboration_name,
  $bob_template_id,
  ['alice', 'bob']
);
```

The template should be approved and added shortly.

Copy code

```
-- View the status of update requests.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.VIEW_UPDATE_REQUESTS($collaboration_name);
```

## Bob: Link a data offering

Continue in **Bob’s account**.

Create sample data and register a data offering:

Copy code

```
-- Create sample data.
CREATE DATABASE IF NOT EXISTS BOB_DB;
CREATE SCHEMA IF NOT EXISTS BOB_DB.BOB_SCH;
CREATE OR REPLACE TABLE BOB_DB.BOB_SCH.BOB_DATA AS
  SELECT * FROM SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS_2 LIMIT 100;

-- Register Bob's data offering.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.REGISTER_DATA_OFFERING(
    $$
    api_version: 2.0.0
    spec_type: data_offering
    version: v1
    name: bob_customer_data
    datasets:
     - alias: my_customer_list
       data_object_fqn: BOB_DB.BOB_SCH.BOB_DATA
       object_class: custom
       allowed_analyses: template_only
       schema_and_template_policies:
         hashed_email:
           category: join_standard
           column_type: hashed_email_b64_encoded
         status:
           category: passthrough
    $$
);
SET bob_data_offering_id = '<bob_data_offering_id>';
```

The collaboration specification lists `bob` as a potential data provider for both `alice` and `bob`. Link the data offering into the
collaboration, and share it with both `alice` and `bob`:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.LINK_DATA_OFFERING(
  $collaboration_name,
  $bob_data_offering_id,
  ['alice', 'bob']
);

-- Verify that both data offerings are now available.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.VIEW_DATA_OFFERINGS(
  $collaboration_name
);
```

You don’t need approvals when you share data with other collaborators.

## Alice: Run an analysis

Switch back to **Alice’s account**.

Alice runs the `alice_only_template`, which is available only to Alice. The template joins Alice’s data offering
with Bob’s data offering on the hashed email column and groups results by status.

First, view the available data offerings and templates:

Copy code

```
-- View available data offerings.
-- Note the view names in the TEMPLATE_VIEW_NAME column; you need these for the analysis spec.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.VIEW_DATA_OFFERINGS(
  $collaboration_name
);

-- View available templates.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.VIEW_TEMPLATES(
  $collaboration_name
);
```

Now, run the analysis. Replace the placeholders with actual values. Replace the `source_tables` names with view names from
VIEW\_DATA\_OFFERINGS.

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.RUN(
  $collaboration_name,
    $$
    api_version: 2.0.0
    spec_type: analysis
    description: Alice runs the alice_only_template with both data offerings.
    template: '<alice_only_template_id>'
    template_configuration:
      view_mappings:
        source_tables:
          - '<alice_data_offering_view_name>'
          - '<bob_data_offering_view_name>'
    $$
  );
```

The results show the count of matching records grouped by status from Alice’s data.

## Bob: Run an analysis

Switch to **Bob’s account**.

Bob runs the `bob_shared_template`, which is available to both collaborators. This template cross-tabulates the statuses from
both tables.

Replace the `source_tables` placeholders with actual view names from VIEW\_DATA\_OFFERINGS.

Copy code

```
-- View available data offerings and templates.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.VIEW_DATA_OFFERINGS(
  $collaboration_name
);
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.VIEW_TEMPLATES(
  $collaboration_name
);

-- Run the analysis.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.RUN(
    $collaboration_name,
    $$
    api_version: 2.0.0
    spec_type: analysis
    description: Bob runs the bob_shared_template with both data offerings.
    template: '<bob_shared_template>'
    template_configuration:
      view_mappings:
        source_tables:
          - '<alice_data_offering_view_name>'
          - '<bob_data_offering_view_name>'
    $$
);
```

The results show a cross-tabulation of statuses from both data offerings, with the count of matching records for each combination.

Bob cannot run `alice_only_template` because Alice did not include Bob as a permitted user
for that template in the collaboration specification. Try running it to see what happens.

## Alice: Clean up resources

Switch to **Alice’s account** to clean up all the resources used.

Tearing down a collaboration is a multi-step process. Call TEARDOWN, wait for the status to reach `LOCAL_DROP_PENDING`,
and then call TEARDOWN again:

Copy code

```
-- Start the teardown process.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.TEARDOWN($collaboration_name);

-- Check status. Repeat until the status is LOCAL_DROP_PENDING.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.GET_STATUS($collaboration_name);

-- Complete the teardown.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.TEARDOWN($collaboration_name);

-- Clean up the sample database.
DROP DATABASE IF EXISTS ALICE_DB;
```

Switch to Bob’s account and clean up the sample database:

Copy code

```
DROP DATABASE IF EXISTS BOB_DB;
```

Note

Tearing down the collaboration doesn’t delete registered templates or data offerings from either account’s registry.

## Summary

In this tutorial, you learned how to:

- Register templates and data offerings in the clean rooms registry.
- Create a collaboration with a YAML specification that defines collaborators, roles, data, and templates.
- Join a collaboration from a second account.
- Link templates and data offerings to an existing collaboration using update requests.
- Run analyses as different collaborators with different levels of access.

### Next steps

- You can find tutorials, sample worksheets, and video walkthroughs in [Sample Worksheets and Videos](/user-guide/cleanrooms/tutorials-and-samples).
- Learn more about collaboration specifications in the [Overview of Snowflake Data Clean Rooms](/user-guide/cleanrooms/overview).
- Explore the full [Snowflake Data Clean Rooms Collaboration API](/user-guide/cleanrooms/collaboration-api-reference).
- Learn about [collaboration roles](/user-guide/cleanrooms/roles) and how to manage access.
- Learn how to [activate query results](/user-guide/cleanrooms/activation) to export data to a collaborator’s account.
