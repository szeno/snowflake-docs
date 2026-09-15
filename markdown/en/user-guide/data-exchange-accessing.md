# Access a Data Exchange

Data exchange is not enabled for all accounts

To inquire about enabling a data exchange, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

When logging in to the Data Exchange for administrative purposes (for example, joining the exchange, configuring the exchange, configuring data listings), the member must have the ACCOUNTADMIN role.

When logging in to the Data Exchange as a consumer:

- All roles can browse data listings.
- All roles with the ACCOUNTADMIN role can request and get data.
- All roles with the [IMPORT SHARE](/user-guide/security-access-privileges-shares#label-import-share-privilege) and CREATE DATABASE privileges can get and request data.

Note

If you are using private connectivity to the Snowflake service and wish to access the Snowflake Marketplace through the new Snowflake web interface, you must first create a CNAME record, as described in the Snowflake documentation:

- [AWS PrivateLink and Snowflake](/user-guide/admin-security-privatelink)
- [Azure Private Link and Snowflake](/user-guide/privatelink-azure)
- [Google Cloud Private Service Connect and Snowflake](/user-guide/private-service-connect-google)

## Sign in to your Data Exchange as a Data Exchange Admin

To access your Data Exchange, sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).

After your Data Exchange is provisioned by Snowflake, you can administer your exchange using Snowsight.
See [Configure and use a Data Exchange](/user-guide/data-exchange-using).

To add or remove provider profiles, use the **Provider Profiles** tab of the **Manage Exchanges** page.
See [Manage provider profiles](/user-guide/data-exchange-becoming-a-provider).

## Sign in to a Data Exchange as a member

Note

To access a data exchange, your account must be added to the exchange by the Data Exchange Admin.

After you become a member of a data exchange:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **External sharing**.
3. Select the **Shared with you** tab.

See [Configure and use a Data Exchange](/user-guide/data-exchange-using). If you are a data provider, you can also manage data in the exchange.
