# Auto-fulfillment for listings

If you’re a provider, you can use Cross-Cloud Auto-Fulfillment (auto-fulfillment) for a listing to automatically replicate your data product to other Snowflake regions without having to manually replicate data.

When auto-fulfillment is enabled for a listing, Snowflake automatically fulfills your data product to consumer regions as
needed. A data product is any share or application package that is attached to your listing.

By using auto-fulfillment, you can avoid manually replicating your data products and approving requests for your listings,
helping consumers access your listings faster.

Note

Using Cross-Cloud Auto-Fulfillment in a Snowflake Native App with Snowpark Container Services is only supported on Amazon Web Services (AWS)
and Microsoft Azure. See
[Understand limitations in the Snowflake Native App Framework](/developer-guide/native-apps/limitations)
for more information.

## Understanding auto-fulfillment

Note

Auto-fulfillment isn’t available on trial accounts. Auto-fulfillment is configured on listings, and to offer listings, you must use a full account.

Auto-fulfillment lets you offer a data product in any supported Snowflake region, based on the availability and access options
you select for your listing, without having to manually replicate data.

You can configure and enable auto-fulfillment when a listing is in either draft or published state. When auto-fulfillment
is enabled for a listing, Snowflake automatically fulfills your listing’s product to regions as needed.

How you make your data product available in other regions depends on your data product and how consumers access your listing:

