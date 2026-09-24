# Managing Cross-Cloud Auto-Fulfillment in Snowflake Data Clean Rooms

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

## About Cross-Cloud Auto-Fulfillment

In the default clean room environment, a clean room can be shared only with accounts in the same cloud region. That is, the
provider and consumer must be in the same cloud region.

If you want to collaborate with a collaborator whose account is in a different region than you, you must enable
[Cross-Cloud Auto-Fulfillment](/collaboration/provider-listings-auto-fulfillment) for your clean
room environment and your clean room as shown on this page.

You can determine your own cloud region by running `SELECT CURRENT_REGION();`

Note

Cross-Cloud Auto-Fulfillment is sometimes referred to as *LAF*, which stands for [listings auto-fulfillment](/collaboration/provider-listings-auto-fulfillment).

## Enabling Cross-Cloud Auto-Fulfillment

You can enable Cross-Cloud Auto-Fulfillment using either the API or the UI. However, note the [limitations for cross-region collaboration](#label-dcr-laf-limitations).

**Implementation steps**

- [Prerequisites](#prerequisites)
- [Enabling Cross-Cloud Auto-Fulfillment in the UI](#enabling-cross-cloud-auto-fulfillment-in-the-ui)
- [Enabling Cross-Cloud Auto-Fulfillment in the API](#enabling-cross-cloud-auto-fulfillment-in-the-api)

### Prerequisites

In order to enable Cross-Cloud Auto-Fulfillment for an account, an org admin for all collaborators must first enable it on the account by
calling [SYSTEM$ENABLE\_GLOBAL\_DATA\_SHARING\_FOR\_ACCOUNT](/sql-reference/functions/system_enable_global_data_sharing_for_account).

Learn more about [auto-fulfillment](/collaboration/provider-listings-auto-fulfillment) and [managing auto-fulfillment privileges](/collaboration/provider-listings-auto-fulfillment-manage-privileges).

### Enabling Cross-Cloud Auto-Fulfillment in the UI

A clean rooms administrator enables Cross-Cloud Auto-Fulfillment at the account level for all
new and existing clean rooms by following these steps:

1. [Sign in to the clean rooms UI](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in) with your administrator account.
2. Browse to **Admin > Snowflake Admin**.
3. Toggle on **Cross-Cloud Auto-Fulfillment**.
4. No additional steps are required by the provider or consumer when creating or joining a clean room in the UI. However, if you
   later create or join a clean room in the API, you must follow the API instructions for providers and consumers.

### Enabling Cross-Cloud Auto-Fulfillment in the API

Follow these instructions to create or install a clean room in the API, even if you have already enabled Cross-Cloud Auto-Fulfillment in
the UI.

#### Account administrator actions

To enable Cross-Cloud Auto-Fulfillment for an account using the API, administrators in both the provider and consumer accounts must run the following SQL code using the ACCOUNTADMIN role. You need to run this only once per account.

Copy code

```
USE ROLE ACCOUNTADMIN;
-- Optionally check first to see if LAF is enabled on the account.
CALL samooha_by_snowflake_local_db.library.is_laf_enabled_on_account();

-- If LAF is not enabled, enable it.
CALL samooha_by_snowflake_local_db.library.enable_laf_on_account();
```

#### Provider and consumer actions

After Cross-Cloud Auto-Fulfillment is enabled for an account, here is how to enable Cross-Cloud Auto-Fulfillment
when creating or installing a clean room:

1. **The provider** publishes the clean room in the normal way by calling `provider.create_or_update_cleanroom_listing`.
2. **The consumer** installs the clean room by calling `consumer.install_cleanroom`. If the consumer is in a different cloud region from
   the provider, `consumer.install_cleanroom` fails with a message that Cross-Cloud Auto-Fulfillment replication is being installed.
3. **The consumer** continues to call `consumer.install_cleanroom` until it returns success. Installation takes several minutes.

   At this point, the consumer has basic clean room functionality. To support client custom template requests, provider-run
   analyses, and provider activation, follow this additional step:
4. **The provider** calls `provider.mount_request_logs_for_all_consumers` until the procedure reports success. This means that communication from the consumer to the provider is enabled.

**Full setup code example:**

1. **Provider:** The provider creates, shares, and publishes a clean room in the standard way.

   Copy code

   ```
   USE WAREHOUSE APP_WH;
   USE ROLE SAMOOHA_APP_ROLE;

   SET cleanroom_name = 'LAF example';
   SET consumer_locator = '<CONSUMER_LOCATOR>';
   SET consumer_account_name = '<CONSUMER_DATA_SHARING_ACCOUNT_ID>';

   CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.provider.cleanroom_init($cleanroom_name);

   CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.provider.set_default_release_directive(
     $cleanroom_name,
     'V1_0', '0');

   CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.provider.add_consumers(
     $cleanroom_name,
     $consumer_locator,
     $consumer_account_name);

   CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.provider.create_or_update_cleanroom_listing($cleanroom_name);
   ```
2. **Consumer:** The consumer installs the clean room.

   Copy code

   ```
   USE WAREHOUSE APP_WH;
   USE ROLE SAMOOHA_APP_ROLE;

   SET cleanroom_name = 'LAF example';
   SET provider_locator = '<PROVIDER_LOCATOR>';

   -- Initial call starts the process and returns a cross-cloud/region replication failure.
   -- Continue to call this procedure until it returns a success message.
   CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.consumer.install_cleanroom(
     $cleanroom_name,
     $provider_locator);

   -- Continue with standard clean room configuration and use.
   -- The consumer can run analyses, but client custom templates, provider run, and provider analysis
   -- aren't supported until the provider takes the action shown in the next step.
   ...
   ```
3. **Provider:** After the consumer installs the clean room, the provider must mount the requests share to enable
   request-based actions between the provider and consumer. Request-based actions include provider requests to run an analysis and consumer
   requests to add a template to the clean room.

   Copy code

   ```
   -- Call mount_request_logs_for_all_consumers until it reports success.
   provider.mount_request_logs_for_all_consumers($cleanroom_name);
   ```

   Full provider/consumer functionality is now available.

## Refresh frequency for cross-region accounts

Requests and data between the provider and consumer when on different cloud regions are subject to replication frequency settings.

### Requests and data from provider to consumer

This includes all data and requests from the provider to the consumer, such as creating or updating a clean room, changing provider data, requests for permission (such as provider-run analyses), and approvals for requests (such as consumer templates).

You can change the provider to consumer refresh rate by calling .

| Data | Default refresh rate |
| --- | --- |
| Provider clean room data, such as the following:   - Provider datasets - Provider-run requests - Clean room policies - Provider clean room metadata | - Clean rooms created after July 24, 2025: **30 minutes**. - Older clean rooms: Default to your   [account’s replication refresh schedule](/sql-reference/parameters#label-listing-auto-fulfillment-replication-refresh-schedule) (or 24 hours, if not set). |

Expand

Show lessSee more

### Requests and data from consumer to provider

The following table shows the default refresh frequency for data and requests from the consumer to the provider.

You can [control the consumer to provider refresh rate](/collaboration/provider-listings-auto-fulfillment-update-refresh-frequency)
for each clean room.

| Data | Default refresh rate |
| --- | --- |
| Requests, approvals, and changes such as the following:  - Requests to provider (such as a request to add a template) - Approvals to provider (such as an approval for provider-run analyses) - Changes to linked consumer data. - Status and results for provider-run requests. | - Clean rooms created after July 24, 2025: **10 minutes** - Older clean rooms: **1 hour** |
| Provider activation data: | - Clean rooms created after July 24, 2025: **10 minutes** - Older clean rooms: **15 minutes** |

Expand

Show lessSee more

## Costs associated with cross-region collaboration

There are additional costs associated with collaborators who are in a different region. For more information about how these costs are
incurred, see [Auto-fulfillment costs](/collaboration/provider-understand-cost-auto-fulfillment).

## Limitations on cross-region collaboration

The following limitations exist on cross-region collaboration:

- When using the clean rooms UI, you can enable cross-region collaboration with other UI users in the [same UI gateway region](/user-guide/cleanrooms/web-app-introduction#label-web-app-hosting). For example, accounts in AWS US East (Ohio) can share with accounts in AWS US West (Oregon) because they have the same UI gateway region (AwS US East (N. Virginia). Accounts in AWS US East (Ohio) can’t collaborate with accounts on AWS Canada, because they don’t share a gateway region. However, any account can be configured for cross-region collaboration when using the API.
- A provider cannot use differential privacy in the clean room.
- Collaborators cannot link external tables and iceberg tables in clean rooms.
- A consumer cannot run a multi-provider analysis.
- An account cannot act as both provider and consumer in cross-cloud collaboration scenarios due to replication type conflicts that can
  occur.
- See [additional considerations when enabling cross-region collaboration](/collaboration/provider-listings-auto-fulfillment#label-listings-auto-fulfill-considerations).
