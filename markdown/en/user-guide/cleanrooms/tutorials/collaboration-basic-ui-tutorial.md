# Tutorial: Get started with collaboration clean rooms (Snowsight)

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

## Introduction

This tutorial is aimed at analysts and developers who want to create and use collaboration clean rooms with the
Snowflake Data Clean Rooms UI in Snowsight. You will work through a two-account scenario where two collaborators
share data, share an analysis template, and run an analysis, doing most of the work in the UI.

This tutorial covers a similar scenario to
[Tutorial: Get started with collaboration clean rooms (API)](/user-guide/cleanrooms/tutorials/collaboration-basic-api-tutorial), but uses the Snowsight UI instead of the
Collaboration API. The UI calls the Collaboration API based on your inputs, so you can mix the two.

Creating the tables that the sample data lives in happens outside the Data Clean Rooms UI, in a Snowsight
workspace. Everything after that is done in the UI, and the tutorial provides a workspace SQL alternative wherever the
UI relies on Cortex Code.

### What you will learn

This tutorial shows you how to:

- Register a data offering and the built-in overlap analysis template.
- Create a collaboration with a partner using a step-by-step wizard, including your resources as you go.
- Review and join a collaboration from a second account.
- Share a data offering into a collaboration you’ve already joined.
- Run an analysis and tear the collaboration down, all from the UI.

### Requirements to run this tutorial

- Two Snowflake accounts, Enterprise Edition or higher, each with the Snowflake Data Clean Rooms environment installed.
  If clean rooms isn’t installed, see [Installing the Snowflake Data Clean Rooms environment](/user-guide/cleanrooms/installing-dcr).
- Your clean rooms environment must be version 14.6 or later. For more information, see
  [Managing clean room environment updates](/user-guide/cleanrooms/managing-updates).
- The appropriate [collaboration privileges](/user-guide/cleanrooms/manage-access) granted to your role, or the
  SAMOOHA\_APP\_ROLE role. Alice’s role needs CREATE COLLABORATION; Bob’s role needs REVIEW COLLABORATION and
  JOIN COLLABORATION.
- To register data offerings and templates directly in the UI, [Cortex Code](/user-guide/cortex-code/cortex-code-snowsight)
  must be enabled for the account. If Cortex Code isn’t available, use the workspace SQL alternative provided in each
  registration step.

Note

This tutorial requires **two separate Snowflake accounts**. You will run Alice’s steps in one account and Bob’s steps
in the other. Each section heading indicates which account to use.

## Collaboration basics

A collaboration clean room allows multiple parties to share and analyze data securely without exposing raw data to each
other. Collaborations are defined by a YAML specification that lists the collaborators, their data, and what each party
can do.

In this tutorial, Alice and Bob each contribute one data offering. Alice includes her data offering and the built-in
audience overlap template when she creates the collaboration. Bob registers his own data offering while that’s
happening, then reviews the collaboration, joins it, and shares his data offering in. Finally, Alice runs the template,
which joins the two collaborators’ data on a shared column and reports the overlap.

The two accounts show the two ways to add resources to a collaboration: Alice declares hers up front in the create
wizard, and Bob shares his after joining.

Key concepts used in this tutorial:

- **Collaboration**: Lets multiple parties securely share and analyze data without exposing raw data to each other.
  One owner creates it and invites collaborators.
- **Collaboration roles**: Each collaborator is assigned one or more roles:

  - **Owner**: Creates and manages the collaboration. There is exactly one owner per collaboration.
  - **Data provider**: Contributes data offerings that other collaborators can use in analyses.
  - **Analysis runner**: Runs templates against the shared data. Each analysis runner has a list of data providers and
    templates available to use.

    In this tutorial:

    - **Alice** is the collaboration **owner**, a **data provider**, and an **analysis runner**.
    - **Bob** is a **data provider** and an **analysis runner**.
- **Data offering**: A set of one or more views a data provider contributes to a collaboration, with policies that
  control how collaborators can use the data.
- **Template**: A registered JinjaSQL query that analysis runners execute against a data offering.

The Snowsight UI organizes the clean room workflow into three top-level tabs, reached by selecting
**Data sharing** » **Data clean rooms** in the navigation menu:

