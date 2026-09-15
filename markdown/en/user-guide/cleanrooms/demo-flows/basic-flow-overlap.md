# Use case: Overlap and segmentation

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

Snowflake provides an overlap and segmentation template to determine which entities exist in the data for all collaborators, and show
aggregated information about those entities.

When using this template, two parties each add one or more tables to a clean room. Entities in these tables are
joined or identified by the join columns that you specify. Additionally, the overlap count can be broken down and filtered by
particular segmentation attributes. This enables parties to gain insight of the overlap between their datasets, which can help determine
the value of collaboration and facilitate other downstream use cases in the clean room. The consumer specifies which columns to join on and
which columns to show. All projected columns must either be grouped or aggregated with an aggregation function. Entity-identifying columns
are blocked from the query results and differential privacy is applied by the clean room to further protect information about specific
entities. If enabled by the clean room creator, the results can be activated to a third party (clean rooms UI only).

For example, an advertiser can conduct an overlap analysis on a publisher’s inventory to help inform the value of
buying media on that publisher. The advertiser then activates the IDs of their desired audience back to the publisher for
targeting purposes.

The overlap and segmentation template is available for use in both the clean rooms UI and in code. The clean rooms UI enables easy usage
of identity providers and activation to third-party partners, while the code usage enables multiple tables from both the provider and
consumer.

Tip

If you enable differential privacy with the Audience Overlap template, do not compute overlap statistics. Doing so will consume most of
the user’s privacy budget, leaving little or no budget to run analyses.

## Clean rooms UI usage

In the clean rooms UI, this use case is supported through a ready-made template called **Audience Overlap & Segmentation**. Although
this template is targeted for marketing and advertising use cases, it can be used for any overlap and segmentation use case across all
industries. Follow the steps below to learn how to create and use this template.

Note

When running this analysis in the clean rooms UI, overlap percentages can vary depending on who runs the analysis. This is because the
percentage is calculated as (*matched IDs in my table*)/(*total IDs in my table*). For example if collaborator A has 100 IDs
while B has 500 IDs. If they both overlap 50 IDs, then A will see a 50% overlap while B will see only 10% overlap.

Also, If the same ID from collaborator A’s data matches multiple IDs in collaborator B’s data, the overlap will vary depending on who runs
the analysis.

**Web template features:**

- One-click activation, if configured by your clean room administrator.
- One-click usage of identity providers, if configured by your clean room administrator.
- Support for provider-run analyses.
- Both sides can import data and specify columns that can be joined, projected, and activated.
- Overlap query on one consumer and one provider table from the available tables.
- Configurable differential privacy.

Note

Try out the [web interface tutorial](/user-guide/cleanrooms/v1/tutorials/cleanroom-web-app-tutorial) to see a full end-to-end
walkthrough of using clean rooms in the clean rooms UI. This template is also covered in this tutorial.

### Step 1: Provider creates the clean room

Here is how a provider creates and configures a clean room with the **Audience Overlap & Segmentation** template:

