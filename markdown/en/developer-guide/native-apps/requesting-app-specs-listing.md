# Request data sharing via listings

This topic describes how to configure the specifications of a Snowflake Native App
to request permission to share data with providers or third parties through
listings. This enables use cases such as compliance reporting, telemetry
sharing, and data preprocessing.

## Share data from an app with providers or third parties

Some Snowflake Native Apps need to share data back with the provider or with third-party Snowflake accounts for
various business purposes. Common use cases include the following:

- **Compliance reporting:** Sharing audit logs or compliance data with regulatory accounts
- **Telemetry and analytics:** Sending usage metrics back to the provider for product improvement
- **Data preprocessing:** Sharing transformed data with partner accounts
- **Support and troubleshooting:** Providing diagnostic data to support teams

To enable data sharing from an app, the app needs to provide both shares and
listings. A share contains the database objects to be shared, and a listing
provides the mechanism to share data across accounts and regions.

For more information about data shares, see [About Secure Data Sharing](/user-guide/data-sharing-intro).

To configure an app to share data using listings, follow these steps:

1. Use [automated granting of privileges](/developer-guide/native-apps/requesting-auto-privs) to request privileges from
   the consumer to create shares and listings.
2. Create a share and grant database objects to it.
3. Create an external listing attached to the share.
4. To request permission from the consumer to share data with specific target
   accounts, use [application specifications](/developer-guide/native-apps/requesting-app-specs).

Note

Unlike other app specification types, each LISTING specification is associated with exactly one
listing object. An app cannot create multiple app specifications for the same listing.

## App specification workflow for sharing data

Configuring an app to share data by using listings follows this general workflow:

1. Providers configure [automated granting of privileges](/developer-guide/native-apps/requesting-auto-privs) for the app.
   This grants the app privileges to create shares and listings.

   > Note
   >
   > App specifications require `manifest_version: 2` to be set in the manifest file.