- **Collaborations**: Create, join, and manage the collaborations you share with collaborators.
- **Data Offerings**: Register and manage the data offerings you can add to collaborations.
- **Templates**: Register and manage the analysis templates you can add to collaborations.

For more information, see [Data Clean Rooms UI in Snowsight](/user-guide/cleanrooms/collab-ui-overview).

## Alice: Register a data offering

Start in **Alice’s account**. Before you create the collaboration, register the resources you want to include in it: a
data offering and an analysis template.

A data offering is a set of one or more views a data provider contributes to a collaboration, with policies that
control how collaborators can use the data. Register a data offering from the sample data you create in this section.

### Create sample data

The data a clean room uses lives in your own account, so you create it outside the Data Clean Rooms UI. Open a
Snowsight workspace and run the following SQL to create sample data for Alice:

Copy code

```
USE WAREHOUSE APP_WH;
USE ROLE SAMOOHA_APP_ROLE;

-- Secondary roles must be disabled to register and link resources.
USE SECONDARY ROLES NONE;

-- Create sample data for Alice.
CREATE DATABASE IF NOT EXISTS ALICE_DB;
CREATE SCHEMA IF NOT EXISTS ALICE_DB.ALICE_SCH;
CREATE OR REPLACE TABLE ALICE_DB.ALICE_SCH.ALICE_DATA AS
  SELECT HASHED_EMAIL, STATUS, AGE_BAND
  FROM SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS
  LIMIT 100;
```

### Register in the UI

1. In the **Data clean rooms** page header, select the **Data Offerings** tab.
2. Select **New Offering**.
3. In the **Object Explorer**, select the `ALICE_DB.ALICE_SCH.ALICE_DATA` table.
4. Select a **Registry**, the catalog that holds your registered resources. To use the default account registry, leave
   the registry unset. For more information, see [Registries](/user-guide/cleanrooms/registries).
5. Select **Create with CoCo**.

Cortex Code opens and helps you configure the data offering’s column policies and complete the registration. Configure
the offering to expose two columns: `hashed_email` as the join column and `status` as a passthrough column. When you’re
finished, note the data offering’s name and ID from the detail page.

Note

The **New Offering** option requires [Cortex Code](/user-guide/cortex-code/cortex-code-snowsight). If Cortex Code isn’t
enabled for your account, use the workspace alternative below.

### Register in a workspace (alternative)

If Cortex Code isn’t available, register the same data offering by running the following SQL in a workspace:

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

Either way, the data offering now appears on the **Data Offerings** tab, ready to link into the collaboration.

## Alice: Register the overlap template

This tutorial uses `standard_audience_overlap`, a built-in template that joins two data offerings on a shared column
and reports the overlap between them. This template is one of the standard templates that Snowflake provides. You don’t
need to write it; you only need to make sure it’s registered in your account.

1. In the **Data clean rooms** page header, select the **Templates** tab.
2. In the **Search templates** bar, search for `standard_audience_overlap`.

If the template already appears, you’re ready to share it. If it doesn’t appear, register the standard templates by
running the following SQL in a workspace, then search again:

Copy code

```
USE ROLE SAMOOHA_APP_ROLE;

-- Register the built-in standard templates.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.REGISTER_STANDARD_DCR_TEMPLATES();
```

For more information about the overlap template, see [Overlap and activation](/user-guide/cleanrooms/collab-overlap-and-activation).

## Alice: Create a collaboration

Still in **Alice’s account**, create the collaboration and include the data offering and template you just registered.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **Data clean rooms**.
3. Select **Create Collaboration**. The wizard opens with four steps.

**Step 1: Collaboration information**

- Enter a **Collaboration Name**, for example `ui_tutorial_collaboration`.
- Optionally enter a **Description**.
- Select **Next**.

**Step 2: Collaborator details**

Your account is automatically added as the **owner**. Configure both collaborators and the resources each one brings.

- For the owner (Alice), set an **Alias** such as `alice`, and select both the **Data Provider** and
  **Analysis Runner** roles. Add the resources you registered:
  - **Data Offering IDs**: Alice’s data offering. The ID combines the registered name and version, so the data
    offering registered earlier in this tutorial has the ID `alice_customer_data_v1`.
  - **Template IDs**: `standard_audience_overlap_v0`.
