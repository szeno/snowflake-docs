# Create an additional Snowflake Open Catalog account

Feature — Generally Available

Not available in government regions.

Note

New customers should use [Snowflake Horizon Catalog](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon)
for Apache Iceberg™ tables and multi-engine interoperability with Iceberg. Customers who
haven’t previously created a Snowflake Open Catalog account can’t sign up for their first Open
Catalog account.

Existing Snowflake Open Catalog customers can continue to use and can create additional
Open Catalog accounts if necessary.

This topic applies to existing Snowflake Open Catalog customers who already have at least one Open Catalog account and need to create an
additional Open Catalog account. Customers who haven’t previously created a Snowflake Open Catalog account can’t use this workflow to sign
up for their first Open Catalog account. New customers should use [Snowflake Horizon Catalog](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon)
for Apache Iceberg™ tables and multi-engine interoperability with Iceberg.

Eligible existing Open Catalog customers can create an additional Open Catalog account by using Snowsight or the CREATE ACCOUNT Snowflake
SQL command.

**Note**

> To create an additional Open Catalog account, you must be a user with the organization administrator (ORGADMIN) role.

## Create an additional account by using Snowsight

To create an additional Open Catalog account by using Snowsight, do the following:

1. Sign in to Snowsight.
2. Select **Admin** > **Accounts**.
3. In the **+ Account** drop-down, select **Create Snowflake Open Catalog Account**.
4. In the **Create Snowflake Open Catalog Account** dialog, complete the fields:

   - **Cloud:** The cloud provider where you want to store Apache Iceberg™
     tables.
   - **Region:** The region where you want to store Iceberg tables.
   - **Edition:** The edition for your Open Catalog account.
5. Select **Next**.
6. In the **Create New Account** dialog, complete the **Account Name**, **User Name**, **Password**, and **Email** fields.
7. Select **Create Account**.

   Your additional Open Catalog account is created and a confirmation box appears.
8. In the confirmation box, select the **Account Locator URL** to open
   the Account Locator URL in your web browser.
9. Bookmark the Account Locator URL. When signing in to Open
   Catalog, you must specify the Account Locator URL.

## Create an additional account by using Snowflake SQL

To create an additional Open Catalog account by using Snowflake SQL, run the following
CREATE ACCOUNT SQL command:

Copy code

```
CREATE ACCOUNT <account_name>
ADMIN_NAME = <admin_user_name>
ADMIN_PASSWORD = '<admin_user_password>'
MUST_CHANGE_PASSWORD = { TRUE | FALSE }
EMAIL = '<admin_user_email>'
EDITION = standard
REGION = <cloud_region>
POLARIS = TRUE;
```

For more information, see [CREATE ACCOUNT](https://docs.snowflake.com/en/sql-reference/sql/create-account).

**Important**

> After you run the CREATE ACCOUNT SQL command, copy the accountLocatorUrl in the command output and save it for signing in to Open Catalog.

[![accountLocatorUrl for a Snowflake Open Catalog account.](/static/images/user-guide/opencatalog/img/account-locator-url.png)](/static/images/user-guide/opencatalog/img/account-locator-url.png)
