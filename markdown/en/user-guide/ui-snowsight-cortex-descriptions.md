# Generate descriptions with Snowflake Cortex

You can use Snowsight and the power of the
[Snowflake Cortex COMPLETE function](/sql-reference/functions/complete-snowflake-cortex) to automatically generate descriptions for a
column, table, or view. The Cortex Powered Object Descriptions feature leverages Snowflake-hosted large language models (LLMs) to evaluate
object metadata and, if desired, sample data to generate the description.

The generated description, once saved, is preserved in the COMMENT property of the column, table, or view. You can view the
description anywhere the COMMENT property is displayed, which includes the following:

- The **Table Details** and **View Details** tabs in Snowsight.
- The **Columns** tab for the table or view in Snowsight.
- The output of a [DESCRIBE TABLE](/sql-reference/sql/desc-table) command.
- The output of the Account Usage [TABLES](/sql-reference/account-usage/tables) view.

A user with *any privilege* on the table, view, or column can view the description after it is saved.

Note

You can also call a stored procedure to programmatically generate object descriptions using Snowflake Cortex. For more information, see
[Using SQL to automatically generate object descriptions](/user-guide/sql-cortex-descriptions).

## Cortex descriptions access control requirements

To use the Cortex Powered Object Descriptions feature, you must have:

- The [SNOWFLAKE.CORTEX\_USER database role](/sql-reference/snowflake-db-roles#label-snowflake-db-roles-cortex-user).
- The USAGE privilege on a warehouse.

You must also set the [CORTEX\_MODELS\_ALLOWLIST](/sql-reference/parameters#label-cortex-models-allowlist) parameter to allow access to the `mistral-7b` and
`llama3.1-8b` models. By default, this parameter is set to `'All'`, which allows access to all models. If the parameter has been
changed, ensure that these models are included. For more information about controlling model access with this parameter, see
[Account-level allowlist parameter](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-allowlist).

### LLM regional requirements

Your region must support the LLM used by Snowflake Cortex to generate the descriptions. If you have the required privileges, but do not see
this feature, check the [availability of the COMPLETE function](/user-guide/snowflake-cortex/aisql-regional-availability#label-cortex-llm-availability). If the COMPLETE function is not
supported in your region, you need to enable [cross-region inference](/user-guide/snowflake-cortex/cross-region-inference) to use the
feature.

## Supported objects

You can generate descriptions for the following objects:

- All table types
- Views
- Materialized views
- Columns that are in tables and views.

## Create, edit, and save descriptions with Snowflake Cortex

The steps to generate and edit Snowflake Cortex Powered Descriptions are in the following subsections.

### Generate and save descriptions

To generate and save a description for a table or view, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the OWNERSHIP privilege.
2. Navigate to the table or view for which you want to generate descriptions.
3. If prompted, select a warehouse.
4. On the **Table Details** tab or **View Details** tab, select **Generate with Cortex**.
5. If you want to edit the description, select the pencil icon and edit the description.
6. Select **Save**.

Note

Users with the OWNERSHIP privilege can execute the following to let users with the role `my_role` generate descriptions. In this example, the user has an ACCOUNTADMIN role:

Copy code

```
USE ROLE ACCOUNTADMIN;
GRANT USAGE ON WAREHOUSE ai_wh TO ROLE my_role;
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE my_role;
```

### Create descriptions for all columns at once

Snowsight lets you generate descriptions for multiple columns at once, with a limit of 50 columns at a time. To generate
descriptions for all columns in a table or view with a single action, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the [required privileges](#label-cortex-descriptions-access-control).
2. Navigate to the table or view that contains the columns.
3. If prompted, select a warehouse.
4. Select the **Columns** tab.
5. Select **Generate Descriptions** in the toolbar.
6. If prompted, decide whether to use [sample data](#label-cortex-description-sample-data-inputs).
7. If you want to edit a description, select the pencil icon.
8. Select the columns you want to save.
9. Select **Save**.
10. If your table or view has more than 50 columns and you want to generate descriptions for the remainder of the columns, repeat this
    process.

### Create descriptions for a single column

To generate a description for a single column, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the [required privileges](#label-cortex-descriptions-access-control).
2. Navigate to the table or view that contains the columns.
3. If prompted, select a warehouse.
4. Select the **Columns** tab.
5. Find the column, hover over its row in the **Description** column, and then select **Generate with Cortex**.
6. If prompted, decide whether to use [sample data](#label-cortex-description-sample-data-inputs).
7. If you want to edit the description, select the pencil icon.
8. Select **Save**.

### Overwrite existing descriptions

To replace a user-specified description with a generated description, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the [required privileges](#label-cortex-descriptions-access-control).
2. Navigate to the table or view for which you want to edit descriptions.
3. Select a warehouse if one is not already in use.
4. Edit the descriptions for tables, views, and columns:

   - Tables and views: In the **Table Details** tab, select the pencil icon to edit the existing description, and select
     **Generate with Cortex**.
   - Columns: In the **Columns** tab, select the pencil icon for existing descriptions, and select **Generate with Cortex**.
5. Select **Save**.

## Generate descriptions without saving

To generate a description of a table or view, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the SELECT privilege.
2. Navigate to the table or view for which you want to generate descriptions.
3. If prompted, select a warehouse.
4. On the **Table Details** tab or **View Details** tab, select **Describe Table**.

Note

The table owner can’t save the descriptions generated by selecting the **Describe Table** button. If you are a table owner who wants to
edit and save descriptions, select **Generate with Cortex** in the **Description** section of the page.

## Sample data inputs

When generating a description for a column, you can rely only on metadata, or you can choose to use sample data to
improve the Snowflake Cortex Powered Description. Sample data refers to data within a particular column that is evaluated when you
use Snowflake Cortex to generate descriptions. If you choose to use sample data, Snowflake uses a portion of the sample data to generate the
description, which leads to more accurate descriptions. Sample data is not stored by Snowflake as Usage Data.

The decision to use sample data is specific to the individual user. The first time you generate a column description in a browser
session, you will be prompted to decide whether to use sample data. The pop-up box defaults to yes and allows you to choose to disable
sample data before proceeding. Your browser stores your response to this question for the duration of your
[Snowflake session](/user-guide/session-policies) and you won’t be asked again until your next session. You can also use your
[User Profile](/user-guide/ui-snowsight-profile) to set your preference for whether to use sample data.

Note

Sample data can cross regional boundaries if the region supports Snowflake Cortex. For more information, see
[LLM regional requirements](#label-cortex-descriptions-regions).

## Cost considerations

Generating descriptions incurs the following costs:

- Credits consumed by the warehouse in use.
- Credits charged for the use of Snowflake Cortex with smaller LLMs like Mistral-7b and Llama 3.1-8b. These charges appear on a bill as
  AI-Services, which includes all uses of Snowflake Cortex.

## Legal Notices

This feature relies on the COMPLETE function to generate a recommended object description, which the user may save (with or without
revision) or reject. When the user initiates the description generation, Usage Data may be collected through the COMPLETE function.

Until a description is explicitly saved by the user, it is not retained by Snowflake. If the user saves the description, an object comment
is created. The saved comment is stored as a [metadata field](/sql-reference/metadata).

For additional information about the use of AI, see [Snowflake AI and ML](/guides-overview-ai-features).