- Select **Add Collaborator** and configure Bob:
  - **Alias**: `bob`
  - **Account Identifier**: Bob’s account identifier, in the form `ORG_NAME.ACCOUNT_NAME`.
  - **Roles**: select both **Data Provider** and **Analysis Runner**.
  - Leave **Template IDs** and **Data Offering IDs** empty. Bob shares his data offering after he joins.
- Select **Next**.

**Step 3: Resource mapping**

Use the checkbox matrices to control which analysis runners can use which resources. Every analysis runner must have at
least one data provider mapped to it. If you leave the data offerings matrix empty, the wizard reports a
**Data Offering Mapping Required** error when you submit.

- In the data offerings matrix, select the checkboxes under both the `alice` and `bob` analysis runner aliases. This
  lets Alice and Bob each use the other’s data offerings, including the one Bob shares after he joins.
- In the template matrix, give both `alice` and `bob` access to `standard_audience_overlap_v0`.
- Select **Next**.

**Step 4: Final review**

Review the configuration. The wizard shows the collaboration specification that it builds from your entries, which for
this tutorial looks like the following:

Copy code

```
api_version: 2.0.0
spec_type: collaboration
name: ui_tutorial_collaboration
owner: alice
collaborator_identifier_aliases:
  alice: <alice_account_identifier>
  bob: <bob_account_identifier>
analysis_runners:
  alice:
    data_providers:
      alice:
        data_offerings:
        - id: alice_customer_data_v1
      bob:
        data_offerings: []
    templates:
    - id: standard_audience_overlap_v0
  bob:
    data_providers:
      alice:
        data_offerings:
        - id: alice_customer_data_v1
      bob:
        data_offerings: []
    templates:
    - id: standard_audience_overlap_v0
```

Bob’s data offerings lists are empty because he shares his data offering after he joins. For more information about
what each section of the specification means, see [Collaboration specification](/user-guide/cleanrooms/spec-collaboration).

To enable auto-join so Alice’s account joins the collaboration automatically after it’s created:

1. Turn on **Auto Join Collaboration**. The **Enable Auto Join** dialog opens.
2. Under **Role and warehouse**, select a role (for example, SAMOOHA\_APP\_ROLE) and a warehouse (for example, APP\_WH)
   for the background task. The dialog confirms when the role you select has the required permissions.
3. Select **Yes, Enable Auto Join**.
4. Select **Submit**.

Note

Auto-join creates a Snowflake task that uses the selected warehouse to complete the join, which consumes compute
credits until the collaboration is ready. If your role isn’t SAMOOHA\_APP\_ROLE, it must have the EXECUTE TASK
account-level privilege. The role you select applies only to auto-join; the rest of the UI keeps using the role in your
profile. For more information, see [Create a collaboration in Snowsight](/user-guide/cleanrooms/collab-ui-create).

The collaboration is created and an invitation is sent to Bob. Because you enabled auto join, Alice’s account joins on
its own.

Note

Creation and auto join run in the background and can take up to 10 minutes.

You don’t have to wait. Switch to Bob’s account and set up his data offering while the collaboration is being created.

## Bob: Register a data offering

Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as **Bob**. Registering a data offering is independent of any collaboration, so you
can do it while Alice’s collaboration is still being created. You share it into the collaboration after you join.

### Create sample data

As in Alice’s account, create the source table outside the Data Clean Rooms UI. Open a Snowsight workspace and
run the following SQL to create sample data for Bob:

Copy code

```
USE WAREHOUSE APP_WH;
USE ROLE SAMOOHA_APP_ROLE;
USE SECONDARY ROLES NONE;

CREATE DATABASE IF NOT EXISTS BOB_DB;
CREATE SCHEMA IF NOT EXISTS BOB_DB.BOB_SCH;
CREATE OR REPLACE TABLE BOB_DB.BOB_SCH.BOB_DATA AS
  SELECT HASHED_EMAIL, STATUS, AGE_BAND
  FROM SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS_2
  LIMIT 100;
```

### Register in the UI

