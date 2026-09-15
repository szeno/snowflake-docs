# Configure private connectivity for the Snowflake Open Catalog UI

[Business Critical Feature](https://docs.snowflake.com/en/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To ask about upgrading, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Feature — Generally Available

Not available in government regions.

This topic describes how to configure private connectivity for the Snowflake Open Catalog UI. This configuration, combined with configuring
private connectivity for your Open Catalog account, allows you to access the Open Catalog UI through private connectivity instead of over
the public internet. For more information, see the [prerequisites for configuring private connectivity for the Snowflake Open Catalog UI](#prerequisites).

Configuring private connectivity for the UI is similar to configuring it for your Open Catalog account. However, when you configure it for
the UI, you need to configure additional DNS entries because the UI is hosted under a different domain, compared to your account.

## Prerequisites

- Before you configure private connectivity for the Open Catalog UI, you must set up inbound private connectivity for your Open Catalog
  account. If you don’t, you won’t be able to use the UI.

  To set up inbound private connectivity for your Open Catalog account, follow the guide specific to the cloud platform that hosts your Open Catalog account:

  - [AWS](private-connectivity-inbound-configure-aws)
  - [Azure](private-connectivity-inbound-configure-azure)

## Step 1: Retrieve your PrivateLink URLs

In this procedure, you retrieve PrivateLink URLs, which you use to configure private connectivity.

1. Sign in to Snowflake Open Catalog.
2. In the navigation menu, select **Settings**.
3. On the Settings page, copy the values for the following settings into a text editor:

   - PrivateLink Account URL
   - Regionless PrivateLink Account URL
   - Regionless Snowsight PrivateLink URL
   - Snowsight PrivateLink URL

   For descriptions of each setting, see
   [Return values for the SYSTEM$GET\_PRIVATELINK\_CONFIG system function](https://docs.snowflake.com/en/sql-reference/functions/system_get_privatelink_config#returns)
   in the Snowflake documentation. In this topic, the names of the account settings are in JSON format.

Note

- Remember that the description refers to a Snowflake account, but your value is actually for your Snowflake Open
  Catalog account. For example, the `privatelink-account-url` is the URL for your Snowflake Open Catalog account.
- You need the **Regionless Snowsight PrivateLink URL** and **Snowsight PrivateLink URL** settings because if an Open Catalog user navigates to the Regionless Account URL, the user is redirected to Snowsight.
- Optional: To retrieve these values in JSON format, [Create a Snowflake CLI connection for Open Catalog](private-connectivity-outbound-manage-endpoints-aws#step-1-create-a-snowflake-cli-connection-for-open-catalog),
  and then call the SYSTEM$GET\_PRIVATELINK\_CONFIG system function.

## Step 2: Confirm your settings

To use private connectivity with the Open Catalog UI, configure your DNS, and ensure that firewalls allow access to the relevant values:

1. Confirm that your DNS settings can resolve the values.
2. To confirm that you can connect to Open Catalog from your browser, use each of the PrivateLink URLs.
3. Optional: To use the account name URL (the value for **Regionless PrivateLink Account URL**) as your primary URL to access Open Catalog,
   contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support), and request that all URL redirects point to the URL
   specified by **Regionless PrivateLink Account URL**.
