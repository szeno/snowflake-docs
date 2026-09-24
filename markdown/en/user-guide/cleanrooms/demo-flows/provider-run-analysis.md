# Provider-run analyses

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

## Overview

The default clean room configuration enables only the consumer to run an analysis in the clean room. However, the provider can request
permission from the consumer to run a specific template in a specific clean room using consumer data. Provider-run analysis can be enabled
and run using either the clean rooms UI or code.

The following diagram shows the data flow and main components in a basic provider-run analysis:

[![Basic data flow direction in a provider-run analysis](/static/images/cleanrooms/provider-run-analysis.svg)](/static/images/cleanrooms/provider-run-analysis.svg)

1. In a basic provider-run analysis, the consumer and provider both link their data into the clean room. Source data is linked into the
   clean room as private views in the account where the data lives.
2. When the provider runs an analysis, the provider’s data is shared with the clean room app in the consumer’s account. The analysis runs
   on the consumer’s account.
3. The encrypted results are temporarily written to the consumer DB in the consumer’s account.
4. The encrypted results are copied to the analysis results back share on the provider’s account (also called the governance back share)
   and decrypted. Because the analysis runs on the consumer’s account, the consumer is billed for the analysis.

For more information, see [Snowflake Data Clean Rooms: Installed objects](/user-guide/cleanrooms/v1/installation-details).

### Templates that support provider-run analyses

The following templates support provider-run analyses:

- **Audience Overlap & Segmentation**
- **SQL Query** (UI only)
- Custom templates (API only)

### Billing and cost details

Provider-run analyses run in the consumer’s account, and consumers are billed for a provider-run analysis. To stop incurring
costs from provider-run analyses, the consumer must uninstall the clean room.

A consumer can estimate the number of credits consumed by the provider within the last *N* days by executing the following query.
Specify the number of previous days as a negative number.

Copy code

```
-- Estimate the number of credits consumed in the past 5 days.
SELECT * FROM TABLE(SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.LIBRARY.PRA_CONSUMPTION_UDTF(-5));
```

When a provider runs an analysis in the clean rooms UI, the clean room uses auto-scaling logic based on dataset sizes to choose a warehouse
for the provider’s analysis.

When a provider creates and runs a clean room using the API, the provider can explicitly choose a warehouse size and type from a set of
permissible values specified by the consumer.

### General notes

- Providers can activate results to their own account using the UI or the API, or to third-party providers if using the UI. For information
  about how to enable activation and view results, see [Activating query results](/user-guide/cleanrooms/v1/activation).
- If the consumer and provider are in different cloud regions, [Cross-cloud auto-fulfillment](/user-guide/cleanrooms/v1/enabling-laf)
  must be enabled in both accounts and for both clean rooms.

  Note that provider-run cross-cloud queries can take some time to run because provider source data must be replicated from the provider to
  the consumer, and query results from the consumer to the provider, all across cloud regions.
- Any templates run by the provider require column names or aliases for all columns generated in the results. If a column is
  aggregated (for example, `SUM(col1)`) or calls a custom function (for example, `cleanroom.my_function(p.hashed_email)`), the template
  must explicitly specify a column name alias as shown here:

  Copy code

  ```
  SELECT SUM(col1) AS TOTAL FROM my_db.my_sch.T; -- Correct
  SELECT SUM(col1)          FROM my_db.my_sch.T; -- Error: aggregated column needs an explicit alias.
  ```

## Provider-run analyses in the UI

Here is how to enable provider-run analysis in a new clean room when using the clean rooms UI:

