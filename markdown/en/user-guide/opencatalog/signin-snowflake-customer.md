# Sign in to Snowflake Open Catalog

Feature — Generally Available

Not available in government regions.

Note

New customers should use [Snowflake Horizon Catalog](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon)
for Apache Iceberg™ tables and multi-engine interoperability with Iceberg. Customers who
haven’t previously created a Snowflake Open Catalog account can’t sign up for their first Open
Catalog account.

Existing Snowflake Open Catalog customers can continue to use and can create additional
Open Catalog accounts if necessary.

This topic describes how existing Snowflake Open Catalog customers sign in to an existing Open Catalog account.

## Sign in using your Open Catalog credentials

If your sign-in credentials are managed by Open Catalog, you can access Open Catalog over the public internet or through private connectivity:

- [Using the internet](#using-the-internet)
- [Using private connectivity](#using-private-connectivity)

### Using the internet

To access Open Catalog over the public internet, follow these steps:

1. In a supported web browser, navigate to
   <https://app.snowflake.com/>.
2. For **Account identifier**, enter your account identifier. If you’ve previously signed in to Open Catalog, you might see an account name
   that you can select.
3. Enter your username and password, and select **Sign in**.
4. If prompted, enter your multi-factor authentication (MFA) passcode.

### Using private connectivity

After completing the [configuration to use private connectivity](private-connectivity-ui-configure), access Open Catalog:

1. In a supported web browser, navigate to one of the following URLs for your Open Catalog account:

   - **PrivateLink Account URL**
   - **Regionless PrivateLink Account URL**

   To retrieve these URLs, see [Retrieve your PrivateLink URLs](private-connectivity-ui-configure#step-1-retrieve-your-privatelink-urls).
2. Enter your username and password, and select **Sign in**.
3. If prompted, enter your multi-factor authentication (MFA) passcode.

## Sign in using SSO

If your sign-in credentials are managed by an identity provider, follow these steps to sign in:

1. In a supported web browser, navigate to
   <https://app.snowflake.com/>.
2. For **Account identifier**, enter your account identifier.
3. Select **Sign in using [identity provider name]**.
4. In the window that appears, enter your username and password and select **Sign in**.
5. If prompted, enter your multi-factor authentication (MFA) passcode.
