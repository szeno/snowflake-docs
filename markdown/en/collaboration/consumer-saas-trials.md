# Trial SaaS applications from listings

Some Snowflake Marketplace listings offer an Integrated SaaS delivery method. An Integrated SaaS listing lets you start a free
trial of a provider’s SaaS application directly from the listing page. When you start a trial, Snowflake creates a
database, warehouse, system user, and system role in your account that the provider uses to read or ingest the data
that you authorize.

To find applications that you can trial, browse the Snowflake Marketplace for the Integrated SaaS applications category, and
then apply the **Free to Try** or **Instantly accessible** filters.

Because the provider’s application is a Snowflake Marketplace listing, you can return to it at any time. The same listing
serves as a single place to discover the provider’s data products, start a trial, and purchase the data product,
including the ability to draw down on your Snowflake capacity commitment with
[Snowflake Marketplace Capacity Drawdown](/collaboration/marketplace-capacity-drawdown).

## Requirements

To start an Integrated SaaS trial, you must meet the following requirements:

- You must use the ACCOUNTADMIN role, or a custom role with the privileges required to create the objects listed in the
  trial dialog (such as a database, warehouse, user, and role). To switch to the account administrator role, in the
  lower-left corner, select your name » **Switch role** » **ACCOUNTADMIN**.
- You must have a verified email address in Snowflake. To verify your email address:

  Snowsight:
  :   In some cases, you automatically receive an email prompting you to **Please Validate Your Email**. If you didn’t, follow these
      steps to verify your email address:

      1. sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
      2. in the lower-left corner, select your name » **Settings**.
      3. In **My Profile**, configure your email address:

         - If you don’t have an email address listed, enter an email address in the **Email** field, and then select **Save**.
         - If you can’t enter an email address, an account administrator must either add an email address on your behalf or grant your user
           the role with the OWNERSHIP privilege on your user.
         - If you didn’t receive an email, select **Resend verification email**. Snowflake sends a verification email to the address listed.
      4. Open your email, and then select the link in the email to validate your email address.

## Start a SaaS trial

To trial a SaaS application from a listing:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Snowflake Marketplace**, and then search for the listing
   that you want to trial.
3. Open the listing, and then select **Start free trial** in the upper right.

   To learn what the trial includes before starting, select the **Your free trial** tab on the listing page. The
   **Free trial** card describes the trial terms, and the **What to expect** card summarizes the Snowflake objects
   that will be created and the next steps with the provider.
