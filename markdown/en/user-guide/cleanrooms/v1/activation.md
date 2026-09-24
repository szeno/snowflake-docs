# Activating query results

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

## Overview of activation

The provider or consumer can send template results outside of the clean room in a process called *activation*. Snowflake supports three
types of activation:

- **Provider activation**, where results are pushed to a table in the provider’s Snowflake account.
- **Consumer activation**, where results are pushed to a table in the consumer’s Snowflake account.
- **Third-party activation**, where the provider or consumer pushes results to a Snowflake-approved third-party, such as Google Ads or Meta
  Ads Manager, through an [activation connector](/user-guide/cleanrooms/connector-activation).

In all cases, the template must support activation, and parties should approve activation for any columns of their own data that will be
activated. Data providers specify which columns of their data are activated by setting an activation policy. For more about clean room
policies see [Understanding Snowflake Data Clean Room policies](/user-guide/cleanrooms/v1/policies).

Activation supports differential privacy, if enabled, and respects differential privacy rules and budgets.

Important

If the consumer and provider are in different cloud regions, you need to enable [Cross-cloud auto-fulfillment](/user-guide/cleanrooms/laf) in both accounts and for both clean rooms.

## Provider and consumer activation

You can configure a clean room to save template results in the provider’s or consumer’s Snowflake account. Both the provider and consumer
must approve activation of any data out of the clean room.

Activation is implemented using a dedicated activation template. In the clean rooms UI, an activation template can be associated with
an analysis template, and the user can run the analysis template, view the results, then run the associated
activation template. The Snowflake-provided **Audience Overlap & Segmentation** flow does this.

An activation template need not be identical to any associated analysis template. The activation template is often a subset of the analysis
template.

### Supported templates

The following templates support provider and consumer activation:

