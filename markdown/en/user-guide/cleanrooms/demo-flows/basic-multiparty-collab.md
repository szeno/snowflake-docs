# Basic multi-party collaboration

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

## Introduction

This topic walks through the steps to create a basic multi-party collaboration. It demonstrates how to register templates and data
offerings, how to add data to the initial version of a collaboration, and how collaborators can add resources after the collaboration is
created. It also demonstrates how to run queries using templates and data resources in the collaboration.

## Basic clean room collaboration workflow

Here is a basic multi-party clean room collaboration scenario:

1. The collaboration [owner](/user-guide/cleanrooms/roles) registers any templates or data offerings that they want to appear in the
   initial configuration of the collaboration.
2. The owner optionally asks any intended collaborators to register templates or data offerings that they want to appear in the initial
   configuration of the collaboration. Collaborators then give the resource IDs of the registered items to the owner.
3. The owner [creates a collaboration](#label-dcr-collaboration-create-collaboration). The collaboration is defined by a
   collaboration YAML spec that lists the collaborators, their collaboration roles, and all resources that should be present in the initial
   version of the collaboration.

   - The owner can request to add or remove collaborators and change collaborator roles after the collaboration is created by calling [EDIT](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-edit-reference) (a [preview feature](/release-notes/preview-features)). These changes take effect after the affected collaborators approve them.
   - Additional resources can be added by collaborators after the collaboration is created, if their collaboration role permits it.
   - If your collaboration shares data with users in other cloud hosting regions, the sharer must [enable Cross-Cloud Auto-Fulfillment on their account](/user-guide/cleanrooms/laf#label-dcr-collab-enabling-laf).
4. Collaborators [review and join the collaboration](#label-dcr-collaboration-join-collaboration).
5. Collaborators can then optionally
   [link additional resources to the collaboration](#label-dcr-collaboration-add-resources-to-collab), such as templates and data
   offerings, depending on their collaboration roles. Additional resources can be added to a collaboration at any time.
6. Analysis runners can [run any templates assigned to them](#label-dcr-collab-run-an-analysis) in the collaboration, using any data
   available to them in the collaboration. The analysis runner bears the cost of the analysis. Templates can be designed either to return
   query results in the response or to [activate results to the caller or another collaborator](/user-guide/cleanrooms/activation#label-dcr-collaboration-activating-results).

The following sections describe the details of each of these steps.

## Create a collaboration

To create a collaboration, you design a [collaboration spec](/user-guide/cleanrooms/spec-collaboration#label-dcr-collaboration-spec-yaml) that defines all the collaborators
[and their collaboration roles](/user-guide/cleanrooms/roles).

If you want to make resources available in a collaboration as soon as it is created, the collaboration owner
[registers and links those resources](#label-dcr-collaboration-add-resources-to-collab) before creating the collaboration, and
includes the resource IDs in the collaboration spec.

If the owner expects to use resources from collaborators, the owner can also prompt those users to register their resources and give the
owner the resource IDs to include in the collaboration spec. The owner also indicates in the collaboration spec where no resources are
linked now, but can be linked in the future.

The owner then calls INITIALIZE to begin creating the collaboration. By default, INITIALIZE also automatically joins the owner to the
collaboration. This is an asynchronous process, so the owner must call GET\_STATUS until the status is JOINED.

The following snippet demonstrates creating and joining a collaboration.

Copy code

```
  CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.INITIALIZE(
    $$
    api_version: 2.0.0
    spec_type: collaboration
    name: my_first_collaboration
    owner: alice
    collaborator_identifier_aliases:
      alice: example_com.acct_abc
      bob: another_example.acct_xyz
    analysis_runners:
      bob:
        data_providers:
          alice:
            data_offerings: [] -- alice has not provided data to bob, but can do so in the future.
          bob:
            data_offerings: [customers_v1]  -- bob has registered a data offering and made it available to himself.
        templates: []   -- No templates available yet for bob.
      alice:
        data_providers:
          alice:
            data_offerings: []
          bob:
            data_offerings: []
        templates: []
    $$,
    'APP_WH'            -- Use this warehouse for initialization.
  );                    --  XSMALL or SMALL warehouses are recommended for initialization.
  SET collaboration_name = 'my_first_collaboration';

  -- INITIALIZE automatically joins the owner. Check status until JOINED.
  CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.GET_STATUS($collaboration_name);

  -- Collaboration is visible here when it's joined.
  CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.VIEW_COLLABORATIONS();
```

**Notes on the script:**

- The collaboration consists of two collaborators, with the aliases `alice` and `bob`. You can use a full data-sharing ID anywhere you
  use an alias, but that is much less user-friendly.
- `alice` is the owner.
- Both `alice` and `bob` are analysis runners.
- Both `alice` and `bob` are data providers to each other.
- If you are a data provider, you must include the `data_offerings` field. This field can be populated or empty, indicating that there
  are no data offerings now, but they can be added later.
- `alice` isn’t providing data to `bob` or herself, but can do so later (lines 14, 22).
- `bob` has already registered a data offering, and provided it to himself in the initial collaboration (line 16).
- `bob` isn’t providing data to `alice`, but can do so later (line 24).
- Neither `alice` nor `bob` has templates available yet, but they can be assigned later (lines 18, 25). Note that the
  `templates` field is optional for an analysis runner. If you omit this field during initialization, collaborators can still assign
  templates to this analysis runner later.

## Link resources to a collaboration

Collaborators can link resources into a collaboration, or remove resources that they have linked into the collaboration, according to their
collaboration role. There are two steps to linking a resource into a collaboration:

1. The resource owner creates a [resource definition spec](/user-guide/cleanrooms/spec-reference) for the resource and uses it to
   register the resource in their account. You can register the resource in your account’s
   [default registry](/user-guide/cleanrooms/registries), or use a custom registry.
2. A collaborator links the resource into a collaboration. Resources can be linked into a collaboration either when the collaboration is
   created, by hard-coding the resource ID into the YAML definition used to create the collaboration, or after the collaboration is created
   and joined, by calling the appropriate procedure to link the resource into the collaboration.

After the resource is linked in, it can be used by the designated collaborators. Some resource types, such as templates, can be linked in
by any collaborator; other resources, such as data offerings, can be linked in only by users with the data provider collaboration role.
However, note that you must join a collaboration before any resources you contributed become available to the collaboration.

If you share data with users in other cloud hosting regions, the sharer must
[enable Cross-Cloud Auto-Fulfillment on their account](/user-guide/cleanrooms/laf#label-dcr-collab-enabling-laf).

Resources are available only to the collaborators designated by the collaboration spec.

Note

Updates to an existing collaboration, such as linking or removing resources, are asynchronous and take some time to complete. Call
VIEW\_UPDATE\_REQUESTS to see the status of an update. Using a resource before it becomes fully available can result in
inconsistent behavior.

Resources support versioning; however, creating a new resource with a new version doesn’t remove the previous version from the
collaboration. Resources are uniquely named by combining the user-provided name and version (and alias, for data offerings).

To learn more about using resources in your collaboration, see [Resources](/user-guide/cleanrooms/resources).

## Review and join a collaboration

You must join a collaboration to share resources and run analyses in the collaboration.

- *The creator* joins automatically when calling INITIALIZE if `auto_join_warehouse` is provided. If `auto_join_warehouse` isn’t
  provided, the creator calls JOIN after INITIALIZE is complete.
- *Non-creators* call REVIEW, and then JOIN.
  - REVIEW returns an overview of the collaboration and its resources. You can call REVIEW only once.
  - JOIN installs the collaboration clean room in your account and joins the collaboration.

Both INITIALIZE and JOIN are asynchronous procedures that take several minutes to complete. You must call GET\_STATUS to see when each step
is complete.

Important

If your account’s cloud hosting region is different from the collaboration owner’s, REVIEW triggers additional asynchronous setup
steps. Call REVIEW repeatedly until it returns a successful response, indicating that setup is complete.

Joining is an asynchronous process; call GET\_STATUS to see when your status is listed as JOINED.

## Run an analysis

If you have the analysis runner role in a collaboration, you can run analyses against data sources shared with you in the collaboration.

Collaborations support two types of queries:

- **Template analyses.** These queries run a template (a templated JinjaSQL statement) linked into the collaboration. Templates can be
  either analysis templates, which return results immediately to you, or activation templates, which save results to the Snowflake account
  of a designated participant.
- **Free-form SQL queries.** If allowed by a data provider, you can access specified data offerings using SQL when signed in with your
  collaborator credentials. You run SQL queries directly, without calling a Collaboration API procedure, by accessing the fully qualified
  view name exposed by the collaboration.

The analysis runner bears the cost of running an analysis.

The collaboration specification determines whether you can run a template, activate results, or run free-form SQL queries. Your
capabilities, as well as the data and templates available for you to use, are described in the collaboration specification.

Note

Columns from the data sources might have new names when exposed to the template or user. See [Source column renaming](/user-guide/cleanrooms/resources-data-offerings#label-dcr-source-column-renaming) to
learn how and when source columns are renamed. Templates and user-provided arguments (such as a join column name) must use the final
name, not the original name, if the column is renamed.

Learn more about all these analysis types in the following sections.

- [Run an analysis from a template](#run-an-analysis-from-a-template)
- [Enable and run free-form SQL queries on your data](#enable-and-run-free-form-sql-queries-on-your-data)
- [Run an analysis with your own data when you use Standard Edition](#run-an-analysis-with-your-own-data-when-you-use-standard-edition)
- [Activate results](#activate-results)

### Run an analysis from a template

To run an analysis from a template, view the list of templates that you can run, view the list of data offerings that you can use, then
call RUN with your values either as individual parameters or as an analysis specification in YAML format.

Tables that you pass into the `source_tables` field in the run configuration populate the `source_table` parameter in the template. The
template’s `my_table` parameter is not populated or used unless you are using Snowflake Standard Edition with your own data.

Note

Resource installation is asynchronous. If a template was just installed, it can take a short while before it is available to run. If
the template includes a code spec, it can take additional time before the template is available.
[See how to determine when a code spec is available](/user-guide/cleanrooms/resources-code-specs#label-dcr-collab-check-patch-update-for-code-spec).

The following example lists data offerings and templates that the user can access, then runs an analysis using the `sales_join_template`
template (which is assumed to be listed by VIEW\_TEMPLATES), passing in five named arguments to the template.

Copy code

```
-- See which data offerings are available.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.VIEW_DATA_OFFERINGS($collaboration_name);

-- See which templates you can run.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.VIEW_TEMPLATES($collaboration_name);

-- Pass in the arguments in analysis YAML format.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.RUN(
  $collaboration_name,
  $$
    api_version: 2.0.0
    spec_type: analysis
    name: My_analysis
    description: Sales results Q2 2025
    template: sales_join_template

    template_configuration:
      view_mappings:
        source_tables:
          -  user1_alias.data_offering_v1.table_1
          -  user2_alias.another_data_offering_v1.table_2
      arguments:                                            -- The template defines conv_purchase_id and the other four arguments.
         conv_purchase_id: PURCHASE_ID                      -- You must examine a template to see which arguments it supports.
         conv_purchase_amount: PURCHASE_AMOUNT
         publisher_impression_id: IMPRESSION_ID
         publisher_campaign_name: CAMPAIGN_NAME
         publisher_device_type: DEVICE_TYPE
  $$ );
```

### Enable and run free-form SQL queries on your data

A data provider can grant analysis runner permission to run arbitrary SQL queries against their data offerings.
This means that the analysis runner can run an arbitrary SQL query directly against the data offering, rather than calling a template.

To learn more about free-form SQL queries, see [Free-form SQL queries](/user-guide/cleanrooms/free-form-sql).

### Run an analysis with your own data when you use Standard Edition

If you use Standard Edition, you can run an analysis [in the standard way](#label-dcr-collab-run-an-analysis). However,
you can’t link data into the collaboration to share with other users. The only way to pass your own datasets into a template is to use the
technique described here.

**To use your own data in a collaboration on Snowflake Standard Edition:**

1. Register your data offering by calling REGISTER\_DATA\_OFFERING.
2. Call LINK\_LOCAL\_DATA\_OFFERING to link your data into the collaboration for you to use. No other collaborators can see or access data
   linked locally.
3. Use the data offering ID when you call [RUN](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-run-reference).

> - If you are using the parameterized version of RUN, pass your data offering IDs to the `local_template_view_names` parameter
> - If you are using the YAML version of RUN, provide your data offering IDs in the `local_view_mappings.my_tables` stanza of the request
>
> Tip
>
> `local_template_view_names` and `local_view_mappings.my_tables` populate the `my_table` parameter in the template.

The following example shows how to run a template using the YAML format version of the run procedure. This example includes the
`my_tables` field, which is populated by calling LINK\_LOCAL\_DATA\_OFFERING.

Copy code

```
-- See what data offerings are available. Your own local data will be listed here as well.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.VIEW_DATA_OFFERINGS($collaboration_name);

-- Pass in the arguments in analysis YAML format.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.RUN(
  $collaboration_name,
  $$
    api_version: 2.0.0
    spec_type: analysis
    name: my_analysis
    description: Cross-purchase results for Q4 2025
    template: mytemplate_v1

    template_configuration:
      view_mappings:
        source_tables:
          - ADVERTISER1.ADVERTISER_DATA_V1.CUSTOMERS
          - PUBLISHER.ADVERTISER_DATA_V1.CUSTOMERS
      local_view_mappings:
        my_tables:
          - PARTNER.MY_DATA_V1.MY_CUSTOMERS # Populate my_table array with my own table.
      arguments:  # Template arguments, as name: value pairs
         conv_purchase_id: PURCHASE_ID
         conv_purchase_amount: PURCHASE_AMOUNT
         publisher_impression_id: IMPRESSION_ID
         publisher_campaign_name: CAMPAIGN_NAME
         publisher_device_type: DEVICE_TYPE
  $$ );
```

### Activate results

If the data provider and the collaboration spec allow it, you can save analysis results to your own Snowflake account, or the Snowflake
account of a designated collaborator. A template either activates results or returns results immediately, not both.

To learn more about activation, see [Activating query results](/user-guide/cleanrooms/activation).

## Leave or delete a collaboration

- Non-owners leave a collaboration by calling LEAVE. Any data offerings they have provided will be removed from the collaboration. You
  can’t rejoin a collaboration after leaving it.
- Collaboration owners can’t leave a collaboration because ownership can’t be transferred. A collaboration owner can drop a collaboration for all collaborators by calling TEARDOWN.

Both processes are asynchronous. You must call GET\_STATUS to monitor the status, and call LEAVE or TEARDOWN again when GET\_STATUS shows the
status as LOCAL\_DROP\_PENDING.

After the owner tears down a collaboration, every collaborator who was still a member sees the LOCAL\_DROP\_PENDING status and must call LEAVE
once to remove the clean room application and collaboration metadata from their own account. For details, see
[LEAVE](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-leave-reference).

## Examples

The following SQL examples demonstrate how to create and run a basic collaboration:

- [Two-party collaboration example](#two-party-collaboration-example)
- [Single-party collaboration example](#single-party-collaboration-example)

### Two-party collaboration example

The following example demonstrates a two-party collaboration, where one party (named “alice”) is the collaboration creator, a data provider
for herself and “bob”, and an analysis runner. “bob” is a data provider for himself and “alice”, and is also an analysis runner.

The example demonstrates the following actions:

- Creating a collaboration.
- Registering templates and data offerings.
- Linking a template and data offering at collaboration creation time.
- Joining a collaboration.
- Linking additional resources to an existing collaboration.
- Running an analysis.

To run this example, you must have two separate accounts with Snowflake Data Clean Rooms installed.

You can either download the files and upload them to your Snowflake account, or copy and paste the example code into worksheets in two
separate accounts by using Snowsight.

File downloads"alice" code"bob" code

Download the source SQL files, then upload them into two separate accounts that have Snowflake Data Clean Rooms installed:

- [Collaboration owner “alice” worksheet](/static/samples/clean-rooms/demo-collaboration-hub-alice.sql)
- [Collaboration member “bob” worksheet](/static/samples/clean-rooms/demo-collaboration-hub-bob.sql)

Copy code

```
-- Basic Snowflake Collaboration Data Clean Rooms example.
-- This file represents user "alice" in a two-collaborator clean room example.

-- Run this worksheet in a Snowflake account with access to the latest version of
-- Snowflake Data Clean Rooms.

-- This file demonstrates the following actions:
-- * How to register a template and a dataset
-- * How to create a collaboration with pre-registered resources.
-- * How to add a template to a collaboration that has already been created, and the
--   template approval flow.
-- * How to run an analysis.

-- This scenario involves two collaborators: bob and alice
-- bob and alice each submits one data source
-- bob and alice are data providers for themselves and each other
-- bob submits one template that only alice can use
-- alice submits one template that they can both use, and one template that only alice can use

-- For more information, read docs.snowflake.com/user-guide/cleanrooms/overview

USE WAREHOUSE APP_WH;
USE ROLE SAMOOHA_APP_ROLE;

-- Secondary roles must be disabled to call link_data_offerings.
USE SECONDARY ROLES NONE;

CREATE DATABASE IF NOT EXISTS ALICE_DB;
CREATE SCHEMA IF NOT EXISTS ALICE_DB.ALICE_SCH;
CREATE OR REPLACE TABLE ALICE_DB.ALICE_SCH.ALICE_DATA AS SELECT * FROM samooha_sample_database.demo.customers LIMIT 100;

-- Register a data offering to use in the initial collaboration definition.
CALL samooha_by_snowflake_local_db.registry.register_data_offering(
    $$
    api_version: 2.0.0
    spec_type: data_offering
    version: v1
    name: <alice data offering name>
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

-- Save the ID of the registered data offering.
SET alice_data_offering_id = '<data_offering_id>';

CALL samooha_by_snowflake_local_db.registry.view_registered_data_offerings();

-- Register a template to use in the initial collaboration definition.
CALL samooha_by_snowflake_local_db.registry.register_template(
$$
api_version: 2.0.0
spec_type: template
name: alice_only_template
version: <version_number>
type: sql_analysis
description: A test template
template:
  SELECT t1.status, COUNT(*)
    FROM IDENTIFIER( {{ source_table[0] }} ) AS t1
    JOIN IDENTIFIER( {{ source_table[1] }} ) AS t2
    ON t1.hashed_email_b64_encoded = t2.hashed_email_b64_encoded
    GROUP BY t1.status;
$$);

-- Save the ID of the registered template.
SET my_template_id = '<alice_only_template_id>';
CALL samooha_by_snowflake_local_db.registry.view_registered_templates();

-- Create a collaboration with the previously registered template and data offering.
-- The collaboration supports two collaborators, with aliases alice (this account) and bob.
-- Owner: alice
-- Analysis runners:
--   * alice, using her own data, and the template you created and registered earlier.
--   * bob, with no listed templates or data.
-- Data providers:
--   * alice and bob, for alice
--   * alice and bob, for bob
-- Resources added: The template and data offering alice registered earlier.
-- You will add more templates and data offerings to these users later. Only these
-- users are invited to the collaboration, and no additional users can be added later.
-- Replace the <...> placeholders with the appropriate values.
-- Account data sharing IDs are -- SELECT CURRENT_ORGANIZATION_NAME() || '.' || CURRENT_ACCOUNT_NAME();
CALL samooha_by_snowflake_local_db.collaboration.initialize(
$$
api_version: 2.0.0
spec_type: collaboration
name: my_first_collaboration_1_0
owner: alice
collaborator_identifier_aliases:
  alice: <my account data sharing ID>
  bob: <bob account data sharing ID>
analysis_runners:
  bob:
    data_providers:
      alice:
        data_offerings:
        - id: <alice data offering ID>
      bob:
        data_offerings: []
  alice:
    data_providers:
      alice:
        data_offerings:
        - id: <alice data offering ID>
      bob:
        data_offerings: []
    templates:
    - id: <alice only template ID>
$$,
'APP_WH'
);
SET collaboration_name = '<collaboration_name>';

-- INITIALIZE automatically joins the owner. Check status until JOINED.
CALL samooha_by_snowflake_local_db.collaboration.get_status($collaboration_name);

-- Collaboration is visible here when the owner has joined.
CALL samooha_by_snowflake_local_db.collaboration.view_collaborations();

-- Auto-approve any template requests from other collaborators that affect you.
CALL samooha_by_snowflake_local_db.collaboration.set_configuration(
  $collaboration_name,
  'TEMPLATE_AUTO_APPROVAL',
  'true'
);

-- SWITCH TO collaborator to join the collaboration and add a template
-- The template will be auto-approved.

-- Create a new template.
CALL samooha_by_snowflake_local_db.registry.register_template(
    $$
    api_version: 2.0.0
    spec_type: template
    name: both_use_template
    version: 2026_01_12_V1
    type: sql_analysis
    description: test_description
    template:
      select * from identifier({{ source_table[0] }}) limit 5;

    $$
);
SET both_use_template = '<template ID>';

-- Ask to add the template to the collaboration. You must ask bob, because you're
-- including bob in the sharing list. When you share a template with yourself,
-- you auto-approve it.
CALL samooha_by_snowflake_local_db.collaboration.add_template_request(
  $collaboration_name,
  $both_use_template,
  ['alice', 'bob']   -- List of collaborators who can use this template.
  );

-- SWITCH TO bob to approve the request. Request wasn't approved automatically
-- because bob didn't enable auto-approve.

-- See if bob approved the request.
CALL samooha_by_snowflake_local_db.collaboration.view_update_requests($collaboration_name);

-- See what the collaboration spec looks like now, after all the resource updates.
-- Collaboration updates are asynchronous, so if all changes that you made aren't present,
-- wait a minute or two, and then try again.
CALL samooha_by_snowflake_local_db.collaboration.view_collaborations() ->>
  SELECT "COLLABORATION_SPEC" FROM $1 WHERE "SOURCE_NAME" = $collaboration_name;

-- SWITCH TO bob to add a data offering.

-- Run an analysis.
-- Tables are scoped as <data_offering_id>.<alias>.
CALL samooha_by_snowflake_local_db.collaboration.view_data_offerings(
  $collaboration_name
);
SET $bob_data_offering = '<bob data offering ID>';

CALL samooha_by_snowflake_local_db.collaboration.view_templates(
  $collaboration_name
);

-- Run bob's template.
-- Replace the placeholders with your variables.
CALL samooha_by_snowflake_local_db.collaboration.run(
  $collaboration_name,
    $$
    api_version: 2.0.0
    spec_type: analysis
    description: <optional description of the analysis>
    template: '<alice_only_template>'
    template_configuration:
      view_mappings:
        source_tables:
          - '<alice_data_offering_view_name>'
          - '<bob_data_offering_view_name>'
    $$
  );

-- Multi-step cleanup process to delete the collaborations.
-- Doesn't delete registered resources.
CALL samooha_by_snowflake_local_db.collaboration.teardown($collaboration_name);
CALL samooha_by_snowflake_local_db.collaboration.get_status($collaboration_name);

-- When get_status reports LOCAL_DROP_PENDING, call teardown again.
CALL samooha_by_snowflake_local_db.collaboration.teardown($collaboration_name);

DROP DATABASE ALICE_DB;
```

Copy code

```
-- Basic Snowflake Collaboration Data Clean Rooms example.
-- This file represents user "bob" in a two-collaborator clean room example.

-- Run this worksheet in a Snowflake account with access to the latest version of
-- Snowflake Data Clean Rooms.

-- This file  demonstrates the following actions:
-- * Joining a collaboration
-- * Registering and adding a template and a data offering to an existing collaboration.
-- * Running an analysis.

-- For more information, read docs.snowflake.com/user-guide/cleanrooms/overview

USE WAREHOUSE APP_WH;
USE ROLE SAMOOHA_APP_ROLE;

-- Secondary roles can't be active when calling join or link_data_offering.
USE SECONDARY ROLES NONE;

-- Create sample data.
CREATE DATABASE IF NOT EXISTS BOB_DB;
CREATE SCHEMA IF NOT EXISTS BOB_DB.BOB_SCH;
CREATE OR REPLACE TABLE BOB_DB.BOB_SCH.BOB_DATA AS SELECT * FROM samooha_sample_database.demo.customers_2 LIMIT 100;

-- See which collaborations you are invited to, or have joined.
CALL samooha_by_snowflake_local_db.collaboration.view_collaborations();

-- Use SOURCE_NAME column value from the response to view_collaborations().
SET collaboration_name = '<collaboration name>';

-- Use OWNER_ACCOUNT column value from the response to view_collaborations().
SET collaborator_data_sharing_id = '<collaborator_id>';

-- Review and join the collaboration.
-- Joining is asynchronous, so you must call get_status until the status is JOINED before
-- you can perform actions on the collaboration.
CALL samooha_by_snowflake_local_db.collaboration.review($collaboration_name, $collaborator_data_sharing_id);
CALL samooha_by_snowflake_local_db.collaboration.join($collaboration_name);
CALL samooha_by_snowflake_local_db.collaboration.get_status($collaboration_name);

-- Demonstrate the auto-approve flow.
-- Alice enabled auto-approve on her account, so this request will
-- be auto-approved, and the template will be added immediately.

-- Create a template.
CALL samooha_by_snowflake_local_db.registry.register_template(
    $$
    api_version: 2.0.0
    spec_type: template
    name: auto_approve_template
    version: V1
    type: sql_analysis
    description: test_description
    template:
      SELECT * FROM IDENTIFIER({{ source_table[0] }}) LIMIT 10;
    $$
);
SET auto_approve_template = '<template_id>';

CALL samooha_by_snowflake_local_db.collaboration.add_template_request($collaboration_name, $auto_approve_template, ['alice', 'bob']);
CALL samooha_by_snowflake_local_db.collaboration.view_update_requests($collaboration_name);

-- SWITCH TO other account and request adding a template, and then come back to approve the request.

-- You haven't enabled template auto-approve, so you must approve the request before the template is added.
CALL samooha_by_snowflake_local_db.collaboration.view_update_requests($collaboration_name);
CALL samooha_by_snowflake_local_db.collaboration.approve_update_request(
  $collaboration_name,
  '<request_ID>'
);

-- SWITCH TO bob to see the request status.

-- Register your own data offering.
CALL samooha_by_snowflake_local_db.registry.register_data_offering(
    $$
    api_version: 2.0.0
    spec_type: data_offering
    version: v3
    name: bob_data
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

SET my_data_id = '<data offering id>';

-- Share the data offering with yourself and alice.
CALL samooha_by_snowflake_local_db.collaboration.link_data_offering(
  $collaboration_name,
  $my_data_id,
  ['alice', 'bob']
);

CALL samooha_by_snowflake_local_db.collaboration.view_data_offerings(
  $collaboration_name
);

-- View templates that you can use in this collaboration. You can run only templates that list you in the
-- SHARED_WITH column.
CALL samooha_by_snowflake_local_db.collaboration.view_templates($collaboration_name);

-- Run an analysis with your template.
CALL samooha_by_snowflake_local_db.collaboration.run(
    $collaboration_name,
    $$
    api_version: 2.0.0
    spec_type: analysis
    description: <optional description of the analysis>
    template:  '<both_use_template>'
    template_configuration:
      view_mappings:
        source_tables:
          -  '<my_data_offering_view_name>'
          -  '<bob_data_offering_view_name>'
    $$
);

-- SWITCH TO other account to run an analysis.

-- Try running an analysis using alice-only template.
-- This will fail, because you aren't listed as an analysis
-- runner for this template.
CALL samooha_by_snowflake_local_db.collaboration.run(
  $collaboration_name,
  $$
  api_version: 2.0.0
  spec_type: analysis
  description: <optional description of the analysis>
  template: '<alice_only_template>'
  template_configuration:
    view_mappings:
      source_tables:
        - '<my_data_offering_view_name>'
        - '<bob_data_offering_view_name>'
  $$
);

-- Clean up resources.
DROP DATABASE BOB_DB;
```

### Single-party collaboration example

This example demonstrates how to create and use a collaboration if you have only a single account for testing.

The example demonstrates creating a collaboration with a data offering and a template, then adding another data offering and template
after the collaboration is created, and running analyses.

You can either download the file and upload it to your Snowflake account, or copy and paste the example code into a worksheet by using
Snowsight.

File downloadExample code

Download the source SQL file, then upload it into a Snowflake account that has Snowflake Data Clean Rooms installed:

- [Single account collaboration worksheet](/static/samples/clean-rooms/demo-collaboration-single-user.sql)

Copy code

```
-- ============================================================================
-- Single-user Collaboration Clean Rooms demo
-- ============================================================================
-- This example demonstrates a basic Snowflake Data Clean Rooms collaboration
-- using a single Snowflake account and a single role: SAMOOHA_APP_ROLE.
-- One user acts as the owner, data provider, and analysis runner.
--
-- The user creates two sample datasets, registers two data offerings and two
-- templates, then creates a collaboration with one data offering and one template each.
--  After the collaboration is created, the user links the remaining data offering and
-- template, then runs an analysis with each template. Finally, the code
-- cleans up all resources used.
--
-- For more information, see:
--   docs.snowflake.com/user-guide/cleanrooms/overview
--   docs.snowflake.com/user-guide/cleanrooms/spec-reference
-- ============================================================================

-- ============================================================================
-- SETUP: Create sample databases and data.
-- ============================================================================

USE ROLE SAMOOHA_APP_ROLE;
USE WAREHOUSE APP_WH;

-- You can't use secondary roles with most collaboration procedures.
USE SECONDARY ROLES NONE;

CREATE DATABASE IF NOT EXISTS DEMO_DB;
CREATE SCHEMA IF NOT EXISTS DEMO_DB.DATA_SCH;

-- Dataset 1: 300 rows from CUSTOMERS.
CREATE OR REPLACE TABLE DEMO_DB.DATA_SCH.CUSTOMERS_1 AS
  SELECT HASHED_EMAIL, STATUS, AGE_BAND
  FROM SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS
  LIMIT 300;

-- Dataset 2: 300 rows from CUSTOMERS_2.
CREATE OR REPLACE TABLE DEMO_DB.DATA_SCH.CUSTOMERS_2 AS
  SELECT HASHED_EMAIL, STATUS, AGE_BAND
  FROM SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS_2
  LIMIT 300;

-- ============================================================================
-- Register data offerings and templates.
-- ============================================================================

-- Register the first data offering.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.REGISTER_DATA_OFFERING(
  $$
  api_version: 2.0.0
  spec_type: data_offering
  version: V1
  name: customers_1
  datasets:
    - alias: customers_1
      data_object_fqn: DEMO_DB.DATA_SCH.CUSTOMERS_1
      object_class: custom
      allowed_analyses: template_only
      schema_and_template_policies:
        hashed_email:
          category: join_standard
          column_type: hashed_email_b64_encoded
        status:
          category: passthrough
        age_band:
          category: passthrough
  $$
);

SET data_offering_1_id = '<data_offering_1_id>';

-- Register the second data offering.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.REGISTER_DATA_OFFERING(
  $$
  api_version: 2.0.0
  spec_type: data_offering
  version: V1
  name: customers_2
  datasets:
    - alias: customers_2
      data_object_fqn: DEMO_DB.DATA_SCH.CUSTOMERS_2
      object_class: custom
      allowed_analyses: template_only
      schema_and_template_policies:
        hashed_email:
          category: join_standard
          column_type: hashed_email_b64_encoded
        status:
          category: passthrough
        age_band:
          category: passthrough
  $$
);

SET data_offering_2_id = '<data_offering_2_id>';

-- Register a template that joins two tables on hashed_email and returns
-- a count of rows grouped by age_band.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.REGISTER_TEMPLATE(
$$
api_version: 2.0.0
spec_type: template
name: age_band_count
version: V1
type: sql_analysis
description: Joins two tables on hashed_email and returns age_band with row counts.
template:
  SELECT t1.age_band, COUNT(t1.age_band) AS age_band_count
    FROM IDENTIFIER({{ source_table[0] }}) AS t1
      JOIN IDENTIFIER({{ source_table[1] }}) AS t2
      ON t1.hashed_email_b64_encoded = t2.hashed_email_b64_encoded
    GROUP BY t1.age_band;
$$
);

SET age_band_template_id = '<age_band_template_id>';

-- Register a template that joins two tables on hashed_email and returns
-- a count of rows grouped by status.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.REGISTER_TEMPLATE(
$$
api_version: 2.0.0
spec_type: template
name: status_count
version: V1
type: sql_analysis
description: Joins two tables on hashed_email and returns status with row counts.
template:
  SELECT t1.status, COUNT(t1.status) AS status_count
    FROM IDENTIFIER({{ source_table[0] }}) AS t1
      JOIN IDENTIFIER({{ source_table[1] }}) AS t2
      ON t1.hashed_email_b64_encoded = t2.hashed_email_b64_encoded
    GROUP BY t1.status;
$$
);

SET status_template_id = '<status_template_id>';

-- Confirm that both data offerings and both templates are registered.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.VIEW_REGISTERED_DATA_OFFERINGS();
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.VIEW_REGISTERED_TEMPLATES();

-- ============================================================================
-- Create the collaboration with one data offering and one template.
-- ============================================================================

-- Replace <account_data_sharing_id> with:
--   SELECT CURRENT_ORGANIZATION_NAME() || '.' || CURRENT_ACCOUNT_NAME();
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.INITIALIZE(
  $$
  api_version: 2.0.0
  spec_type: collaboration
  name: single_user_demo
  owner: me
  collaborator_identifier_aliases:
    me: <account_data_sharing_id>
  analysis_runners:
    me:
      data_providers:
        me:
          data_offerings:
            - id: <data_offering_1_id>
      templates:
        - id: <age_band_template_id>
  $$,
  'APP_WH'
);

SET collaboration_name = '<collaboration_name>';

-- Verify that the owner has joined. Repeat until status is JOINED.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.GET_STATUS($collaboration_name);

-- ============================================================================
-- Link the remaining data offering and template into the collaboration.
-- ============================================================================

-- Link the second data offering.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.LINK_DATA_OFFERING(
  $collaboration_name, $data_offering_2_id, ['me']);

-- Add the status_count template to the collaboration.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.ADD_TEMPLATE_REQUEST(
  $collaboration_name, $status_template_id, ['me']);

-- ============================================================================
-- List resources and run analyses.
-- ============================================================================

-- List all data offerings in the collaboration.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.VIEW_DATA_OFFERINGS($collaboration_name);

-- List all templates in the collaboration.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.VIEW_TEMPLATES($collaboration_name);

-- Run the age_band_count template.
-- Replace placeholders with the template name/version and view names from
-- VIEW_TEMPLATES and VIEW_DATA_OFFERINGS.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.RUN(
  $collaboration_name,
  $$
  api_version: 2.0.0
  spec_type: analysis
  description: Count matching rows grouped by age_band.
  template: '<age_band_count_template_name_and_version>'
  template_configuration:
    view_mappings:
      source_tables:
        - '<data_offering_view_1>'
        - '<data_offering_view_2>'
  $$
);

-- Run the status_count template.
-- Replace placeholders with the template name/version and view names from
-- VIEW_TEMPLATES and VIEW_DATA_OFFERINGS.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.RUN(
  $collaboration_name,
  $$
  api_version: 2.0.0
  spec_type: analysis
  description: Count matching rows grouped by status.
  template: '<status_count_template_name_and_version>'
  template_configuration:
    view_mappings:
      source_tables:
        - '<data_offering_view_1>'
        - '<data_offering_view_2>'
  $$
);

-- ============================================================================
-- CLEANUP: Delete the collaboration, registered resources, and sample data.
-- ============================================================================

-- Teardown is a multi-step process. Call TEARDOWN, then wait for GET_STATUS
-- to report LOCAL_DROP_PENDING, then call TEARDOWN again.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.TEARDOWN($collaboration_name);
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.GET_STATUS($collaboration_name);

-- When GET_STATUS reports LOCAL_DROP_PENDING, call TEARDOWN again to complete.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.TEARDOWN($collaboration_name);

-- Unregister the data offerings and templates from the default registry.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.UNREGISTER_DATA_OFFERING($data_offering_1_id);
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.UNREGISTER_DATA_OFFERING($data_offering_2_id);
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.UNREGISTER_TEMPLATE($age_band_template_id);
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.UNREGISTER_TEMPLATE($status_template_id);

-- Drop the sample database.
DROP DATABASE IF EXISTS DEMO_DB;
```