1. In the **Data clean rooms** page header, select the **Data Offerings** tab.
2. Select **New Offering**.
3. In the **Object Explorer**, select the `BOB_DB.BOB_SCH.BOB_DATA` table.
4. Select a **Registry**, or leave it unset to use the default account registry.
5. Select **Create with CoCo**, and let Cortex Code help you expose `hashed_email` as the join column and `status` as a
   passthrough column.

### Register in a workspace (alternative)

If Cortex Code isn’t available, register Bob’s data offering by running the following SQL in a workspace:

Copy code

```
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
```

## Bob: Review and join the collaboration

Still in **Bob’s account**, review Alice’s invitation and join.

1. In the navigation menu, select **Data sharing** » **Data clean rooms**.
2. In the page header, select the **Collaborations** tab, then select the **Invited** tab.
3. In the **Ready to Review** section, find the `ui_tutorial_collaboration` card. If it isn’t there yet, refresh the
   page. Alice’s collaboration can take up to 10 minutes to reach your account.
4. Select **Start Review** on the card.
5. Optionally enter a **Collaboration name** for your account, then select **Submit**. The review runs in the
   background and can take several minutes.
6. Close the review wizard and return to the **Invited** tab, refreshing the page as needed. When the review finishes,
   the `ui_tutorial_collaboration` card moves to the **Pending Join** section.
7. Select **Join** on the card and review the details of the collaboration, including the collaborators, roles, and
   included resources. When you’re satisfied, proceed to join.

After joining, the collaboration moves to your **Joined** tab.

Tip

If [Cortex Code](/user-guide/cortex-code/cortex-code-snowsight) is enabled, you can select **Explain** or **Help Decide**
in the join wizard to get a natural language summary of the collaboration.

## Bob: Share the data offering

Now that you’ve joined, link the data offering you registered so Alice can use it.

1. Open `ui_tutorial_collaboration` from the **Joined** tab.
2. Select the **Data Offerings** tab.
3. Select **Share Data Offering**.
4. Select the **Registry** that holds your data offering. Select **Default** to use the default account registry, which
   is where you registered it.
5. Select your data offering (for example, `bob_customer_data_v1`) from the **Data Offering ID** list.
6. Select the analysis runners who should have access: `alice` and `bob`.
7. Select **Submit Request**.

The request appears on the **Update Requests** tab with a status of **Pending**. Sharing a data offering doesn’t
require approval from other collaborators, so you don’t need to ask Alice to approve it. Monitor the status on the
**Update Requests** tab until it changes to **Completed**, which indicates that the data offering is available to use
in the collaboration.

## Alice: Run the analysis

Switch back to **Alice’s account**. Confirm that `ui_tutorial_collaboration` appears on the **Collaborations** tab
» **Joined**, which means auto join finished. Now that both data offerings are available in the collaboration, run
the overlap analysis.

1. Select the **Collaborations** tab and open `ui_tutorial_collaboration`.
2. Select the **Templates** tab.
3. Select `standard_audience_overlap_v0` to view its details, including
   required parameters and the SQL logic.
4. Select **Open in Workspaces**.

A workspace opens with a pre-configured `COLLABORATION.RUN` statement. The generated SQL includes the collaboration
name, the template, and placeholders for the source tables and the template’s parameters.

