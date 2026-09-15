# Access and install listings as a consumer

Whether you explored listings on the Snowflake Marketplace and found a listing that you want to access or purchase, or a provider shared a
private listing with you, this topic guides you through accessing and installing listings as a consumer.

## Access a private listing

To access a private listing that was shared with you, do the following:

Note

You must use the ACCOUNTADMIN role or another role with the CREATE DATABASE and IMPORT SHARE privileges to access a listing.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **External sharing**.
3. On the **Shared with you** page under **Privately shared listings**, select the listing you want to access.
4. Select **Get**.

## Accessing listings on the Snowflake Marketplace

After you explore listings on the Snowflake Marketplace, access the listings you’re interested in.

Note

You must use the ACCOUNTADMIN role or another role with the CREATE DATABASE and IMPORT SHARE privileges to access and install a listing.

You can access free and paid listings on the Snowflake Marketplace. To access a free listing on the Snowflake Marketplace, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Snowflake Marketplace**.
3. Search or browse to the listing you want to access.
4. Select **Get** to access a listing already available in your region. A dialog opens with details about the listing. If you have to
   request the listing to be replicated to your region, select **Request**.
5. (Optional) Specify a database name for the data in the listing.
6. (Optional) Add roles to grant access to the database created from the listing.
7. Select **Get**.
8. In the confirmation dialog that appears, select **Open** to open a [Snowsight worksheet](/user-guide/ui-snowsight-worksheets) with an example query in a new tab, or
   select **Done**.

To access a paid listing on the Snowflake Marketplace, see [Accessing paid listings](#label-access-paid-listings).

## Accessing paid listings

You can access paid listings that are privately shared with you, called private listings, or paid listings on the Snowflake Marketplace.
Before you access a paid listing, you can trial it first. See [Trial a listing](/collaboration/consumer-listings-exploring#label-trial-paid-listing).

Note

You must use the ACCOUNTADMIN role or another role with the CREATE DATABASE and IMPORT SHARE privileges to access a listing.
To purchase a paid listing, your role must also have the PURCHASE DATA EXCHANGE LISTING privilege.

You must also set up your account to pay for listings. See [Pay for Snowflake Marketplace listings](/collaboration/consumer-listings-paying).

After setting up your account to pay for listings, do the following to access a paid listing:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Search or browse to the listing you want to access.
3. Select **Get**.
4. Select the **Paid** option and review details about the price.
5. Select **Next**.
6. (Optional) Add a purchase order (PO) number to be associated with this listing for billing purposes.
7. (Optional) Specify a database name for the data in the listing. If you trialed the listing, Snowflake uses the database name that you
   specified for the trial.
8. (Optional) Add roles to grant access to the database created from the listing.
9. If you are eligible to [use your Capacity commitment to pay](/collaboration/marketplace-capacity-drawdown#label-marketplace-capacity-drawdown),
   **Pay with Marketplace Capacity Drawdown** is selected by default. Optionally disable this selection to pay with a credit card,
   invoice, ACH, wire transfer, or another supported method.
10. Select **Buy** to purchase the listing.

Note

If your organization administrator (i.e. an account with or granted the ORGADMIN role) has not previously
accepted the [Provider and Consumer Terms](https://www.snowflake.com/legal/snowflake-provider-and-consumer-terms/), the **Setup incomplete** dialog appears and a reminder email is sent requesting that
they review and accept these terms. You cannot get access to the listing until these terms are accepted.

If an organization administrator has previously accepted the terms, then you can continue.

11. In the confirmation dialog that appears, select **Open** to open a [Snowsight worksheet](/user-guide/ui-snowsight-worksheets)
    with an example query in a new tab, or select **Done**.

Note

If you are not yet eligible to use your Capacity commitment, you can see the date after which your Capacity balance will be used to
pay for the listing. Snowflake Marketplace invoices received after that date can be paid with your Capacity balance.

### Modify your listing payment method

Changes made to your listing payment method are saved automatically and take effect in the next billing cycle.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Snowflake Marketplace**.
3. Select a paid listing, and then select **Manage Purchase**.
4. Optional. If you participate in the [Marketplace Capacity Drawdown Program](/collaboration/marketplace-capacity-drawdown#label-marketplace-capacity-drawdown), select **Pay with Marketplace Capacity Drawdown**.
5. Optional. In the **Payment method** area, select **Show more** and then select an alternate payment method.

## Access a limited trial listing on the Snowflake Marketplace

Limited trial listings let providers offer a time-limited or functionality-limited trial of a data product, with unlimited access to the
full data product available on request.

The workflow of a limited trial listing works as follows:

- [Trial the data product](/collaboration/consumer-listings-exploring#label-trial-paid-listing).
- If you want, [request unlimited access to the full data product](#label-request-limited-trial-listing).
- Access the private listing shared by the provider containing the full data product.

### Request a limited trial listing

At any time after you start to [trial a listing](/collaboration/consumer-listings-exploring#label-trial-paid-listing), you can request unlimited access to the full data product.

To request unlimited access to the full data product of a limited trial listing, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Snowflake Marketplace**.
3. Search or browse to the listing you want to request.
4. Select **Request**.
5. Complete the form that appears with your contact information. If you use an email address from a free email provider, you need to provide
   additional details.

Note

If you see an error, your user profile might be missing some contact information. If you have an administrator role, see
[Add user details to your user profile](/user-guide/ui-snowsight-profile#label-user-details-and-preferences) to update your profile using Snowsight. Otherwise, contact an
account administrator to update your user details.

After you request a limited trial listing, the listing provider is notified and contacts you. You might need to agree to additional
commercial terms or pricing agreements with the provider before the provider fulfills your request for unlimited access to the full data
product.

After the provider fulfills your request, you can access the private listing shared with you. See [Access a private listing](#label-access-private-listing).

## Limitations for accessing listings from accounts in U.S. government regions

If you access listings from an account in US government region, the following limitations apply:

- You cannot get paid listings.
- You cannot get listings for a Snowflake Native App.
- You cannot get Snowflake connectors.
- You cannot get listings that use manual fulfillment.

Some other listings on the Snowflake Marketplace might be unavailable in your region, but you can contact the provider for more details:

Cause:
:   You cannot access a listing in your region because it uses manual fulfillment instead of auto-fulfillment.

Solution:
:   Contact the provider to determine whether the data product attached to the listing can be offered to you privately.
    Some data products include objects other than the [objects supported for auto-fulfillment](/collaboration/provider-understand-auto-fulfillment-objects#label-listings-auto-fulfill-supported-objects)
    and therefore cannot be made available in your region.

Cause:
:   The provider chose not to offer the listing in your region.

Solution:
:   Contact the provider to request that they offer the listing in your US government region.

Cause:
:   The listing is paid.

Solution:
:   You cannot get the listing. Customers with accounts in US government regions cannot pay for listings at this time.
