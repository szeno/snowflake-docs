# Configure and use a Data Exchange

Data exchange is not enabled for all accounts

To inquire about enabling a data exchange, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Use the information provided here to perform Data Exchange administrative and user tasks.

After you sign in to your Data Exchange as a Data Exchange Admin, you can perform the following tasks:

- Set up your Data Exchange.
- Create, update, or delete provider profiles. New profiles must be approved by a data exchange administrator. See [Manage provider profiles](/user-guide/data-exchange-becoming-a-provider).
- Update contact email.
- Manage profile editors.
- Manage membership in the data exchange.
- Assign roles to members of the data exchange. See [Grant privileges to other roles](/user-guide/data-exchange-marketplace-privileges).

Note

When logging in to a data exchange for administrative purposes such as joining the exchange, configuring the exchange, or configuring data listings, the member must have the ACCOUNTADMIN role.

## Set up your Data Exchange

Note

To create a Data Exchange, contact your Snowflake representative or
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

### Invite members and assign roles

After the Data Exchange is set up, you can start inviting accounts as members and designating them as data providers, data consumers,
or both. You invite members using their Snowflake account name or account URL.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **External sharing**.
3. Navigate to the **Manage exchanges** tab.
4. Select the exchange you want to manage.
5. Select the **Members** tab.
6. Select **Add Member** to add a new member. To manage an existing member, select their member row.
7. Select the role for the member, **Provider** or **Consumer**, by selecting the appropriate checkbox.
8. Save your changes.

### Manage member listings

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **External sharing**.
3. Select the **Manage exchanges** tab.
4. Select the exchange you want to manage.
5. Select the **Member Listings** tab.
6. Select **Any**, **Pending**, or **Reviewed** to manage listings in different states.
7. Open a listing by selecting its row.
8. View the listing, or select **Review** to review the listing and approve or deny it for your Data Exchange.

### Manage member profiles

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **External sharing**.
3. Select the **Manage exchanges** tab.
4. Select the exchange you want to manage.
5. Select the **Member Profiles** tab. On the tab, you can do the following:
   - Select **Pending** or **Reviewed** to view profiles in different states.
   - You can view already reviewed profiles, or select **Review** to approve or deny a member profile.

### Access consumer listings

All users can browse listings in the Data Exchange, but only users with the ACCOUNTADMIN role or the [IMPORT SHARE](/user-guide/security-access-privileges-shares) privilege can get or request data.

If you do not have sufficient privileges, you can do one of the following:

- Request your ACCOUNTADMIN to grant you the IMPORT SHARE privilege.
- Request your ACCOUNTADMIN to get data, and grant you IMPORTED PRIVILEGES on the database created from the share.
  For more information, see [Granting privileges on an imported database](/user-guide/data-share-consumers#label-granting-privileges-on-shared-database).

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **External sharing**.
3. Select the **Shared with you** tab.

### Browse data listings

After you sign in to a Data Exchange, review the **Listings** section of the **Shared With You** tab to view available listings.

In a Data Exchange, the following types of listings are available to you:

- [Free listings](/collaboration/collaboration-listings-about#label-free-listing), which you can
  access by selecting **Get** to create a database out of the shared data inside of your Snowflake account.
- Personalized listings, which you can access by selecting **Request** to request access to the data. An email notification is sent to
  the data provider with your request.

### View listing requests

Note

To see requests from listings on the Snowflake Marketplace, such as those for personalized listings or free listings in another region,
use **Provider Studio**.
See [Managing Listing Requests as a Provider](/collaboration/provider-listings-managing).

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **External sharing**.
3. Select the **Requests** tab.
4. Select **Inbound**.

   When a request is denied, a comment is provided next to the request, explaining the reason for denial. In such cases, you can make the necessary adjustments and resubmit your request.

### Access shared data

1. When your request for a listing in the Data Exchange is approved, sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **External sharing**.
3. Select the **Shared with you** tab.
4. Locate the listing you requested and select **Get Data** for the listing.
5. Enter the name for the database to create in your account from the share.
6. Select roles that you want to have access to the database created from the share.
7. Accept Snowflake’s consumer terms and the provider’s terms of use. You only need to accept the listing terms when you create a database from a share for the first time.

   Note

   Accepting terms using SQL is not supported.
8. Select **Create Database**.

   After you create the database from share, the **Get Data** button is replaced with the **View Database** button.

   See also: [Usage metrics shared with providers](/user-guide/data-sharing-intro#label-usage-metrics-shared-with-providers)