- If your data product is an application package, use auto-fulfillment to make your data product available in other regions.
- If your data product is a share, use auto-fulfillment in most cases:
  - For free or limited trial listings on the Snowflake Marketplace, you can use Cross-Cloud Auto-Fulfillment or
    [manually replicate the data](https://other-docs.snowflake.com/en/collaboration/provider-listings-managing#label-manually-replicate-listing).
  - For paid listings, you use auto-fulfillment.
  - For all listings shared with specific consumer accounts, Snowsight automatically detects whether or not the target account
    is in a different region and enables auto-fulfillment. You cannot manually replicate private listings to other regions.

When you make a data product available in other regions, you incur additional costs.
See [Auto-fulfillment costs](/collaboration/provider-understand-cost-auto-fulfillment).

## How auto-fulfillment works

As a provider, when you set up Cross-Cloud Auto-Fulfillment for your listing, Snowflake manages provisioning for a *secure share area* (SSA) and the
auto-fulfillment of your data product to remote regions. The SSA is managed by Snowflake.
If your data product already exists in the remote region, consumers in that region can get the data product instantly.

Each listing has a data product associated with it, whether a share or an application package. That data product contains objects from
one or more databases, as well as application logic for an application package. Exactly when your data product is auto-fulfilled to a remote region depends on how you make your listing available:

- Private listings are auto-fulfilled after the specified consumers get your listing.
- Public listings shared on Snowflake Marketplace are auto-fulfilled after a consumer in the specific region
  gets the listing.

When your data product is auto-fulfilled to a new region for the first time, it’s transferred to an SSA in that region. Auto-fulfillment can be configured with SUB\_DATABASE or SUB\_DATABASE\_WITH\_REFERENCE\_USAGE settings.

- SUB\_DATABASE allows selected objects to be available on-demand.
- SUB\_DATABASE\_WITH\_REFERENCE\_USAGE provides account-level scheduling for application packages.

Note

Specifying FULL\_DATABASE for the auto-fulfillment refresh type is deprecated.

Multiple listings can use the same database, but the database is only auto-fulfilled once to a new region.

Note

For Business Critical Edition (BCE), the handling of shared data differs from high-security deployments like VPS.
While BCE does not require creating a separate SSA for the region, it enforces strict data security and compliance with
features like Tri-Secret Secure encryption.

For deployments such as Virtual Private Snowflake (VPS) and government-specific Snowflake environments, there is a separate
secure share area (SSA) for each deployment. This ensures that auto-fulfillment remains compliant with strict security and
data isolation requirements unique to those environments.

## How auto-fulfillment refreshes data

When you set up auto-fulfillment for your listing, you can configure a refresh interval for your data product.

After the initial auto-fulfillment of your data product to the SSA in a region, changes to your data product are synced from
your account based on the configured data refresh:

| Data refresh type | Description |
| --- | --- |
| Trigger-based data refresh | Providers can use [SYSTEM$TRIGGER\_LISTING\_REFRESH](/sql-reference/functions/system_trigger_listing_refresh) to trigger an on-demand data refresh, ensuring that consumers receive the most current information.  Snowflake recommends using trigger-based data refresh when an upstream extract-transform-load (ETL) pipeline process completes and you want to trigger a replication when the data is ready. For example, if you are a data provider who delivers stock analysis to financial institutions, you can trigger an update to all the analysts with new datasets as soon as they are updated in your upstream ETL pipeline.  **Note:** This feature is only available using SQL. |
| Trigger-based refresh of an application package | If the data product of a listing is an application package, providers can set the [SYSTEM$TRIGGER\_LISTING\_REFRESH](/sql-reference/functions/system_trigger_listing_refresh) to trigger an on-demand refresh of the application package. However, providers must run this function each time the application package needs to be refreshed.  To configure the application package to refresh each time the release directive is modified, use the LISTING\_AUTO\_REFRESH clause of the [ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package) command. |
| Interval-based data refresh | Providers can establish an interval-based data refresh for all consumers of a listing, with time periods ranging from one minute to eight days. Each listing associated with a database operates on the same refresh interval.  Interval-based data refresh configuration is recommended when you require updates at a predefined cadence. For example, providers who refresh datasets weekly can use interval-based refresh to update their database on the same schedule. Each refresh completion triggers the next refresh according to the cadence. See [Set the account-level refresh interval](/collaboration/provider-listings-auto-fulfillment-set-refresh-interval) for details.  **Note:** This feature is available using SQL or **Provider Studio** in Snowsight. |
| Schedule-based data refresh | Providers can establish a timestamp and schedule for data refreshes across all consumers of a listing. Every listing that utilizes a database will adhere to the same refresh schedule.  Schedule-based data refresh is recommended for use cases where listing updates need to occur at a specific timestamp and schedule. For example, data providers who need to offer a predictable timestamp for when refreshes are available to all consumers can use schedule-based data refresh.  Interval-based and schedule-based data refreshes cannot be used simultaneously. If both are set up, one will override the other. For example, if a cron expression is set up for a scheduled refresh that already has a refresh interval, it will be overridden to support scheduled refresh. See [auto\_fulfillment](/progaccess/listing-manifest-reference#label-listing-api-manifest-auto-fulfillment) for details.  **Note:** This feature is available using SQL or **Provider Studio** in Snowsight. |

Expand

Show lessSee more

### Data products as shares vs application packages

When you set up auto-fulfillment for your listing, the data product you offer determines how you set up the data refresh.

- If your data product is a share, set a data refresh when you configure auto-fulfillment for a listing. The data refresh applies to the database associated with the listing. If multiple listings share objects from that database, they share the same data refresh type and schedule/interval.
- If your data product is an application package, set a data refresh at the account level that applies to every application package available from your account.

## Considerations for auto-fulfillment

When you use auto-fulfillment for your listings, consider the following:

- Snowflake supports having multiple databases with the same name. Auto-fulfillment creates a single secure share area (SSA) account in the target region, and the SSA can’t have two databases with the same name. As a result, if you have two or more databases with the same name in the source account, auto-fulfillment will append a unique prefix to the database name to avoid conflicts in the SSA account. For example, imagine the following scenario:

  - An organization has two accounts, production and dev.
  - Production and dev each have a database named `AnyCompanyData`.

  Because the destination will always have one SSA account with two databases, auto-fulfillment will append a prefix to the duplicate database name, resulting in two databases: `AnyCompanyData` and `PrefixXXXXX_AnyCompanyData`.
- If you signed up for Snowflake using AWS Marketplace, Google Cloud Marketplace, or Azure Marketplace, you can only create accounts and
  SSAs in those clouds. Fulfilling listings to regions outside of your current cloud service region will fail.
- Depending on the size of your data product, it can take some time for the data product to be available to the consumer.
  The size of your data product can also affect the cost of auto-fulfillment.
  See [Auto-fulfillment costs](/collaboration/provider-understand-cost-auto-fulfillment) for details about cost.
- Object-level mode (SUB\_DATABASE) is used by default.
- (Deprecated) If a listing uses objects that are located in a database that’s already in full database mode (FULL\_DATABASE), a warning displays in Snowsight and the database remains in full database mode.
- Snowflake compiles the listing auto-fulfillment refresh history and sends emails for failed listing refreshes daily. These messages are sent to the email address specified on the listing.
- If the provider has a tag that includes a masking policy at the *account* level, auto-fulfillment doesn’t take that masking policy into account when auto-fulfilling the data product. For auto-fulfillment, the scope of sharing is at the database, schema, and table level, but not at the account level.
- Auto-fulfillment enforces a default 10TB limit on the size of the data product. For more information, refer to the
  [The database is larger than 10 terabytes](/collaboration/provider-listings-auto-fulfillment-troubleshoot-setup#label-laf-troubleshoot-database-too-large) troubleshooting topic. After assessing the cost implications, an account administrator can increase the size limit by setting the [LISTING\_AUTO\_FULFILLMENT\_INITIAL\_REFRESH\_SIZE\_LIMIT\_IN\_TB](/sql-reference/parameters#label-listing-auto-fulfillment-initial-refresh-size-limit-in-tb) parameter.

- If you use [Tri-Secret Secure](/user-guide/security-encryption-tss), you must contact
  [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) to enable Tri-Secret Secure for the secure share areas used for auto-fulfillment.
  - With Tri-Secret Secure, query results are encrypted using one key from the provider, one from Snowflake, and one from the consumer. Each key independently governs access. If a key is revoked, only its owner loses access. For example, revoking the provider key does not prevent the consumer from accessing data that has already been retrieved.