- Audience Overlap & Segmentation
- [Custom templates](/user-guide/cleanrooms/v1/custom-templates#label-dcr-v1-custom-templates-activation)

### Supported combinations

Activation can be run either by the provider or by the consumer. (Learn more about
[provider-run analyses](/user-guide/cleanrooms/demo-flows/provider-run-analysis).)

The following combinations are supported:

|  | Provider activation | Consumer activation | Third-party activation |
| --- | --- | --- | --- |
| Provider-run | ✅ | ❌ | UI only |
| Consumer-run | ✅ | ✅ | UI only |

Expand

Show lessSee more

### Results

**Provider activation results** are saved to the provider’s account in the table
SAMOOHA\_BY\_SNOWFLAKE\_LOCAL\_DB.PUBLIC.PROVIDER\_ACTIVATION\_SUMMARY.

**Consumer activation results** are saved to the consumer’s account in the table
SAMOOHA\_BY\_SNOWFLAKE\_LOCAL\_DB.PUBLIC.CONSUMER\_DIRECT\_ACTIVATION\_SUMMARY.

See [viewing results](#label-cleanrooms-provider-consumer-view-results) to learn how to read the data.

### Implementing provider or consumer activation

Clean rooms UIClean rooms API

**Setup**

- Activation when using the clean rooms UI requires that the clean rooms account [allows activation](/user-guide/cleanrooms/admin-tasks#label-cleanrooms-administer-activation).
- For provider-run activation, the clean room must be [configured to support provider-run analysis](/user-guide/cleanrooms/demo-flows/provider-run-analysis).

**1. Create or join a clean room**

When creating or joining a clean room, in the **Configure Analysis & Query** step, under **Activation Settings**, specify which
columns should be added to the results activated to your account.

**2. Run the template and activate results**

To run the activation associated with your analysis, complete these steps:

1. Run your analysis.
2. After running an analysis, select **Results** » **Activate**.
3. Under **Activation Hub** select the name of the provider or consumer account to activate to.
4. Provide information specific to the activation template, such as descriptive segmentation names or activation
   columns.
5. Provide a segment name: this is an arbitrary string used to identify a set of results from a given run. You can provide a different
   string for each activation to group each run’s results separately, or you can use the same segment name over multiple runs
   if you want to combine results.
6. Select **Push Data**.
7. To learn how to view activated results, see [Viewing provider and consumer activation results](#label-cleanrooms-provider-consumer-view-results).

Activation is performed differently depending on who runs it, and whether it’s consumer or provider activation.

Consumer activation (consumer-run)Provider activation (consumer-run)Provider activation (provider-run)

Important

The first time a consumer activates data to a provider account in a clean room, the provider must establish a data pipeline by
signing in to the clean room UI for that account and staying signed in for up to 30 minutes. This needs to be done only once per
clean room per consumer. Until that is done, data will not appear in the provider’s account, even if the activation succeeds.

Here is how a consumer can push results to their own Snowflake account.

**Provider**

> 1. Create the clean room, link datasets, and set join policies, as for a standard clean room.
> 2. Either choose a [supported Snowflake standard template](#label-dcr-activation-supported-templates), or add a
>    [custom activation template](/user-guide/cleanrooms/v1/custom-templates#label-dcr-v1-custom-templates-activation) to the clean room. If this clean room is to be used
>    in the UI, you must provide a web form with the proper activation fields, as described in the template documentation.
> 3. Enable the template for consumer activation by calling `provider.enable_template_for_consumer_activation`.
> 4. To specify which provider columns can be activated, set the activation policy in the clean room for the enabled template by
>    calling `provider.set_activation_policy`.
> 5. Add consumer collaborators, set the default release directive, and publish the clean room, as usual.

**Consumer**

> 1. Install the clean room, link datasets, and set join policies, as for a standard clean room.
> 2. To specify which consumer columns can be activated, set the activation policy in the clean room for that template by calling
>    `consumer.set_activation_policy`.
> 3. Run the activation by calling `consumer.run_activation`, with the last parameter set to TRUE to indicate a consumer
>    activation.
> 4. View the results, as described below.

**Examples**

Download the following examples and upload them as worksheet files in your Snowflake account. You will need separate accounts for
the provider and consumer, each with the clean rooms API installed. Replace the information as noted in the sample files. [See instructions to upload a SQL worksheet into your Snowflake account](/user-guide/cleanrooms/tutorials-and-samples#label-dcr-list-of-sample-notebooks-and-worksheets).

- [Provider example code](/static/samples/clean-rooms/c-run-c-activation-p.sql)
- [Consumer example code](/static/samples/clean-rooms/c-run-c-activation-c.sql)

Here is how a consumer can push results to a provider’s Snowflake account.

Important

If the consumer and provider don’t **both** have the clean rooms UI installed, and the consumer is activating to the provider:

- The **consumer** must run the following SQL command:

  Copy code

  ```
  ALTER SHARE SAMOOHA_INTERNAL_GOVERNANCE_SUMMARY_SHARE_NAV2
    ADD ACCOUNTS = $provider_account_data_sharing_id;
  ```

  where `$provider_account_data_sharing_id` is the provider’s [Data Sharing Account Identifier](/user-guide/admin-account-identifier#label-account-name-data-sharing)
- The **provider** must run the following procedure:

  Copy code

  ```
  CALL samooha_by_snowflake_local_db.provider.mount_provider_activations_share(
    $consumer_account_data_sharing_id, TRUE, FALSE);
  ```

  where `$consumer_account_data_sharing_id` is the consumer’s [Data Sharing Account Identifier](/user-guide/admin-account-identifier#label-account-name-data-sharing).

**1. Provider**

> 1. Create the clean room in the standard way.
> 2. Link datasets. The provider must also link the SAMOOHA\_BY\_SNOWFLAKE\_LOCAL\_DB.LIBRARY.TEMP\_PUBLIC\_KEY table into the clean
>    room.
> 3. Set the join policy in the standard way.
> 4. Either choose a [supported Snowflake standard template](#label-dcr-activation-supported-templates), or add a
>    [custom activation template](/user-guide/cleanrooms/v1/custom-templates#label-dcr-v1-custom-templates-activation) to the clean room. If this clean room is to be used
>    in the clean rooms UI, you must [provide a web form](/user-guide/cleanrooms/demo-flows/custom-templates#label-dcr-define-user-form) with
>    the proper activation fields.
> 5. To specify which provider columns can be activated, set the activation policy in the clean room for that template by calling
>    `provider.set_activation_policy`.
> 6. Add consumer collaborators, set the default release directive, and publish the clean room, as usual. (If you do not have the
>    clean room UI installed, call `provider.setup_provider_activation_share_mount_task` after adding consumers.)

**2. Consumer**

> 1. Install the clean room, link datasets, and set join policies, as for a standard clean room.
> 2. Set the activation policy in the clean room for that template to specify which consumer columns can be activated by calling
>    `consumer.set_activation_policy`.
> 3. Run the activation by calling `consumer.run_activation`, with the last argument set to FALSE to indicate a provider
>    activation.
>
> Note
>
> An encrypted version of the activated data is stored on the consumer’s account for 28 days in the table
> SAMOOHA\_LOCAL\_DB\_NAME\_PLACEHOLDER.PUBLIC.CONSUMER\_ACTIVATION\_SUMMARY. Data older than 28 days is removed from the consumer’s
> account.

**3. Provider**

> 1. The first time a consumer activates data to your account you must sign in to the clean rooms UI for this account for about 30
>    minutes after the consumer has activated data. After that, the data will appear in your account. This is done only once per clean room per consumer account. Later activations by the same consumer in the same clean room do not need this step.
>
>    The results must be decrypted before being saved to your account, which can take some time.
>    The decryption task times out after 60 minutes; if this happens, call
>    [provider.update\_activation\_warehouse](/user-guide/cleanrooms/provider#label-dcr-api-provider-update-activation-warehouse) to increase the warehouse
>    size used for decryption.
> 2. View the results, as described below.

**Examples**

Download the following examples and upload them as worksheet files in your Snowflake account. You will need separate accounts for
the provider and consumer, each with the clean rooms API installed. Replace the information as noted in the sample files. [See instructions to upload a SQL worksheet into your Snowflake account](/user-guide/cleanrooms/tutorials-and-samples#label-dcr-list-of-sample-notebooks-and-worksheets).

- [Provider example code](/static/samples/clean-rooms/c-run-p-activation-p.sql)
- [Consumer example code](/static/samples/clean-rooms/c-run-p-activation-c.sql)

Here is how a provider can push results their own Snowflake account. This combines several techniques, including custom templates,
provider-run analysis, and provider activation, and so involves several rounds of request and approval between the provider and
consumer.

**1. Provider**

> 1. Create the clean room, link datasets, and set join policies, as for a standard clean room, **with one exception**: You must
>    link in the table `samooha_by_snowflake_local_db.library.temp_public_key`. Provider-run data is encrypted, and this enables
>    encryption and decryption of the results.
> 2. Either choose a [supported Snowflake standard template](#label-dcr-activation-supported-templates), or add a
>    [custom activation template](/user-guide/cleanrooms/v1/custom-templates#label-dcr-v1-custom-templates-activation) to the clean room. If this clean room is to be used
>    in the UI, you must provide a web form with the proper fields to support activation, as described in the template
>    documentation.
> 3. Set the activation policy in the clean room for that template to specify which provider columns can be activated by calling
>    `provider.set_activation_policy`.
> 4. Add consumer collaborators in the standard way. If you do not have the clean room UI installed you must call
>    `provider.setup_provider_activation_share_mount_task` after adding users.
> 5. Enable provider-run analysis in the clean room by calling `provider.enable_provider_run_analysis`. This must be done
>    **after** adding collaborators but **before** collaborators install the clean room. If you change this setting after a
>    consumer installs the clean room, the consumer must reinstall the clean room for the change to take effect.
> 6. Set the default release directive and publish the clean room, as usual.

**2. Consumer**

> 1. Install the clean room, link datasets, and set join policies as in a standard clean room.
> 2. Set the activation policy in the clean room for that template to specify which consumer columns can be activated by calling
>    `consumer.set_activation_policy`.

**3. Provider**

> - Request permission from the consumer to run your activation template by calling `provider.request_provider_activation_consent`.

**4. Consumer**

> 1. Grant the provider permission to run a given template in this clean room by calling `consumer.enable_templates_for_provider_run`.
> 2. Grant the provider permission to activate results from a given template in this clean room by calling `consumer.approve_provider_activation_consent`.

**5. Provider**

> 1. Enable consumer data to be shared in a provider activation by calling `provider.mount_request_logs_for_all_consumers`.
> 2. Run the activation template by calling `provider.submit_analysis_request`). The request takes several minutes to appear in
>    the logs; check status by calling `provider.check_analysis_status`. Note that even after status is reported as
>    SUCCESS, additional time is required for results to be decrypted and written to the provider’s Snowflake table.
>    All decrypted data is appended at one time to the results table. Keep checking the results table periodically for your segment
>    or activation ID. The **decryption task times out after 60 minutes**; if this happens, call
>    [provider.update\_activation\_warehouse](/user-guide/cleanrooms/provider#label-dcr-api-provider-update-activation-warehouse) to increase the warehouse
>    size used for decryption.
>
> Note
>
> To modify a template after the consumer approves it, you must take the following steps, or else
> `provider.submit_analysis_request` will continue to run the last approved version of the template.
>
> 1. Provider updates the template by calling `provider.add_custom_sql_template`. No need to call
>    `create_or_update_cleanroom_listing` again.
> 2. Consumer calls `consumer.enable_templates_for_provider_run`.
> 3. Consumer calls `consumer.approve_provider_activation_consent`.
> 4. The updated template is now ready for provider activation.

**Common errors**

- `Object cleanroom_name.CLEANROOM.TEMP_RESULT_DATA does not exist or not authorized` - Temporary results table could not
  be generated for some reason. Could be a SQL error in the template, or your template didn’t explicitly generate a table; look at
  the error details.
- `Query validation checks failed` - Some columns used in the template that weren’t in the activation policies.

**Examples**

Download the following examples and upload them as worksheet files in your Snowflake account. You will need separate accounts for
the provider and consumer, each with the clean rooms API installed. Replace the information as noted in the sample files.
[See instructions to upload a SQL worksheet into your Snowflake account](/user-guide/cleanrooms/tutorials-and-samples#label-dcr-list-of-sample-notebooks-and-worksheets).

- [Provider example code](/static/samples/clean-rooms/p-run-p-activation-p.sql)
- [Consumer example code](/static/samples/clean-rooms/p-run-p-activation-c.sql)

### Viewing provider and consumer activation results

#### Activation results location and format

All activation results are appended to a clean room designated table in the provider’s or consumer’s account. Each row in the table maps to
a row in the query result. Results from each run are appended to the table (the table is not cleared before each run). You can distinguish
between different runs by the ACTIVATION\_ID column, which is unique per activation, or the SEGMENT column, which can be specified by the
caller for each activation run.

Note

Provider activation results are written in encrypted format to a temporary table in the consumer’s localDB. The results are then copied
over to the provider’s account and decrypted before saving. This extra move and decryption step can cause delays with large result sets.

- **Provider activation results** are stored in SAMOOHA\_BY\_SNOWFLAKE\_LOCAL\_DB.PUBLIC.PROVIDER\_ACTIVATION\_SUMMARY in the provider’s account.
- **Consumer activation results** are stored in SAMOOHA\_BY\_SNOWFLAKE\_LOCAL\_DB.PUBLIC.CONSUMER\_DIRECT\_ACTIVATION\_SUMMARY in the consumer’s
  account.

These tables contain the following columns:

USER\_ID:
:   One row of results, in JSON format, where the keys are the column names and the values are the value for that column in that row.
    The object also contains a column for each argument passed into the template.

ACTIVATION\_ID:
:   A unique ID for each request. The ID is returned from a successful activation request. You can filter by this column to
    get all results for the same activation run, or filter by SEGMENT if you reuse the same segment name across multiple runs. This is the
    same as the query request ID returned by `submit_analysis_request` or `run_activation`.

CLEANROOM\_NAME:
:   Name of the clean room where the query was run.

CONSUMER:
:   (*Provider activation only*) The consumer who approved this activation.

PROVIDER:
:   (*Consumer activation only*) The provider who approved this activation.

SEGMENT:
:   An arbitrary string value that you assign when you run the activation. This column enables you to join results across
    multiple query runs.

TIMESTAMP:
:   When the activation was run.

**Provider activation example**

```
SELECT * FROM SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.PUBLIC.PROVIDER_ACTIVATION_SUMMARY WHERE segment = 'my_segment';

                             USER_ID                          |   CLEANROOM_NAME |   SEGMENT  | CONSUMER |          TIMESTAMP      |  ACTIVATION_ID
"{""AGE_BAND"":55,""ITEM_COUNT"":2328,""STATUS"":""MEMBER""}" |  test activation | my_segment | ABC1234  | 2025-04-01 16:27:14.068 | cleanroomactivationdataanalysisresults20250401231728469
"{""AGE_BAND"":20,""ITEM_COUNT"":88,""STATUS"":""PLATINUM""}" |  test activation | my_segment | ABC1234  | 2025-04-01 16:27:14.068 | cleanroomactivationdataanalysisresults20250401231728469
"{""AGE_BAND"":80,""ITEM_COUNT"":18,""STATUS"":""GOLD""}"     |  test activation | my_segment | ABC1234  | 2025-04-01 16:27:14.068 | cleanroomactivationdataanalysisresults20250401231728469
...
```

#### Reading provider or consumer activation results

Run the appropriate SQL command to view results activated to your Snowflake account:

**View provider activation results**

Copy code

```
SELECT *
   FROM SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.PUBLIC.PROVIDER_ACTIVATION_SUMMARY
   [WHERE segment = <SEGMENT_NAME>] [AND activation_id = <ACTIVATION_ID>];
```

**View consumer activation results**

Copy code

```
SELECT *
   FROM SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.PUBLIC.CONSUMER_DIRECT_ACTIVATION_SUMMARY
   [WHERE segment = <SEGMENT_NAME>] [AND activation_id = <ACTIVATION_ID>];
```

Each row of data is combined into an object in the `USER_ID` column. You can flatten results using a query like the following:

Copy code

```
-- Assuming columns AGE_BAND, STATUS, and ITEM_COUNT
SELECT
  item:"AGE_BAND",
  item:"STATUS",
  item:"ITEM_COUNT"
FROM (SELECT parse_json(user_id)
      AS item
      FROM SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.PUBLIC.PROVIDER_ACTIVATION_SUMMARY
      WHERE segment = $segment_name)
ORDER BY item:"AGE_BAND", item:"STATUS" ASC
LIMIT 20 ;
```

**View the latest 10 result rows in Snowsight:**

> 1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
> 2. In the navigation menu, select **Catalog** » **Explorer**.
>
>    - **For provider activation** navigate to `SAMOOHA_BY_SNOWFLAKE_LOCAL_DB` » `PUBLIC` » `Tables` »
>      `PROVIDER_ACTIVATION_SUMMARY`.
>    - **For consumer activation** navigate to `SAMOOHA_BY_SNOWFLAKE_LOCAL_DB` » `PUBLIC` » `Tables` »
>      `CONSUMER_DIRECT_ACTIVATION_SUMMARY`.
> 3. Select **Data Preview**.

## Third-party activation

Third-party activation deposits query results in the account of a Snowflake-approved third party using a
[third-party activation connector](/user-guide/cleanrooms/connector-activation).

Third-party activation is supported only in the clean rooms UI, and not using custom templates.

Activation when using the clean rooms UI is supported only if the clean rooms account [allows activation](/user-guide/cleanrooms/admin-tasks#label-cleanrooms-administer-activation).

The clean rooms administrator must configure the environment to support third-party activation connectors, select the allowed connectors,
and configure them, before they can be used in any clean room.

Third-party activation supports both consumer- and provider-run analyses.

### Supported templates

The following templates support third-party activation:

- Audience Overlap & Segmentation

### Implementing third-party activation

1. **Create or join the clean room:** When creating or joining the clean room, in the **Configure Analysis & Query** step, under
   **Activation Settings**, specify which columns should be added to the results activated to your account.
2. **Activate results:**
   1. Run your analysis.
   2. After running an analysis, select **Results** » **Activate**.
   3. Under **Activation Hub** select the name of the third-party provider to activate to.
   4. Provide information specific to the provider. This can be providing descriptive names or selecting which columns to activate. The
      tooltips on the page should provide additional information for that provider.
   5. Select **Push Data**.