4. In the **Connect to *provider* to start your trial** dialog (where *provider* is the name of the provider that owns
   the listing), review the following information:

   - The information that will be shared with the provider: your first name, last name, and email address.
   - The Snowflake objects that will be created in your account, named based on the provider. For details, see
     [Objects created for the application](#label-saas-trial-objects).
   - The privileges that will be granted to the system role, and the role hierarchy that will be set up. The PUBLIC role
     is granted to the new role, and the new role is granted to the SYSADMIN role so that account administrators can
     manage the trial.
   - Any optional grants that the listing requests. To review them, expand **Optional Grant**, and then select the
     grants that you want to authorize.
   - The legal terms for connecting to the provider.
5. Select **Connect to *provider***.

   Snowflake creates the listed objects in your account, and then redirects you to the provider’s site to finish
   activating your trial account.

After your trial is active, querying data and using the warehouse incurs standard Snowflake compute charges, but you
aren’t charged for the listing during the trial period.

## Objects created for the application

During the connection process, the following Snowflake objects for the provider’s application are created in your
account. Each object name uses a `PC_` prefix followed by the provider’s ID in uppercase, shown here as `<PROVIDER>`.
For example, for the provider `fivetran`, the database is named `PC_FIVETRAN_DB`.

| Object name | Type | Notes |
| --- | --- | --- |
| `PC_<PROVIDER>_DB` | Database | This database is empty and can be used to load or store data for querying. To use existing databases that already contain data, authorize access through the optional grants in the trial dialog, or grant access manually after the process completes. |
| `PC_<PROVIDER>_WH` | Warehouse | The default size of the warehouse is X-Small, but can be changed if needed. |
| `PC_<PROVIDER>_USER` | System user | This is the user that connects to Snowflake from the provider’s application. A random password for the user is automatically generated. |
| `PC_<PROVIDER>_ROLE` | Role | The PUBLIC role is granted to this custom role, which enables the role to access any objects owned by or granted to the PUBLIC role. In addition, this role is granted to the SYSADMIN role, which enables users with the SYSADMIN role (or higher) to also access any Snowflake objects created for the provider’s access. |

Expand

Show lessSee more

Tip

The preceding objects are created to enable a quick, convenient setup:

- If you prefer to use existing Snowflake objects (databases, warehouses, users, and so on), you can update the
  preferences in the provider’s application to reference the desired objects in Snowflake.
- An account administrator can use [ALTER USER](/sql-reference/sql/alter-user) to change the generated password for
  `PC_<PROVIDER>_USER`.
- To enable access to objects owned by (or granted to) roles other than PUBLIC, grant the other roles to
  `PC_<PROVIDER>_ROLE`.

## Automated application features and resource usage

Provider applications might include automated features, such as dashboards that run on a schedule and consume compute
resources. We encourage you to read the product documentation for the application and to
[monitor usage](/user-guide/warehouses-load-monitoring) of the `PC_<PROVIDER>_WH` warehouse to avoid unexpected Snowflake
credit usage by the application.

## Add provider IP addresses to network policies

If you use a [network policy](/user-guide/network-policies) to restrict access to your Snowflake account based on user
IP address, provider applications can’t access your account unless you add the provider’s IP addresses to the list of
allowed IP addresses in the network policy. For detailed instructions, see [Modify a network policy](/user-guide/network-policies#label-modifying-network-policies).

The following table lists the IP addresses to add for each provider (if available and supported) or provides links to
pages on the provider sites for this information:

| Provider | IP addresses | Notes |
| --- | --- | --- |
| ALTR | `3.145.219.176/28`   `35.89.45.128/28`   `44.203.133.160/28` |  |
| CARTO | N/A |  |
| Coalesce | N/A |  |
| Dataiku | N/A |  |
| dbt Labs | `52.22.161.231`   `52.45.144.63`   `54.81.134.249` |  |
| Domo | N/A |  |
| Etleap | N/A |  |
| Fivetran | `52.0.2.4` | For more setup details, see the [Fivetran Documentation](https://fivetran.com/docs/warehouses/snowflake). |
| Hunters | `18.192.165.147`   `34.223.20.125`   `34.223.186.164`   `34.223.221.217`   `52.32.222.121`   `52.35.55.27`   `52.35.219.75`   `52.40.78.172`   `54.68.155.124`   `54.72.125.231`   `54.73.199.243`   `54.75.50.99`   `54.212.81.93`   `54.214.94.117`   `54.220.191.11` |  |
| Hevo Data CDC for ETL | TBD |  |
| Hex | N/A |  |
| Hightouch | N/A |  |
| Informatica | N/A |  |
| Informatica Data Loader | N/A |  |
| Keboola | N/A |  |
| Matillion Data Productivity Cloud | N/A |  |
| Sigma | `104.197.169.18`   `104.197.193.23` |  |
| SnapLogic | Various | For the IP addresses, see the [SnapLogic Documentation](https://docs-snaplogic.atlassian.net/wiki/spaces/SD/pages/1439269/Network+Setup#NetworkSetup-IPAddressWhitelisting). |
| SqlDBM | N/A |  |
| Striim | N/A |  |
| ThoughtSpot | `35.164.213.211` |  |

Expand

Show lessSee more

## Launch the application

After your trial is active, open the provider’s application from the provider’s site to begin using it. Because the
application remains a Snowflake Marketplace listing, you can return to the listing at any time to manage your trial, discover
related data products, or purchase the data product.

## Stop a trial

If you decide to discontinue a trial for any reason, complete the following steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. To switch to the account administrator role, in the lower-left corner, select your name » **Switch role**
   » **ACCOUNTADMIN**.
3. Open a new worksheet in [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) and run the following command to remove the connection:

   Copy code

   ```
   select system$remove_etl_integration('<partner_id>');
   ```

   Replace `<partner_id>` with the provider’s ID, which is the same ID used to name the objects that were created for
   the trial (for example, `fivetran`).

   This command automatically drops the database, warehouse, system user, and role that were created for the trial, so
   you don’t need to drop those objects manually.
4. If the trial does not expire on its own, contact the provider to end your participation in the trial.

Note

Removing the connection doesn’t remove the Snowflake Marketplace trial record for the listing. As a result, you can’t start a
new trial of the same listing on an account that has already trialed it. To trial the listing again, use a different
account or contact the provider.

## Troubleshooting

### A trial already exists

If a trial for the listing is already active in your account, the dialog displays a notice indicating that you must
contact the provider directly for more information. Only one active trial per listing is supported in an account.

Starting a trial can also fail with a message that a connection already exists in either of the following cases:

- Your account previously trialed the listing. Because removing a connection doesn’t remove the Snowflake Marketplace trial
  record, you can’t start a new trial of the same listing on an account that has already trialed it. To trial the
  listing again, use a different account or contact the provider.
- Your organization already has an account with the provider, initiated either with the provider directly or on another
  one of your Snowflake accounts. In this case, the trial for this account must be initiated directly through the
  provider.
