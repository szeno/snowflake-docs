# Manage apps

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how to manage a Snowflake Native App after it is installed in a consumer
account.

## View installed Snowflake Native Apps and Streamlit apps

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Apps**.

   A list of installed applications and Streamlit apps appears in the **Installed Apps** list.

## View the readme file for an app

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Apps**.
3. Select an app.
4. Select the **Settings** icon in the toolbar.
5. Select the **About the app** tab.

## Grant application roles to account roles

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Apps**.
3. Select an app.
4. Select the **Settings** icon in the toolbar.
5. Select the **Access management** tab.
6. In the **Account roles with access** pane select **Add**.
7. Select a role in the **Account roles** list.
8. Select **Close**.

## Use a SQL command to grant application roles to account roles

To grant an application role to an account role in the consumer account using SQL commands,
use GRANT APPLICATION ROLE of the GRANT DATABASE ROLE command as
shown in the following example:

Copy code

```
GRANT APPLICATION ROLE hello_snowflake_app.app_public TO ROLE data_manager;
```

## Launch an app

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Apps**.
3. Select an app.
4. Select the **Settings** icon in the toolbar.
5. Click **Launch App**.

## Use custom budgets to monitor credit usage for an app

[Budgets](/user-guide/budgets) allow you to define a monthly spending limit on the
[compute costs](/user-guide/cost-understanding-compute) for an app. You can create
and configure a custom budget to monitor the credit usage for the objects owned by the app that consume credits.

When you add an app to a custom budget, the objects that are owned by the app and that consume credits are added to the
custom budget automatically. These include the warehouses and compute pools that are owned by the app.

Warehouses and compute pools that are **shared** are not tracked by the custom budget automatically, although
you can add these to the custom budget manually. When you create a custom budget for an app, you cannot add objects created
and owned by an app to a separate custom budget. However, you can add warehouses and compute pools that are shared to a separate
custom budget.

### Set up the required role to create a custom budget for an app

To create or edit a custom budget for an app, you must use a role that has the correct privileges. See
[Custom budgets](/user-guide/budgets/custom-budget).

### Create a custom budget for an app in Snowsight

