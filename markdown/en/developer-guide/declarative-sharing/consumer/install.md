# Install a Declarative Native App

Feature — Generally Available

Support for Snowflake Declarative Native Apps is available to all accounts.

Snowflake Declarative Native Apps are databases that you can use to gain access to data and functionality shared by Snowflake data providers.

You can use Snowsight to install and access Declarative Native Apps, or you can use SQL commands to access the data directly.

After you install an app, you can share it with other members of your organization.

# Security

Declarative Native Apps have a similar security model to secure data sharing:

- Apps only have access to the data included in the app.
- Apps can’t access the consumer’s private data.
- Apps aren’t allowed to make external calls or to access data outside of the Snowflake account.

## Prerequisites

To install a Declarative Native App, you must have a Snowflake account and a role with either of the following:

- The **ACCOUNTADMIN** role
- A role with both **CREATE APPLICATION** and **IMPORT LISTING** privileges

To purchase a paid listing, the role must also have the **PURCHASE DATA EXCHANGE LISTING** privilege.

### Grant installation privileges

An ACCOUNTADMIN can allow members of the organization to install
Declarative Native Apps by granting privileges to the member’s role,
using the [GRANT privileges TO ROLE](/sql-reference/sql/grant-privilege) command:

Copy code

```
GRANT CREATE APPLICATION ON ACCOUNT TO ROLE <role_name>;
GRANT IMPORT LISTING ON ACCOUNT TO ROLE <role_name>;
```

## Install an app

Roles with installation privileges can install a Declarative Native App from the Snowflake Marketplace, or from a privately shared listing.

Snowflake MarketplaceFrom a privately shared listingFrom SQL

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Snowflake Marketplace**.
3. Search or browse to the listing you want to access.
4. Select the listing, and select **Get** or **Buy**.
5. (Optional) Enter a name for **Application name**.
6. Select **Get**.
7. Select **Open** to view the app, or select **Done** to finish.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Apps**.
3. Select the tile for the listing under Recently shared with you.
4. Select **Get**.
5. Select **Options** and enter a name for the app.
6. Select the warehouse where you want to install the app.
7. Select **Get**.
8. Select **Open** to view your listing or **Done** to finish.
9. Explore the listing as you would any other listing.

1. Show the available listings in the Snowflake Marketplace with the command: [SHOW AVAILABLE LISTINGS IN DATA EXCHANGE SNOWFLAKE\_DATA\_MARKETPLACE](/sql-reference/sql/show-available-listings).

   Copy code

   ```
   SHOW AVAILABLE LISTINGS IN DATA EXCHANGE SNOWFLAKE_DATA_MARKETPLACE;
   ```
2. Install the app with the command: [CREATE APPLICATION FROM LISTING](/sql-reference/sql/create-application).

   Copy code

   ```
   CREATE APPLICATION <app_name> FROM LISTING <listing_name>;
   ```

The user who installs the app is the app owner. The app owner and the ACCOUNTADMIN have access to all objects shared in the app, including notebooks, tables, views, and other objects.

## Share access to the app

The app owner (or the ACCOUNTADMIN) can share access to the data and features in a Snowflake Declarative Native App
with members of their organization by their organization role.

They can share access to the entire app, or for some apps, they can share access to a subset of the data and features in the app, defined by app roles.

> [![App owners assign app roles to teams in their organization](/static/images/ds-native-apps/dsna-app-roles.png)](/static/images/ds-native-apps/dsna-app-roles.png)

### Share access to all data and features in an app

App owners can share access to all of the data and features in an app with the command: [GRANT IMPORTED PRIVILEGES ON APPLICATION](/sql-reference/sql/grant-privilege).

In this example, an app owner imports privileges for the application `marketing_data_app` to the `team_admin_role` organizational role:

Copy code

```
GRANT IMPORTED PRIVILEGES ON APPLICATION marketing_data_app TO ROLE team_admin_role;
```

Note

Sharing app access doesn’t share the ability to share app privileges with others.

### App roles: Share access to a portion of the data and features in an app

Some Declarative Native Apps include app roles, which provide access to a subset of the data and features in an app. App owners can assign app roles to their organization roles. This grants members of the organization roles access to the data and features defined in the app roles.

1. List the available roles with the command: [SHOW APPLICATION ROLES](/sql-reference/sql/show-application-roles). For example:

   Copy code

   ```
   SHOW APPLICATION ROLES IN APPLICATION marketing_data_app;
   ```

   The command lists the available app roles. If the app has no app roles, the command returns an empty result set.
2. Grant app roles to teams by their organization roles with the command: [GRANT APPLICATION ROLE … TO ROLE](/sql-reference/sql/grant-application-role).

   Copy code

   ```
   GRANT APPLICATION ROLE marketing_data_app.sales TO ROLE sales_team_west;
   ```

Considerations:

- Consumers can’t share access to individual objects in the app, such as individual tables, views, or notebooks, except as defined by app roles.
- Consumers can’t define new app roles, or modify the existing app roles.
- Consumers can’t share access to the objects in the app with members outside their organization.

## Access the app

For information about using the app, see [Access content in a Declarative Native App](/developer-guide/declarative-sharing/consumer/access-app-content).