2. Providers add the
   [CREATE SHARE and CREATE LISTING privileges](#label-native-apps-app-spec-add-listing-priv) to the
   manifest file.
3. Providers add SQL statements to the setup script to create the following objects as required:

   - [Share](/sql-reference/sql/create-share)
   - [External listing](/sql-reference/sql/create-listing)
   - [App specification](/sql-reference/sql/alter-application-set-app-spec)

   The setup script creates the share and listing when the app is installed or
   upgraded. The app specification can be created during setup or at runtime
   through a stored procedure.
4. When configuring the app, consumers review and approve the target accounts
   and auto-fulfillment settings on the listing.
   Auto-fulfillment settings are only applicable for cross-region sharing.
   For more information on how consumers view and approve app specifications, see [Approve app specifications](/developer-guide/native-apps/ui-consumer-app-spec).

## App specification definition for sharing data

For an app specification of type LISTING, the app specification definition contains the following entries:

- `TARGET_ACCOUNTS`: A comma-separated list of target accounts to share
  data with, enclosed in single quotes. Each account must be specified in the
  format `OrgName.AccountName`; for example:
  `'ProviderOrg.ProviderAccount,PartnerOrg.PartnerAccount'`.
- `LISTING`: The identifier of the listing object created by the app.
- `AUTO_FULFILLMENT_REFRESH_SCHEDULE`: Optional. The refresh schedule for cross-region data
  sharing. Can be specified as `<num> MINUTE` or `USING CRON <expression>`.

Note

The listing name in the app specification must match an existing listing created by the app.
After this is set, the listing name cannot be changed.

## Set the version of the manifest file

To enable automated granting of privileges for an app, set the version at the
beginning of the manifest file, as shown in the following example:

Copy code

```
manifest_version: 2
```

## Add the CREATE SHARE and CREATE LISTING privileges to the manifest file

The CREATE SHARE and CREATE LISTING privileges allow the app to create shares
and listings during installation or upgrade.

- To configure an app to request
  these privileges, add the following code to the `privileges` section of
  the manifest file:

  Copy code

  ```
  manifest_version: 2
  ...
  privileges:
    - CREATE SHARE:
     description: "Create a share for sharing compliance data with provider"
    - CREATE LISTING:
     description: "Create a listing for cross-region sharing of compliance data"
  ...
  ```

If you set the `manifest_version` to 2 in the manifest file, Snowflake automatically grants
the CREATE SHARE and CREATE LISTING privileges to the app during installation or upgrade.

## Create a share and grant objects to it

1. To create a share for data sharing, add the
   [CREATE SHARE](/sql-reference/sql/create-share) command to the setup script, as shown
   in the following example:

Copy code

```
CREATE SHARE IF NOT EXISTS compliance_share;
```

1. Grant the database objects you want to share, as shown in the following
   example:

> Copy code
>
> ```
> GRANT USAGE ON DATABASE app_created_db TO SHARE compliance_share;
> GRANT USAGE ON SCHEMA app_created_db.reporting TO SHARE compliance_share;
> GRANT SELECT ON TABLE app_created_db.reporting.metrics TO SHARE compliance_share;
> ```

Note

Apps can only share data from the following sources:

- Databases created by the app: The app must be the owner of these databases.

Apps can choose to directly grant privileges on an object to a share or grant a database
role to share. For more information, see [How to share database objects](/user-guide/data-sharing-gs#label-data-sharing-share-options).
Apps cannot directly add target accounts to the share. This is controlled through the app specification.

## Create an external listing

1. To create an external listing attached to the share, add the
   [CREATE LISTING](/sql-reference/sql/create-listing) command to the setup script as shown in the following
   example:

   Copy code

   ```
   CREATE EXTERNAL LISTING IF NOT EXISTS compliance_listing
   SHARE compliance_share
     AS
     $$
    title: "Compliance Data Share"
    subtitle: "Regulatory compliance reporting data"
    description: "Share compliance and audit data with authorized accounts"
    listing_terms:
      type: "OFFLINE"
     $$
     PUBLISH = FALSE
     REVIEW = FALSE;
   ```

Note

- Apps can only attach shares, not application packages, to a listing.
- Apps cannot directly add target accounts or auto-fulfillment configuration
  to the listing.
- The listing manifest can only include the following properties: title,
  subtitle, description, and listing\_terms.
- All new listings must be created in an unpublished state, with both PUBLISH
  and REVIEW set to FALSE.
- The listing title and description can be customized based on the consumer
  info, allowing providers to distinguish data sources.

## Create an app specification for a listing

1. To create an app specification for a listing, follow this example:

   Copy code

   ```
   ALTER APPLICATION SET SPECIFICATION shareback_spec
     TYPE = LISTING
     LABEL = 'Compliance Data Sharing'
     DESCRIPTION = 'Share compliance data with provider for regulatory reporting'
     TARGET_ACCOUNTS = 'ProviderOrg.ProviderAccount,AuditorOrg.AuditorAccount'
     LISTING = compliance_listing
     AUTO_FULFILLMENT_REFRESH_SCHEDULE = '720 MINUTE';
   ```

   This command creates an app specification named `shareback_spec` that requests permission to
   share data with the specified target accounts.
2. For cross-region sharing, the `AUTO_FULFILLMENT_REFRESH_SCHEDULE` parameter is required.
   You can set it to one of the following values:

   - `'<num> MINUTE'`: Number of minutes, with a minimum of 10 minutes,
   - and a maximum of 8 days or 11520 minutes (eight days)
   - `'USING CRON <expression> <time_zone>'`: Cron expression with time
     zone

Note

- The app should only create the app specification after the listing and share objects exist.
- Each listing can only have one associated app specification.
- Updating the target accounts creates a new pending request for consumer approval.

## Consumer approval workflow

For more information on how consumers view and approve app specifications, see [Approve app specifications](/developer-guide/native-apps/ui-consumer-app-spec).

Consumer approval of a LISTING app specification triggers this workflow:

- Snowflake automatically adds the target accounts to the listing.
- If specified, Snowflake configures the auto-fulfillment refresh schedule.
- The listing becomes visible to the target accounts.
- Data attached to the listing can be queried from the approved accounts.

Consumer rejection of a LISTING app specification triggers this workflow:

- Auto-fulfillment is disabled.
- The listing remains published, allowing the consumer to continue viewing the shared data.
- All target accounts are removed from the listing, with the exception of the current account where the app is installed.
- Data attached to the listing can no longer be queried by target accounts other than the current account.

## Validating the listing configuration

Apps can validate that the listing has been properly configured after approval by running the following commands:

Copy code

```
-- Check if the app specification is approved:
SHOW APPROVED SPECIFICATIONS IN APPLICATION;

-- Validate the listing configuration:
DESC LISTING compliance_listing;
```

## Best practices for LISTING app specifications

When implementing data sharing through app specification, consider the following
best practices:

- **Share integrity:** Snowflake does not prevent consumers from modifying
  shares created by an application. As a result, the provider is responsible
  for implementing measures to protect the integrity of the underlying shared
  data.
- **Error handling:** Implement proper error handling for cases where the app
  specification is declined or not yet approved.
- **Cross-region considerations:** The app provider is responsible for setting
  refresh schedules that balance data freshness requirements with cost
  considerations. Although Listing Auto Fulfillment costs are billed to the app
  consumer, the provider’s choice of schedule should be cost-aware to minimize
  the unnecessary cost for the app consumer.
- **Compliance:** Document clearly what data you are sharing, and why you are
  sharing it, in the app specification description.

## Using callback functions with LISTING app specifications

Apps can use lifecycle callbacks to respond when consumers approve or decline
listing specifications by adding the following code to the manifest file:

Copy code

```
lifecycle_callbacks:
  specification_action: callbacks.on_spec_update
```

In the setup script, add the following callback stored procedure:

Copy code

```
CREATE OR REPLACE PROCEDURE callbacks.on_spec_update (
  name STRING,
  status STRING,
  payload STRING)
RETURNS STRING
LANGUAGE SQL
AS
$$
BEGIN
  IF (name = 'SHAREBACK_SPEC' AND status = 'APPROVED') THEN
    -- Start populating shared tables
    CALL populate_compliance_data();
  ELSEIF (name = 'SHAREBACK_SPEC' AND status = 'DECLINED') THEN
    -- Clean up or notify provider
    CALL cleanup_share_data();
  END IF;
  RETURN 'Processed specification update';
END;
$$;
```

The procedure allows the app to react appropriately to consumer decisions about app’s data sharing request.

## Viewing shareback data as a provider

After a consumer approves the LISTING app specification and data is shared, the provider
can view the shared listing and access the data. Providers can do this using either
Snowsight or SQL.

SnowsightSQL

1. Sign in to Snowsight as a user with the ACCOUNTADMIN role.
2. In the navigation menu, select **Data sharing** » **External sharing**.
3. Select the **Shared with you** tab.
4. Find the shareback listing from the consumer and select it.
5. Follow the prompts to install the listing and create a database from the shared data.

1. To find the listing shared by the consumer, run [SHOW AVAILABLE LISTINGS](/sql-reference/sql/show-available-listings)
   with the `IS_SHARED_WITH_ME` filter:

   Copy code

   ```
   SHOW AVAILABLE LISTINGS IS_SHARED_WITH_ME = TRUE;
   ```
2. Identify the `listing_global_name` of the shareback listing from the output. Then create a
   database from the listing:

   Copy code

   ```
   CREATE DATABASE shareback_data FROM LISTING '<listing_global_name>';
   ```

   Note

   Creating a database from a listing requires the IMPORT LISTING privilege on the account.

## Viewing shareback data as a consumer

Before approving a LISTING app specification, consumers should inspect the data that the app
intends to share. This provides full visibility into the actual content of a share, allowing
consumers to verify the following:

- The data being shared matches what the provider described in the app specification.
- No sensitive or unexpected data is included in the share.
- The data meets any internal compliance or governance requirements.

Consumers can inspect data prior to approval and continue to query it at any time after approval.
Use either Snowsight or SQL to view the shared data.

SnowsightSQL

1. Sign in to Snowsight as a user with the ACCOUNTADMIN role.
2. Navigate to the app’s page.
3. In the application page, select the **Permissions** tab.
4. Under **Data sharing**, click **Review** for a requested data share. The following
   details are displayed:

   - The name of the data share listing
   - The reason that the app is requesting to share data
   - The accounts that have access to the data share
   - The replication schedule for the data share
5. To preview the data, click the **Preview data** button. The shared data is displayed in
   table format, grouped by schema. Note that the shared data is not editable.
6. To view shared data for other schemas or tables, use the drop-down menus.
7. To open the data in a worksheet for further querying, click the **Open in workspace** button.

The Uniform Listing Locator (ULL) is a unique identifier for app-created listings that allows
consumers to query shared datasets directly. To find the ULL for a specific listing, check the
`uniform_listing_locator` column in the output of the SHOW LISTINGS or DESC LISTING commands.

To query the shared data, reference objects using the ULL, which contains a `NATIVEAPP$`
prefix followed by the listing SQL name:

Copy code

```
SHOW SCHEMAS IN DATABASE NATIVEAPP$MY_LISTING;
SHOW OBJECTS IN SCHEMA NATIVEAPP$MY_LISTING.MY_SCHEMA;
SELECT * FROM NATIVEAPP$MY_LISTING.MY_SCHEMA.MY_TABLE;
```

## Limitations

This section describes limitations when using app specifications.

Auditing
:   Snowflake doesn’t offer built-in auditing for data that an app shares
    back to the provider. If a consumer has compliance or regulatory requirements
    that include an audit trail, they must coordinate directly with the provider
    to implement their own separate monitoring solutions.

Sharing from within the application
:   Snowflake does not recommend data sharing with the provider directly from
    within the application because Listing Auto Fulfillment is not currently
    supported for data shared in this manner.
