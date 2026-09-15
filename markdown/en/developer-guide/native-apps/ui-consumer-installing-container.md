# Install and manage an app with containers

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how to use [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) to install a Snowflake Native App with Snowpark Container Services.

## Workflow for installing an app with containers from a listing

To find and install a listing for a Snowflake Native App with Snowpark Container Services:

1. [Set up the privileges required to install a listing](#label-nativeapps-consumer-listings-privs-container).
2. Install the listing.

   - If you are installing a privately shared listing, refer to [Install an app with containers from a privately shared listing](#label-nativeapps-consumer-listings-install-container)
   - If you are installing a listing shared on the Snowflake Marketplace, refer to
     [Working with Snowflake Marketplace Listings for an app](#label-nativeapps-consumer-listings-install-marketplace-container).
3. [View the installed listing](/developer-guide/native-apps/ui-consumer-managing-applications#label-nativeapps-consumer-listings-view).
4. Refer to [Allow access to a consumer account](/developer-guide/native-apps/ui-consumer-granting-privs) for information on tasks related to managing an app.

## Set up required privileges

To access a listing, you must use the ACCOUNTADMIN role or another role with the IMPORT SHARE and
CREATE privileges on the app.

After an app is installed, the app owner can grant access to the app
using application roles. Refer to [Grant application roles to account roles](/developer-guide/native-apps/ui-consumer-managing-applications#label-nativeapps-consumer-grant-app-roles) for details.

Note

To pay for an app, your role must also have the PURCHASE DATA EXCHANGE LISTING privilege and you must meet additional
criteria. For more information, see
[Pay for Snowflake Marketplace listings](/collaboration/consumer-listings-paying).

## Install an app with containers from a privately shared listing

Note

As a provider, you can test your app by creating a private listing, sharing it with another account in your organization
that you have access to, signing in to that account, and following these steps to install the app.

To install an app with containers from a private listing:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Apps**.
3. In **Recently shared with you**, select the tile for the listing.
4. Select **Get**, or for a monetized app, select **Buy**.
5. Select **Options**, then enter a name for the app.
6. Select the warehouse where you want to install the app.
7. Select **Get**.

   The **Installing app** dialog displays. It may take some time to install the app.
   After the app is installed, the dialog displays **Successfully Installed**.
8. Select **Configure**.

   This displays a list of the privileges and references to objects the app requires.
9. Click **Grant** to grant the privileges required by the app.

   Apps with containers frequently require the following privileges:

   - CREATE COMPUTE POOL allows the app to create a compute pool in your account.
   - BIND SERVICE ENDPOINT allows services in the app to connect to each other.
10. Click **Activate**.

The app begins activation. Depending on the complexity of the app, this may take some time.

After activation, the **Settings** page is displayed.

11. After the activation is complete, select **Launch App**.

## Install an app from a Snowflake Marketplace listing

To install an app from a Snowflake Marketplace listing, perform the following steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Snowflake Marketplace**.
3. Search or browse to the listing you want to access.
4. Select the tile for the listing.
5. Select **Get**, or for a monetized app, select **Buy**.
6. Select **Options**, then enter a name for the app.
7. Select the warehouse where you want to install the app.
8. Select **Get**.

   The **Installing app** dialog displays. It may take some time to install the app.
   After the app is installed, the dialog displays **Successfully Installed**.
9. Select **Configure**.

   This displays a list of the privileges and references to objects the app requires.
10. Click **Grant** to grant the privileges required by the app.

Apps with containers frequently require the following privileges:

- CREATE COMPUTE POOL allows the app to create a compute pool in your account.
- BIND SERVICE ENDPOINT allows services in the app to connect to each other.

11. Click **Activate**.

The app begins activation. Depending on the complexity of the app, this may take some time.

After activation, the **Settings** page is displayed.

12. After the activation is complete, select **Launch App**.

## View the compute pools used by an app with containers

An app with containers provides a **Compute** tab that allows you to view information about
the compute pools used by an app. For information about managing other components of an app,
see [Manage apps](/developer-guide/native-apps/ui-consumer-managing-applications).

To view the compute pools used by an app:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Apps**.
3. Select the app whose compute pools you want to view.
4. Select the **Compute** tab.

This tab displays the following information for each compute pool:

- The name of the compute pool and its status.
- The number of jobs running in the compute pool.
- The number of services running in the compute pool.
- The number of nodes currently assigned to the compute pool.
- The minimum number of nodes the compute pool can contain.
- The maximum number of nodes the compute pool can contain.
- The instance family of the compute pool.

For more information on these properties, see
[CREATE COMPUTE POOL](/sql-reference/sql/create-compute-pool)
