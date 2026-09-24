# Run an analysis in the UI

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

The [clean rooms UI](/user-guide/cleanrooms/v1/web-app-introduction) of a Snowflake Data Clean Room provides an intuitive UI that allows business
users to create and use clean rooms without worrying about code complexities.

This topic provides an introduction to tasks that you complete as you work with a clean room. It describes the actions of the provider who
creates and shares a clean room along with the consumer who uses that clean room.

## Run an analysis as a provider

If a provider has [configured a clean room to allow provider-run analyses](/user-guide/cleanrooms/demo-flows/provider-run-analysis#label-dcr-enable-provider-run-analysis-ui),they can run an analyses in the clean room.

A provider can run an analysis in a properly configured clean room through either of the following actions:

- Select **Clean Rooms** from the left navigation, find the tile for the clean room on the **Created** tab, and select **Run**.
- Select **Analyses & Queries** from the left navigation, and run an existing analysis or create a new one just like a consumer would.

The provider selects which collaborator has the data that they want to include in their analysis.

Important

If a consumer allows a provider to run an analysis on a template, the consumer, not the provider, is charged for the credits consumed by
the provider’s analysis. After the consumer has allowed the provider to run analyses, the consumer must uninstall the clean room to stop
incurring costs.

If a consumer wants to obtain an estimate of the number of credits consumed by the provider within a specific time period, they can
execute the following query, where `-5` returns an estimate of the previous 5 days of compute consumption by the provider:

Copy code

```
SELECT * FROM TABLE(SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.LIBRARY.PRA_CONSUMPTION_UDTF(-5));
```

Administrators can monitor the analyses being run by the provider: see [Monitor provider-run analyses](/user-guide/cleanrooms/admin-tasks#label-cleanrooms-admin-monitor-provider-run).

Consumers can monitor billing due to provider-run analyses: see [Billing and cost details](/user-guide/cleanrooms/demo-flows/provider-run-analysis#label-dcr-provider-run-billing-and-costs).

Providers can [activate results to their own account](/user-guide/cleanrooms/v1/activation#label-clean-rooms-push-provider-run-analysis).

### Limitations on provider-run analyses

When using the clean rooms UI to run an analysis, the provider has the following limitations:

- Not all templates are supported. Currently, the Audience Overlap & Segmentation and SQL Query templates are supported.
- If the collaborators are in different clouds or regions:
  - Consumers must [enable cross-cloud auto-fulfillment](/user-guide/cleanrooms/v1/enabling-laf#label-cleanrooms-get-started-ccaf) on their account.
  - Results for a provider-run analysis are returned based on the combined refresh frequency between both parties. Providers and consumers
    should coordinate so the refresh frequency of the provider application and the consumer listing are similar (for example, both have a
    frequency of 15 minutes). This ensures that results are returned promptly.

## Run an analysis as a consumer

As a consumer, you can use either the **Clean Rooms** page or the **Analyses & Queries** page to run analyses in an installed clean
room.

To use the **Clean Rooms** page to run a new analysis based on the types of analyses that the provider has made available in the clean
room:

1. [Sign in to your clean room environment in the clean rooms UI](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in).
2. In the left navigation, select **Clean Rooms**.
3. On the **Joined** tab, find the clean room in the list and select **Run**.
4. Select the analysis type, and then select **Proceed**.
5. Add filters to the analysis. There are two reasons why filter values might not be available:

   - The column contains more than 20 distinct values.
   - The clean room was recently installed, and has not finished processing preview values for the column. You can re-run the analysis when
     these values become available.
6. Select **Run**.
7. Optional: Expand the **Save Analysis & Query** section to save the analysis for future use.

To use the **Analyses & Queries** page to run existing analyses or create and run a new analysis:

1. [Sign in to your clean room environment in the clean rooms UI](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in).
2. In the left navigation, select **Analyses & Queries**.
3. Do one of the following:
   - To run an existing analysis, use the filters to find the analysis and run it.
   - To create and run a new analysis based on the types of analyses that the provider has made available in the clean room,
     select **+ New Analysis & Query**.

## Select a warehouse for an analysis

You can select which [warehouse](/user-guide/warehouses-overview) you want to use to run an analysis. Increasing the
size or changing the type of the warehouse can speed up the analysis.

Note

The type of template determines what type of warehouse you can select for the analysis.
For example, some templates (like Audience Overlap) only allow regular warehouses.

The option to select a different warehouse appears next to the **Run** button on a template. This option does not appear for all
templates.

Be aware that increasing the size of a warehouse or using a Snowpark-optimized warehouse can increase the cost of running the
analysis. For information about how credit consumption grows as you use a larger warehouse, see [Warehouse size](/user-guide/warehouses-overview#label-warehouse-size) and
[Billing for Snowpark-optimized warehouses](/user-guide/warehouses-snowpark-optimized#label-snowpark-wh-credits).

For a description of the warehouses that are available, see [Warehouses](/user-guide/cleanrooms/v1/installation-details#label-cleanrooms-installation-details-warehouses).

If you are an administrator who wants to create additional warehouse options, see [Using a different warehouse](/user-guide/cleanrooms/admin-tasks#label-cleanrooms-admin-add-warehouse).

## View details about a clean room

You can obtain details about a clean room, including:

- A **Collaborator Summary** tab that lists the templates in the clean room along with the tables and join columns of your collaborator.
- A **My Summary** tab that lists your tables and join columns.
- A **Table Relations** tab that lists the relationship between your tables and the tables of your collaborator (that is, how the tables are
  joined).
- A **Data Stats** tab that provides the following metrics for your tables:
  - **My table:** Shows how many distinct identifiers belong to a certain group. Note that statistics are updated every 24 hours so there
    might be a delay between modifying the clean room and seeing the updated statistics. Also note that columns with more than 20 distinct
    values are not shown.
  - **Overlap stats:** A clean room with either the Audience Overlap & Segmentation or SQL Query templates will show overlap stats
    to the consumer. These statistics describe how many distinct identifiers (join columns) belong to a certain group based on
    the attribute columns enabled in the template. You can select up to 2 attribute columns to view statistics breakdowns for. The data
    is generated after the initial installation and is refreshed whenever a user logs into the clean rooms UI. Note that
    in the bar graph visualization only the first 5 rows of data are plotted based on the default sorting
    provided. Statistics that take longer than 10 minutes to run for a particular breakdown will not be available.

To access these clean room details, complete these steps:

1. [Sign in to your clean room environment in the clean rooms UI](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in).
2. In the left navigation, select **Clean Rooms**.
3. Click on the tile for the clean room.

Clean room details are also available in the **Clean Rooms Details** section when you are running an analysis.

## Download and share results

A user who wants to share the aggregate results they generated within the clean room can download the results of
the clean room analysis as a .csv file, and then share these results with others outside of Snowflake, including sharing with a clean room
collaborator via email.