You can create or edit a custom budget for an app directly from the app configuration page. You can also do it from the **Budgets** tab
in Snowsight (see [Use Snowsight to create a custom budget](/user-guide/budgets/custom-budget#label-ui-create-custom-budget)).

To create a custom budget for an app from the app configuration page, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Apps**.
3. Select the app whose custom budget you want to view.
4. Select the **Cost management** tab.
5. Select **Create Budget**.
6. Select **Budget**.
7. Enter a **Budget name**.
8. Select the database and schema in which to create your budget.
9. Enter the **Spending limit**.
10. Enter the email addresses to receive notifications.

Note

Each email address added for custom budget notifications must be
[verified](/user-guide/notifications/email-notifications). The
notification email setup fails if any email address in the list is *not* verified.

11. Select **Resources to monitor**.
12. Select the app to add to the custom budget.

- To add an app, expand **Native Apps** to select an app.
- To add a database, expand **Databases** to select a database.
- To add objects in a schema, expand the schema to list available objects. Expand the object category
  (for example, **Tables** or **Tasks**) to select objects.
- To add a warehouse, expand **Warehouses** to select a warehouse.
- To add a compute pool, expand **Compute Pools** to select a compute pool.

Note

- When you select a database or schema, all [supported objects](/user-guide/budgets/custom-budget#label-budgets-supported-objects)
  (for example, tables) contained within the database or schema are also added to the custom budget.
- You can only add an object to one custom budget. If an object is currently included in one custom
  budget and you add that object to a second custom budget, Snowflake removes the object from the first
  custom budget without issuing a warning.

### Create a custom budget for an app by using SQL

To create a custom budget for an app by using SQL, see
[Use SQL commands to create a custom budget](/user-guide/budgets/custom-budget#label-create-custom-budget-sql).

## Monitor an app

By default, an app owner can use different SQL commands to view information about an app
in the consumer account. To allow other roles in the consumer account to use these commands,
you can delegate the MONITOR privilege to another role.

Copy code

```
GRANT MONITOR ON APPLICATION hello_snowflake_app TO ROLE data_analyst;
```

You can also grant the MONITOR privilege on the app to another app as shown in the following example:

Copy code

```
GRANT MONITOR ON APPLICATION hello_snowflake_app TO APPLICATION another_app;
```

The MONITOR privilege allows the role to run the following commands:

- [DESCRIBE APPLICATION](/sql-reference/sql/desc-application)
- [SHOW REFERENCES](/sql-reference/sql/show-references)
- [SHOW OBJECTS OWNED BY APPLICATION](/sql-reference/sql/show-objects-owned-by-application)
- [SHOW SPECIFICATIONS](/sql-reference/sql/show-specifications)
- [DESCRIBE SPECIFICATION](/sql-reference/sql/desc-specification)

## What to do if an app is unavailable

To check the status of an app, run the
[SHOW APPLICATIONS](/sql-reference/sql/show-applications) command and determine the
`upgrade_status` value. When an app is unavailable, the
[DESCRIBE APPLICATION](/sql-reference/sql/desc-application) command
fails and the error message provides information about why the app is unavailable.

The following table lists the reasons an app is unavailable and methods for resolving
the issue:

| Reason | Possible resolution |
| --- | --- |
| Snowflake disabled the app. | Contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) |
| The consumer account is inactive after being locked or suspended. | The app is re-enabled when the account is restored. |
| The version of the app was dropped from the application package in the provider account. | In this situation the app is no longer usable and must be uninstalled and reinstalled from a current listing. |
| The consumer exceeded the usage limit for a [usage based trial](/collaboration/consumer-listings-exploring#label-trial-paid-listing). | See [Trial a listing](/collaboration/consumer-listings-exploring#label-trial-paid-listing) for possible options. |
| The app was installed from a paid listing, but payment information was not provided or is not current. | Pay for the listing. See [Pay for Snowflake Marketplace listings](/collaboration/consumer-listings-paying) for more information. |
| The trial duration of the listing has exceeded. | Contact the app provider. |
| The provider disabled the app. | Contact the app provider. |

Expand

Show lessSee more

## Uninstall a Snowflake Native App

You can uninstall an app using Snowsight or by running SQL commands.

To uninstall an app, you must use a role that has the OWNERSHIP privilege on the
app. See [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership).

To transfer ownership of objects owned by the app that exist outside the app, you
must use a role that has the MANAGE GRANTS privilege on the objects. See
[Access control considerations](/user-guide/security-access-control-considerations).

### Uninstall an app in Snowsight

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Apps**.
3. Next to the app, select **…**, then select **Uninstall**.

   If the app created objects that exist outside the app, a dialog appears showing
   a list of the objects and their types.

   1. Select one of the following:
      - **Yes, transfer selected objects to a role**.

        If you select this option, choose a role from the list. This role becomes the
        new owner of the object.

        Caution

        When using Snowsight, only the following objects owned by the Snowflake Native App
        can be transferred to a different role:

        - Database
        - Schema
        - Table
        - Views
      - **No, delete all objects created outside the app**.

        If you select this option, the objects will be deleted when the app is
        uninstalled.
4. Select **Uninstall**.

### Use SQL commands to uninstall an app

1. Use the `SHOW OBJECTS OWNED BY APPLICATION` command to view the objects owned by
   the Snowflake Native App that exist outside the app as shown in the following example:

   Copy code

   ```
   SHOW OBJECTS OWNED BY APPLICATION hello_snowflake_app;
   ```

   This command shows a list of objects and their types.
2. Optionally, to transfer ownership of an object to a different role, use the
   [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command as shown in the following example.

   Copy code

   ```
   GRANT OWNERSHIP ON DATABASE na_external_db TO ROLE consumer_role;
   ```
3. To delete the app, run the
   [DROP APPLICATION](/sql-reference/sql/drop-application) command as shown in the
   following example:

   Copy code

   ```
   DROP APPLICATION hello_snowflake_app CASCADE;
   ```

   Note

   If you do not transfer ownership of the objects owned by the app to a different role, you must used the `CASCADE` option. If objects owned
   by the app still exist you can’t drop the app without using the `CASCADE` option.
