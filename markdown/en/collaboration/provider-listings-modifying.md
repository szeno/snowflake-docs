# Modify published listings

This topic describes how to modify listings after they have been published to the Snowflake Marketplace or shared with consumers as a private listing.

## Privileges required to edit listings

To modify listings, you must be the listing owner or have the MODIFY privilege on a listing. See [MODIFY privilege on a listing](/user-guide/data-exchange-marketplace-privileges#label-modify-on-data-exchange-listing).

## Edit a listing published on the Snowflake Marketplace

When editing a listing published on the Snowflake Marketplace, consider the following:

- When you edit a listing published on the Snowflake Marketplace, a new draft listing is created. To make those changes available to
  consumers, you must resubmit the draft listing for approval and publishing.
- Editing the available regions and business needs fields do not require approval. You can make these changes at any time.
- If you remove a region that was previously available, consumers in that region no longer have access to the shared
  dataset.
- When a new version of a listing is published, the previous version is replaced and cannot be recovered.

If you want to update the data product associated with a listing, see [Update a data share](#label-update-share-listing).

To edit a listing published on the Snowflake Marketplace, complete the following steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select **Listings**, then select the listing you want to edit.

   - To add or remove regions where the listing is available, click **Edit** in the **Region Availability** section. You can skip
     the rest of the steps as no administrator approval is required.
   - To add or update compliance certification badges, see [Add compliance badges to a listing](#label-listings-update-with-compliance-badge).
   - To change other fields, such as the listing description, click **Edit** in the applicable section and select **Continue** when
     prompted. This creates a new draft listing that is not visible to consumers until submitted, approved, and published.
   - If you have existing changes in progress, select the **New Draft** toggle next to the listing title to continue working on
     an existing draft. You can discard this draft by selecting the **Delete** button at the top right of the page.
4. Select **Submit for Approval** when you are ready to submit your new draft listing for review.

## Edit a private listing

You can edit draft or published private listings in **Provider Studio**. If you edit a published private listing, any changes that you
make are immediately available to consumers after you save those changes.

If you want to update the data product associated with a listing, see [Update a data share](#label-update-share-listing) for guidance.

To edit a private listing, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select **Listings**, then choose the listing you want to edit.
4. Make the changes that you want, then click **Save**.

## As a Snowflake Marketplace provider, edit an existing Snowflake Marketplace listing to be available in a VPS deployment

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Note

This feature isn’t enabled by default. Providers must reach out to Snowflake Support to enable this feature. For more information, see [Snowflake Marketplace version 2 listings in VPS deployments](/collaboration/collaboration-marketplace-about#label-about-snow-marketplace-vps).

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select **Listings**, then select the listing to be edited.
4. Scroll to the **Region Availability** section and select **Set region availability**.
5. Click **Select regions**, then select the VPS region or region groups where you want your listing to be available.
   Region groups and regions that have deployments in VPS are indicated with an info icon.

   Hover over that icon to see information about the deployment.

   Additional fulfillment costs may incur for listings offered in regions that have deployments in VPS.

   For more information about how auto-fulfillment incurs costs, see [Auto-fulfillment costs](/collaboration/provider-understand-cost-auto-fulfillment).
6. Select **Save** when you’re done.

Note

Changing the region availability or the business needs doesn’t require approval from the Snowflake Marketplace team.

Any other changes that you make will require the listing to be re-reviewed and approved by the Snowflake Marketplace team.

## As a VPS provider, edit a VPS listing to be available in Snowflake Marketplace

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Note

This feature isn’t enabled by default. Providers must reach out to Snowflake Support to enable this feature. For more information, see [Snowflake Marketplace version 2 listings in VPS deployments](/collaboration/collaboration-marketplace-about#label-about-snow-marketplace-vps).

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select **Listings**, then select the listing you want to edit.
4. Scroll to the **Region Availability** section and select **Set region availability**.
5. Click **Select regions**, then select the VPS region or region groups where you want your listing to be available.
   Region groups and regions that have deployments in VPS are indicated with an info icon.

   Hover over that icon to see information about the deployment.

   Additional fulfillment costs may incur for listings offered in regions that have deployments in VPS.

   For more information about how auto-fulfillment incurs costs, see [Auto-fulfillment costs](/collaboration/provider-understand-cost-auto-fulfillment).
6. Select **Save** when you’re done.

Note

Changing the region availability or the business needs doesn’t require approval from the Snowflake Marketplace team.

Any other changes that you make will require the listing to be re-reviewed and approved by the Snowflake Marketplace team.

## Add compliance badges to a listing

To add or update compliance certification badges on an existing listing, follow the steps in [Compliance certifications](/collaboration/provider-listings-reference#label-listings-compliance-certifications). The same Snowsight and SQL procedures apply whether you are adding badges to a new or existing listing.

## Unpublish a listing

To hide a listing from the Snowflake Marketplace without deleting it, you can unpublish the listing.

Note

When you unpublish a listing, existing consumers can still access the data product associated with the listing unless you also remove them
from the share. See [Update a data share](#label-update-share-listing). To remove a listing and access to the listing for all consumers using the listing,
delete the listing. See [Remove listings as a provider](/collaboration/provider-listings-removing).

To unpublish a listing, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select **Listings**.
4. Select the name of the listing you wish to unpublish.
5. In the top-right corner of the listing page, select the vertical ellipsis ([![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)), and then select **Unpublish** to
   begin unpublishing the listing.

   A confirmation message displays, reminding you that unpublishing a listing removes the listing from Snowflake Marketplace, but existing
   consumers will continue to have access to the listing.
6. Select **Unpublish** to complete the unpublish process.

   The status at the top of the page changes from **Live** to **Unpublished**. You can select that status to view the listing status summary.

Note

If the listing was automatically replicated to other regions using auto-fulfillment, the listing remains replicated to the remote regions.
To remove the replicated data product from other regions, change the region availability of the listing. For more information, see
[Region availability](/collaboration/provider-listings-reference#label-listings-set-up-region-avail).

## Republish a listing

When you republish a listing on the Snowflake Marketplace, you do not need to submit the listing for approval unless you made changes to the listing.

To republish a listing, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select **Listings**.
4. Select the name of the listing you want to republish.
5. In the top-right corner, select **Publish** to republish the listing.
   - A message displays, confirming that the listing is available on Snowflake Marketplace. From this message, you can select to view the listing
     on Snowflake Marketplace, or you can select **Done** to return to the listing page.
   - The status at the top of the listing page changes from **Unpublished** to **Live**.

## Update a data share

In addition to modifying a listing, you can modify the data share attached as the data product a specific listing. You cannot remove or
replace the data product for a published listing.

For example, you might want to add a data column to a secure view, or rename objects to follow the [Identifier requirements](/sql-reference/identifiers-syntax).

Important

Every time you modify the share associated with a listing, you must notify the consumers to make sure that you do not break their processes.
Examples of breaking changes to a data share include the following:

- Adding/removing a column
- Renaming objects
- Removing objects

To update the objects in a data share, see [Working with Shares](/user-guide/data-sharing-provider).

## Modify paid listings

You can modify the price and pricing plan for paid listings, with some restrictions.

### Change the price of a paid listing

If you want to change the price of a paid listing in the Snowflake Marketplace, you must resubmit the listing for approval.
The approval is a technical part of the process of republishing a modified listing.
Snowflake does not provide feedback about the price change.

You cannot change the price of a listing to zero dollars. To make a paid listing free, you must create a new listing.

After the newly priced listing is approved and published, Snowflake automatically notifies current consumers of the listing about the
price change using the billing contact email address associated with each consumer’s account.

After you change the price of your pricing plan:

- New consumers see and are billed according to the new pricing plan immediately.
- Existing consumers are billed the previous rate until the end of their current billing cycle.
  - If you change the price less than 30 days before the next billing cycle begins, customers are billed the previous rate for the
    next billing cycle and the new rate for the following billing cycle.
  - If you change the price more than 30 days before the next billing cycle begins, customers are billed the new rate for the next billing
    cycle.

For example, for a usage-based pricing plan that bills monthly, if you change the price on October 15th, existing consumers are billed
the previous rate for their October invoice and November invoice, but charged the new rate for the December invoice.

For specific scenarios, refer to this example table:

| Pricing plan | Billing cycle | Plan start date | Price change date | Invoice where new price is reflected |
| --- | --- | --- | --- | --- |
| Usage-based | 1 month | Jan 1, 2023 | Jun 15, 2023 | Aug 1, 2023 |
| Usage-based | 1 month | Jan 1, 2023 | Jun 2, 2023 | Aug 1, 2023 |
| Usage-based | 1 month | Jan 1, 2023 | May 30, 2023 | Jul 1, 2023 |
| Subscription-based | 3 months, recurring | Jan 1, 2023 | Feb 15, 2023 | Apr 1, 2023 |
| Subscription-based | 3 months, recurring | Jan 1, 2023 | Mar 15, 2023 | Jul 1, 2023 |

Expand

Show lessSee more

### Change the pricing plan of a paid listing

You can change the pricing plan for a paid listing when you edit the listing. If you want to change the pricing plan, consider the following:

- You cannot remove a pricing plan from a paid listing to make it a free listing. See [Change Existing Listings to Paid Listings](#change-existing-listings-to-paid-listings).
- You cannot change the type of pricing plan. If your listing currently has a
  [usage-based pricing plan](/collaboration/provider-listings-pricing-model#label-listings-usage-pricing-model), you cannot change the plan to a
  [subscription-based pricing plan](/collaboration/provider-listings-pricing-model#label-listings-subscription-pricing-model), and vice versa.
- If your paid listing is published in the Snowflake Marketplace, you must resubmit the listing for approval after changing the pricing plan.
  After the updated pricing plan is approved and the updated listing is published, Snowflake automatically notifies current consumers of
  the listing about the pricing plan change using the billing contact email address associated with each consumer’s account.

When you change the pricing plan, existing consumers are charged based on the new pricing plan after the end of their
next billing cycle. New consumers see the new pricing plan immediately.

### Change existing listings to paid listings

You cannot convert a free listing into a paid listing. If you published a listing without a pricing plan, one cannot be added later.

If you want to offer a paid listing, you must attach a pricing plan to the listing before it is first published.

Similarly, you cannot convert a paid listing into a free listing. If you published a listing with a pricing plan, you cannot change the
pricing plan to null, or change the price to zero. To change the price to some other amount, see [Change the price of a paid listing](#label-change-listing-price).

If you want to change the type of listing that you offer, create the new listing that you want to offer and unpublish the existing listing.
For example, if you want to replace a free listing with a paid listing, unpublish the free listing and create a paid listing with the same
contents. See [Unpublish a listing](#label-unpublish-listing).