1. The provider [creates and configures a clean room](/user-guide/cleanrooms/manage-clean-rooms#label-dcr-create-cleanroom), using one of the
   [supported templates](#label-dcr-templates-that-support-provider-analysis). Configure the clean room up to the **Share Clean Room** step.
2. In the **Share Clean Room** step of clean room configuration, the provider selects **Enable run analysis & query** next to
   their own account to enable them to run all templates in this clean room that support provider-run analysis.

   - This setting cannot be changed after a clean room is created; if you want to change permission for a specific account to run
     queries in a published clean room, you must delete the clean room and create a new one.
3. The consumer [joins and configures the clean room](/user-guide/cleanrooms/manage-clean-rooms#label-cleanrooms-web-app-install) as usual for all templates in the clean
   room, including any templates that support provider analysis. If the consumer does not want to enable a provider to run a specific
   template, they can omit required details for that template.

   - When the consumer joins the clean room, they are warned before joining that provider-run analysis is enabled for that clean
     room.
   - The consumer can run queries as soon as the clean room is joined, but there is a delay of up
     to 30 minutes before the provider can run the template. This setup delay occurs only during the initial join step; if the provider
     later adds other provider-run templates, the provider can run them as soon as the consumer configures their clean room for that
     template.
4. After the join step completes, the clean room is available for both [provider run analyses](/user-guide/cleanrooms/web-app-working#label-web-app-provider-run) and
   [consumer run analyses](/user-guide/cleanrooms/web-app-working#label-web-app-working-run-analysis-consumer).

   **Important:**

   - Providers must wait about 10 minutes after the consumer installs the clean room before they can run an analysis. The delay is for
     additional background configuration required for provider-run analyses.
   - The consumer is billed for all analyses in this clean room, whether run by the provider or consumer.

## Provider-run analyses in the API

Here is how to enable provider-run analysis in a new clean room using the clean rooms API:

1. **Provider**

   1. Creates and configures the clean room and data and policies in the standard way.
   2. Adds consumers in the standard way.
   3. Enables provider-run analysis for specific consumer accounts in the clean room by calling
      `provider.enable_provider_run_analysis`.

      **Important:**

      - The provider must call `provider.enable_provider_run_analysis` **after** adding consumers to a clean
        room, but **before** any consumer installs the clean room. Each consumer account must approve this request for their data to be
        accessible for provider-run analyses in this clean room.
      - Any time the provider changes the provider-run analysis setting for a clean room, the clean room must be
        re-installed by all consumers for the change to take effect. Because it can be difficult to force all collaborators to
        re-install a clean room, it is more reliable for the provider to delete a published, shared clean room when changing the analysis
        permissions, and then create a new clean room with the desired permissions.
   4. Publishes the clean room.
   5. Lets the consumer know that the clean room is available, the name of the clean room, and what templates you want to run in
      the clean room.
2. **Consumer**

   1. Installs the clean room and links in data in the standard way.
   2. Sets any [join and column policies](/user-guide/cleanrooms/v1/policies) needed on their data.
   3. Allows provider-run analysis for specific templates in the clean room by calling either
      `consumer.enable_templates_for_provider_run` (for multiple templates) or `consumer.approve_template` (for one template).

      Note

      If the provider changes a template after the consumer approves it, the consumer must approve the template again. Until the
      template is re-approved, the old cached version of the approved template will be run by the provider.
   4. (*Optional*) A consumer can limit the warehouse type or sizes available for provider-run analyses: see
      [Restricting warehouse size and type limits](#label-dcr-restricting-warehouse-size-for-provider-run).
   5. Tells the provider that they have installed the clean room and approved provider-run analyses.
3. **Provider**

   1. After the consumer has installed the clean room, the provider enables analyses to access consumer data by enabling data sharing
      from the consumer to the provider account. The process for this depends on whether the provider and consumer are in the same
      cloud region or different cloud regions:

      - If the provider and consumer are in **the same cloud region,** the provider calls
        `provider.mount_request_logs_for_all_consumers` once. If a new consumer account installs the clean room later and the provider
        wants to use consumer data in this template, the provider must re-run this procedure to be able to access that data.
      - If the provider and consumer are in **different cloud regions**, the provider and consumer must enable
        [cross-cloud auto-fulfillment](/user-guide/cleanrooms/v1/enabling-laf). When a provider runs an analysis across regions,
        the query can take some time to complete, because query data is sent from the provider’s region to the consumer’s region and
        back.
   2. Calls `provider.view_warehouse_sizes_for_template` to see if the consumer has limited the type and size of warehouse used for
      the analysis. If the consumer has limited warehouse sizes for provider run analyses, the provider must specify permitted
      `warehouse_type` and `warehouse_size` values in the analysis request in the next step. If the consumer has not specified
      warehouse limits, those fields are optional in the analysis request. For more information, see
      [Restricting warehouse size and type limits](#label-dcr-restricting-warehouse-size-for-provider-run).
   3. Runs the analysis by calling `provider.submit_analysis_request` with the template name, the table names, and the template
      arguments. If the consumer has specified limits on warehouse sizes or types, the provider must also specify the warehouse size and
      type in the analysis request.

      - Save the request ID returned by `provider.submit_analysis_request`; the ID is needed to check the status and results of the
        analysis.
   4. Checks the status of the analysis by calling `provider.check_analysis_status`. When status is reported as `COMPLETED`,
      call `provider.get_analysis_result` to get the analysis results.

### Restricting warehouse size and type limits

Because the consumer is billed for provider-run analyses, the consumer is able to dictate what sizes and types of warehouse the provider
can use to run an analysis in their account. Here is how a consumer sets warehouse size and type limitations, and how a provider chooses a
warehouse size and type when running an analysis:

1. The consumer calls `consumer.set_provider_run_configuration` and specifies which warehouse sizes and types a provider can use
   for a specific template. In the following snippet, the consumer limits providers to using STANDARD warehouses of size MEDIUM or LARGE when running `template_1`:

   Copy code

   ```
   CALL samooha_by_snowflake_local_db.consumer.set_provider_run_configuration(
     $cleanroom_name,
     {
       'template_1': {
         'warehouse_type': 'STANDARD',
         'warehouse_size': ['MEDIUM', 'LARGE']}
     });
   ```
2. The provider calls `provider.view_warehouse_sizes_for_template` to see which warehouse sizes and types are permitted for
   provider-run analyses on that template.

   Copy code

   ```
   CALL samooha_by_snowflake_local_db.provider.view_warehouse_sizes_for_template(
     $cleanroom_name,
     'template_1',
     $consumer_account_loc
   );
   ```
3. The provider specifies a warehouse size and type to use in their analysis run request.

   Copy code

   ```
   CALL samooha_by_snowflake_local_db.provider.submit_analysis_request(
     $cleanroom_name,
     $consumer_locator_id,
     'template_1',
     ['SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS'],
     ['SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS'],
     object_construct(
       'dimensions', ['c.REGION_CODE'],
       'measure_type', ['AVG'],
       'measure_column', ['c.DAYS_ACTIVE'],
       'warehouse_type', 'STANDARD',      -- Any other value would cause the request to fail.
       'warehouse_size', 'LARGE'          -- Only MEDIUM and LARGE supported.
     )
   );
   ```

Tip

The following procedures manage which side can run an analysis in the clean room:

**Consumer-run analysis** (*allowed by default*): Changes are applied immediately.

> - `provider.enable_consumer_run_analysis`
> - `provider.disable_consumer_run_analysis`

**Provider-run analysis** (*disabled by default*): Changes require reinstallation by the consumer.

> - `provider.enable_provider_run_analysis` (*requires the consumer to approve by calling
>   consumer.enable\_templates\_for\_provider\_run*)
> - `provider.disable_provider_run_analysis`

### Install and run the code example

You can download and install a complete running example to create and run a provider-run analysis. To run this
example, you need two Snowflake accounts in the same organization and cloud hosting region with the Snowflake Data Clean Room environment
installed.

1. [Download the example notebook](/static/samples/clean-rooms/provider-analysis-notebook.ipynb).
2. Install the notebook in both your provider and consumer accounts.

   To upload a notebook, do the following:

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
3. Run the provider and consumer actions as indicated, in the order shown in the notebook.