1. Sign in to the clean rooms UI and [create a new clean room](/user-guide/cleanrooms/manage-clean-rooms#label-dcr-create-cleanroom).
2. Under **Add Data**, do the following:

   1. Choose the tables to link (import) into the clean room. If the tables you need aren’t listed, speak to a clean rooms administrator.
3. Under **Specify Join Policies**, do the following:

   - Choose which columns a collaborator can join on from your tables. Remember that joinable columns can’t also be shown or used in the
     analysis for segmentation, filtering, or grouping.
   - If you want to use an identity provider to help resolve entities that might have multiple identifiers, for example a single
     individual who has multiple email accounts in different databases, choose an identity provider in the **Identity Hub**.
4. Under **Configure Analysis & Query**, do the following:

   1. Select **Audience Overlap & Segmentation** as the analysis type. (You can select multiple templates for a clean room.) The
      configuration options for each template will be shown on the page.
   2. For **Tables**, choose which tables that you linked earlier should be available to consumers in this clean room with this template.
   3. Use **Segmentation & Attribute Columns** to choose which columns are shown in the query results. The collaborator can show, filter,
      and group by selected columns. Collaborators can activate these attribute values when Snowflake Activation is enabled in the clean
      room. If you don’t see a column listed here, it’s probably because you marked it as joinable, and a column can’t be both joinable
      and visible in the query results.
   4. **Allow categorical value previews during filtering** specifies whether previews show actual values. It is enabled by default if
      there are fewer than 20 distinct values in the column, but disabled by default if there are more than 20 distinct values, to protect
      PII.
   5. Review the **Activation Settings** section to enable, configure, or disable activation for the results data:

      - Select **ID Columns** that should be available during activation use cases. By default, join policy columns are auto-selected.
      - Enable **Allow non-overlap activation** to activate IDs from your dataset without matching IDs in your collaborator’s dataset.
        For example, if you brought in 100 IDs and ran an overlap analysis with your collaborator and only 25 IDs overlapped, non-overlap
        activation would activate the 75 unmatched IDs from your dataset.
      - Review **Enabled Partners** to ensure only your preferred activation destinations are enabled in your clean room. If you require
        a change to enabled destinations, speak to a clean rooms administrator.
   6. Update default **Privacy Settings** as needed:

      - **Threshold Value** is enabled by default and set to 5. This prevents results showing for any groups where the distinct count of
        a join policy column is below this threshold.
      - **Differential Privacy** is disabled by default. When enabled, it provides protection against potential differencing attacks by
        adding noise to the results and limiting the number of daily queries. Learn more about
        [Differential Privacy in Snowflake Data Clean Rooms](/user-guide/cleanrooms/differential-privacy) and understand the costs of
        enabling this feature.
5. Under **Share clean rooms**, do the following:

   - Expand the **Select collaborator** menu to add collaborators to the clean room. Collaborators will receive an email inviting them to
     join and use your clean room, as described next. The collaborators list on the page shows all accounts, including your own, that can
     access this clean room.
   - Select **Enable run analysis and query** next to a collaborator to control whether that account can run a template in the clean room.
     By default, your own account cannot run an analysis in the clean room (that is,
     [provider-run analyses](/user-guide/cleanrooms/demo-flows/provider-run-analysis) is disabled by default). By default, consumers
     can run any template in the clean room.

### Step 2: Consumer joins the clean room

Here is how a consumer joins and configures a clean room that includes the **Audience Overlap & Segmentation** analysis template:

1. [Sign in to the clean rooms UI and join the clean room](/user-guide/cleanrooms/manage-clean-rooms#label-cleanrooms-web-app-install).
2. Under **Add Data**, do the following:

   - Choose the tables to link (import) into the clean room. If the tables you need aren’t listed, speak to a clean rooms administrator.
3. Under **Specify Join Policies**, do the following:

   - Decide which joinable columns in your data map to joinable columns in the provider’s data. You will specify which of these columns to
     join on during each run.
   - If you want to use an identity provider to help resolve entities that might have multiple identifiers - for example a single individual
     who has multiple email accounts in different databases - choose an identity provider in the **Identity Hub**.
4. In the **Configure Analysis & Query** step, do the following:

   - Select the **Audience Overlap & Segmentation** analysis to show the configuration options for that template.
   - Choose which of your tables should be used in this analysis from the **Tables** dropdown menu.
   - Use **Segmentation & Attribute Columns** to choose which columns are shown in the query results. These columns can also be activated
     when Snowflake Activation is enabled in the clean room. If you don’t see a column listed here, it’s probably because you marked it as
     joinable, and a column can’t be both joinable and visible in the query results.
   - Select **ID Columns** that should be available during activation use cases. By default, join policy columns are auto-selected.
   - Optionally enable **Allow activation for clean room provider** to allow the clean room provider to activate to the supported
     activation destinations. This option is shown only when provider-run is enabled in the clean room. Note that enabling this
     allows row-level data to be activated back to the provider’s account. Note that the consumer is charged for compute costs
     when running provider queries and activation, although the consumer must agree to allow the provider action.
   - Review **Enabled Partners** to ensure that preferred activation destinations are enabled in the clean room. If you require a change
     to the enabled destinations, contact the clean room provider.
5. Click **Finish** to save your results. To run the analysis, see the next section.

### Step 3: Consumer runs the analysis

Note

The default configuration allows only the consumer to run an analysis using this template. To enable provider-run
analysis with this template, the provider must open the **Share clean rooms** tab in the clean room configuration and select
**Enable run analysis and query** next to their account name.

After the provider and consumer have configured the clean room for audience overlap and segmentation, either party that has permissions to
run an analysis can do so like this:

1. In the clean rooms UI, navigate to **Clean rooms**.
2. Select **Run** for the clean room where you configured the audience overlap, and then choose **Audience Overlap & Segmentation > Proceed**.
   (Alternatively, visit the **Analyses & Queries** page, select **+ New Analysis & Query**, choose the
   **Audience Overlap & Segmentation** type, then choose the clean room that has that analysis type configured.)
3. Set up the details of the run in the **Query Configurations section**:

   - **My tables** - Choose which of your tables to join on your collaborator’s tables.
   - **Collaborator table** - Choose a collaborator table to join on your table.
   - **My join columns** - Select all the columns to join on between the tables.
   - **User segmentation** - Optionally select grouping columns.
   - **Filters** - Optionally provide one or more filters on columns specified as segmentation and attribute columns during setup.
   - **Privacy settings** - This query implements differential privacy, and a minimum number of rows per grouping. You can see your used
     and remaining differential privacy and minimum group size here.
4. If conducting the analysis as a consumer, you can change the [warehouse size](/user-guide/warehouses-overview) to improve query
   times by selecting a larger warehouse or reduce cost by selecting a smaller warehouse. When conducting an analysis as a provider,
   warehouse selection is not available, but auto-scaling will try to optimize query times.
5. Select **Run**. If this is a new query, do the following:

   - Specify a name for your analysis & query.
   - Optionally [schedule a repeating analysis](/user-guide/cleanrooms/v1/schedule-analysis).
6. Select **Save** to start or schedule the run. It can take some time to complete each run. You can check on the analysis status or
   results in the **Analysis & Queries** page in the clean rooms UI.

## Code usage

You can download and run a sample notebook showing how to use the overlap and segmentation example in SQL code. This example can be uploaded and run in Snowsight.

The notebook does not demonstrate how to use identity providers, [activation](/user-guide/cleanrooms/v1/activation)
to third-party providers, or [provider-run analyses](/user-guide/cleanrooms/demo-flows/provider-run-analysis). See the
linked topics to demonstrate how to do those actions in code.

**Prerequisites**

You must have two accounts in the same organization with Snowflake Data Clean Rooms installed. Use one account for the provider,
the other account for the consumer.

**Install and run the code example**

1. [Download the example notebook](/static/samples/clean-rooms/overlap-segmentation.ipynb).
2. Install the notebook in both your provider and consumer accounts. To upload a notebook, do the following:

   1. sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
   2. in the navigation menu, select **Projects** » **Notebooks**.
   3. Select **+ Notebook** » **Import .ipynb file**.
   4. Select the .ipynb file you downloaded.
   5. Name the file as desired, and choose a database and schema.
   6. Keep the default warehouse `APP_WH`.
   7. Select **Create**.
   8. To create the clean room, open the notebook in the provider account and complete the provider portion.
   9. Open the notebook in the consumer account and complete the consumer portion to install and configure the clean room and run the
      template.
