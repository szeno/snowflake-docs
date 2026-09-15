# Create and publish a listing

This topic contains procedures for creating and publishing a listing privately or on the Snowflake Marketplace.

## Prerequisites for listing creation

- Agree to the [Snowflake Provider and Consumer Terms](https://other-docs.snowflake.com/en/collaboration/consumer-becoming#label-collaboration-consumer-terms). Acceptance of the Snowflake Provider and Consumer Terms is not required when creating free or paid off-platform private listings, but you must review and accept the [Snowflake Customer-Controlled Data Sharing Functionality Terms](https://www.snowflake.com/legal/data-sharing-terms/).
- Review the [Provider Policies](https://www.snowflake.com/provider-policies/).
- [Create a provider profile](/collaboration/provider-becoming#label-creating-provider-profile-marketplace) to offer paid listings or listings on the Snowflake Marketplace.
- If you want to charge for your data product, [set up your account to provide paid listings](/collaboration/provider-becoming#label-monetization-provider-onboarding).
- Get access to a role with the [required roles and privileges](#label-required-roles-and-privileges).
- Prepare the data for your listing. See [Prepare data for a listing](/collaboration/provider-listings-preparing).

To learn more about the requirements for becoming a provider, see [Use listings as a provider](/collaboration/provider-becoming).

## Required roles and privileges

Within the provider account, you can use the ACCOUNTADMIN role, or a custom role that has been granted the necessary privileges. If you use a custom role, an ORGADMIN must first delegate privileges to the ACCOUNTADMIN role, which can then grant them to your custom role. See [Set up roles and privileges for listings](/collaboration/provider-listings-preparing#label-set-up-access-listings).

The privileges you need depend on the task:

| Task | Required roles and privileges |
| --- | --- |
| Create a data listing | Global CREATE LISTING; CREATE SHARE; OWNERSHIP (or sufficient grants) on the database, schemas, and objects being shared |
| Create a Native App listing | Global CREATE LISTING; OWNERSHIP on the application package |
| Modify or configure a listing | OWNERSHIP on the listing, or MODIFY on the listing |
| Publish a listing | OWNERSHIP on the listing; the publishing role must own the attached share or application package; an approved provider profile |
| Add a trial to a paid listing | ACCOUNTADMIN, or OWNERSHIP on the listing |
| Publish a paid listing | The requirements to publish a listing, plus a Stripe Express account. See [Provide paid listings](/collaboration/provider-becoming#label-monetization-provider-onboarding). |

Expand

Show lessSee more

Important

If different roles create the share and the listing, grant the MODIFY privilege on the listing to the role that owns the share or application package. You can’t transfer OWNERSHIP of a share.

For more about granting sharing privileges, see [Set up roles and privileges for listings](/collaboration/provider-listings-preparing#label-set-up-access-listings).

## Considerations for sharing listings to accounts in US government regions

Non-government providers who want to share listings with consumer accounts in US government regions must consider the following details:

- The account in the US government region must enable data sharing and collaboration. See [Prepare to access listings from accounts in U.S. government regions](/collaboration/consumer-becoming#label-listings-setup-gov-consumer).
- You must use Cross-Cloud Auto-Fulfillment, and your data product can only contain or reference
  [objects supported for auto-fulfillment](/collaboration/provider-understand-auto-fulfillment-objects#label-listings-auto-fulfill-supported-objects).
- If you offer a listing to US government regions on the Snowflake Marketplace or directly to a consumer account in a
  [US government region](/user-guide/intro-regions#label-us-gov-regions), the secure share area (SSA)
  created to auto-fulfill the listing to that region incurs costs at the rate specific to that region. See the consumption table
  available from [Snowflake Legal](https://www.snowflake.com/legal/), the [pricing guide](https://www.snowflake.com/resource/the-simple-guide-to-snowflake-pricing/) and
  [Auto-fulfillment costs](/collaboration/provider-understand-cost-auto-fulfillment).

## Share data or apps with specific consumers using a private listing

You can create free or paid listings to share directly with specific consumers. You might create a private listing to fulfill a request
from a limited trial listing, or to share data or apps with a consumer with whom you already have a business relationship.

You must know a consumer’s account identifier to share a listing with them. See [Finding the organization and account name for an account](/user-guide/admin-account-identifier#label-account-name-find).

Note

Your role must have the required privileges to create a listing.
See [Privileges required for working with listings](/collaboration/provider-becoming#label-permissions-required-for-working-with-listings-and-shares).

### Create a free (or paid off-platform) private listing

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select **Create Listing** » **Specified Consumers**.
4. In the **Edit listing title** dialog, enter a name for your listing.
5. Select the **Add data product** button, then click **+ Select** to select the objects to attach to the listing.

   - If you select one or more database objects, Snowflake creates a secure share with those objects.
     You can change the name of the secure share.
   - If you select an existing secure share, the name of that share appears.
6. In the **Access type** dropdown, select **Free**.
7. In the **Who can access** section, add the [organization and account names](/user-guide/admin-account-identifier#label-account-name-find) for the consumers that you want to share the listing with.

   1. If you add a consumer account in a region that isn’t your local region, Snowflake enables [auto-fulfillment](/collaboration/provider-listings-auto-fulfillment) to replicate data to the remote region after a consumer gets your listing. Complete the following additional steps:
      1. In the **Auto-fulfillment** section, enter a value and select an interval to specify how often to replicate your data product from your region to the remote region.
      2. If you don’t have a default warehouse set, select a warehouse to use for auto-fulfillment.
8. Enter a description for your listing.
9. In the **Legal Terms** section, select the legal terms that apply to your listing.

   If you don’t see any legal terms, you must first accept the [Snowflake Provider and Consumer Terms](https://other-docs.snowflake.com/en/collaboration/consumer-becoming#label-collaboration-consumer-terms).
10. (Optional) In the **Attributes** section, add custom attributes to your listing. For more information, see [Required for public listings. Define additional attributes that](/collaboration/provider-listings-reference#label-listings-data-product-attributes).
11. (Optional) Click in the **Data dictionary** section to add featured objects from the listing’s data dictionary. For more information, see [Set up a data dictionary for your listing](/collaboration/provider-listings-reference#label-listings-data-dictionaries-setup).
12. (Optional) Click in the **Business needs** section to add tags that describe the business needs that your data product addresses. For more information, see [Required for public listings. At least 1 business need is required.](/collaboration/provider-listings-reference#label-listing-provider-business-need).
13. (Optional) Click in the **Quick Start Examples** section to add sample SQL queries or a notebook that demonstrate how to use the data product. For more information, see [Attach a notebook to a Snowflake Marketplace listing](#label-listings-attach-notebook-to-listing).
14. Select **Publish** to publish the listing to the selected consumers. Snowflake saves your listing if you don’t publish it immediately.

### Create a paid private listing

The following example shows how to create a private listing that includes a pricing plan and an offer.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select **Create Listing** » **Specified Consumers**.
4. In the **Edit listing title** dialog, enter a name for your listing.
5. Select the **Add data product** button, then click **+ Select** to select the objects to attach to the listing.

   - If you select one or more database objects, Snowflake creates a secure share with those objects.
     You can change the name of the secure share.
   - If you select an existing secure share, the name of that share appears.
6. In the **Access type** dropdown, select **Paid**.
7. In the **Who can access** section, add the [organization and account names](/user-guide/admin-account-identifier#label-account-name-find) for the consumers that you want to share the listing with.

   - If you add a consumer account in a region that isn’t your local region, Snowflake enables [auto-fulfillment](/collaboration/provider-listings-auto-fulfillment) to replicate data to the remote region after a consumer gets your listing. Complete the following additional steps:
     1. In the **Auto-fulfillment** section, enter a value and select an interval to specify how often to replicate your data product from your region to the remote region.
     2. If you don’t have a default warehouse set, select a warehouse to use for auto-fulfillment.
8. Enter a description for your listing.
9. In the **Legal Terms** section, select the legal terms that apply to your listing.

   If you don’t see any legal terms, you must first accept the [Snowflake Provider and Consumer Terms](https://other-docs.snowflake.com/en/collaboration/consumer-becoming#label-collaboration-consumer-terms).
10. (Optional) In the **Attributes** section, add custom attributes to your listing. For more information, see [Required for public listings. Define additional attributes that](/collaboration/provider-listings-reference#label-listings-data-product-attributes).
11. (Optional) Click in the **Data dictionary** section to add featured objects from the listing’s data dictionary. For more information, see [Set up a data dictionary for your listing](/collaboration/provider-listings-reference#label-listings-data-dictionaries-setup).
12. (Optional) Click in the **Business needs** section to add tags that describe the business needs that your data product addresses. For more information, see [Required for public listings. At least 1 business need is required.](/collaboration/provider-listings-reference#label-listing-provider-business-need).
13. (Optional) Click in the **Quick Start Examples** section to add sample SQL queries or a notebook that demonstrate how to use the data product. For more information, see [Attach a notebook to a Snowflake Marketplace listing](#label-listings-attach-notebook-to-listing).
14. Click in the **Pricing** section to set up pricing information for your listing. For more information about pricing plans and offers, see [Pricing plans and offers](/user-guide/collaboration/listings/pricing-plans-offers/pricing-plans-and-offers).
15. In the **Pricing plans** tab, select **Create pricing plan**.
16. In the **Settings** dialog, specify a display name for your pricing plan, then click **Next**.
17. In the **Pricing details** dialog, specify a pricing model. You can choose either **Usage-based** or **Flat fee**.

    - If you select **Usage-based**, specify the following details:

      - The usage-based access fee (monthly fee).
      - The cost per query and the number of included queries (optional).
      - The maximum monthly charge (optional).
    - If you select **Flat fee**, specify the flat fee amount and the billing frequency.
18. Click **Next**.
19. In the **Summary** dialog, review the pricing details, then click **Done**.
20. Navigate to the **Offers** tab.
21. In the **Offers** tab, select **+ Create offer**.
22. In the **Offer details** dialog, specify details for the offer.

    1. Select **Standard offer**.
    2. In the **Purchase type** dropdown, select **Self-serve** to allow consumers to see the price and purchase the listing directly, or select **Sales-led** to require consumers to contact you to purchase the listing.
    3. Specify a name for the offer.
    4. Select **Next**.
23. In the **Billing and payments** dialog, select the pricing plan to attach to this offer.

    1. In the **Select a pricing plan** dropdown, select the pricing plan that you created earlier.
    2. Select a contract type of either **Limited-time** or **Recurring (Subscription)**.
    3. Specify a contract duration.
    4. In the **Payment options** dropdown, select whether to charge customers based on the pricing plan or to allow payment in installments.

       - If you select **Accept installments**, specify the number of installments and the frequency of the installments.
    5. Specify the date of the first invoice or to invoice when the offer is accepted.
    6. (Optional) Specify whether to require consumers to include a credit card on file to purchase the listing.
    7. Select **Next**.
24. In the **Description** dialog, enter information about the offer that users will see.

    1. Specify an offer name to display to consumers.
    2. Specify the price to display to consumers.
    3. (Optional) Specify a tagline to display to consumers.
    4. Specify the text for the button that consumers click to purchase the listing.
    5. (Optional) Specify any value propositions for the offer.
25. Select **Next**.
26. Return to the **Listing details** tab. You will see that the offer you created is now attached to the listing.
27. Select **Publish** to publish the listing to the selected consumers.

If you exit without publishing, the listing is saved as a draft.

### Create a trial

In a usage-based trial, you can offer a number of free queries that consumers can run against your data product. After all free queries have been used, the consumer must purchase the data product to run additional queries.

To add a trial to a listing, the listing must have a data product attached and you must have the ACCOUNTADMIN role or the OWNERSHIP privilege on the listing. To learn more about the privileges required to manage listings, see [Prepare data for a listing](/collaboration/provider-listings-preparing).

1. Create a listing that includes a pricing plan and offer, as created in the previous example.
2. On the **Listing details** tab, click in the **Trial (optional)** area, and select one of the following usage trial types:

   - **Limited usage** (available for usage-based pricing plans only)

     Enter a value in the **Number of Free Queries During Trial** field.

     This value indicates the number of free queries that consumers can run against your data product. After all free queries have been used, the consumer must purchase the data product to run additional queries.
   - **Limited time**

     Enter a value in the **Length of Trial** field.
   - **Limited functionality**

     Limit the listing’s data product to only the objects and features that you want to include in the trial.
   - **Limited functionality and time**

     Enter a value in the **Length of Trial** field, and limit the listing’s data product to only the objects and features that you want to include in the trial.
3. Select **Save**.
4. Select **Publish** to publish the listing to the selected consumers.

   If you exit without publishing, the listing is saved as a draft.

### Convert a direct share to a free (or paid off-platform) private listing

You can convert a direct share to a free (or paid off-platform) private listing or to a listing published on Snowflake Marketplace. When you do so:

- Existing consumers retain access to the share.
- You gain access to usage analytics starting from the date the listing is published. Historical usage data is not available.
- You can use auto-fulfillment to share with consumers in remote regions if you are not already using replication for the objects in your
  share and if your share only contains objects supported by auto-fulfillment. For more information, see [Objects supported for auto-fulfillment](/collaboration/provider-understand-auto-fulfillment-objects#label-listings-auto-fulfill-supported-objects).
- You cannot convert your share to a paid listing if your share has active consumers.

To convert a direct share to a free private listing, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select **Create Listing** » **Snowflake Marketplace**.
4. In the **Create Listing** window, enter a name for your listing.
5. Enter a subtitle and select a profile for your listing.
6. Select the **Product type** drop-down, then select an existing secure share that backs the direct share, instead of picking individual
   database objects.

   When you select an existing share, its name appears as the attached data product for the listing.
7. In the **Access type drop-down**, select **Free** to offer a data product that is freely available to consumers.

   Note

   To convert a direct share to a paid private listing, select **Paid** in the **Access type** drop-down.
8. In the **Who can access** section, add the [data sharing account identifier](/user-guide/admin-account-identifier#label-account-name-find) for the consumer that you want to share the listing with.
9. [Configure the remaining listing fields](#label-listings-create-configure) to prepare it for publishing.
10. [Submit the listing for approval and publishing](#label-listings-create-publish).

If you decide to use auto-fulfillment to support remote consumers of your share, coordinate the following workflow with the remote consumers of your data:

1. After you publish the listing, let consumers in remote regions know how to access the listing. See [Access a private listing](/collaboration/consumer-listings-access#label-access-private-listing).
2. After the consumers in remote regions get your listing, auto-fulfillment replicates the data to the remote region. See [Objects supported for auto-fulfillment](/collaboration/provider-understand-auto-fulfillment-objects#label-listings-auto-fulfill-supported-objects).
3. When auto-fulfillment completes, the consumer receives an email that the data is available. At that point, the consumer must do the
   following:
   1. Drop the existing imported database created from the direct share.
   2. Get the listing and create a database, using the same name as the database imported from the direct share.

After setting up your direct share as a listing, you can use **Provider Studio** to manage and modify your listing.
For more information, see [Modify published listings](/collaboration/provider-listings-modifying) and [Monitor listing use](/collaboration/provider-listings-monitor-studio).

Tip

To ensure a seamless transition for your high-priority clients, consider implementing a dedicated validation window following the data migration. This allows sensitive accounts an allocated period to verify that their information has successfully moved from the initial share to the final listing.

## Share data or apps publicly on Snowflake Marketplace

Note

Before you create and publish a paid listing on Snowflake Marketplace, contact your business development partner at Snowflake.
If you do not have a business development partner, [submit a case with Marketplace Operations](https://snowforce.my.site.com/s/provider-onboarding-case).
This step is required for listing approval.

To publish data, Snowflake Native Apps, or Connected Apps on Snowflake Marketplace, your role must have the required privileges to create a listing. See [Privileges required for working with listings](/collaboration/provider-becoming#label-permissions-required-for-working-with-listings-and-shares).

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select **Create Listing** » **Snowflake Marketplace**.
4. In the **Create Listing** window, enter a name for your listing.
5. Enter a subtitle and select a profile for your listing.
6. Select the **Product type** drop-down, then select the product type associated with the listing. The following product types are available:

   - **Secure share**: Attach data or other objects from your account.
   - **Native App**: Attach applications that run directly and securely in a consumer’s account.
   - **Connected App**: List an application that connects to the consumer’s Snowflake account to process data.

     Before attaching a Connected Application to a listing, complete the [Connected Application listing enablement steps](/collaboration/guidelines-reqs-for-listing-apps#label-connected-apps-pre-enablement) and review the [Connected Applications guidelines](/collaboration/guidelines-reqs-for-listing-apps#label-guidelines-reqs-connected-apps).
7. In the **Access type** drop-down, select one of the following options:

   - **Free** to offer a data product that is freely available to consumers.
   - **Limited trial** to offer a trial of your data product, with unlimited access to the data product available on request.
   - **Paid** to charge for your data product on Snowflake Marketplace.

   > Note
   >
   > If you select **Paid** for the **Access type**, and you want to change it, you have to delete the current draft and create a new one.
8. [Configure the remaining listing fields](#label-listings-create-configure) to prepare it for publishing.
9. [Submit the listing for approval and publishing](#label-listings-create-publish).

### As a Snowflake Marketplace provider, create a listing in a Virtual Private Snowflake (VPS) deployment

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

If you’re a Snowflake Marketplace provider, follow these steps to create a [V2 listing](/collaboration/collaboration-listings-about#label-v1-vs-v2-listings) in a VPS deployment:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select **Create Listing** » **Snowflake Marketplace**.
4. In the **Create Listing** window, enter a name for your listing.
5. Select **Add data product**.
6. In the **Data product**, click **+ Select** to select the objects to attach to the listing.
7. In the **Access type** dropdown, select one of the following options:

   - **Free** to offer a data product that is freely available to consumers.
   - **Limited trial** to offer a trial of your data product, with unlimited access to the data product available on request.
   - **Paid** to charge for your data product on Snowflake Marketplace.

   > Note
   >
   > If you select **Paid** for the **Access type**, and you want to change it, you have to delete the current draft and create a new one.
8. Scroll to the **Region Availability** section and select **Set region availability**.

   1. By default, the region availability is set to **All Regions**. To change this setting, select the **All regions** edit button, then select **Custom regions**.
   2. Click **Select regions**, and then select the [region groups](/collaboration/collaboration-marketplace-about#label-about-snow-marketplace-vps) where you want your listing to be available.

      Review the region groups and regions. Region groups and regions that have deployments in VPS are indicated with an info icon.

      Hover over that icon to see information about the deployment.

      Additional fulfillment costs may incur for listings offered in regions that have deployments in VPS.

      For more information about how auto-fulfillment incurs costs, see [How auto-fulfillment incurs costs](/collaboration/provider-understand-cost-auto-fulfillment#label-listings-how-laf-incurs-costs).

      Note

      If providers don’t want to target VPS regions, they can open a Worksheet and replace region grouping names within individual region names in the listing manifest.
   3. Select **Done**.
9. [Configure the listing](#label-listings-create-configure) to prepare it for publishing.
10. [Submit the listing for approval and publishing](#label-listings-create-publish).

### As a VPS provider, create a listing in Snowflake Marketplace

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

If you’re a VPS provider, follow these steps to create a [V2 listing](/collaboration/collaboration-listings-about#label-v1-vs-v2-listings) that’s available in Snowflake Marketplace:

Note

VPS providers can’t create paid listings.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select **Create Listing** » **Snowflake Marketplace**.
4. In the **Create Listing** window, enter a name for your listing.
5. Select **Add data product**.
6. In the **Data product**, click **+ Select** to select the objects to attach to the listing.
7. In the **Access type** dropdown, select one of the following options:

   - **Free** to offer a data product that is freely available to consumers.
   - **Limited trial** to offer a trial of your data product, with unlimited access to the data product available on request.
8. Scroll to the **Region Availability** section and select **Set region availability**.

   1. By default, the region availability is set to **All Regions**. To change this setting, select the **All regions** edit button, then select **Custom regions**.
   2. Click **Select regions**, and then select the [region groups](/collaboration/collaboration-marketplace-about#label-about-snow-marketplace-vps) where you want your listing to be available.

      Review the region groups and regions. Region groups and regions that have deployments in VPS are indicated with an info icon.

      Hover over that icon to see information about the deployment.

      Additional fulfillment costs may incur for listings offered in regions that have deployments in VPS.

      For more information about how auto-fulfillment incurs costs, see [How auto-fulfillment incurs costs](/collaboration/provider-understand-cost-auto-fulfillment#label-listings-how-laf-incurs-costs).

      Note

      If providers don’t want to target VPS regions, they can open a Worksheet and replace region grouping names within individual region names in the listing manifest.
   3. Configure the fulfillment method. By default, the fulfillment method is set to **Automatic**.
   4. Select **Done**.
9. [Configure the listing](#label-listings-create-configure) to prepare it for publishing.
10. [Submit the listing for approval and publishing](#label-listings-create-publish).

## Configure a listing

You must provide additional details for paid private listings and any listing offered on the Snowflake Marketplace before you can submit your
listing for approval or publish it to specific consumers.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select the **Listings** tab, then select the draft listing you want to configure.
4. Select **Add** next to each section that appears on the page and provide the required information.

   As you provide information for each section, refer to [Configure listings](/collaboration/provider-listings-reference) for information on each
   field. The specific properties available to edit depend on the type of listing that you create.

## Publish a listing

After creating and configuring a listing, you can publish a listing.

The specific procedures for publishing a listing depend on whether you’re publishing a free (or paid off-platform) private listing, offering a paid listing
privately, or offering any listing on the Snowflake Marketplace:

- [Publish a listing to specific consumers](#publish-a-listing-to-specific-consumers)
- [Publish a listing on the Snowflake Marketplace](#publish-a-listing-on-the-snowflake-marketplace)

To publish a listing, you must use the ACCOUNTADMIN role or another role with the OWNERSHIP privilege for the listing that you want to publish.

When you publish a listing, it is visible to consumers in all current and future Marketplace regions, but consumers can only get, purchase,
or request your product in regions you select.

### Publish a listing to specific consumers

To share a private listing with specific consumer accounts, you must publish the listing to those accounts. Private listings
do not appear on the Snowflake Marketplace.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select the **Listings** tab, then select the draft listing you want to publish.
4. Select **Publish**.

After you publish the listing, it’s available for the selected consumers to access on the **Data sharing** » **External sharing** page.

For more information, see [Access and install listings as a consumer](/collaboration/consumer-listings-access).

Note

After you publish a private listing, you cannot change the share associated with the listing.

### Publish a listing on the Snowflake Marketplace

Every listing in the Snowflake Marketplace must go through the review and approval process. After a listing is approved, it can be published in
the Snowflake Marketplace. If a listing is rejected, review the feedback comments, update the listing, and resubmit it for approval.

#### Submit your listing for approval

Before you can publish a listing to the Snowflake Marketplace, you must submit the listing to Snowflake for approval.

If you want to submit your listing for approval but the option to **Submit for Approval** is disabled, check the following:

- You completed the steps to configure the listing. See [Configure a listing](#label-listings-create-configure).
- You are the ACCOUNTADMIN or have the OWNERSHIP privilege for the data product attached to the listing.
- All sample SQL queries attached to the listing pass validation.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select the **Listings** tab, then select the draft listing you want to submit for approval.
4. Select **Submit for Approval**.
5. After the listing is reviewed by Snowflake, the state changes to **Approved** or **Denied**.

   If the listing has been denied, update the listing based on the feedback provided in comments, and resubmit it for
   approval.

   When a listing is approved or denied, an email notification is sent to both the **Business Contact** and **Technical Contact** email
   addresses in the provider profile associated with the listing.

#### Publish your listing

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select the **Listings** tab, then select the approved listing you want to publish.
4. Select **Publish**.

After you publish your Snowflake Marketplace listing for the first time, subsequent changes to the listing that require approval from Snowflake
are published automatically after approval. To prevent your listing from being automatically published,
see [Deactivate automatic publishing](#label-deactivate-auto-publish).

When you publish a listing, it is visible to consumers in all current and future Snowflake Marketplace regions. Consumers can only get, purchase,
or request your product in regions you select. See [Auto-fulfillment for listings](/collaboration/provider-listings-auto-fulfillment) for more about region availability.

After publishing your Snowflake Marketplace listing, you can define a [referral link](/collaboration/provider-listings-referral-link) for the listing.
Referral links let you give consumers a direct link to your listing.

### Deactivate automatic publishing

After a listing is published, you can deactivate automatic publishing for future changes to the listing.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select the **Listings** tab, then select the approved listing for which you want to deactivate automatic publishing.
4. On the listing details page, select **Settings**.
5. In the **Publishing** section of the **Listing Settings**, select **Edit Publishing**.
6. In the **Publish Setting** window, select **Manual**.
7. Select **Save**.

The listing is no longer automatically published. Now, when you make changes to your listing, you must manually publish the listing.
See [Publish your listing](#publish-your-listing).

## Attach a notebook to a Snowflake Marketplace listing

Providers can add a notebook to a listing to show potential consumers how they can leverage and benefit from a data product. The listings
can be available on the Snowflake Public Marketplace, Internal Marketplace, or as a private listing to a select set of consumers.

A provider can attach a notebook that was fully run with results to a listing. The results can include tabular outputs or visualization to describe
the value of the data products within a listing. Providers can include both Python-based and SQL-based examples in the notebook and add clear
Markdown explanations to guide consumers.

Note

Notebooks attached to a listing are view-only and can’t be cloned, downloaded, or interacted with by the consumer.

To attach a notebook to a listing, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Notebooks**.
3. [Create a notebook](/user-guide/ui-snowsight/notebooks-create).
4. In each cell of the notebook, select **Run all** or **Run** to generate results. Ensure that you run in each cell.
5. To verify that the notebook runs successfully, locate the green run-status indicator.
6. To end your Notebooks session, select the **Active** drop-down and select **End session**.
7. In the navigation menu, select **Marketplace** » **Provider Studio**. You can attach a notebook to all listing types.
8. [Create a new listing](#label-listings-create-configure) or choose an existing listing.
9. Select **+ Add data product**.
10. Choose **+ Select**.
11. In the **Quick Start Examples** section, select **Add Notebook**.
12. Select the notebook to attach. You can use the search feature to find a specific notebook.
13. Select **Save**.
14. To publish the listing to the selected consumers, select **Publish**.

> Note
>
> To update the contents of the notebook after attaching it to a listing, you must remove the notebook from the listing and attach it again.

## Remove a notebook from a listing

1. In the navigation menu, select **Marketplace** » **Provider Studio**.
2. In the **Quick Start Examples** section, select the notebook to remove.
3. Select **Remove Notebook**.

> Note
>
> If you lose ownership of the notebook, or if you delete it or remove it from your shared resources, a copy remains with the listing.

## Limitations when attaching notebooks to listings

- Providers can only attach one notebook to a listing, and the provider must have OWNERSHIP privileges on the notebook.
- Consumers can only view the notebook and its results in the listings.
- Changes in the notebook aren’t automatically updated in the listing. To reflect the latest changes, you must remove the notebook and add it back again.