To find the view names to use for the source tables, run the following pre-configured statement in the same workspace:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.VIEW_DATA_OFFERINGS('ui_tutorial_collaboration');
```

Each value in the `template_view_name` column has the format `user_alias.data_offering_id.dataset_alias`. If you used
the names in this tutorial, Alice’s view is `alice.alice_customer_data_v1.customer_list` and Bob’s is
`bob.bob_customer_data_v1.my_customer_list`.

Edit the generated run statement in three places:

- Replace `$collaboration_name`, which is an unset SQL variable, with your collaboration name as a string literal:
  `'ui_tutorial_collaboration'`.
- Replace the source table placeholders with the two `template_view_name` values.
- Supply the template’s arguments. `join_clauses` and `count_column` are required.

The order of the source tables matters. The template aliases the first view as `p1` and the second as `p2`, and it
counts matches against `p2`. Because Alice is running the analysis, put Alice’s view second so that the match rate is
calculated against her data.

The finished statement looks like the following:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.RUN(
  'ui_tutorial_collaboration',
  $$
  api_version: "2.0.0"
  spec_type: "analysis"
  name: "audience_overlap_alice_vs_bob"
  description: "Standard audience overlap between Alice's and Bob's customer lists, broken down by status."
  template: "standard_audience_overlap_v0"

  template_configuration:
    view_mappings:
      source_tables:
        - "bob.bob_customer_data_v1.my_customer_list"
        - "alice.alice_customer_data_v1.customer_list"
    local_view_mappings:
      my_tables: []
    arguments:
      join_clauses:
        - "p1.hashed_email_b64_encoded = p2.hashed_email_b64_encoded"
      count_column:
        - "hashed_email_b64_encoded"
      my_where_clause: ""
      source_where_clause: ""
      my_group_by:
        - "p2.status"
      source_group_by:
        - "p1.status"
  $$
);
```

Note the following about the arguments:

- `join_clauses` defines what the template treats as a match. The template joins the two data offerings on this
  condition, so a record in Bob’s data overlaps with a record in Alice’s when their hashed email values are the same.
- `count_column` is the column the template counts to produce the overlap figure. Counting hashed email reports how
  many distinct customers appear in both data offerings.
- `source_group_by` and `my_group_by` segment the results. They take the `p1` and `p2` aliases respectively, so
  `p1.status` is Bob’s status column and `p2.status` is Alice’s.

The results show the overlap between the two collaborators’ data, segmented by both parties’ `status` values. For more
information about the template, see [Overlap and activation](/user-guide/cleanrooms/collab-overlap-and-activation).

Tip

Instead of **Open in Workspaces**, you can select **Run** to open Cortex Code, which generates the run specification,
explains the template’s parameters, suggests values, and runs the analysis for you after you confirm. This is useful when
you’re unfamiliar with a template’s parameters. For more information, see
[Run analysis and activation in Snowsight](/user-guide/cleanrooms/collab-ui-run-analysis).

## Alice: Clean up resources

Switch to **Alice’s account** to tear down the collaboration. Only the owner can tear down a collaboration, and doing so
removes it for all collaborators.

1. Select the **Collaborations** tab.
2. On the `ui_tutorial_collaboration` card, select the actions menu ([![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)).
3. Select **Teardown**.
4. In the confirmation dialog, select **Yes, teardown**.

Warning

Tearing down a collaboration is irreversible. All collaborators lose access to the collaboration, and any data shared
through the collaboration is no longer accessible.

Tearing down the collaboration doesn’t delete the registered data offerings or templates from either account’s
registry. To remove the sample data, drop the sample databases in each account.

In Alice’s account:

Copy code

```
DROP DATABASE IF EXISTS ALICE_DB;
```

In Bob’s account:

Copy code

```
DROP DATABASE IF EXISTS BOB_DB;
```

## Summary

In this tutorial, you learned how to use the Snowflake Data Clean Rooms UI in Snowsight to:

- Register a data offering in the UI, with a workspace SQL alternative.
- Register the built-in `standard_audience_overlap` template.
- Create a collaboration with a partner using the wizard, including a data offering and a template in the spec.
- Review and join a collaboration from a second account.
- Share a data offering into a collaboration you’ve already joined.
- Run an analysis and tear the collaboration down, all from the UI.

### Next steps

- Try a similar scenario with the Collaboration API in
  [Tutorial: Get started with collaboration clean rooms (API)](/user-guide/cleanrooms/tutorials/collaboration-basic-api-tutorial).
- Explore the full [Data Clean Rooms UI in Snowsight](/user-guide/cleanrooms/collab-ui-overview) and its workflows.
- Learn more about the overlap analysis and activation in [Overlap and activation](/user-guide/cleanrooms/collab-overlap-and-activation).
- Learn about [collaboration roles](/user-guide/cleanrooms/roles) and how to [manage access](/user-guide/cleanrooms/manage-access).
- Find more tutorials, sample worksheets, and video walkthroughs in [Sample Worksheets and Videos](/user-guide/cleanrooms/tutorials-and-samples).
